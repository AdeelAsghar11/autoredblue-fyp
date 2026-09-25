from autoredblue.graph.build_graph import build_reason_then_parse_graph
from autoredblue.llm.parsing import parse_action

VALID_COMPLETION = '<action><tool>x</tool><args>{"ok": true}</args></action>'
MALFORMED_COMPLETION = "no tags here at all"


def test_retry_loop_recovers_after_transient_failures():
    completions = iter([MALFORMED_COMPLETION, MALFORMED_COMPLETION, VALID_COMPLETION])
    errors_seen = []

    def reason_fn(state):
        errors_seen.append(state.get("llm_error"))
        return next(completions)

    graph = build_reason_then_parse_graph(reason_fn, parse_action, max_attempts=3)
    result = graph.invoke({})

    assert result["llm_failed"] is False
    assert result["llm_result"] == {"tool": "x", "args": {"ok": True}}
    assert result["llm_attempts"] == 3
    assert len(errors_seen) == 3
    assert errors_seen[0] is None
    assert errors_seen[1] is not None
    assert errors_seen[2] is not None


def test_retry_loop_gives_up_gracefully_after_max_attempts():
    errors_seen = []

    def reason_fn(state):
        errors_seen.append(state.get("llm_error"))
        return MALFORMED_COMPLETION

    graph = build_reason_then_parse_graph(reason_fn, parse_action, max_attempts=3)
    result = graph.invoke({})

    assert result["llm_failed"] is True
    assert "llm_result" not in result
    assert result["llm_attempts"] == 3
    assert len(errors_seen) == 3


def test_retry_loop_succeeds_immediately_without_retrying():
    calls = []

    def reason_fn(state):
        calls.append(state.get("llm_error"))
        return VALID_COMPLETION

    graph = build_reason_then_parse_graph(reason_fn, parse_action, max_attempts=3)
    result = graph.invoke({})

    assert result["llm_failed"] is False
    assert result["llm_attempts"] == 1
    assert len(calls) == 1
