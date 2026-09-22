"""Scope allow-list check (module 0, pre-recon gate).

Owner: Adeel (graph/orchestration engineering): no explicit owner is
named in docs/PROJECT.md or docs/ARCHITECTURE.md for this module;
attributed here to Adeel since it is plain gating code, not an LLM agent,
and sits with the rest of the graph/orchestration engineering. Flag if
this should instead sit with Asad's Recon Agent.

Plain code, no LLM (docs/ARCHITECTURE.md "0. Scope Allow-list Check").
Confirms `target` exactly matches an entry in config/allowlist.yaml
(copied and populated from config/allowlist.example.yaml) and refuses to
proceed otherwise. Runs before the Recon Agent.
"""

from __future__ import annotations

# TODO: import yaml; load config/allowlist.yaml relative to the repo root


def is_in_scope(target: str) -> bool:
    """Return True if `target` exactly matches an allow-list entry.

    TODO: load config/allowlist.yaml, compare against `target`, raise a
    clear error (not proceed silently) if the allow-list file is missing,
    see config/allowlist.example.yaml for the expected format.
    """
    raise NotImplementedError
