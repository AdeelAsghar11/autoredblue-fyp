"""FastAPI backend for the AutoRedBlue dashboard.

Owner: Asad.

Serves both the API and the browser-based frontend, running on the same
machine as the agent pipeline, locally-served, not internet-facing
(docs/ARCHITECTURE.md "7. Dashboard (UI module)"). Screens: target/scope
entry, live pipeline status, the human-approval interface (the actual
control for the gate in docs/ARCHITECTURE.md section 2), and the
findings/report viewer.
"""

from __future__ import annotations

# TODO: from fastapi import FastAPI


def create_app():
    """Build and return the FastAPI app.

    TODO: routes for target/scope entry, live pipeline status, the
    human-approval interrupt, and the findings/report viewer.
    """
    raise NotImplementedError
