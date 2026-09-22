"""PyWebView desktop entry point for the AutoRedBlue dashboard.

Owner: Asad.

Wraps the FastAPI-served dashboard (dashboard/api.py) in a native OS
window via PyWebView, satisfying the "Desktop Application" Project
Streams classification (docs/DECISIONS.md 2026-09-06) without changing
how the dashboard itself is built.
"""

from __future__ import annotations

# TODO: import webview (pywebview)
# TODO: from autoredblue.dashboard.api import create_app


def main():
    """Start the FastAPI app and open it in a native PyWebView window.

    TODO
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
