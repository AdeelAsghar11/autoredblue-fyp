"""Thin subprocess wrapper around Nmap.

Owner: Asad (used by the Recon Agent, agents/recon.py).

Runs Nmap as a subprocess and returns its raw XML output for the Recon
Agent to parse. No LLM involvement here: this is plumbing, not reasoning.
"""

from __future__ import annotations

# TODO: import subprocess


def run_nmap(target: str, *args: str) -> str:
    """Run Nmap against `target` and return the raw XML output.

    TODO
    """
    raise NotImplementedError
