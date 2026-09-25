"""Local model serving wrapper around Ollama.

Owner: Adeel (shared infra underlying every agent's LLM calls; not called
out separately from "graph/orchestration engineering" in docs/PROJECT.md
or docs/ARCHITECTURE.md, attributed here since every agent node depends
on it).

Thin client around the Ollama HTTP API. Reads host/model from
config/settings.yaml (see config/settings.example.yaml), with
OLLAMA_HOST/OLLAMA_MODEL environment variables (see .env.example) taking
priority when set. Every agent that calls the LLM goes through this
module; no agent should talk to Ollama directly.
"""

from __future__ import annotations

import os
from pathlib import Path

import ollama
import yaml

_SETTINGS_PATH = Path(__file__).resolve().parents[3] / "config" / "settings.yaml"
_FALLBACK_HOST = "http://localhost:11434"
_FALLBACK_MODEL = "qwen2.5-coder:7b"


def _load_settings() -> dict:
    if not _SETTINGS_PATH.is_file():
        return {}
    try:
        data = yaml.safe_load(_SETTINGS_PATH.read_text(encoding="utf-8"))
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def _resolve(key: str, env_var: str, fallback: str) -> str:
    env_value = os.environ.get(env_var)
    if env_value:
        return env_value
    settings = _load_settings().get("ollama")
    if isinstance(settings, dict) and settings.get(key):
        return settings[key]
    return fallback


def generate(prompt: str, *, model: str | None = None, host: str | None = None) -> str:
    """Send `prompt` to the configured Ollama model and return the raw
    text completion.

    `model`/`host` override config/settings.yaml and the environment
    when passed explicitly; otherwise resolution order is env var ->
    config/settings.yaml -> a hardcoded dev-machine fallback.
    """
    resolved_host = host or _resolve("host", "OLLAMA_HOST", _FALLBACK_HOST)
    resolved_model = model or _resolve("model", "OLLAMA_MODEL", _FALLBACK_MODEL)
    client = ollama.Client(host=resolved_host)
    response = client.generate(model=resolved_model, prompt=prompt)
    return response.response
