import pytest
import yaml

from autoredblue.agents.scope_check import is_in_scope


def _write_allowlist(tmp_path, content):
    path = tmp_path / "allowlist.yaml"
    path.write_text(yaml.safe_dump(content), encoding="utf-8")
    return path


def test_allowed_target_passes(tmp_path):
    path = _write_allowlist(
        tmp_path,
        {"allowed_targets": [{"host": "localhost", "port": 8080, "description": "DVWA"}]},
    )
    assert is_in_scope("localhost:8080", allowlist_path=path) is True


def test_target_not_on_list_is_refused(tmp_path):
    path = _write_allowlist(
        tmp_path,
        {"allowed_targets": [{"host": "localhost", "port": 8080, "description": "DVWA"}]},
    )
    assert is_in_scope("example.com:443", allowlist_path=path) is False


def test_target_missing_port_is_refused(tmp_path):
    path = _write_allowlist(
        tmp_path,
        {"allowed_targets": [{"host": "localhost", "port": 8080, "description": "DVWA"}]},
    )
    assert is_in_scope("localhost", allowlist_path=path) is False


def test_empty_allowlist_file_fails_closed(tmp_path):
    path = tmp_path / "allowlist.yaml"
    path.write_text("", encoding="utf-8")
    assert is_in_scope("localhost:8080", allowlist_path=path) is False


def test_malformed_yaml_fails_closed(tmp_path):
    path = tmp_path / "allowlist.yaml"
    path.write_text("not: [valid yaml: structure", encoding="utf-8")
    assert is_in_scope("localhost:8080", allowlist_path=path) is False


def test_missing_allowed_targets_key_fails_closed(tmp_path):
    path = _write_allowlist(tmp_path, {"something_else": []})
    assert is_in_scope("localhost:8080", allowlist_path=path) is False


def test_allowed_targets_wrong_type_fails_closed(tmp_path):
    path = _write_allowlist(tmp_path, {"allowed_targets": "localhost:8080"})
    assert is_in_scope("localhost:8080", allowlist_path=path) is False


def test_missing_allowlist_file_raises(tmp_path):
    missing = tmp_path / "does_not_exist.yaml"
    with pytest.raises(FileNotFoundError):
        is_in_scope("localhost:8080", allowlist_path=missing)
