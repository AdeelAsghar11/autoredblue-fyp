"""Thin wrapper around OWASP ZAP.

Owner: Adeel (used by the Scan Agent, agents/scan.py).

Drives a ZAP scan (unauthenticated or authenticated pass) against
in-scope assets and returns its raw output for the Scan Agent to collect
into `scan_findings_raw`.
"""

from __future__ import annotations

# TODO: ZAP has a REST API (python-owasp-zap-v2.4) as well as a CLI,
# decide which at implementation time.


def run_zap_scan(target: str, *, authenticated: bool = False):
    """Run a ZAP scan against `target`.

    TODO
    """
    raise NotImplementedError
