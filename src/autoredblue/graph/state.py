"""Shared LangGraph state object for the AutoRedBlue pipeline.

Owner: Adeel (graph/orchestration engineering).

The graph state is the single source of truth for a run, not the model's
chat history, see docs/ARCHITECTURE.md "The state object". Every agent
node reads from and writes to this structure; nothing is passed between
agents except through here.
"""

from __future__ import annotations

from typing import Any, NotRequired, TypedDict


class AuditState(TypedDict):
    """Fields carried through the graph for a single audit run.

    See docs/ARCHITECTURE.md "The state object" for what each field means
    and which agent writes it. Only `target` needs to be set on the
    initial state passed to the graph; every other field is written by
    some node as the run progresses, so all but `target` are NotRequired.
    """

    target: str
    scope_allowlist: NotRequired[list[dict[str, Any]]]
    # scope_allowed: set by the scope_check node (module 0), routes the
    # graph to recon or to a halt. Graph-internal, not in ARCHITECTURE.md's
    # state list since that list predates the graph wiring itself.
    scope_allowed: NotRequired[bool]
    recon_findings: NotRequired[dict[str, Any]]
    scan_findings_raw: NotRequired[dict[str, Any]]
    triaged_findings: NotRequired[list[dict[str, Any]]]
    approval_state: NotRequired[bool]
    verification_results: NotRequired[list[dict[str, Any]]]

    # TODO: retry/error-tracking fields for the parse-failure retry loop
    # (docs/ARCHITECTURE.md "Graph & orchestration engineering", pattern 1).
