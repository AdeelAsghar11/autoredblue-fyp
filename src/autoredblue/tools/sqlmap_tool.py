"""Thin subprocess wrapper around sqlmap.

Owner: Adeel (used by the Scan Agent, agents/scan.py).

Runs sqlmap as a subprocess against a specific parameter/endpoint the
Scan Agent has identified as worth testing, and returns its raw output.
"""

from __future__ import annotations

# TODO: import subprocess


def run_sqlmap(target_url: str, *args: str) -> str:
    """Run sqlmap against `target_url` and return the raw output.

    TODO
    """
    raise NotImplementedError
