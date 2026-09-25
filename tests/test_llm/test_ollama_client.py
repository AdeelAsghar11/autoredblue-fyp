from unittest.mock import MagicMock, patch

import autoredblue.llm.ollama_client as ollama_client_module
from autoredblue.llm.ollama_client import generate


def test_uses_explicit_model_and_host(monkeypatch):
    monkeypatch.delenv("OLLAMA_HOST", raising=False)
    monkeypatch.delenv("OLLAMA_MODEL", raising=False)
    fake_response = MagicMock(response="hello")
    fake_client = MagicMock()
    fake_client.generate.return_value = fake_response

    with patch.object(ollama_client_module.ollama, "Client", return_value=fake_client) as client_cls:
        result = generate("prompt", model="custom-model", host="http://custom:1234")

    client_cls.assert_called_once_with(host="http://custom:1234")
    fake_client.generate.assert_called_once_with(model="custom-model", prompt="prompt")
    assert result == "hello"


def test_env_vars_override_settings_file(monkeypatch, tmp_path):
    settings_path = tmp_path / "settings.yaml"
    settings_path.write_text("ollama:\n  host: http://from-file:1\n  model: from-file-model\n")
    monkeypatch.setattr(ollama_client_module, "_SETTINGS_PATH", settings_path)
    monkeypatch.setenv("OLLAMA_HOST", "http://from-env:2")
    monkeypatch.setenv("OLLAMA_MODEL", "from-env-model")

    fake_response = MagicMock(response="ok")
    fake_client = MagicMock()
    fake_client.generate.return_value = fake_response

    with patch.object(ollama_client_module.ollama, "Client", return_value=fake_client) as client_cls:
        generate("prompt")

    client_cls.assert_called_once_with(host="http://from-env:2")
    fake_client.generate.assert_called_once_with(model="from-env-model", prompt="prompt")


def test_falls_back_to_settings_file_when_no_env_vars(monkeypatch, tmp_path):
    settings_path = tmp_path / "settings.yaml"
    settings_path.write_text("ollama:\n  host: http://from-file:1\n  model: from-file-model\n")
    monkeypatch.setattr(ollama_client_module, "_SETTINGS_PATH", settings_path)
    monkeypatch.delenv("OLLAMA_HOST", raising=False)
    monkeypatch.delenv("OLLAMA_MODEL", raising=False)

    fake_response = MagicMock(response="ok")
    fake_client = MagicMock()
    fake_client.generate.return_value = fake_response

    with patch.object(ollama_client_module.ollama, "Client", return_value=fake_client) as client_cls:
        generate("prompt")

    client_cls.assert_called_once_with(host="http://from-file:1")
    fake_client.generate.assert_called_once_with(model="from-file-model", prompt="prompt")


def test_falls_back_to_hardcoded_default_when_nothing_configured(monkeypatch, tmp_path):
    missing_settings_path = tmp_path / "does_not_exist.yaml"
    monkeypatch.setattr(ollama_client_module, "_SETTINGS_PATH", missing_settings_path)
    monkeypatch.delenv("OLLAMA_HOST", raising=False)
    monkeypatch.delenv("OLLAMA_MODEL", raising=False)

    fake_response = MagicMock(response="ok")
    fake_client = MagicMock()
    fake_client.generate.return_value = fake_response

    with patch.object(ollama_client_module.ollama, "Client", return_value=fake_client) as client_cls:
        generate("prompt")

    client_cls.assert_called_once_with(host=ollama_client_module._FALLBACK_HOST)
    fake_client.generate.assert_called_once_with(
        model=ollama_client_module._FALLBACK_MODEL, prompt="prompt"
    )
