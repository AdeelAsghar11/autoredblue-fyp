"""The generic reason-then-parse retry loop (ROADMAP step 3.4).

Owner: Adeel (graph/orchestration engineering).

Implements ARCHITECTURE.md "Graph & orchestration engineering" pattern 1
as a real LangGraph cycle, kept in its own module (not graph/build_graph.py)
so agent modules like agents/recon.py can import it without a circular
import back to build_graph.py, which itself imports the agents.
"""

from __future__ import annotations

from typing import Callable

from langgraph.graph import END, StateGraph

from autoredblue.graph.state import AuditState
from autoredblue.llm.parsing import ParseError


def build_reason_then_parse_graph(
    reason_fn: Callable[[AuditState], str],
    parse_fn: Callable[[str], dict],
    max_attempts: int = 3,
):
    """Generic reason-then-parse-with-retry subgraph.

    A reasoning node produces a raw completion, a parser node tries to
    parse it, and a conditional edge routes back to the reasoning node
    on failure (with the previous llm_error available in state for
    `reason_fn` to fold into its next prompt), capped at `max_attempts`.
    On repeated failure past the cap, the graph ends with
    `llm_failed=True` instead of raising, so one bad completion doesn't
    crash the run.

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
