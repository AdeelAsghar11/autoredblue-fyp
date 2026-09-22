"""Shared LangGraph state object for the AutoRedBlue pipeline.

Owner: Adeel (graph/orchestration engineering).

The graph state is the single source of truth for a run, not the model's
chat history, see docs/ARCHITECTURE.md "The state object". Every agent
node reads from and writes to this structure; nothing is passed between
agents except through here.
"""

from __future__ import annotations

from typing import Any, TypedDict


class AuditState(TypedDict):
    """Fields carried through the graph for a single audit run.

    See docs/ARCHITECTURE.md "The state object" for what each field means
    and which agent writes it.
    """

    target: str
    scope_allowlist: list[dict[str, Any]]
    recon_findings: dict[str, Any]
    scan_findings_raw: dict[str, Any]
    triaged_findings: list[dict[str, Any]]
    approval_state: bool
    verification_results: list[dict[str, Any]]

    # TODO: retry/error-tracking fields for the parse-failure retry loop
    # (docs/ARCHITECTURE.md "Graph & orchestration engineering", pattern 1).
