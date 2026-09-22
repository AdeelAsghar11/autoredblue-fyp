"""Checkpointers for the AutoRedBlue graph.

Owner: Adeel (graph/orchestration engineering).

Two distinct checkpointers, per docs/ARCHITECTURE.md "Graph & orchestration
engineering":
- an in-memory checkpointer for the human-approval interrupt (pattern 3):
  state only needs to survive while a human is being asked to approve.
- a SQLite (on-disk) checkpointer for the Verification Agent's
  cross-session resume (pattern 4): state must survive a process restart,
  potentially days later, after a human applies a fix.
"""

from __future__ import annotations

# TODO: from langgraph.checkpoint.memory import MemorySaver
# TODO: from langgraph.checkpoint.sqlite import SqliteSaver


def get_approval_checkpointer():
    """Return the in-memory checkpointer used for the pre-scan approval gate.

    TODO
    """
    raise NotImplementedError


def get_verification_checkpointer():
    """Return the SQLite checkpointer used for the Verification Agent's
    cross-session resume.

    TODO
    """
    raise NotImplementedError
