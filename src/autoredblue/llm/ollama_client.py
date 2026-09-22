"""Local model serving wrapper around Ollama.

Owner: Adeel (shared infra underlying every agent's LLM calls; not called
out separately from "graph/orchestration engineering" in docs/PROJECT.md
or docs/ARCHITECTURE.md, attributed here since every agent node depends
on it).

Thin client around the Ollama HTTP API. Reads host/model from
config/settings.yaml (see config/settings.example.yaml). Every agent
that calls the LLM goes through this module; no agent should talk to
Ollama directly.
"""

from __future__ import annotations

# TODO: import requests (or the `ollama` python package)


def generate(prompt: str, *, model: str | None = None) -> str:
    """Send `prompt` to the configured Ollama model and return the raw
    text completion.

    TODO
    """
    raise NotImplementedError
