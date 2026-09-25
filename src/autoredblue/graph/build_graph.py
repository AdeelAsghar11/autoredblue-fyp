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

from langgraph.graph import END, StateGraph

from autoredblue.agents.scope_check import is_in_scope
from autoredblue.graph.state import AuditState

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
