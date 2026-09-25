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

from autoredblue.graph.retry_loop import build_reason_then_parse_graph
from autoredblue.llm import ollama_client, parsing
from autoredblue.tools import nmap_tool, subfinder_tool

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


def _split_target(target: str) -> tuple[str, int]:
    host, _, port_str = target.partition(":")
    return host, int(port_str)


def _build_reason_fn(raw_nmap_output: str):
    """Build the retry loop's `reason_fn` for one recon run.

    Closes over the raw Nmap output (fixed for the whole retry loop) and
    folds the previous attempt's parse error back into the prompt when
    present, the "error appended to context" half of the retry pattern
    (ROADMAP step 3.4, ARCHITECTURE.md pattern 1).
    """

    def reason_fn(state) -> str:
        prompt = build_perceptor_prompt(raw_nmap_output)
        previous_error = state.get("llm_error")
        if previous_error:
            prompt += (
                f"\n\nYour previous attempt could not be parsed: {previous_error}\n"
                "Fix the <action> block and try again, following the format exactly."
            )
        return ollama_client.generate(prompt)

    return reason_fn


def run_recon(state) -> dict:
    """Run Nmap + subfinder against `state["target"]` and return updated
    `recon_findings`.

    Nmap runs in its plain-text (-oN) format, the same shape the LLM
    perceptor was validated against (ROADMAP step 3.3), and is turned
    into structured `open_ports` findings via the reason-then-parse
    retry loop (step 3.4), capped at 3 attempts. subfinder's subdomain
    list is passed through as-is; no LLM involvement there, it's already
    structured. If the model still can't produce a parseable result
    after 3 tries, recon_findings records the failure instead of
    crashing the pipeline.
    """
    host, port = _split_target(state["target"])
    raw_nmap_output = nmap_tool.run_nmap(host, "-sV", "-p", str(port), output_format="normal")
    subdomains = subfinder_tool.enumerate_subdomains(host)

    retry_graph = build_reason_then_parse_graph(
        _build_reason_fn(raw_nmap_output), parsing.parse_action, max_attempts=3
    )
    retry_result = retry_graph.invoke({})

    if retry_result.get("llm_failed"):
        return {
            "recon_findings": {
                "open_ports": [],
                "subdomains": subdomains,
                "error": retry_result.get("llm_error"),
            }
        }

    open_ports = retry_result["llm_result"]["args"].get("open_ports", [])
    return {"recon_findings": {"open_ports": open_ports, "subdomains": subdomains}}
