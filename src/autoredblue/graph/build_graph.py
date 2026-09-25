"""LangGraph StateGraph wiring for the AutoRedBlue pipeline.

Owner: Adeel (graph/orchestration engineering).

Builds the graph described in docs/ARCHITECTURE.md "Pipeline overview":
scope check -> recon -> human approval gate -> scan -> triage -> report,
with the Verification Agent resumed separately after a fix is applied.
Also owns the patterns in docs/ARCHITECTURE.md "Graph & orchestration
engineering": retry-on-parse-failure (graph/retry_loop.py), conditional
routing on state, and the approval interrupt.

Sequencing note (docs/PROGRESS.md "Next concrete task"): the first version
of this module wires only the thin end-to-end slice (Recon -> one scan
type -> basic report) with the retry loop and approval interrupt built in
from the start, not all five agents at once.

Current state (ROADMAP step 3.5): scope_check -> the real Recon Agent
(agents/recon.py::run_recon, backed by Nmap, subfinder, and the LLM
perceptor's retry loop). The stub recon node from step 2.2 is gone.
"""

from __future__ import annotations

from pathlib import Path

from langgraph.graph import END, StateGraph

from autoredblue.agents.recon import run_recon
from autoredblue.agents.scope_check import is_in_scope
from autoredblue.graph.state import AuditState


def _route_after_scope_check(state: AuditState) -> str:
    return "recon" if state.get("scope_allowed") else END


def build_graph(allowlist_path: Path | None = None):
    """Wire scope_check -> the real Recon Agent and compile the graph.

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
    graph.add_node("recon", run_recon)
    graph.set_entry_point("scope_check")
    graph.add_conditional_edges(
        "scope_check",
        _route_after_scope_check,
        {"recon": "recon", END: END},
    )
    graph.add_edge("recon", END)
    return graph.compile()
