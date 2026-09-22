"""Scan Agent.

Owner: Adeel.

Orchestrates OWASP ZAP, Nikto, and sqlmap against in-scope assets found by
Recon. Uses Playwright to drive the login form for authenticated scanning
and to reach JavaScript-rendered content. Runs an unauthenticated pass
followed by an authenticated pass (docs/ARCHITECTURE.md "3. Scan Agent").

Implements the plain-text-reason-then-parse tool-calling pattern (see
llm/parsing.py and docs/ARCHITECTURE.md "TOOL-CALLING PATTERN"): the model
reasons and chooses a tool in loose XML-ish tags with no grammar
constraint; a separate parsing step turns that into the JSON each tool
wrapper needs. Do not switch this to Ollama's strict JSON/grammar-
constrained mode, see docs/DECISIONS.md 2026-08-24 for why.
"""

from __future__ import annotations

# TODO: from autoredblue.tools import zap_tool, nikto_tool, sqlmap_tool, playwright_tool
# TODO: from autoredblue.llm import ollama_client, parsing


def run_unauthenticated_pass(state):
    """Scan everything reachable with no account.

    TODO
    """
    raise NotImplementedError


def run_authenticated_pass(state):
    """Log in with the provided low-privilege test account (via
    tools/playwright_tool.py) and re-scan what's now reachable.

    TODO
    """
    raise NotImplementedError
