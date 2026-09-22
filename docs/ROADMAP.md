# ROADMAP.md: AutoRedBlue

> The full build plan, in dependency order. `PROGRESS.md` is a short snapshot of right now; this is the complete path from zero to done. If they conflict, `PROGRESS.md` wins for "what's actually true today", update this file to match, don't silently trust whichever looks more convenient.

## How to use this file
- Work top to bottom. The order is load-bearing: each step assumes every step above it is done and tested. Skipping ahead is how the project breaks itself in a way that's hard to trace back.
- A box gets checked only after the step is built **and** its Test line passes. Not before.
- After checking a box: commit with the suggested message, then push. One commit per step, not one commit per phase, so a broken step is a single revertible commit, not a tangle of five.
- If a step turns out to depend on something not yet built, or the order genuinely needs to change: stop, fix the order here first, log the change as a dated line in `DECISIONS.md`, then continue. Don't improvise silently, that's exactly the kind of drift that cost a cleanup pass on this project once already.
- Steps marked **[parallel-safe]** don't depend on the step directly above them and can be picked up out of order by whoever's free, everything else is strictly sequential.
- For *how* to build a step, see the matching section of `ARCHITECTURE.md`, linked inline. This file is sequencing and pass/fail criteria only, it doesn't restate design detail that lives elsewhere.

---

## FYP-I: prove the thin slice end to end

### 0. Environment
- [ ] **0.1 Install the base stack.** Build: Python, LangGraph, FastAPI, ChromaDB, Ollama, Docker installed on the personal PC. No OS install needed first, see `PROGRESS.md`. Test: `ollama run` responds to a basic prompt; `docker run hello-world` succeeds. Commit: `chore: base environment setup`.
- [ ] **0.2 Pull a dev-scale model.** Build: pull a 3B–7B model sized to the 1660 Super's 6GB VRAM. Test: model answers a basic tool-calling-style prompt without erroring. Commit: `chore: pull dev model`.
- [ ] **0.3 Bring up DVWA.** Build: `docker-compose up` for DVWA per the scaffold's `docker-compose.yml`. Test: DVWA's login page loads in a browser at its local port. Commit: `chore: DVWA target running`. **[parallel-safe]**
- [ ] **0.4 Manually run Nmap and ZAP against DVWA.** Build: nothing, no agent code yet. Run both tools by hand from a terminal. Test: you have real Nmap and ZAP output saved as sample files, you personally understand what each looks like. Commit: `docs: sample tool output for reference` (commit the saved output under `tests/fixtures/`). (whoever hasn't used these tools before; this is the literacy step from `PROGRESS.md`)

### 1. Scope Allow-list Check (module 0)
No LLM, no graph, pure code, zero dependencies on anything else in this list. Genuinely the safest possible first real code.
- [ ] **1.1 Define the allow-list format.** Build: finalize `config/allowlist.example.yaml`'s schema. Test: a human can read it and know exactly what's in/out of scope. Commit: `feat: allowlist schema`.
- [ ] **1.2 Implement the check.** Build: `src/autoredblue/agents/scope_check.py`, given a target string, return allowed/refused. Test: an allowed target passes; a target not on the list is refused; an empty or malformed allowlist file fails closed (refuses), not open. Commit: `feat: scope allow-list check`.

### 2. Minimal graph skeleton
Prove the graph mechanics work with trivial nodes before adding any real complexity on top.
- [ ] **2.1 Define the state object.** Build: `src/autoredblue/graph/state.py` with just the fields needed so far (`target`, `scope_allowlist`, `approval_state`). See `ARCHITECTURE.md`'s "The state object". Test: state can be constructed and serialized. Commit: `feat: initial graph state schema`.
- [ ] **2.2 Wire a 2-node graph: scope check → stub recon.** Build: the stub node just logs "recon ran", no real tool call yet. Test: run against an allowed target, both nodes fire in order; run against a disallowed target, the graph stops before the stub node ever runs. Commit: `feat: minimal graph proves scope-gate mechanics`.

### 3. Real Recon Agent (module 1): the core reliability pattern, proven early on purpose
- [ ] **3.1 Wrap Nmap as a callable tool.** Build: `src/autoredblue/tools/nmap_tool.py`, subprocess call, parse XML output. Test: run against DVWA, get back a structured list of open ports matching what you saw by hand in step 0.4. Commit: `feat: Nmap tool wrapper`.
- [ ] **3.2 Wrap subfinder similarly.** Build: `src/autoredblue/tools/subfinder_tool.py`. Test: runs without error against a target with no subdomains to find, returns an empty result cleanly rather than erroring. Commit: `feat: subfinder tool wrapper`.
- [ ] **3.3 Implement the plain-text-reason-then-parse pattern, for this one node only.** Build: LLM reasons in loose XML tags, a separate Python step parses it into the tool call. See `ARCHITECTURE.md`'s "TOOL-CALLING PATTERN". Test: given raw Nmap output, the LLM correctly turns it into a structured state update, at least 8 times out of 10 tries. Commit: `feat: recon agent LLM perceptor`.
- [ ] **3.4 Add the retry loop.** Build: parse failure → loop back to the LLM node with the error appended → retry, capped at 3 attempts. Test: deliberately feed a malformed model output in a test and confirm it retries and recovers, or fails gracefully after 3 tries rather than crashing the run. Commit: `feat: retry loop on parse failure`.
- [ ] **3.5 Full Recon Agent against DVWA.** Build: wire 3.1–3.4 together as the real Recon Agent node, replacing the stub from 2.2. Test: run against DVWA, confirm it correctly reports the ports/services you already know are there. Commit: `feat: Recon Agent complete`.

### 4. Human Approval Gate (module 2)
- [ ] **4.1 Implement the interrupt.** Build: LangGraph in-memory checkpointer, pipeline pauses after Recon, before Scan. See `ARCHITECTURE.md`'s "Graph & orchestration engineering". Test: the pipeline genuinely stops and waits, state is intact when it does. Commit: `feat: human-approval interrupt`.
- [ ] **4.2 Test both outcomes.** Build: nothing new. Test: approving resumes execution correctly; denying halts the run cleanly with no partial side effects. Commit: `test: approval gate resume/deny paths`.

### 5. RAG knowledge base **[parallel-safe with 3 and 4, no dependency on either]**
- [ ] **5.1 Stand up ChromaDB.** Build: `src/autoredblue/rag/chroma_store.py`. Test: can write and read back a test document. Commit: `feat: ChromaDB store`.
- [ ] **5.2 Ingest CVE/OWASP reference material.** Build: `src/autoredblue/rag/ingest_cve_owasp.py`. Test: a query for a known vulnerability class (e.g. "SQL injection") returns relevant retrieved chunks. Commit: `feat: CVE/OWASP corpus ingested`.

### 6. One scan type, unauthenticated only (thin slice of module 3)
Deliberately not the full Scan Agent yet, just enough to complete the FYP-I slice.
- [ ] **6.1 Wrap OWASP ZAP as a tool.** Build: `src/autoredblue/tools/zap_tool.py`, unauthenticated scan only. Test: run against DVWA, get back real findings, at least one should be a known DVWA vulnerability. Commit: `feat: ZAP tool wrapper, unauthenticated`.
- [ ] **6.2 Wire it into the graph as the Scan node.** Build: replaces nothing yet, this is the graph's first real Scan node, gated by the approval interrupt from step 4. Test: full pipeline run, scope check → recon → approval → scan, produces real ZAP findings for DVWA. Commit: `feat: thin-slice Scan Agent (ZAP only, unauth only)`.

### 7. Basic Report Agent (thin slice of module 5)
- [ ] **7.1 Minimal report generation.** Build: for each finding from step 6, retrieve relevant material from the RAG store (step 5) and draft a plain-language paragraph. No triage yet, no severity scoring, that's FYP-II. Test: a generated report entry is readable, accurate, and actually references the retrieved CVE/OWASP material, not just generic text. Commit: `feat: basic Report Agent`.

### 8. FYP-I milestone
- [ ] **8.1 Full thin slice, start to finish.** Build: nothing new, this is integration only. Test: a single command runs scope check → recon → approval gate → one-tool scan → basic report against DVWA, and produces a real, readable report file. This is the artifact for the 7th-semester evaluation. Commit: `milestone: FYP-I thin slice complete`.
- [ ] **8.2 SRDS deliverable.** Build: use case, sequence, class, and ER diagrams plus functional/non-functional requirements, covering the full system (not just the thin slice). Test: matches what's actually described in `ARCHITECTURE.md`, and satisfies the department's stated SRDS requirement. Commit: `docs: SRDS`.

---

## FYP-II: full richness

### 9. Full Scan Agent (rest of module 3)
- [ ] **9.1 Add Nikto.** Build: `src/autoredblue/tools/nikto_tool.py`. Test: against DVWA, findings are consistent with what ZAP already found (no wild contradictions), plus anything new Nikto specifically catches. Commit: `feat: Nikto tool wrapper`.
- [ ] **9.2 Add sqlmap.** Build: `src/autoredblue/tools/sqlmap_tool.py`. Test: against DVWA's known SQL injection point, sqlmap correctly identifies it. Commit: `feat: sqlmap tool wrapper`.
- [ ] **9.3 Add Playwright for authenticated scanning.** Build: `src/autoredblue/tools/playwright_tool.py`, drives the DVWA login form. Test: an authenticated session is established, and content only reachable post-login is now visible to the scan. Commit: `feat: Playwright authenticated pass`.
- [ ] **9.4 Confirm both passes run.** Build: nothing new. Test: one full scan run produces distinct findings for the unauthenticated pass and the authenticated pass, some findings genuinely only show up in one or the other. Commit: `test: dual-pass scan coverage confirmed`.

### 10. Full Triage Agent (module 4)
- [ ] **10.1 Deduplication.** Build: `src/autoredblue/agents/triage.py`, dedup logic against the now-real multi-tool findings from phase 9. Test: a deliberately duplicated finding (same issue reported by two tools) collapses to one. Commit: `feat: Triage dedup`.
- [ ] **10.2 CVSS severity scoring.** Build: same file, scoring logic. Test: a known-severe finding (e.g. SQL injection) scores higher than a known-minor one (e.g. a missing security header). Commit: `feat: CVSS scoring`.
- [ ] **10.3 Reproducible-request generation.** Build: for each kept finding, save a benign request or Playwright snippet that demonstrates it. Findings that can't be reduced to one get downgraded. Test: the saved request, replayed manually, reproduces the condition. Commit: `feat: reproducible-request generation`.

### 11. Report Agent refinement
- [ ] **11.1 Wire real Triage output in.** Build: replace the FYP-I basic version's direct scan-output input with real triaged, scored findings. Test: report entries now include severity and are ordered by it. Commit: `feat: Report Agent uses Triage output`.
- [ ] **11.2 Per-finding fix suggestions.** Build: specific, not generic, remediation text per finding. Test: a human reviewer confirms the suggested fix is actually correct for that specific finding. Commit: `feat: specific remediation suggestions`.

### 12. Verification Agent (module 6)
- [ ] **12.1 SQLite checkpointer.** Build: `src/autoredblue/graph/checkpointer.py`'s persistent variant, distinct from step 4's in-memory one, this one needs to survive a process restart. Test: kill the process mid-run, restart, confirm state is recoverable. Commit: `feat: persistent checkpointer for cross-session resume`.
- [ ] **12.2 Replay logic.** Build: `src/autoredblue/agents/verify.py`, replays a saved request (from step 10.3) against a patched target. Test both directions: manually "fix" a DVWA issue, confirm Verification reports it resolved; leave one unfixed, confirm it correctly reports still-vulnerable. Commit: `feat: Verification Agent`.

### 13. Dashboard (module 7) **[parallel-safe from the start, only needs the state schema from step 2.1, can be scaffolded well before step 9]**
- [ ] **13.1 FastAPI backend skeleton.** Build: `src/autoredblue/dashboard/api.py`, routes for each pipeline stage's data, can be built against mocked data before the real pipeline is ready. Test: routes respond with the right shape. Commit: `feat: dashboard API skeleton`.
- [ ] **13.2 Target/scope configuration screen.** Test: can set a target and see it reflected in `config/allowlist.yaml`-driven state. Commit: `feat: scope config screen`.
- [ ] **13.3 Live pipeline status view.** Test: shows which agent is currently running, updates in real time against a real pipeline run. Commit: `feat: live status view`.
- [ ] **13.4 Approval interface.** Build: wires to the interrupt from step 4. Test: clicking approve/deny in the UI actually resumes/halts a real paused run. Commit: `feat: dashboard approval control`.
- [ ] **13.5 Findings/report viewer.** Test: displays a real report from a real run, correctly. Commit: `feat: report viewer`.
- [ ] **13.6 PyWebView desktop packaging.** Build: `src/autoredblue/dashboard/desktop.py`. See `ARCHITECTURE.md`'s Dashboard section for why PyWebView over Electron/Tauri. Test: the whole thing opens as a native window, double-click launch, not "open your browser". Commit: `feat: desktop packaging via PyWebView`.

### 14. Second target + evaluation harness
- [ ] **14.1 Bring up Juice Shop.** Build: add to `docker-compose.yml`. Test: full pipeline runs against it without target-specific code changes. Commit: `feat: Juice Shop as second target`.
- [ ] **14.2 Ground-truth labels.** Build: `eval/ground_truth/` for both DVWA and Juice Shop, the known vulnerabilities each actually has. Test: a human review confirms the labels are accurate. Commit: `feat: ground-truth vulnerability labels`.
- [ ] **14.3 Precision/recall scoring.** Build: `eval/run_eval.py`. Test: produces a real number, not a placeholder, against both targets. Commit: `feat: precision/recall evaluation`.
- [ ] **14.4 Local-vs-cloud comparison.** Build: same harness, run once against the local model, once against a cloud baseline. Test: both produce comparable output the harness can actually diff. Commit: `feat: local-vs-cloud comparison`.

### 15. Lab PC validation
- [ ] **15.1 Re-run the full pipeline on the A4000.** Test: confirm behavior holds at the real target-tier model size, note any divergence from dev-machine results. Commit: `test: lab PC validation run`.

### 16. Wrap-up
- [ ] **16.1 Final FYP report.**
- [ ] **16.2 Deployment packaging finalized.**
- [ ] **16.3 Defense materials.**
