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
"""

from __future__ import annotations

# TODO: from langgraph.graph import StateGraph
# TODO: from autoredblue.graph.state import AuditState


def build_graph():
    """Wire the StateGraph and return the compiled graph.

    TODO:
    - add nodes for scope_check, recon, scan, triage, report (verify is a
      separately-resumed graph, see checkpointer.py)
    - add the retry loop: reasoning node -> parser node -> conditional edge
      (success -> continue, failure -> back to reasoning node, capped at N)
    - add the human-approval interrupt before the scan node
    - add conditional routing for zero-findings short-circuits
    """
    raise NotImplementedError
