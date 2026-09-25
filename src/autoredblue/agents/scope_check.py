"""Scope allow-list check (module 0, pre-recon gate).

Owner: Adeel, graph/orchestration layer (docs/AGENTS.md team ownership).
Plain code, no LLM (docs/ARCHITECTURE.md "0. Scope Allow-list Check").
Confirms `target` exactly matches an entry in config/allowlist.yaml
(copied and populated from config/allowlist.example.yaml) and refuses to
proceed otherwise. Runs before the Recon Agent.
"""

from __future__ import annotations

from pathlib import Path

import yaml

DEFAULT_ALLOWLIST_PATH = Path(__file__).resolve().parents[3] / "config" / "allowlist.yaml"


def _load_allowed_targets(allowlist_path: Path) -> list[dict]:
    """Load the `allowed_targets` entries from an allow-list YAML file.

    Fails closed: any problem with the allow-list's *contents* (empty
    file, invalid YAML, missing/wrong-typed `allowed_targets`, malformed
    entries) returns an empty list rather than raising, so is_in_scope()
    ends up refusing every target instead of accidentally allowing one.
    A missing *file* is a different kind of problem (a setup mistake,
    not an empty scope) and is left to the caller to raise on.
    """
    raw = allowlist_path.read_text(encoding="utf-8")

    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError:
        return []

    if not isinstance(data, dict):
        return []

    targets = data.get("allowed_targets")
    if not isinstance(targets, list):
        return []

    return [
        entry
        for entry in targets
        if isinstance(entry, dict) and "host" in entry and "port" in entry
    ]


def is_in_scope(target: str, allowlist_path: Path | None = None) -> bool:
    """Return True if `target` ("host:port") exactly matches an allow-list entry.

    Raises FileNotFoundError if the allow-list file itself does not
    exist: that means the project was never set up for a run (see
    config/allowlist.example.yaml), which should stop things loudly
    rather than silently refuse or silently allow. Any other problem
    with the file's contents fails closed (refuses) via
    _load_allowed_targets, per ARCHITECTURE.md's scope-gate requirement.
    """
    path = allowlist_path or DEFAULT_ALLOWLIST_PATH
    if not path.is_file():
        raise FileNotFoundError(
            f"Allow-list not found at {path}. Copy "
            "config/allowlist.example.yaml to config/allowlist.yaml and "
            "populate it before running any scan."
        )

    host, sep, port_str = target.partition(":")
    if not sep:
        return False
    try:
        port = int(port_str)
    except ValueError:
        return False

    return any(
        entry.get("host") == host and entry.get("port") == port
        for entry in _load_allowed_targets(path)
    )
