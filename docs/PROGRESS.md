# PROGRESS.md: AutoRedBlue

> Current status. Update at the end of every work session. Keep it short: what's done, what's next, what's blocking.

## Phase
FYP-I, pre-build. Proposal approved by supervisor (Dr Saeed Ur Rehman). Architecture finalised and research-verified; graph-engineering scope and the two-machine hardware plan are now explicit. No code written yet.

## Done
- [x] Idea selected and scoped (AutoRedBlue: local multi-agent web-app security audit).
- [x] Proposal written, approved by supervisor.
- [x] Supervisor feedback incorporated: two-pass (unauthenticated + authenticated) scanning defined; target profile defined as Pakistani public-sector portals, with DVWA/Juice Shop/Metasploitable as legal stand-ins.
- [x] Competitive + academic research round completed (findings 1–4).
- [x] Architecture finalised: 4 agents → **5 agents** (added Verification Agent); tool-calling pattern set (plain-text-reason-then-parse); planning stance set (code owns sequencing).
- [x] Context files created (PROJECT / ARCHITECTURE / DECISIONS / PROGRESS / RESEARCH).
- [x] **All research claims independently verified (2026-08-25).** Almost all real; 4 corrections (Excalibur is actually PentestGPT V2; Red-MIRROR & PoC-Adapt are exploitation-side; Shannon is cloud/Claude-API-based, not local); 1 dropped (NRT-Bench, actually about nuclear-plant operator agents, irrelevant). No decisions changed. See RESEARCH.md verification log.

## Next concrete task
**No OS install needed to start.** "Platform: Linux" on the proposal is the deployment-target story, not a development blocker. Ollama, Docker, Nmap, OWASP ZAP, sqlmap, Playwright, and the whole Python stack (LangGraph/FastAPI/ChromaDB/PyWebView) all run natively on Windows. Only Nikto is genuinely annoying on native Windows, use WSL2 for it when you get there (`wsl --install`, no dual-boot needed), not before. Lab PC's actual OS still unconfirmed, check before it matters for the real evaluation run.

**The full, granular, dependency-ordered build plan now lives in `ROADMAP.md`.** Check the first unchecked box there and start. This section used to list the first few steps directly; that became a second copy of the same plan the moment `ROADMAP.md` existed, so it's gone from here on purpose, not by accident.

**2026-09-25 environment setup session (dev PC):**
- `uv venv` created at `.venv` (Python 3.11.15, matches the `>=3.11` pin), `uv pip install -e ".[dev]"` done, `uv.lock` generated. All ROADMAP-0 Python deps (LangGraph, FastAPI, ChromaDB, Ollama client, Playwright, PyWebView, PyYAML, pytest) import cleanly.
- `.env` and `config/allowlist.yaml` / `config/settings.yaml` created from their `.example` templates (still gitignored, as intended).
- Ollama service started and confirmed working: `qwen2.5:7b` and `qwen2.5-coder:7b` (the model `.env.example`/`ARCHITECTURE.md` actually specify) both pulled and tested, including a reason-then-tool-call-style prompt. `nvidia-smi` confirms the GTX 1660 Super loads the 7B model at ~4.7GB/6GB VRAM, in line with the ROADMAP's sizing assumption.
- Known non-blocking gap: Playwright's own `playwright install chromium` browser-binary download times out against `cdn.playwright.dev` from this network. Not needed until step 9.3 (FYP-II); retry later or via a different network.

**2026-09-25 follow-up (same day): Docker unblocked.** The Hyper-V/Virtual Machine Platform fix from earlier in the session (elevated `dism.exe /online /enable-feature`, reboot) took: `wsl -d docker-desktop` now starts cleanly instead of failing with `HCS_E_HYPERV_NOT_INSTALLED`. Started Docker Desktop, waited for the engine, ran `docker run hello-world`: it pulled and ran successfully. ROADMAP 0.1 and 0.2 both fully pass now (Ollama half already confirmed above, Docker half confirmed just now). Boxes checked, committed, pushed.

**2026-09-25, same session: ROADMAP 0.3 done.** `docker compose up -d dvwa` brings up `vulnerables/web-dvwa`, confirmed listening on `localhost:8080` with the real DVWA login page (`<title>Login :: Damn Vulnerable Web Application (DVWA) v1.10 *Development*</title>`). Box checked, committed, pushed. Next up: 0.4 (manually run Nmap and ZAP against DVWA by hand, save sample output, tool-literacy step) then module 1 (allow-list check).

**2026-09-26, ROADMAP 0.4 done.** Installed Nmap 7.80 via winget (clean, fast). OWASP ZAP's native Windows installer stalled at a fixed byte count downloading from GitHub releases, twice in a row (same class of CDN-download flakiness already seen with Playwright's browser binaries on this network); switched to the official `zaproxy/zap-stable` Docker image instead, which pulled fine (Docker Hub layers unaffected). Ran `nmap -sV -p 8080 --script=http-title,http-headers localhost`, confirmed DVWA (Apache 2.4.25, DVWA v1.10 login page), saved to `tests/fixtures/nmap_dvwa.{txt,xml}`. Ran a ZAP baseline (passive) scan via `docker run zaproxy/zap-stable zap-baseline.py -t http://host.docker.internal:8080`, 16 real WARN-level findings (missing security headers, cookie flags, debug error disclosure, etc.), saved HTML/JSON reports plus the automation-framework plan to `tests/fixtures/zap_dvwa_report.{html,json}` and `zap.yaml`. Box checked, committed, pushed. Note for step 6.1 (`zap_tool.py`): the Docker image plus `zap-baseline.py --auto` pattern used here worked cleanly and is a reasonable basis for the real tool wrapper, no need to fight the native Windows installer again. Next up: module 1 (allow-list check, `config/allowlist.yaml`).

## Open risks / watch-items
- **#1 risk, unchanged:** small-model tool-calling reliability. The plain-text-reason-then-parse decision (with its retry loop) is the mitigation; validate it in the thin slice before committing to it everywhere.
- **Graph/orchestration engineering is real, distinct scope**, not something LangGraph provides for free: retry loops, conditional routing, the approval-gate interrupt, and the Verification Agent's cross-session resume all need to be explicitly built. See ARCHITECTURE.md's new "Graph & orchestration engineering" section.
- **Dev machine (1660 Super, 6GB) is below the lab machine (A4000, 16GB VRAM)**: expect slower inference and a smaller model during daily development; don't judge reliability from the dev machine alone, validate on the lab PC before drawing conclusions.
- **Learning curve:** neither team member has security-tooling experience. Budget FYP-I time for TryHackMe / PortSwigger Web Security Academy alongside the build (bounded: OWASP Top 10 literacy, not becoming a researcher).
- **Parsing overhead:** Nmap (XML), ZAP (JSON), Nikto, sqlmap all output differently. Budget explicit time for normalisation before agent logic sits on top.
- **Citation hygiene (resolved but stay careful):** research claims are now verified, but when writing the report cite the *corrected* names/facts from RESEARCH.md (PentestGPT V2 not "Excalibur"; do not cite NRT-Bench; Shannon is cloud-based). Re-verify anything new before it goes in.

## Not started
- All five agents (design done, no code).
- ChromaDB / RAG knowledge base.
- Evaluation harness (precision/recall vs DVWA & Juice Shop ground truth; local-vs-cloud model comparison).
- Deployment packaging.
