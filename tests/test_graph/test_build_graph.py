from unittest.mock import patch

import yaml

from autoredblue.graph.build_graph import build_graph

VALID_COMPLETION = (
    '<action><tool>record_findings</tool>'
    '<args>{"open_ports": [{"port": 8080, "protocol": "tcp", "service": "http", '
    '"product": "Apache httpd", "version": "2.4.25"}]}</args></action>'
)


def _write_allowlist(tmp_path, targets):
    path = tmp_path / "allowlist.yaml"
    path.write_text(yaml.safe_dump({"allowed_targets": targets}), encoding="utf-8")
    return path


def test_allowed_target_runs_scope_check_then_real_recon(tmp_path):
    allowlist_path = _write_allowlist(
        tmp_path, [{"host": "localhost", "port": 8080, "description": "DVWA"}]
    )
    graph = build_graph(allowlist_path=allowlist_path)

    with (
        patch(
            "autoredblue.agents.recon.nmap_tool.run_nmap",
            return_value="8080/tcp open http Apache httpd 2.4.25",
        ) as mock_nmap,
        patch(
            "autoredblue.agents.recon.subfinder_tool.enumerate_subdomains", return_value=[]
        ) as mock_subfinder,
        patch("autoredblue.agents.recon.ollama_client.generate", return_value=VALID_COMPLETION),
    ):
        result = graph.invoke({"target": "localhost:8080"})

    assert result["scope_allowed"] is True
    assert result["recon_findings"] == {
        "open_ports": [
            {
                "port": 8080,
                "protocol": "tcp",
                "service": "http",
                "product": "Apache httpd",
                "version": "2.4.25",
            }
        ],
        "subdomains": [],
    }
    mock_nmap.assert_called_once_with("localhost", "-sV", "-p", "8080", output_format="normal")
    mock_subfinder.assert_called_once_with("localhost")


def test_disallowed_target_stops_before_recon_node(tmp_path):
    allowlist_path = _write_allowlist(
        tmp_path, [{"host": "localhost", "port": 8080, "description": "DVWA"}]
    )
    graph = build_graph(allowlist_path=allowlist_path)

    with patch("autoredblue.agents.recon.nmap_tool.run_nmap") as mock_nmap:
        result = graph.invoke({"target": "evil.example.com:80"})

    assert result["scope_allowed"] is False
    assert "recon_findings" not in result
    mock_nmap.assert_not_called()
