# AGENTS.md — AutoRedBlue

Read `docs/PROJECT.md`, `docs/ARCHITECTURE.md`, `docs/DECISIONS.md`, `docs/PROGRESS.md`, and `docs/RESEARCH.md` before making any change in this repo. They are the actual source of truth: architecture, every design decision and why it was made, current status, and verified research backing the approach. This file is a pointer and a set of hard boundaries, not a replacement, nothing here overrides what's in those five.

## Non-negotiable boundaries
These exist because they're easy to violate by accident while coding, not because they're likely to be violated on purpose.
- Never write code that attempts real exploitation against a target. Findings get reported, and after a human patches them, verified by replaying a saved benign request. Nothing more. See ARCHITECTURE.md's Scan, Triage, and Verification agent sections.
- Every scan target must be checked against `config/allowlist.yaml` before any tool runs. Never remove or bypass this check, even for local testing convenience.
- Any active or intrusive scan step requires the human-approval gate. Don't build a path that skips it.
- Valid test targets right now: DVWA, OWASP Juice Shop, Metasploitable. No other host, local or remote, until a signed authorisation exists, which it currently does not.

## Working agreements
- Follow PROGRESS.md's "Next concrete task" order. Don't jump to building all five agents before the thin end-to-end slice (Recon → one scan type → basic report, retry loop and approval interrupt included from the start) is proven.
- Log any real design decision in `docs/DECISIONS.md` as you make it: dated, one line, with the one-sentence reason. This has already drifted out of sync with what was actually built once on this project and cost a cleanup pass to fix, don't let it happen again.
- Team ownership (see PROJECT.md for the reasoning): Adeel owns Scan, Triage, Report, Verification, and the graph/orchestration layer. Asad owns Recon, the Dashboard, and documentation.
- No OS install is required to start. Ollama, Docker, Nmap, OWASP ZAP, sqlmap, Playwright, and the Python stack all run natively on Windows. Only Nikto is genuinely annoying there, use WSL2 for it specifically, not before.
- Style: no em dashes in generated documentation or reports. Use commas, colons, or parentheses instead.

## Quick commands
Fill in once the repo has real build/test/run commands.
