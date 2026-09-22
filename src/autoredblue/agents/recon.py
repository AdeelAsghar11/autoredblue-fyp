"""Recon Agent.

Owner: Asad.

Wraps Nmap (port/service discovery) and subfinder (subdomain enumeration)
as subprocesses (see tools/nmap_tool.py, tools/subfinder_tool.py). Parses
raw tool output into `recon_findings` on the graph state. The LLM's only
role here is the "perceptor" role (turning raw tool output into clean
structured state); it does not decide attack strategy
(docs/ARCHITECTURE.md "1. Recon Agent").
"""

from __future__ import annotations

# TODO: from autoredblue.tools import nmap_tool, subfinder_tool
# TODO: from autoredblue.llm import ollama_client


def run_recon(state):
    """Run Nmap + subfinder against `state["target"]` and return updated
    `recon_findings`.

    TODO: shell out via tools/nmap_tool.py and tools/subfinder_tool.py,
    then have the LLM turn the combined raw output into structured
    findings.
    """
    raise NotImplementedError
