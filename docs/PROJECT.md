# PROJECT.md: AutoRedBlue

> One-page overview. Read this first in any new session. If anything below is stale, fix it here before starting work.

## What it is
AutoRedBlue is a multi-agent AI system that automates web application security audits **entirely on the client's own infrastructure**. It chains a set of specialised agents (reconnaissance, scanning, triage, reporting, and remediation verification, added later), coordinated with LangGraph and backed by a single open-weight LLM served locally via Ollama. No scan data, finding, or reasoning ever leaves the client's servers.

## The problem
Pakistani government and public-sector web portals have a documented, recurring pattern of breaches (SQL injection, mass defacement). But under the **National Data Governance Policy 2026**, finalised by the Ministry of IT & Telecommunication with the Pakistan Digital Authority (PDA) and built around the real **WASL framework** for classification-based secure data exchange, sensitive government data must stay hosted and processed inside Pakistan. This makes it legally fraught to send audit data (scan output, application context, vulnerability evidence) to any cloud-hosted AI service. Meanwhile manual penetration testing is slow, costly, and depends on scarce specialists.

## The gap we fill
AI-driven pentesting is now crowded (PentestGPT, PentestAgent, PenHeal, VulnBot, XBOW, PentAGI, Strix, and 39+ catalogued tools), and sovereign/air-gapped AppSec is a real commercial category (e.g. Aptori). So "an AI that finds vulnerabilities" is **not** the novelty, and "runs locally" alone is no longer novel either. Our defensible angle is narrower: a **fully local pipeline engineered specifically to stay reliable on modest, edge-level public-sector hardware (a single 16GB GPU)**, filling the localized-compliance niche that large sovereign-cloud platforms don't target, and tuned to the Pakistani public-sector context.

## The differentiator (one sentence)
A local-only, small-model (7B–14B) security-audit pipeline whose architecture is explicitly designed to work *around* the known failure modes of small local models, so a 14B edge model can do useful multi-step auditing without a cloud API.

## Scope guardrails (do not drift past these)
- **Detect, triage, report, and verify-the-fix.** NOT autonomous exploitation.
- Testing only against local, intentionally-vulnerable targets: **DVWA, OWASP Juice Shop, Metasploitable.** Never a live .gov.pk site (illegal without signed authorisation, which this project does not have).
- Two students, one academic year (FYP-I + FYP-II).
- Two machines, two roles: personal PC (Ryzen 5 5600, 16GB RAM, GTX 1660 Super/6GB VRAM) for development; lab PC (i7-12700K, 32GB RAM, RTX A4000/16GB VRAM) for real evaluation and the numbers that go in the report. Both stay in the 7B–14B model tier (see ARCHITECTURE.md). A single Ollama-served open-weight model.
- A scope allow-list check runs before recon; a human-approval gate runs before any active scan.

## Team & context
- 2 undergraduate BS Artificial Intelligence students, COMSATS University Islamabad, Wah Campus.
- Supervisor: Dr Saeed Ur Rehman.
- **Role split:** Adeel owns Scan, Triage, Report, and Verification Agents plus all graph/orchestration engineering. Asad owns Recon Agent, the Dashboard (UI module), and documentation (SRDS, diagrams, FYP report). See ARCHITECTURE.md for module detail.
- **Role split, the rest of the repo skeleton** (unstated until a coding agent's init flagged the gap): `agents/scope_check.py`, `llm/*`, and `rag/*` are Adeel's, closest fit to the graph/reasoning work he already owns. `docker-compose.yml` and the target-bringup scripts are Asad's, same as the Recon/Dashboard track. `eval/*` is Adeel's, it exists to validate the local-vs-cloud claim his agents make. `tests/*` has no single owner: whoever builds a piece writes its tests.
- Strong AI/ML engineering background; **no prior cybersecurity-tooling experience**: security tools are wrapped, not reimplemented, and the interesting work is the agentic/AI layer around them.

## Current status (summary: see PROGRESS.md for detail)
Proposal approved by supervisor. Architecture finalised and refined across three sessions (initial design, research verification, graph-engineering + hardware clarification). FYP-I build not yet started.

## Files in this project
Six files, each with one job. Read PROJECT.md first in any new session; read the others only as needed.
- **PROJECT.md** (this file): overview, scope guardrails, team. Rarely changes.
- **ARCHITECTURE.md**: the current technical design. Update when a design decision changes.
- **DECISIONS.md**: append-only dated log of what was decided and why. Never rewritten, only added to.
- **PROGRESS.md**: current status, next concrete task, open risks. Updates almost every session.
- **RESEARCH.md**: external research findings and their verification status. Append new findings as dated entries.
- **ROADMAP.md**: the full, dependency-ordered build plan, FYP-I and FYP-II. Work it top to bottom; check a box only once its Test line passes.
