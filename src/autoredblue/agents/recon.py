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

from autoredblue.llm import ollama_client, parsing

_PERCEPTOR_PROMPT_TEMPLATE = """You are the perception step of a security recon agent. \
You will be shown raw Nmap scan output. Think through what it shows, then \
respond with exactly one <action> block and nothing after it.

Required format:
<action>
<tool>record_findings</tool>
<args>{{"open_ports": [{{"port": <int>, "protocol": "tcp or udp", "service": "<name or null>", "product": "<name or null>", "version": "<string or null>"}}]}}</args>
</action>

Rules:
- <args> must be a single valid JSON object with exactly one key, "open_ports", a list.
- Only include ports Nmap reports as open (ignore closed/filtered ports).
- Use null (not omission) for any field Nmap didn't report.
- Write nothing after the closing </action> tag.

Raw Nmap output:
{raw_output}
"""


def build_perceptor_prompt(raw_nmap_output: str) -> str:
    return _PERCEPTOR_PROMPT_TEMPLATE.format(raw_output=raw_nmap_output)


def recon_perceptor(raw_nmap_output: str) -> dict:
    """Turn raw Nmap tool output into structured recon findings.

    Implements the plain-text-reason-then-parse pattern
    (docs/ARCHITECTURE.md "TOOL-CALLING PATTERN") for the Recon Agent's
    perceptor role: the model reasons freely, then emits one
    <action><tool>record_findings</tool><args>{...}</args></action>
    block; llm/parsing.py extracts the JSON. Raises parsing.ParseError on
    malformed model output, caught by the retry loop added in ROADMAP
    step 3.4.
    """
    completion = ollama_client.generate(build_perceptor_prompt(raw_nmap_output))
    parsed = parsing.parse_action(completion)
    return parsed["args"]


def run_recon(state):
    """Run Nmap + subfinder against `state["target"]` and return updated
    `recon_findings`.

    TODO (ROADMAP step 3.5): shell out via tools/nmap_tool.py and
    tools/subfinder_tool.py, then call recon_perceptor() on the combined
    raw output to produce the structured findings.
    """
    raise NotImplementedError
