from pathlib import Path

from autoredblue.tools.nmap_tool import parse_nmap_xml

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "nmap_dvwa.xml"


def test_parses_real_dvwa_scan_output():
    """Parses the real Nmap XML saved in ROADMAP step 0.4 against DVWA.

    Confirms the structured output matches what was actually observed by
    hand: a single open port, 8080/tcp, running Apache 2.4.25.
    """
    findings = parse_nmap_xml(FIXTURE.read_text(encoding="utf-8"))

    assert findings == [
        {
            "port": 8080,
            "protocol": "tcp",
            "state": "open",
            "service": "http",
            "product": "Apache httpd",
            "version": "2.4.25",
        }
    ]


def test_ignores_non_open_ports():
    xml_output = """<?xml version="1.0"?>
    <nmaprun>
      <host>
        <ports>
          <port protocol="tcp" portid="80">
            <state state="filtered"/>
            <service name="http"/>
          </port>
          <port protocol="tcp" portid="443">
            <state state="open"/>
            <service name="https"/>
          </port>
        </ports>
      </host>
    </nmaprun>
    """

    findings = parse_nmap_xml(xml_output)

    assert len(findings) == 1
    assert findings[0]["port"] == 443


def test_handles_port_with_no_service_info():
    xml_output = """<?xml version="1.0"?>
    <nmaprun>
      <host>
        <ports>
          <port protocol="tcp" portid="9999">
            <state state="open"/>
          </port>
        </ports>
      </host>
    </nmaprun>
    """

    findings = parse_nmap_xml(xml_output)

    assert findings == [
        {
            "port": 9999,
            "protocol": "tcp",
            "state": "open",
            "service": None,
            "product": None,
            "version": None,
        }
    ]
