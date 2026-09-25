import pytest

from autoredblue.llm.parsing import ParseError, parse_action


def test_parses_well_formed_action():
    raw = """Let me think about this.
<action>
<tool>record_findings</tool>
<args>{"open_ports": [{"port": 8080, "protocol": "tcp"}]}</args>
</action>
"""
    result = parse_action(raw)
    assert result == {"tool": "record_findings", "args": {"open_ports": [{"port": 8080, "protocol": "tcp"}]}}


def test_ignores_reasoning_text_outside_action_block():
    raw = "I see port 8080 is open. <action><tool>x</tool><args>{}</args></action> done."
    result = parse_action(raw)
    assert result == {"tool": "x", "args": {}}


def test_missing_action_block_raises():
    with pytest.raises(ParseError, match="no <action>"):
        parse_action("just some reasoning with no tags at all")


def test_missing_tool_tag_raises():
    raw = "<action><args>{}</args></action>"
    with pytest.raises(ParseError, match="no <tool>"):
        parse_action(raw)


def test_empty_tool_tag_raises():
    raw = "<action><tool>   </tool><args>{}</args></action>"
    with pytest.raises(ParseError, match="empty"):
        parse_action(raw)


def test_missing_args_tag_raises():
    raw = "<action><tool>x</tool></action>"
    with pytest.raises(ParseError, match="no <args>"):
        parse_action(raw)


def test_invalid_json_in_args_raises():
    raw = "<action><tool>x</tool><args>{not valid json}</args></action>"
    with pytest.raises(ParseError, match="not valid JSON"):
        parse_action(raw)


def test_args_not_object_raises():
    raw = "<action><tool>x</tool><args>[1, 2, 3]</args></action>"
    with pytest.raises(ParseError, match="JSON object"):
        parse_action(raw)
