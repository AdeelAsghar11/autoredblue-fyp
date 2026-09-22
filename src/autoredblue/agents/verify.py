"""Verification Agent.

Owner: Adeel.

Runs after a human has applied a fix, potentially in a different process
days later (needs the SQLite checkpointer from graph/checkpointer.py, not
the in-memory one, see docs/ARCHITECTURE.md "Graph & orchestration
engineering" pattern 4). Its only job: replay the saved request from the
Triage Agent against the patched target and check the response, then
append a "remediation verified / still vulnerable" result to the report
(docs/ARCHITECTURE.md "6. Verification Agent").

Boundary: replays the same benign saved request only. Does not attempt
new exploitation.
"""

from __future__ import annotations

# TODO: from autoredblue.tools import playwright_tool


def verify_fix(finding):
    """Replay `finding`'s saved request against the (now patched) target
    and return an updated verification result.

    TODO
    """
    raise NotImplementedError
