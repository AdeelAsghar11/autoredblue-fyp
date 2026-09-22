# RESEARCH.md — AutoRedBlue

> Research findings and their disposition. Append new findings as dated entries. **All items in this file have now been independently verified** (see Verification Log below). Corrections found during verification are noted inline — cite the corrected version, not the original research doc's wording.

## Verification key
- CONFIRMED — independently verified as real and described accurately.
- CONFIRMED W/ CORRECTION — real, but the original research doc described it wrongly; use the corrected note here.
- DROP — real artifact but not relevant to AutoRedBlue; do not cite.

---

## Verification Log (2026-08-25) — every item checked

### Confirmed-real anchors (safe to cite as-is)
- [CONFIRMED] **WASL framework + Pakistan Digital Authority (PDA) + National Data Governance Policy 2026** — Pakistani press (ProPakistani, TechJuice), Aug 2026. Ownership stays with each government entity; WASL enables classification-based secure exchange.
- [CONFIRMED] **CHECKMATE** — "Automated Penetration Testing with LLM Agents and Classical Planning", arXiv:2512.11143. Real; ~20% higher success / ~50% cheaper confirmed. (Also: a real commercial tool, numasec, is already built on CHECKMATE's deterministic-planner idea — evidence the approach works in practice.)
- [CONFIRMED] **Constraint Tax (tool suppression)** — arXiv:2606.25605 (Li, Zhang, Lv). Real. A related small-model constraint-tax paper (arXiv:2605.26128) independently reports the same effect — the finding is well-supported, not a one-off.
- [CONFIRMED] **Aptori** — real commercial AppSec platform; genuinely does sovereign/on-prem/air-gapped autonomous offensive testing with model routing to local *or* hosted LLMs; multiple 2026 Global InfoSec Awards. Note it also does remediation verification / retest-after-fix — evidence our Verification Agent idea is a real product feature, not speculation.

### Previously-unverified items — now resolved
- [CONFIRMED] **ADACIS / Pentest.LLM / France 2030 / EUR 3M** — Led by Prof. Toufik Ahmed (Univ. Bordeaux / LaBRI) with Knocknock and ADACIS; one of 12 "France 2030" cybersecurity laureates; EUR 3M shared across partners; explicitly a *sovereign* LLM model for NIS2/DORA compliance. Solid evidence that a *government-funded sovereign pentesting LLM* is a real category (strengthens our motivation).
- [CORRECTION] **Red-MIRROR** — CONFIRMED (arXiv:2603.27127), but it is an autonomous web-*exploitation* system (86% on XBOW). Its SRMM/reflection ideas are about agent memory. Cite as related work on the *exploitation* side we deliberately exclude — reinforces our scope boundary rather than something to adopt.
- [CONFIRMED] **July 2026 survey** — arXiv:2607.02605, "A Survey of LLM-Driven Penetration Testing", 81 papers, 2023–2026. Excellent single citation for the Related Work section's landscape framing.
- [CORRECTION] **Excalibur** — CONFIRMED (arXiv:2602.17622), but the published version is titled **"What Makes a Good LLM Agent for Real-world Penetration Testing?" and the system was renamed PentestGPT V2** (same lead author, Gelei Deng, as the original PentestGPT). The Type A / Type B failure taxonomy and Task Difficulty Assessment (TDA) are real. **Cite as PentestGPT V2, not "Excalibur".**
- [CORRECTION] **PoC-Adapt** — CONFIRMED (arXiv:2604.06618), but it is about automated *exploit/PoC generation and verification* (Univ. of Information Technology, Vietnam). Relevant to the *verification* idea but sits on the autonomous-exploitation side; cite as future-work / related, not as something we implement.
- [DROP] **NRT-Bench** — REAL ID (arXiv:2606.20408) but DROP: it is "Benchmarking Multi-Turn Red-Teaming of LLM *Operator Agents in Safety-Critical Control Rooms*" (a simulated nuclear power plant). Nothing to do with web-app security. The original research doc mislabeled it. **Do not cite.**
- [CORRECTION] **Shannon** — CONFIRMED, with important nuance: open-source (AGPL-3.0) autonomous pentester by **Keygraph** (~40K GitHub stars; 96.15% on XBOW). Two facts matter for us: (1) it is a *proof-by-exploitation* tool — it actually exploits to eliminate false positives, i.e. it does the exploitation half we deliberately exclude; (2) **it runs on the Claude API (cloud), ~$40–60 per scan — not local.** This is a *clean contrast* for our sovereignty pitch: the strongest open-source agent in this space is cloud-dependent and cannot be used under a data-residency mandate.
- [CORRECTION] **Dynamiq** — CONFIRMED (getdynamiq.ai), but it is a *general* agentic-AI platform with air-gapped deployment, **not** a pentesting tool. Cite (if at all) as evidence that air-gapped agentic-AI deployment is commercially normal, not as a pentesting competitor.
- [CORRECTION] **Rexon Cyber** — CONFIRMED, but a cybersecurity *consulting/services* firm offering "Air-Gapped LLM Deployment" as a service, not a product like AutoRedBlue. Same use: evidence the sovereign-AI-security niche is real.
- [CORRECTION] **CaptureTheBug** — CONFIRMED, but a *human-led* PTaaS platform with unlimited retesting / verified remediation — not an autonomous AI tool. Validates the "continuous retest / verify-the-fix" model our Verification Agent implements.
- [CAUTION] **"Tool-calling latency = up to 96% of end-to-end inference time"** — plausible and directionally consistent with the constraint-tax literature, but treat as a general claim; if used in the report, attribute cautiously or cite the specific source directly rather than as established fact.

**Net result:** almost every source was real. Four needed material corrections (Excalibur -> PentestGPT V2 name; Red-MIRROR and PoC-Adapt are exploitation-side; Shannon is cloud-based). One (NRT-Bench) is dropped as irrelevant. None of the corrections change any ADOPT/ACKNOWLEDGE decision below.

---

## 2026-08-24 — Findings 1–4 (source: Gemini research round) — dispositions

### Finding 1 — Sovereign pentesting & data residency
**Verified reality:** sovereign/air-gapped AI security is a real, funded, commercial category — Aptori, ADACIS/Pentest.LLM (EUR 3M, France 2030), Dynamiq, Rexon Cyber. Pakistan's WASL/PDA mandate is real.
**Disposition:**
- Market-validation -> **ACKNOWLEDGE** (Related Work). "Runs locally" alone is not novel. Our differentiator sharpens to: *reliable small-model (7B–14B) local operation on modest edge hardware for the localized-compliance niche that big sovereign-cloud platforms don't serve*, tuned to the Pakistani public sector.
- Cryptographic WASL "compliance matrix" -> **ACKNOWLEDGE (Future Extensions)**. Needs the non-public classified WASL spec; whole new subsystem; strong productisation pitch, not FYP scope.

### Finding 2 — Constraint tax / toolshim / decoding engines
**Verified reality:** forcing strict JSON in the reasoning call suppresses small-model reasoning and can suppress tool calls entirely (arXiv:2606.25605, corroborated by 2605.26128).
**Disposition:**
- Core insight -> **ADOPT**. Reason in loose XML, parse to JSON with plain Python in a *separate* step. A simplification vs grammar-constrained mode; directly de-risks our #1 risk.
- Separate fine-tuned toolshim model + custom decoding engine (XGrammar-2) -> **REJECT (build), mention only**. Doesn't fit 16GB alongside the main model; unnecessary at our scale.

### Finding 3 — Remediation verification & reproducible-request triage
**Verified reality:** real gap; leading tools (Aptori, Shannon, CaptureTheBug) treat retest-after-fix / proof-per-finding as core. Note Shannon/PoC-Adapt achieve "proof" via *actual exploitation* — the line we don't cross.
**Disposition:**
- **ADOPT (reduced):** 5th **Verification Agent** replays a *saved benign request* against the patched target and checks the response; Triage must emit that saved request per kept finding (doubling as a false-positive filter). Reuses planned work; no new external tooling. **Boundary:** benign saved request, NOT autonomous exploitation.
- RL-driven autonomous PoC synthesis (PoC-Adapt-style) -> **ACKNOWLEDGE (Future Extensions)**.

### Finding 4 — Externalise planning (CHECKMATE / PEP / TDA)
**Verified reality:** CHECKMATE (arXiv:2512.11143) externalises planning to a classical planner (PEP), ~20% higher success / ~50% cheaper, already used commercially (numasec). PentestGPT V2 (arXiv:2602.17622, formerly "Excalibur") adds Task Difficulty Assessment for the same small-model failure mode.
**Disposition:**
- Architectural principle ("don't let the small model own the long-horizon plan; keep state in code") -> **ADOPT** as a design stance. LangGraph already externalises state; commit to code-owned sequencing + a fixed methodology, LLM only perceives + picks from explicit options.
- Full classical planner (PDDL) + TDA engine -> **ACKNOWLEDGE (Future Extensions)**. A second FYP; the headline future extension (cite CHECKMATE + PentestGPT V2).

---

## Follow-up research tasks
- [x] Verify every previously-unverified item (done 2026-08-25).
- [ ] At implementation time, re-check the current best-available 7B–14B tool-calling open-weight model (field moves fast; don't hard-commit from this note).
- [ ] Skim CHECKMATE (2512.11143) and PentestGPT V2 (2602.17622) properly — both are Related Work citations and justify the code-owns-planning stance.
- [ ] When writing Related Work, use the July survey (2607.02605) as the landscape anchor and cite Shannon as the cloud-dependent contrast case.

---

## 2026-09-06 — Departmental prior art (COMSATS RMS student console)

Not external web research, this is internal departmental prior art Adeel retrieved directly from RMS (automated access was blocked by the site's own robots restriction, so this was a manual check).

- **"Web Application Security Scanner"** — Yasir Ali Khan Wazir (CIIT/FA22-BCS-011/WAH) & Gul Faraz Khan (CIIT/FA22-BCS-122/WAH), supervised by Mr. Taimur Sajjad. Dual-mode (Soft/Deep) rule-based scanner: regex-based XSS detection, payload-fuzzing SQLi, CSRF token checks, static fix suggestions, JWT-based auth for the tool's own users, JSON/PDF/HTML reports. **No AI/LLM component anywhere in the design.** Itself cites an earlier FYP, "Website Pen Tester", as its own prior art.
- **"Website Pen Tester"** — earlier FYP, referenced only by name via the above; not independently retrieved.

**Comparison to AutoRedBlue (used for FYP form fields (d)/(d-1)/(d-2)):**

| | Web Application Security Scanner | AutoRedBlue |
|---|---|---|
| Detection method | Rule-based: regex, payload fuzzing, static rules | LLM-agent reasoning |
| Deployment | Hosted, multi-user web app | Fully local, on the client's own machine |
| "Two modes" axis | Soft/Deep = test aggressiveness | Unauthenticated/authenticated = target's own auth boundary |
| Remediation | Static one-time suggestions | Verification Agent re-tests and confirms the fix |
| Report grounding | Templated | RAG-grounded (CVE/OWASP) |

No overlap found on any of AutoRedBlue's actual differentiators, this is real evidence for (d-2), not an assumption.
