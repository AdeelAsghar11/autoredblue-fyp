from unittest.mock import MagicMock, patch

from autoredblue.tools.subfinder_tool import enumerate_subdomains


def test_returns_empty_list_when_nothing_found():
    fake_result = MagicMock(stdout="")
    with patch(
        "autoredblue.tools.subfinder_tool.subprocess.run", return_value=fake_result
    ) as mock_run:
        result = enumerate_subdomains("nonexistent-domain-autoredblue-test.invalid")

    assert result == []
    mock_run.assert_called_once()


def test_parses_discovered_subdomains():
    fake_result = MagicMock(stdout="www.example.com\napi.example.com\n\n")
    with patch("autoredblue.tools.subfinder_tool.subprocess.run", return_value=fake_result):
        result = enumerate_subdomains("example.com")

    assert result == ["www.example.com", "api.example.com"]
