# PROGRESS.md — AutoRedBlue

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
- [x] **All research claims independently verified (2026-08-25).** Almost all real; 4 corrections (Excalibur is actually PentestGPT V2; Red-MIRROR & PoC-Adapt are exploitation-side; Shannon is cloud/Claude-API-based, not local); 1 dropped (NRT-Bench — actually about nuclear-plant operator agents, irrelevant). No decisions changed. See RESEARCH.md verification log.

## Next concrete task
**No OS install needed to start.** "Platform: Linux" on the proposal is the deployment-target story, not a development blocker. Ollama, Docker, Nmap, OWASP ZAP, sqlmap, Playwright, and the whole Python stack (LangGraph/FastAPI/ChromaDB/PyWebView) all run natively on Windows. Only Nikto is genuinely annoying on native Windows, use WSL2 for it when you get there (`wsl --install`, no dual-boot needed), not before. Lab PC's actual OS still unconfirmed, check before it matters for the real evaluation run.

**Stand up the local environment and prove one thin end-to-end slice before building all five agents.** Specifically, in order:
1. On the **personal PC**: install Ollama; pull a small model (3B–7B) sized to the 1660 Super's 6GB VRAM; confirm it runs and does a basic tool call. This is for code/logic iteration, not evaluation.
2. Get DVWA running locally (Docker) as the first target — do this on whichever machine is more convenient; DVWA itself is not GPU-bound.
3. Run **Nmap and OWASP ZAP by hand** against DVWA — no agent code yet — to (a) build the security-tool literacy the team currently lacks and (b) capture real sample output to develop triage logic against later.
4. Wire the smallest possible LangGraph slice — Recon (Nmap) → one scan type → a basic report — **including the retry-on-parse-failure loop and the human-approval interrupt from day one**, not bolted on later. Validate this on the personal PC with the small model first.
5. Once the slice works end-to-end, re-run it on the **lab PC** with the actual target-tier model (7B–14B) to confirm behaviour holds at the real model size before building the remaining agents.

## Open risks / watch-items
- **#1 risk, unchanged:** small-model tool-calling reliability. The plain-text-reason-then-parse decision (with its retry loop) is the mitigation; validate it in the thin slice before committing to it everywhere.
- **Graph/orchestration engineering is real, distinct scope**, not something LangGraph provides for free: retry loops, conditional routing, the approval-gate interrupt, and the Verification Agent's cross-session resume all need to be explicitly built. See ARCHITECTURE.md's new "Graph & orchestration engineering" section.
- **Dev machine (1660 Super, 6GB) is below the lab machine (A4000, 16GB VRAM)** — expect slower inference and a smaller model during daily development; don't judge reliability from the dev machine alone, validate on the lab PC before drawing conclusions.
- **Learning curve:** neither team member has security-tooling experience. Budget FYP-I time for TryHackMe / PortSwigger Web Security Academy alongside the build. (Bounded — OWASP Top 10 literacy, not becoming a researcher.)
- **Parsing overhead:** Nmap (XML), ZAP (JSON), Nikto, sqlmap all output differently. Budget explicit time for normalisation before agent logic sits on top.
- **Citation hygiene (resolved but stay careful):** research claims are now verified, but when writing the report cite the *corrected* names/facts from RESEARCH.md (PentestGPT V2 not "Excalibur"; do not cite NRT-Bench; Shannon is cloud-based). Re-verify anything new before it goes in.

## Not started
- All five agents (design done, no code).
- ChromaDB / RAG knowledge base.
- Evaluation harness (precision/recall vs DVWA & Juice Shop ground truth; local-vs-cloud model comparison).
- Deployment packaging.
