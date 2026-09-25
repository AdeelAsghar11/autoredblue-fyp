"""Thin subprocess wrapper around subfinder (passive subdomain enumeration).

Owner: Asad (used by the Recon Agent, agents/recon.py).

Runs subfinder as a subprocess and returns a list of discovered
subdomains. No LLM involvement here: this is plumbing, not reasoning.
"""

from __future__ import annotations

import shutil
import subprocess


def _find_subfinder() -> str:
    found = shutil.which("subfinder")
    if not found:
        raise FileNotFoundError(
            "subfinder executable not found on PATH. Install it from "
            "https://github.com/projectdiscovery/subfinder/releases "
            "(see docs/ROADMAP.md step 3.2)."
        )
    return found


def enumerate_subdomains(domain: str) -> list[str]:
    """Run subfinder against `domain` and return discovered subdomains.

    An empty list is the expected, valid result for a target with no
    discoverable subdomains, not a failure: subfinder itself exits 0
    with empty output in that case, and this function passes that
    through cleanly rather than treating it as an error.
    """
    subfinder_bin = _find_subfinder()
    result = subprocess.run(
        [subfinder_bin, "-d", domain, "-silent"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]
