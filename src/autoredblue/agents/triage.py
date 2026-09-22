"""Triage Agent.

Owner: Adeel.

Deduplicates `scan_findings_raw`, filters likely false positives, and
assigns CVSS-based severity. The first genuinely AI-reasoning-heavy stage
(docs/ARCHITECTURE.md "4. Triage Agent").

REPRODUCIBLE-REQUEST REQUIREMENT (docs/DECISIONS.md 2026-08-24): every
finding kept here must carry a saved, replayable request (a concrete HTTP
request or short Playwright snippet) that demonstrates the issue. A
finding that can't be reduced to one is downgraded. This is a benign
saved request that shows the condition, not an autonomous exploit; keep
it that way. The Verification Agent (agents/verify.py) replays this exact
request later.
"""

from __future__ import annotations

# TODO: from autoredblue.llm import ollama_client, parsing


def triage_findings(state):
    """Dedupe + score `scan_findings_raw`, attach a saved replayable
    request per kept finding, and write `triaged_findings`.

    TODO
    """
    raise NotImplementedError
