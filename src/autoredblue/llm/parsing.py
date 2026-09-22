"""The plain-text-reason-then-parse tool-calling pattern.

Owner: Adeel.

docs/ARCHITECTURE.md "TOOL-CALLING PATTERN" (the single most important
reliability decision, docs/DECISIONS.md 2026-08-24): the model outputs
its reasoning and tool choice in loose, guided XML-ish tags (e.g.
<action>, <tool>, <args>) with no grammar constraint, because forcing
strict JSON in the same call the model reasons in measurably degrades
the reasoning (the "constraint tax" effect, arXiv:2606.25605). This
module owns the second step: parsing that loose text into the exact JSON
each tool wrapper needs, in plain Python.

Feeds the retry-on-parse-failure loop in graph/build_graph.py: a parse
failure here is what routes the graph back to the reasoning node.
"""

from __future__ import annotations


class ParseError(Exception):
    """Raised when the model's loose XML-ish output can't be parsed.

    Caught by the retry loop in graph/build_graph.py.
    """


def parse_action(raw_text: str) -> dict:
    """Parse a model completion containing <action>/<tool>/<args>-style
    tags into a plain dict the tool wrappers can consume.

    TODO: regex / small parser, see docs/ARCHITECTURE.md "TOOL-CALLING
    PATTERN". Raise ParseError (not a bare exception) on malformed input
    so the retry loop can catch it specifically.
    """
    raise NotImplementedError
