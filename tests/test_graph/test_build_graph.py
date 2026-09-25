import logging

import yaml

from autoredblue.graph.build_graph import build_graph


def _write_allowlist(tmp_path, targets):
    path = tmp_path / "allowlist.yaml"
    path.write_text(yaml.safe_dump({"allowed_targets": targets}), encoding="utf-8")
    return path


def test_allowed_target_runs_both_nodes_in_order(tmp_path, caplog):
    allowlist_path = _write_allowlist(
        tmp_path, [{"host": "localhost", "port": 8080, "description": "DVWA"}]
    )
    graph = build_graph(allowlist_path=allowlist_path)

    with caplog.at_level(logging.INFO):
        result = graph.invoke({"target": "localhost:8080"})

    assert result["scope_allowed"] is True
    assert result["recon_findings"] == {"stub": True}
    assert "recon ran" in caplog.text


def test_disallowed_target_stops_before_recon_node(tmp_path, caplog):
    allowlist_path = _write_allowlist(
        tmp_path, [{"host": "localhost", "port": 8080, "description": "DVWA"}]
    )
    graph = build_graph(allowlist_path=allowlist_path)

    with caplog.at_level(logging.INFO):
        result = graph.invoke({"target": "evil.example.com:80"})

    assert result["scope_allowed"] is False
    assert "recon_findings" not in result
    assert "recon ran" not in caplog.text
