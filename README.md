# AutoRedBlue

AutoRedBlue is a multi-agent AI system that automates web application security audits **entirely on the client's own infrastructure**. A chain of specialised agents (reconnaissance, scanning, triage, reporting, and remediation verification) is coordinated with LangGraph and backed by a single open-weight LLM served locally via Ollama, so no scan data, finding, or reasoning ever leaves the client's servers. The motivating gap is Pakistan's data-residency requirements for public-sector systems (the WASL framework / National Data Governance Policy 2026): cloud-based AI pentesting tools are legally unusable there, and AutoRedBlue's specific bet is a pipeline engineered to stay reliable on modest, single-GPU edge hardware rather than assuming a large cloud model. Scope is deliberately bounded to detect, triage, report, and verify-the-fix, never autonomous exploitation, and every test run targets a local, intentionally-vulnerable stand-in (DVWA, OWASP Juice Shop, Metasploitable), never a live production site.

## Architecture

Seven modules, wired together as a LangGraph state graph:

0. **Scope allow-list check**: plain code, no LLM; refuses to proceed unless the target exactly matches an entry in `config/allowlist.yaml`.
1. **Recon Agent**: wraps Nmap + subfinder; turns raw tool output into structured findings.
2. **Human approval gate**: a real LangGraph interrupt; nothing scans until a human signs off.
3. **Scan Agent**: orchestrates OWASP ZAP, Nikto, and sqlmap (via Playwright for auth/JS-rendered content) across an unauthenticated pass and an authenticated pass.
4. **Triage Agent**: dedupes and CVSS-scores findings, and requires a saved, replayable request per finding it keeps.
5. **Report Agent**: drafts a plain-language, RAG-grounded (CVE/OWASP via ChromaDB) report with a suggested fix per finding.
6. **Verification Agent**: after a human patches something, replays the saved request from step 4 and records whether it's actually fixed.

A dashboard (FastAPI backend, PyWebView desktop shell) provides the UI for all of the above: target/scope entry, live pipeline status, the approval control, and the findings/report viewer.

The one architectural decision worth knowing up front: the LLM never free-plans the engagement or emits strict JSON while reasoning. Code (the LangGraph state machine) owns sequencing via a fixed audit methodology, and the model reasons in loose plain text that a separate parsing step turns into JSON: this is the "constraint tax" mitigation that keeps a 7B-14B local model usable for multi-step work. See `docs/ARCHITECTURE.md` for the full design and `docs/DECISIONS.md` for why.

## Setup

1. Install Python deps: `pip install -e .` (see `pyproject.toml`).
2. Install [Ollama](https://ollama.com) and pull a model sized to your machine: see `config/settings.example.yaml`'s `vram_tier` and `docs/ARCHITECTURE.md`'s "Model choice". `scripts/setup_ollama.sh` will automate this once implemented.
3. Copy the example config files and fill them in:
   - `config/allowlist.example.yaml` → `config/allowlist.yaml`
   - `config/settings.example.yaml` → `config/settings.yaml`
   - `.env.example` → `.env`
4. Bring up the local targets: `docker compose up -d` (DVWA, OWASP Juice Shop, Metasploitable, see `docker-compose.yml`). `scripts/run_targets.sh` will wrap this once implemented.

## Running it

Not yet, the pipeline isn't implemented. Once the thin end-to-end slice described in `docs/PROGRESS.md` lands, this section will cover invoking the graph against a target and opening the dashboard.

## Two-machine dev/eval split

- **Personal PC** (Ryzen 5 5600, 16GB RAM, GTX 1660 Super / 6GB VRAM): daily development with a 3B-7B model. For iterating on graph logic, prompts, and parsing; not where evaluation numbers come from.
- **Lab PC** (i7-12700K, 32GB RAM, RTX A4000 / 16GB VRAM): the project's real target hardware profile, still in the 7B-14B tier but with headroom and tensor-core speed. This is where the local-vs-cloud evaluation and the numbers in the FYP report come from.

Both machines stay on a single Ollama-served open-weight model; 30B+ models aren't reachable on either, see `docs/ARCHITECTURE.md` for why.

## Team

Adeel Asghar, Asad Mashood, supervised by Dr Saeed Ur Rehman.

## Current status

Scaffolding only: this skeleton exists, but no agent, tool wrapper, or graph logic is implemented yet. See `docs/PROGRESS.md` for what's done, the next concrete task (a thin, hand-built end-to-end slice before any agent code generation), and open risks.
