from unittest.mock import patch

import pytest

from autoredblue.agents.recon import recon_perceptor
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
