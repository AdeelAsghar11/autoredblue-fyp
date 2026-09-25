"""LangGraph StateGraph wiring for the AutoRedBlue pipeline.

Owner: Adeel (graph/orchestration engineering).

Builds the graph described in docs/ARCHITECTURE.md "Pipeline overview":
scope check -> recon -> human approval gate -> scan -> triage -> report,
with the Verification Agent resumed separately after a fix is applied.
Also owns the patterns in docs/ARCHITECTURE.md "Graph & orchestration
engineering": retry-on-parse-failure, conditional routing on state, and
the approval interrupt.

Sequencing note (docs/PROGRESS.md "Next concrete task"): the first version
of this module wires only the thin end-to-end slice (Recon -> one scan
type -> basic report) with the retry loop and approval interrupt built in
from the start, not all five agents at once.

Current state (ROADMAP step 2): a minimal 2-node graph, scope_check ->
stub recon, proving the scope-gate routing mechanics before any real tool
wiring lands in step 3.
"""

from __future__ import annotations

import logging
from pathlib import Path

from typing import Callable

from langgraph.graph import END, StateGraph

from autoredblue.agents.scope_check import is_in_scope
from autoredblue.graph.state import AuditState
from autoredblue.llm.parsing import ParseError

logger = logging.getLogger(__name__)


def stub_recon_node(state: AuditState) -> dict:
    """Placeholder for the real Recon Agent (ROADMAP step 3).

    Only proves the graph fires this node after an in-scope target passes
    the scope check; replaced by the real Nmap/subfinder-backed node in
    step 3.5.
    """
    logger.info("recon ran")
    return {"recon_findings": {"stub": True}}


def _route_after_scope_check(state: AuditState) -> str:
    return "recon" if state.get("scope_allowed") else END


def build_graph(allowlist_path: Path | None = None):
    """Wire the minimal scope_check -> stub recon graph and compile it.

    `allowlist_path` is forwarded to is_in_scope() (defaults to
    config/allowlist.yaml when None); accepting it here lets callers,
    including tests, point the scope check at a different allow-list
    without touching global state.
    """

    def scope_check_node(state: AuditState) -> dict:
        allowed = is_in_scope(state["target"], allowlist_path=allowlist_path)
        return {"scope_allowed": allowed}

    graph = StateGraph(AuditState)
    graph.add_node("scope_check", scope_check_node)
    graph.add_node("recon", stub_recon_node)
    graph.set_entry_point("scope_check")
    graph.add_conditional_edges(
        "scope_check",
        _route_after_scope_check,
        {"recon": "recon", END: END},
    )
    graph.add_edge("recon", END)
    return graph.compile()


def build_reason_then_parse_graph(
    reason_fn: Callable[[AuditState], str],
    parse_fn: Callable[[str], dict],
    max_attempts: int = 3,
):
    """Generic reason-then-parse-with-retry subgraph (ROADMAP step 3.4).

    Implements ARCHITECTURE.md "Graph & orchestration engineering"
    pattern 1 as a real LangGraph cycle: a reasoning node produces a raw
    completion, a parser node tries to parse it, and a conditional edge
    routes back to the reasoning node on failure (with the previous
    llm_error available in state for `reason_fn` to fold into its next
    prompt), capped at `max_attempts`. On repeated failure past the cap,
    the graph ends with `llm_failed=True` instead of raising, so one bad
    completion doesn't crash the run.

    Deliberately generic, not recon-specific: any future reason-then-parse
    node (e.g. the Scan Agent's tool-selection loop) can reuse this by
    supplying its own `reason_fn`/`parse_fn`.
    """

    def reason_node(state: AuditState) -> dict:
        completion = reason_fn(state)
        return {
            "llm_completion": completion,
            "llm_attempts": state.get("llm_attempts", 0) + 1,
        }

    def parse_node(state: AuditState) -> dict:
        try:
            result = parse_fn(state["llm_completion"])
        except ParseError as exc:
            return {"llm_failed": True, "llm_error": str(exc)}
        return {"llm_failed": False, "llm_error": None, "llm_result": result}

    def route(state: AuditState) -> str:
        if not state.get("llm_failed"):
            return "success"
        if state.get("llm_attempts", 0) >= max_attempts:
            return "give_up"
        return "retry"

    graph = StateGraph(AuditState)
    graph.add_node("reason", reason_node)
    graph.add_node("parse", parse_node)
    graph.set_entry_point("reason")
    graph.add_edge("reason", "parse")
    graph.add_conditional_edges(
        "parse",
        route,
        {"success": END, "give_up": END, "retry": "reason"},
    )
    return graph.compile()
