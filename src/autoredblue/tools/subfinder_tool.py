"""Thin subprocess wrapper around subfinder.

Owner: Asad (used by the Recon Agent, agents/recon.py).

Runs subfinder as a subprocess for subdomain enumeration and returns its
raw output for the Recon Agent to parse.
"""

from __future__ import annotations

# TODO: import subprocess


def run_subfinder(target: str, *args: str) -> str:
    """Run subfinder against `target` and return the raw output.

    TODO
    """
    raise NotImplementedError
