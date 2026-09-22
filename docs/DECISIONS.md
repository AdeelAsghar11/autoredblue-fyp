# DECISIONS.md: AutoRedBlue

> Append-only. One dated line per decision, newest at the bottom. Never rewrite history: if a decision is reversed, add a new line reversing it. This is how future-you avoids re-litigating settled choices.

## 2026-08-24: Architecture finalisation session (evaluating research findings 1–4)

- **ADOPT**: Plain-text-reason-then-parse tool calling (Finding 2 core): the LLM outputs reasoning + tool choice in loose XML tags, and plain Python parses it into JSON in a separate step. Reason: strict JSON-in-the-reasoning-call suppresses small-model reasoning (constraint tax, arXiv:2606.25605); parsing separately is *less* work than wiring grammar-constrained mode and directly de-risks our #1 risk.
- **REJECT (build) / mention only**: Separate fine-tuned toolshim model + XGrammar-2 decoding engine (Finding 2 heavy): doesn't fit 16GB alongside the main model, and a custom decoding engine is scope we don't need; a few lines of Python get the same benefit.
- **ADOPT (reduced)**: Verification Agent as a 5th agent that replays a saved benign request against the patched target and checks the response (Finding 3): natural extension of the already-planned "verify-the-fix re-scan"; reuses the saved request from triage, adds no new external tooling. Boundary held: the saved "PoC" is a benign request that shows the condition, not an autonomous exploit generator.
- **ADOPT**: Triage must emit a saved, replayable request per kept finding; findings that can't be reduced to one are downgraded (Finding 3): doubles as a false-positive filter and is the precondition for the Verification Agent.
- **ADOPT (design stance, lightweight)**: Code owns sequencing via a fixed audit methodology in LangGraph; the LLM only perceives (tool output → state) or picks the next action from an explicit list the code provides (Finding 4 principle): we're already most of the way there with LangGraph; this is a clarification, not new work. Gets the "externalise the plan" stability benefit without building a planner.
- **ACKNOWLEDGE**: Market validation that sovereign/air-gapped AI pentesting is real & commercial, e.g. Aptori (Finding 1): sharpens the differentiation argument; goes in Related Work; nothing to build.
- **ACKNOWLEDGE (Future Extensions)**: Formal WASL cryptographic data-sovereignty compliance matrix (Finding 1 heavy): needs the non-public classified WASL spec and is a whole new subsystem; strong future/productisation pitch, not FYP scope.
- **ACKNOWLEDGE (Future Extensions)**: Real classical planner (PDDL) + Task Difficulty Assessment engine, CHECKMATE-style (Finding 4 heavy): a second FYP on its own; cite as the headline future extension (source reports ~20% higher success / ~50% cheaper).
- **ACKNOWLEDGE (Future Extensions)**: RL-driven autonomous PoC synthesis/verification (Finding 3 autonomous end): beyond scope and beyond the detect/report boundary we're deliberately holding.

- **Standing decision (carried from proposal)**: Model served via Ollama, not vLLM (single GPU / single user). Targets remain DVWA / Juice Shop / Metasploitable only. Scope allow-list before recon + human-approval gate before active scan are mandatory, not optional.

- **Verification caveat**: Several source claims are NOT yet independently confirmed (ADACIS/Pentest.LLM/France 2030, Dynamiq, Rexon Cyber, Shannon Open Source, CaptureTheBug, and the Red-MIRROR/PoC-Adapt/survey/NRT-Bench papers). Do not cite these as fact in the written report until verified. Confirmed real: WASL/PDA, CHECKMATE (2512.11143), Constraint Tax (2606.25605), Aptori.

## 2026-08-25: Research verification pass (resolving all unverified items)

- **All previously-unverified research claims independently checked.** Outcome: almost all confirmed real. Corrections recorded in RESEARCH.md. **No ADOPT/ACKNOWLEDGE/REJECT decision from 2026-08-24 changed**: verification only affects how items are cited, not what we build.
- **Correction**: "Excalibur" is published as **PentestGPT V2** (arXiv:2602.17622, Gelei Deng et al.). Cite as PentestGPT V2.
- **Correction**: Red-MIRROR (2603.27127) and PoC-Adapt (2604.06618) are autonomous-*exploitation* systems; cite as related work on the side we exclude, reinforcing our scope boundary.
- **Correction**: Shannon (Keygraph) is real and strong (~40K stars, 96.15% XBOW) but **runs on the Claude cloud API, not locally**. Adopt as our sharpest *contrast* case: the best open-source agent in this space is unusable under a data-residency mandate. This strengthens the differentiation section.
- **Correction**: ADACIS Pentest.LLM (France 2030, EUR 3M) confirmed real; use as evidence a *government-funded sovereign pentesting LLM* is an established category.
- **DROP**: NRT-Bench (2606.20408) is about nuclear-plant operator agents, not web security. Do not cite. (Original research doc mislabeled it.)
- **Standing note**: Dynamiq, Rexon Cyber, CaptureTheBug all confirmed real but are (respectively) a general agentic platform, a consulting service, and a human-led PTaaS, cite as market-context for the sovereign / verify-the-fix niches, not as direct product competitors.

## 2026-08-28: Graph engineering scope + two-machine hardware clarified

- **Clarification**: Graph/loop orchestration engineering was implied but never made explicit. It is real, distinct engineering work: retry loop on tool-call parse failure, conditional routing on state, the human-approval interrupt (needs a checkpointer), and the Verification Agent's cross-session resume (needs persistent, not in-memory, checkpointing). Added as its own section in ARCHITECTURE.md. Sequencing decision: build the retry loop and the approval interrupt as part of the thin end-to-end slice, not after.
- **Clarification**: Confirmed two-machine setup: personal PC (Ryzen 5 5600, 16GB RAM, GTX 1660 Super/6GB VRAM, no tensor cores) for daily development with a small (3B–7B) model; lab PC (i7-12700K, 32GB RAM, RTX A4000/16GB VRAM) for real evaluation. This was already the project's target hardware from the proposal, not a new machine.
- **Correction (important: avoid this mistake in the report)**: The lab PC does NOT unlock "big" (30B+) open-weight models. It stays in the same 7B–14B tier as the dev machine, just with more headroom and real tensor-core speed. Any 30B+ model only becomes reachable via the future-work scaling path (NTC GPUaaS, Siber Koza), never via either of the two current machines.

## 2026-09-06: UI, Project Stream classification, and team ownership decided

- **ADOPT**: UI is a locally-served web dashboard (FastAPI backend + browser frontend), not a public website. Reason: a public/hosted site would contradict the on-premises, nothing-leaves-the-client's-infrastructure pitch. Runs on `localhost`/the local network only.
- **DECIDED**: Project Streams classification on the FYP form: **Desktop Application**, not Web-based. Reason: the department's own Web-based evaluation criteria requires the site to be hosted on free/paid hosting by evaluation time, which AutoRedBlue's backend (Ollama + security tools) cannot satisfy. Desktop Application's requirement (installable/executable) matches the architecture as already designed.
- **DECIDED**: Team ownership: Adeel owns Scan, Triage, Report, and Verification Agents plus all graph/orchestration engineering. Asad owns the Recon Agent, the full Dashboard module, and documentation (SRDS, diagrams, FYP report).
- **Open item, unresolved**: Whether similar FYPs exist in the department (form question (d)/(d-1)) requires checking COMSATS's internal RMS student console directly; an attempted automated check was blocked by the site's own robots restriction. Adeel to check manually and report back.

## 2026-09-06 (cont.): RMS check resolved

- **RESOLVED**: Adeel checked RMS directly. One directly similar FYP found: "Web Application Security Scanner" (Yasir Ali Khan Wazir & Gul Faraz Khan, supervised by Mr. Taimur Sajjad), which itself lists "Website Pen Tester" as its own prior-art reference. Full comparison: their system is entirely rule-based (regex for XSS, payload fuzzing for SQLi), has no AI/LLM component, is a hosted multi-user web app, and its "Soft vs Deep" modes vary test aggressiveness, not authentication state. No overlap with AutoRedBlue's actual differentiators (local AI reasoning, dual-pass auth coverage, remediation verification). Closes the open item above.

## 2026-09-06 (cont.): Desktop packaging tool decided

- **DECIDED**: PyWebView wraps the FastAPI-served dashboard for desktop packaging. Reason: satisfies "Desktop Application" as an installable artifact with zero changes to the dashboard's own build (pure Python, a few lines); rejected Electron (bundles Chromium, needs Node.js) and Tauri (needs a Rust toolchain the stack doesn't otherwise use) as more than the project needs.

## 2026-09-22: Repo init review, em-dash cleanup, ownership gap closed, duplication found

- **Correction (mine)**: AGENTS.md states a no-em-dash style rule for the whole repo; ROADMAP.md violated it 47 times in its own owner tags, written in the same session the rule was added. A coding agent running the scaffold prompt caught this and correctly declined to fix content it didn't author. Went back and checked all seven files: found 180 total em dashes, most predating the rule being confirmed to me at all. All seven files are now clean.
- **RESOLVED**: ownership for the repo skeleton files with no named owner (`agents/scope_check.py`, `llm/*`, `rag/*`, `eval/*`, `docker-compose.yml`, `tests/*`) was flagged as a gap by the same coding agent. Settled using what ROADMAP.md's per-step tags already implied: scope_check/llm/rag/eval to Adeel, docker-compose and target scripts to Asad, tests owned by whoever builds the corresponding piece. Recorded in PROJECT.md.
- **Open item**: the coding agent found the same 5 original docs (PROJECT/ARCHITECTURE/DECISIONS/PROGRESS/RESEARCH) exist twice in the repo, once at root (pre-existing before the scaffold ran) and once under `docs/` (copied there per the scaffold prompt's own instructions). `docs/` is canonical, AGENTS.md and ROADMAP.md both reference paths under `docs/`. Delete the root-level loose copies to leave one source of truth.
- **Confirmed**: `docker-compose.yml`'s Metasploitable service uses the `citizenstig/metasploitable2` community image. Metasploitable has no official Docker image (it's normally VM-distributed), so this is a third-party image, but it's the long-standing, widely-used standard choice for exactly this purpose across security-education Docker setups, and the target it packages is intentionally vulnerable by design regardless. Accepted as-is.
