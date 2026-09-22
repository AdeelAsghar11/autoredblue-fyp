"""Thin subprocess wrapper around Nikto.

Owner: Adeel (used by the Scan Agent, agents/scan.py).

Runs Nikto as a subprocess. docs/PROGRESS.md notes Nikto is genuinely
annoying on native Windows: run it under WSL2 rather than fighting a
native port.
"""

from __future__ import annotations

# TODO: import subprocess


def run_nikto(target: str, *args: str) -> str:
    """Run Nikto against `target` and return the raw output.

    TODO
    """
    raise NotImplementedError
