import json

from autoredblue.graph.state import AuditState


def test_state_can_be_constructed_with_only_target():
    state: AuditState = {"target": "localhost:8080"}
    assert state["target"] == "localhost:8080"


def test_state_can_be_constructed_and_serialized():
    state: AuditState = {
        "target": "localhost:8080",
        "scope_allowlist": [{"host": "localhost", "port": 8080, "description": "DVWA"}],
        "scope_allowed": True,
        "recon_findings": {},
        "scan_findings_raw": {},
        "triaged_findings": [],
        "approval_state": False,
        "verification_results": [],
    }

    serialized = json.dumps(state)
    deserialized = json.loads(serialized)

    assert deserialized == state
