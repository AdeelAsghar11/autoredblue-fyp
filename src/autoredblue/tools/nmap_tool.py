"""Thin subprocess wrapper around Nmap.

Owner: Asad (used by the Recon Agent, agents/recon.py).

Runs Nmap as a subprocess, parses its XML output, and returns a
structured list of open ports/services. No LLM involvement here: this
is plumbing, not reasoning; the Recon Agent's LLM step (ROADMAP 3.3)
only ever sees this structured output, never raw Nmap XML.
"""

from __future__ import annotations

import shutil
import subprocess
import xml.etree.ElementTree as ET

# Nmap's own installer doesn't always put nmap.exe on PATH on Windows;
# fall back to its default install locations rather than requiring the
# caller to know this.
_WINDOWS_FALLBACK_PATHS = (
    r"C:\Program Files (x86)\Nmap\nmap.exe",
    r"C:\Program Files\Nmap\nmap.exe",
)


def _find_nmap() -> str:
    on_path = shutil.which("nmap")
    if on_path:
        return on_path
    for candidate in _WINDOWS_FALLBACK_PATHS:
        if shutil.which(candidate):
            return candidate
    raise FileNotFoundError(
        "nmap executable not found on PATH or in common Windows install "
        "locations. Install it (see docs/ROADMAP.md step 0.4)."
    )


_OUTPUT_FLAGS = {"xml": "-oX", "normal": "-oN"}


def run_nmap(host: str, *args: str, output_format: str = "xml") -> str:
    """Run Nmap against `host` with extra `args` and return raw output.

    `args` are forwarded to Nmap as-is (e.g. "-sV", "-p", "8080"); this
    function doesn't interpret them, it only appends the output flag for
    `output_format` ("xml", the default, for parse_nmap_xml(); "normal"
    for the human-readable -oN format the Recon Agent's LLM perceptor
    was validated against, see ROADMAP step 3.3).
    """
    nmap_bin = _find_nmap()
    result = subprocess.run(
        [nmap_bin, *args, _OUTPUT_FLAGS[output_format], "-", host],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def parse_nmap_xml(xml_output: str) -> list[dict]:
    """Parse Nmap XML output into a structured list of open ports/services.

    Each entry: {"port": int, "protocol": str, "state": str,
    "service": str | None, "product": str | None, "version": str | None}.
    Only ports Nmap reports as "open" are included; the Recon Agent cares
    about the attack surface, not the full closed/filtered port table.
    """
    root = ET.fromstring(xml_output)
    findings: list[dict] = []
    for host_el in root.findall("host"):
        for port_el in host_el.findall("./ports/port"):
            state_el = port_el.find("state")
            if state_el is None or state_el.get("state") != "open":
                continue
            service_el = port_el.find("service")
            findings.append(
                {
                    "port": int(port_el.get("portid")),
                    "protocol": port_el.get("protocol"),
                    "state": state_el.get("state"),
                    "service": service_el.get("name") if service_el is not None else None,
                    "product": service_el.get("product") if service_el is not None else None,
                    "version": service_el.get("version") if service_el is not None else None,
                }
            )
    return findings


def scan_target(host: str, *args: str) -> list[dict]:
    """Run Nmap against `host` and return the parsed, structured findings."""
    return parse_nmap_xml(run_nmap(host, *args))
