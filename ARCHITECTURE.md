# ARCHITECTURE.md — AutoRedBlue

> The finalized technical design. When a design decision changes, update this file and log the change in DECISIONS.md.

## Guiding principle (post-research)
A 7B–14B model served on a single 16GB GPU is the hard constraint everything bends around. The 2026 literature is consistent on *why* small local models fail at agentic work: (a) forcing strict JSON output in the same call the model reasons in suppresses its reasoning ("constraint tax"), and (b) making the model hold a long-horizon plan in its own context leads to dead-end loops and context exhaustion. Our architecture is built to avoid both — **not** by adding heavy new subsystems, but by keeping the model's job small: reason in plain text, let code own the sequencing and the JSON.

## Competitive positioning (verified)
The "runs locally" angle alone is not the novelty — sovereign/air-gapped AI security is a real, funded, commercial category (Aptori; the France-2030-funded ADACIS Pentest.LLM at EUR 3M; Dynamiq; Rexon Cyber). Our defensible niche is narrower and holds up: a *reliable small-model pipeline for modest edge hardware*, for the localized-compliance gap that big sovereign-cloud platforms don't serve. The sharpest single contrast point: **Shannon (Keygraph) — the strongest open-source AI pentester in this space (~40K GitHub stars, 96.15% on XBOW) — runs on the Claude cloud API at ~$40–60 per scan, so it cannot legally be used under a data-residency mandate at all.** That is exactly the gap AutoRedBlue targets. (Shannon is also a full proof-by-exploitation tool — it does the exploitation half we deliberately exclude.)

## Pipeline overview

```
[Scope Allow-list Check]  →  Recon Agent  →  [Human Approval Gate]  →  Scan Agent
                                                                          ↓
                    Report Agent  ←  Triage Agent  ←──────────────────────┘
                          ↓
                 [Human patches]  →  Verification Agent  →  updated Report
```

Backed throughout by: **one Ollama-served open-weight LLM** + a **ChromaDB** vector store (CVE/OWASP reference material for RAG). LangGraph owns the state graph and the sequencing.

## Model choice
- Primary: an open-weight model in the **7B–14B** range with strong native tool-calling. The research points to the Qwen family (e.g. a Qwen2.5-Coder-14B-class model) as the current standard for reliable local tool use at this size; confirm the specific best available build at implementation time rather than hard-committing now.
- Served via **Ollama** (not vLLM — vLLM is for multi-GPU, multi-user serving, which is not our setup).
- A ~14B dense model at 4-bit (~Q4_K_M) fits comfortably in 16GB with room for context. Try a 7B–8B variant too; a faster small model can beat a slow larger one during dev iteration.

## Hardware: two machines, two roles (do not conflate them)
- **Personal dev machine — Ryzen 5 5600, 16GB RAM, GTX 1660 Super (6GB VRAM, no tensor cores).** Below the A4000, not equivalent. 6GB fits a 7B model at Q4 with almost no context headroom; a 3B model is more comfortable for fast iteration. Use this machine for writing and debugging graph logic, prompts, parsing, and tool wiring — everything that doesn't depend on model quality. Not where evaluation numbers come from.
- **Lab machine — i7-12700K, 32GB RAM, RTX A4000 (16GB VRAM).** This is the project's actual target hardware profile and has been since the proposal. Still caps at 7B–14B (same tier as the dev machine, just with real headroom and tensor-core speed, not a jump to "big" models). This is where the local-vs-cloud comparison in the Evaluation Plan is run and where the numbers cited in the report/defense come from.
- **30B+ ("big") open-weight models are not reachable on either machine.** That tier is future-work only (NTC GPUaaS, Siber Koza compute access) — see Future Extensions. Do not plan any FYP-I/II deliverable around a bigger model becoming available.

## The state object (LangGraph)
The graph state is the single source of truth, **not** the model's chat history. It carries at minimum:
- `target` + `scope_allowlist` (the approved in-bounds assets)
- `recon_findings` (open ports, services, discovered assets)
- `scan_findings_raw` (unfiltered scanner output)
- `triaged_findings` (deduped, scored, each with a saved reproducible request — see below)
- `approval_state` (has the human gate been passed?)
- `verification_results` (per-finding: still-vulnerable / fixed)

**Design stance (ADOPTED from Finding 4, lightweight form):** sequencing is decided by the Python graph following a fixed audit methodology, and the LLM only ever (a) reads one tool's output and turns it into a structured state update, or (b) picks the next action from an *explicit list the code gives it*. The model never free-plans the whole engagement in its head. This is the cheap version of CHECKMATE's "externalise the plan" principle — we get the stability benefit from LangGraph + a fixed methodology sequence, without building a classical planner.

## Agent-by-agent

### 0. Scope Allow-list Check (pre-recon gate)
Plain code, no LLM. Confirms `target` exactly matches an entry on the pre-configured allow-list; refuses to proceed otherwise. Demo: point it at an out-of-scope host and show it stop.

### 1. Recon Agent
Wraps **Nmap** (port/service discovery) and **subfinder** (subdomain enumeration). Runs as subprocesses; output parsed into `recon_findings`. The LLM's only role here is turning raw tool output into clean structured state (the "perceptor" role) — it does not decide attack strategy.

### 2. Human Approval Gate (pre-scan gate)
Explicit human sign-off required before any active scanning begins — this is the first point real traffic hits the target. Implemented as a LangGraph interrupt/checkpoint. Not a weakness in the pitch; panels and real engagements expect exactly this.

### 3. Scan Agent
Orchestrates **OWASP ZAP**, **Nikto**, and **sqlmap** against in-scope assets. Uses **Playwright** to (a) drive the login form for authenticated scanning and (b) reach JavaScript-rendered content. Runs in **two passes**:
- *Unauthenticated pass* — everything reachable with no account (outsider's view).
- *Authenticated pass* — logs in with a provided low-privilege test account, re-scans what's now reachable (broken-access-control class of bugs).

Output → `scan_findings_raw`.

**TOOL-CALLING PATTERN (ADOPTED from Finding 2 — the single most important reliability decision):**
Do **not** use Ollama's strict JSON/grammar-constrained mode inside the core reasoning loop. Forcing the model to satisfy a JSON schema *while* reasoning about, say, an SQL-injection attempt measurably degrades the reasoning (the "constraint tax" / tool-suppression effect documented in arXiv:2606.25605). Instead:
1. Prompt the model to output its reasoning and tool choice in **loose, guided XML-ish tags** (e.g. `<action>`, `<tool>`, `<args>`) with no grammar constraint.
2. **Parse** that text into the exact JSON the tool needs with a few lines of ordinary Python (regex / a small parser), in a separate step.

This is the *principle* behind the "toolshim" pattern, implemented at FYP scale. We explicitly do **NOT** build a separate fine-tuned toolshim model or adopt a custom decoding engine (XGrammar-2) — those don't fit 16GB alongside the main model and are unnecessary at our scale. Plain-text-reason-then-parse gets the benefit for free.

### 4. Triage Agent
Deduplicates `scan_findings_raw`, filters likely false positives, assigns a **CVSS**-based severity. This is the first genuinely AI-reasoning-heavy stage and a core contribution.

**REPRODUCIBLE-REQUEST REQUIREMENT (ADOPTED from Finding 3, reduced form):** for every finding it keeps, the Triage Agent must also emit a **saved, replayable request** that demonstrates the issue — a specific HTTP request or a short Playwright snippet. A finding that can't be reduced to a concrete saved request is downgraded. This is a false-positive filter, and it's what makes step 6 possible. **Important boundary:** this "PoC" is a *saved benign request that shows the condition*, NOT an autonomous exploit generator — keeping it benign is what keeps us on the detect/report side of scope.

### 5. Report Agent
For each triaged finding, retrieves relevant CVE/OWASP reference material from ChromaDB (RAG) and drafts a **plain-language** report with a specific suggested fix per item — not a raw tool log. RAG grounding here is also our mitigation against the "confident but wrong" report problem (models producing fluent text with high surface overlap but shaky underlying reasoning).

### 6. Verification Agent (the "Blue" half, ADOPTED from Finding 3)
Runs *after* the human has applied a fix. Its only job: **replay the saved request from step 4 against the patched target and check the response** (e.g. a login-bypass request that returned HTTP 200 before should now return 401/403). Appends a "remediation verified / still vulnerable" result to the report. This is a natural extension of the "verify-the-fix re-scan" already planned as the Blue-team story — it reuses the saved request, adds no new external tooling, and turns a one-shot PDF into a closed detect→fix→verify loop. Boundary: it re-runs the *same benign saved request*, it does not attempt new exploitation.

### 7. Dashboard (UI module — ADDED 2026-09-06)
A locally-served web dashboard, **not a public website**: a backend (FastAPI is a natural fit) serves both the API and a browser-based frontend, running on the same machine as the agent pipeline. The client opens a browser to `localhost` or the machine's own network address — nothing about it is internet-facing, consistent with the on-premises pitch. Screens: target/scope entry, live pipeline status (which agent is currently running), the human-approval interface (the literal approve/deny control for the gate in section 2), and the findings/report viewer.

**Desktop packaging: PyWebView, not Electron/Tauri.** To satisfy "Desktop Application" as an actual installable artifact rather than just a browser bookmark, the FastAPI-served frontend is wrapped with PyWebView, a lightweight Python library that opens a native OS window over the same local web app, using the OS's built-in webview (Edge WebView2 on Windows). Chosen over Electron (bundles a full Chromium instance, much heavier, needs a separate Node.js toolchain) and Tauri (lighter than Electron but needs a Rust toolchain the stack otherwise never touches). PyWebView needs zero changes to how the dashboard itself is built, it is pure Python, a few lines, wrapping work already planned.

**Project Streams classification: Desktop Application, not Web-based.** The university's own evaluation criteria requires "Web-based FYPs" to be online on a free/paid hosting service by evaluation time — AutoRedBlue's backend (Ollama + Nmap/ZAP/sqlmap) cannot run on a typical free web host. "Desktop Application" requires the project to be installable/executable, which is simply what the architecture already is. Use Desktop Application on the FYP proposal form.

## Team ownership (added 2026-09-06)
- **Adeel:** Scan Agent (incl. the tool-calling pattern), Triage Agent, Report Agent, Verification Agent, and all graph/orchestration engineering (retry loops, the approval interrupt, checkpointing).
- **Asad:** Recon Agent, the full Dashboard (module 7), and documentation (SRDS, use case/sequence/class diagrams, the FYP report).

## Graph & orchestration engineering
This is real, distinct engineering work underlying every agent above, not a detail LangGraph handles for free. A "graph" here means the pipeline is allowed to **cycle**, not just flow forward. Four patterns must be built:

1. **Retry loop on parse failure** (required by the plain-text-reason-then-parse decision above): LLM reasoning node → parser node → conditional edge: success → continue; failure → loop back to the LLM node with the error appended to context → retry, capped at a fixed N → on repeated failure, fail that step gracefully rather than crashing the run. Without this loop, one malformed model output kills the pipeline.
2. **Conditional routing on state**: e.g. zero recon findings → skip straight to a "nothing to report" terminal state rather than invoking Scan; zero findings survive Triage → skip the Report Agent's RAG step.
3. **Human Approval Gate = a real interrupt**, not just a pause. Needs a LangGraph checkpointer so state is actually persisted while execution waits for external input, and can resume correctly afterward.
4. **Verification Agent = cross-session resume**, a harder version of #3. It runs after a human patches something, potentially days later, in a different process. State must be persisted to disk (a SQLite checkpointer, not the in-memory one used for #3) so the graph can be reloaded and continued.

**Sequencing note:** build #1 and #3 as part of the thin end-to-end slice (Recon → one scan type → basic report) planned as the next task in PROGRESS.md. Getting retry and interrupt patterns right with two agents is far easier than retrofitting them across all five later.

## What we deliberately did NOT adopt (and why)
- No cryptographic WASL chain-of-custody compliance matrix (needs the non-public classified WASL spec; whole new subsystem).
- No separately fine-tuned toolshim model / custom decoding engine (doesn't fit VRAM; unnecessary at our scale).
- No real classical planner (PDDL) / Task Difficulty Assessment engine (a second FYP on its own).

Each of these is real, relevant, and out of scope on purpose — see Future Extensions below for how to frame them positively in the report.

---

## Future Extensions (real, relevant, out of FYP scope — strong "future work" section for the report/defense)
These are all ACKNOWLEDGE-tier: cite in Related Work / Future Work, do not implement.

1. **Formal WASL data-sovereignty compliance layer.** Extend the scope check into an automated data-classification + residency-tagging system aligned to the WASL framework, with a cryptographically auditable chain of custody proving no data crossed an unauthorised boundary. *(Finding 1 — blocked mainly by WASL spec access; a genuinely fundable productisation step.)*
2. **Dedicated toolshim model + optimised constrained decoding.** Replace the plain-text-parse step with a small fine-tuned model translating reasoning→JSON, plus a modern decoding engine (e.g. XGrammar-2), on hardware with more VRAM. *(Finding 2.)*
3. **Reinforcement-learning-driven PoC synthesis / verification.** More autonomous, adaptive proof-of-concept generation and verification via multi-agent RL. *(Finding 3, autonomous end.)*
4. **Deterministic classical planner (PEP / CHECKMATE) + Task Difficulty Assessment.** Externalise long-horizon attack-path planning to a real classical planner with a formal DAG of the attack surface and TDA-based pruning, letting a small edge model rival larger cloud models on multi-step engagements. *(Finding 4 — the biggest and most promising future extension. Cite CHECKMATE, arXiv:2512.11143, ~20% higher success / ~50% cheaper, already used commercially by the tool "numasec"; and PentestGPT V2, arXiv:2602.17622 — this paper was titled "Excalibur" in the original research doc but is published as PentestGPT V2 — for the Task Difficulty Assessment mechanism.)*
