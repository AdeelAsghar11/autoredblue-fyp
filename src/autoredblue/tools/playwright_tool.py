"""Thin wrapper around Playwright.

Owner: Adeel (used by the Scan Agent for authenticated scanning and by
the Verification Agent to replay saved requests, agents/scan.py and
agents/verify.py).

Two jobs, per docs/ARCHITECTURE.md "3. Scan Agent" and "6. Verification
Agent": (a) drive the target's login form so the Scan Agent's
authenticated pass has a live session, and reach JavaScript-rendered
content; (b) replay a saved Playwright snippet for the Verification
Agent.
"""

from __future__ import annotations

# TODO: from playwright.sync_api import sync_playwright


def login(target_url: str, username: str, password: str):
    """Drive the login form at `target_url` and return an authenticated
    session/context for the Scan Agent's authenticated pass.

    TODO
    """
    raise NotImplementedError


def replay_snippet(snippet: str):
    """Replay a saved Playwright snippet (from a triaged finding) and
    return the resulting response/page state for the Verification Agent.

    TODO
    """
    raise NotImplementedError
