from unittest.mock import patch

import pytest

from autoredblue.agents.recon import recon_perceptor, run_recon
from autoredblue.llm.parsing import ParseError

RAW_NMAP_OUTPUT = "PORT     STATE SERVICE VERSION\n8080/tcp open  http    Apache httpd 2.4.25 ((Debian))\n"

WELL_FORMED_COMPLETION = """The scan shows one open port.
<action>
<tool>record_findings</tool>
<args>{"open_ports": [{"port": 8080, "protocol": "tcp", "service": "http", "product": "Apache httpd", "version": "2.4.25"}]}</args>
</action>
"""


def test_recon_perceptor_parses_llm_output_into_structured_findings():
    with patch(
        "autoredblue.agents.recon.ollama_client.generate", return_value=WELL_FORMED_COMPLETION
    ) as mock_generate:
        result = recon_perceptor(RAW_NMAP_OUTPUT)

    assert result == {
        "open_ports": [
            {
                "port": 8080,
                "protocol": "tcp",
                "service": "http",
                "product": "Apache httpd",
                "version": "2.4.25",
            }
        ]
    }
    prompt_passed = mock_generate.call_args[0][0]
    assert RAW_NMAP_OUTPUT in prompt_passed


def test_recon_perceptor_raises_parse_error_on_malformed_llm_output():
    with patch("autoredblue.agents.recon.ollama_client.generate", return_value="no tags here"):
        with pytest.raises(ParseError):
            recon_perceptor(RAW_NMAP_OUTPUT)


def test_run_recon_returns_structured_findings_on_success():
    state = {"target": "localhost:8080"}
    with (
        patch(
            "autoredblue.agents.recon.nmap_tool.run_nmap", return_value=RAW_NMAP_OUTPUT
        ) as mock_nmap,
        patch(
            "autoredblue.agents.recon.subfinder_tool.enumerate_subdomains",
            return_value=["www.example.com"],
        ) as mock_subfinder,
        patch(
            "autoredblue.agents.recon.ollama_client.generate",
            return_value=WELL_FORMED_COMPLETION,
        ),
    ):
        result = run_recon(state)

    mock_nmap.assert_called_once_with("localhost", "-sV", "-p", "8080", output_format="normal")
    mock_subfinder.assert_called_once_with("localhost")
    assert result == {
        "recon_findings": {
            "open_ports": [
                {
                    "port": 8080,
                    "protocol": "tcp",
                    "service": "http",
                    "product": "Apache httpd",
                    "version": "2.4.25",
                }
            ],
            "subdomains": ["www.example.com"],
        }
    }


def test_run_recon_records_failure_gracefully_after_exhausting_retries():
    state = {"target": "localhost:8080"}
    with (
        patch("autoredblue.agents.recon.nmap_tool.run_nmap", return_value=RAW_NMAP_OUTPUT),
        patch(
            "autoredblue.agents.recon.subfinder_tool.enumerate_subdomains", return_value=[]
        ),
        patch(
            "autoredblue.agents.recon.ollama_client.generate",
            return_value="the model never produces a parseable action",
        ) as mock_generate,
    ):
        result = run_recon(state)

    assert mock_generate.call_count == 3
    assert result["recon_findings"]["open_ports"] == []
    assert result["recon_findings"]["subdomains"] == []
    assert result["recon_findings"]["error"] is not None
