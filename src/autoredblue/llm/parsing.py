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

import json
import re

_ACTION_RE = re.compile(r"<action>(.*?)</action>", re.DOTALL)
_TOOL_RE = re.compile(r"<tool>(.*?)</tool>", re.DOTALL)
_ARGS_RE = re.compile(r"<args>(.*?)</args>", re.DOTALL)


class ParseError(Exception):
    """Raised when the model's loose XML-ish output can't be parsed.

    Caught by the retry loop in graph/build_graph.py.
    """


def parse_action(raw_text: str) -> dict:
    """Parse a model completion containing <action>/<tool>/<args>-style
    tags into a plain dict: {"tool": str, "args": dict}.

    Anything the model wrote outside the <action> block (its reasoning)
    is ignored on purpose, that text did its job by improving the
    reasoning quality and was never meant to be parsed. Raises
    ParseError, not a bare exception, on any malformed input so the
    retry loop can catch it specifically.
    """
    action_match = _ACTION_RE.search(raw_text)
    if not action_match:
        raise ParseError("no <action>...</action> block found in model output")
    action_body = action_match.group(1)

    tool_match = _TOOL_RE.search(action_body)
    if not tool_match:
        raise ParseError("no <tool>...</tool> tag found inside <action>")
    tool = tool_match.group(1).strip()
    if not tool:
        raise ParseError("<tool> tag is empty")

    args_match = _ARGS_RE.search(action_body)
    if not args_match:
        raise ParseError("no <args>...</args> tag found inside <action>")
    args_text = args_match.group(1).strip()

    try:
        args = json.loads(args_text)
    except json.JSONDecodeError as exc:
        raise ParseError(f"<args> content is not valid JSON: {exc}") from exc

    if not isinstance(args, dict):
        raise ParseError("<args> content must be a JSON object")

    return {"tool": tool, "args": args}
