---
phase: 4
plan: 2
wave: 2
depends_on:
  - "1-PLAN.md"
files_modified:
  - .gsd/DISCREPANCY_REPORT.md
  - .gsd/AUDIT.md
  - .gsd/phases/4/2-SUMMARY.md
autonomous: true
user_setup: []

must_haves:
  truths:
    - "All discrepancies across Phases 1–4 are consolidated and deduplicated using the 8 duplicate clusters mapped in RESEARCH.md, producing zero double-counted entries"
    - "The canonical .gsd/DISCREPANCY_REPORT.md is synthesized with complete file:line citations, empirical proof, and exact remediation paths, ranked across Critical, Major, Minor, and Hygiene tiers and grouped into Project, Paper, and Cross-Artifact domains"
    - "The milestone audit report .gsd/AUDIT.md is synthesized following .agent/workflows/audit-milestone.md, detailing requirement satisfaction (REQ-01..REQ-08), technical debt, phase quality verdicts, and a definitive publication readiness evaluation"
  artifacts:
    - ".gsd/DISCREPANCY_REPORT.md"
    - ".gsd/AUDIT.md"
    - ".gsd/phases/4/2-SUMMARY.md"
  key_links:
    - "Canonical discrepancy catalog links findings from .gsd/phases/{1,2,3}/VERIFICATION.md and .gsd/phases/4/evidence/* to .gsd/DISCREPANCY_REPORT.md"
    - "Milestone audit links requirement status in .gsd/REQUIREMENTS.md and .gsd/SPEC.md to .gsd/AUDIT.md"
---

# Plan 4.2: Cross-Phase Discrepancy Deduplication & Milestone Audit Synthesis

<objective>
Consolidate and deduplicate all empirical findings across Phase 1 (Core Pipeline & Docs), Phase 2 (ML/DL & Scripts), Phase 3 (ESWA & Cross-Venue Paper Deliverables), and Plan 4.1 (Quantitative Cross-Reconciliation) using the 8 cross-phase duplicate clusters mapped in `RESEARCH.md`. Synthesize the authoritative, severity-ranked `.gsd/DISCREPANCY_REPORT.md` (Critical / Major / Minor / Hygiene across Project, Paper, and Cross-Artifact domains) and produce the milestone audit report `.gsd/AUDIT.md` following the milestone audit workflow without modifying any project or paper files outside `.gsd/`.
</objective>

<context>
Load for context:
- .gsd/SPEC.md
- .gsd/REQUIREMENTS.md
- .gsd/ROADMAP.md
- .gsd/DECISIONS.md
- .gsd/phases/4/RESEARCH.md
- .gsd/phases/1/VERIFICATION.md
- .gsd/phases/2/VERIFICATION.md
- .gsd/phases/3/VERIFICATION.md
- .gsd/phases/4/evidence/01_corpus_eras_and_language_reconciliation.md
- .gsd/phases/4/evidence/02_shocks_priority_matrix_and_cases_reconciliation.md
- .gsd/phases/4/evidence/03_models_complexity_and_gold_reconciliation.md
- .gsd/phases/4/1-SUMMARY.md
- .agent/workflows/audit-milestone.md
</context>

<tasks>

<task type="auto">
  <name>Deduplicate cross-phase discrepancies and synthesize canonical .gsd/DISCREPANCY_REPORT.md</name>
  <files>
    .gsd/phases/1/VERIFICATION.md
    .gsd/phases/2/VERIFICATION.md
    .gsd/phases/3/VERIFICATION.md
    .gsd/phases/4/evidence/01_corpus_eras_and_language_reconciliation.md
    .gsd/phases/4/evidence/02_shocks_priority_matrix_and_cases_reconciliation.md
    .gsd/phases/4/evidence/03_models_complexity_and_gold_reconciliation.md
    .gsd/phases/4/1-SUMMARY.md
    .gsd/DISCREPANCY_REPORT.md
  </files>
  <action>
    Consolidate and deduplicate all discrepancy records across Phases 1–4 into `.gsd/DISCREPANCY_REPORT.md`:
    1. Inventory and cross-link all findings:
       - Phase 1: 21 numbered `DISC-001..021` plus unnumbered raw schema / duplicate row items.
       - Phase 2: 32 items across DL (`P2-DL-01..11`), ML & Gold Standard (`P2-ML-12..20`, `P2-GOLD-21`), and Scripts (`DISC-P2-22..32`).
       - Phase 3: Active ESWA Manuscript (`P3-ESWA-01..12`), Cross-Venue Telecom Policy (`P3-TP-01..07`), HTML deliverables (`P3-HTML-01..04`), Excel/Figures (`P3-XLSX-FIG`), and 32 paper scripts (`P3-SCRIPTS-01..03`).
       - Phase 4.1: Direct quantitative cross-reconciliation findings against ground truth CSV/JSON/models (Table 1 deployed %, Table 2 CV metrics/t-tests/latency, Table 3 typos, Table 4 language sub-cohorts, Table 5 eras/NSS prose, Table 6 shocks/case studies, Section 5.3 Priority Matrix 88k, Gold standard g600 leakage vs g300, Rogan-Gladen Se/Sp & PABAK provenance, uncited 28% ARPU).
    2. Apply the 8 deduplication clusters mapped in `RESEARCH.md:237-248` to prevent double counting:
       - Cluster 1: Merge dead gold CSV path (`DISC-008` + `P2-ML-16`).
       - Cluster 2: Merge seed annotation LLM identifier (`DISC-009` + `P3-ESWA-12`).
       - Cluster 3: Consolidate `nltk` omissions across manifests (`DISC-010`, `DISC-011`, `P2-ML-20`).
       - Cluster 4: Link word-only BiLSTM architecture claims (`DISC-005` code duplicate + `P2-DL-07` Char-CNN mismatch + `P3-ESWA-12` GloVe/multi-head fiction).
       - Cluster 5: Merge category voting classifier provenance and weights (`DISC-006` + `P2-ML-13` + `P3-ESWA-12`).
       - Cluster 6: Consolidate seed sample count drift `4,499` vs `4,500` and `4,486` Symbolic exclusions (`P2-ML-12`, `P2-ML-18`, `P3-ESWA-06`, `P3-ESWA-07`).
       - Cluster 7: Consolidate broken/stale paper audit scripts (`DISC-P2-22..28` + `P3-SCRIPTS-01..03`).
       - Cluster 8: Reconcile ESWA title prefix `"With Great Reviews..."` across `demo/app.py:114`, `manuscript.tex:32`, `title_page.tex:14`, and legacy drafts (`DISC-017` + `P3-ESWA-04`).
    3. Categorize all entries under 4 standard severity tiers:
       - **Critical:** Integrity breaches, silent runtime failures, fabricated metrics, and data/paper contradictions.
       - **Major:** High-impact defects affecting reproducibility, LaTeX build boxes, model evaluation drift, and missing required modules.
       - **Minor:** Unreferenced labels, rounding/typo differences, code style drift, and localized documentation mismatches.
       - **Hygiene:** Dead files, unanchored regexes, duplicate utility definitions, and manifest cleanup.
    4. Group cleanly into 3 domains:
       - **Group A: Project Codebase & Pipeline Discrepancies** (scrapers, merge logic, model scripts, demo wiring, dependency manifests).
       - **Group B: Research Paper Deliverables Discrepancies** (ESWA manuscript, LaTeX build logs, BibTeX citations, unreferenced floats, Telecom Policy cross-venue drift, HTML HUD/math errors, missing XLSX workbook).
       - **Group C: Cross-Artifact Quantitative Contradictions** (common-window counts, Table 1 deployed %, Table 2 CV metrics/t-tests, Table 3 typos, Table 4 language sub-cohorts, Table 5 eras/NSS prose, Table 6 shocks/case studies, Section 5.3 Priority Matrix 88k, Gold standard g600 leakage vs g300, Rogan-Gladen Se/Sp & PABAK provenance, uncited 28% ARPU).
    5. Ensure every catalog entry contains:
       - Canonical Identifier (e.g. `DISC-CRIT-01`, `DISC-MAJ-01`, etc.)
       - Cross-Phase Traceability IDs (e.g., `[Phase 1: DISC-008, Phase 2: P2-ML-16]`)
       - Exact File and Line References (`file:line`)
       - Empirical Proof / Observed Output
       - Impact Assessment
       - Concrete, Actionable Remediation Step
    6. Include an Executive Discrepancy Matrix summarizing total counts by Severity vs Domain.

    AVOID: Modifying any project source or paper files outside `.gsd/`.
    USE: Markdown formatting with structured tables and clear callouts in `.gsd/DISCREPANCY_REPORT.md`.
  </action>
  <verify>
    python -c "import os; assert os.path.exists('.gsd/DISCREPANCY_REPORT.md'), 'Discrepancy report missing'; print('Discrepancy report verified')"
  </verify>
  <done>
    `.gsd/DISCREPANCY_REPORT.md` exists and contains a deduplicated, severity-ranked (Critical / Major / Minor / Hygiene), domain-grouped (Project / Paper / Cross-Artifact) catalog with exact file:line citations, empirical proof, and remediation actions for all discrepancies across Phases 1–4.
  </done>
</task>

<task type="auto">
  <name>Synthesize final milestone audit report .gsd/AUDIT.md following the milestone audit workflow</name>
  <files>
    .gsd/SPEC.md
    .gsd/REQUIREMENTS.md
    .gsd/ROADMAP.md
    .gsd/DECISIONS.md
    .gsd/DISCREPANCY_REPORT.md
    .gsd/phases/1/VERIFICATION.md
    .gsd/phases/2/VERIFICATION.md
    .gsd/phases/3/VERIFICATION.md
    .gsd/phases/4/1-SUMMARY.md
    .gsd/AUDIT.md
    .gsd/phases/4/2-SUMMARY.md
  </files>
  <action>
    Synthesize `.gsd/AUDIT.md` in strict adherence to `.agent/workflows/audit-milestone.md`:
    1. Milestone Overview:
       - Milestone Name: Project & Paper Discrepancy Audit (v1.0.0).
       - Audit Completion Date: 2026-11-11.
       - Scope: Full repository (`scraped_data_global/`, `data/`, `ml/`, `dl/`, `demo/`, `scripts/`, `paper/`, `archive/`).
       - Summary Metrics: 4 phases, 11 total plans, 0 gap closure plans, total discrepancies identified by severity.
    2. Must-Haves & Requirement Satisfaction Matrix:
       - Explicitly audit requirements `REQ-01` through `REQ-08` from `.gsd/REQUIREMENTS.md`.
       - Map each requirement to its verification artifact, empirical evidence, fulfillment status (Fulfilled), and key findings.
    3. Technical Debt & Architectural Decisions Review:
       - Evaluate adherence to `ADR-001` (Read-only policy, zero git commits) and `ADR-002` (Sequential inherit workspace execution).
       - Document uncommitted working-tree drift (39 modified tracked files + untracked directories).
       - Record local runtime environment debt (Python 3.15.1 lacking `transformers`, `gradio`, `groq`, `sentence-transformers`).
       - Document acknowledged technical debt items across codebase and paper deliverables.
    4. Phase-by-Phase Quality and Verification Review:
       - Phase 1: Core Pipeline, Data, Demo & Documentation Audit (12/12 must-haves verified).
       - Phase 2: ML/DL Models, Gold Standard & Empirical Scripts Audit (9/9 must-haves verified).
       - Phase 3: Research Paper & Cross-Venue Deliverables Audit (13/13 must-haves verified).
       - Phase 4: Cross-Artifact Quantitative Reconciliation & Synthesis (empirically reconciled against ground truth).
    5. Strategic Assessment & Publication Readiness Verdict:
       - Provide a clear, frank assessment of the paper's readiness for submission to ESWA (`Verdict: NOT submission-ready in its current state`).
       - Highlight the primary submission blockers (fabricated/leaked gold standard benchmark, Table 6 non-shock rows and conflation, Table 5 era overlap arithmetic, and unexecuted contingency/t-test/McNemar claims).
       - Outline a prioritized remediation roadmap for authors and developers to bring both the paper and repository into full integrity.
    6. Write `.gsd/AUDIT.md` and generate `.gsd/phases/4/2-SUMMARY.md`.

    AVOID: Modifying any project source or paper files outside `.gsd/`. Do NOT execute git commit or git add.
    USE: Comprehensive markdown following the milestone audit format.
  </action>
  <verify>
    python -c "import os; assert os.path.exists('.gsd/AUDIT.md'), 'Audit report missing'; print('Audit report verified')"
  </verify>
  <done>
    `.gsd/AUDIT.md` exists and contains the complete milestone audit detailing requirement satisfaction (REQ-01..REQ-08), technical debt, phase quality reviews, and publication readiness assessment.
  </done>
</task>

</tasks>

<verification>
After all tasks complete, verify:
- [ ] `.gsd/DISCREPANCY_REPORT.md` exists, contains deduplicated discrepancies across Phases 1–4 ranked by severity (Critical / Major / Minor / Hygiene), grouped into Project / Paper / Cross-Artifact, with file:line citations and remediation actions.
- [ ] `.gsd/AUDIT.md` exists, follows `.agent/workflows/audit-milestone.md`, documents requirement fulfillment (REQ-01..REQ-08), and evaluates publication readiness.
- [ ] `.gsd/phases/4/2-SUMMARY.md` is generated summarizing completion of Plan 4.2.
</verification>

<success_criteria>
- [ ] All tasks verified passing with exit code 0
- [ ] No project source, data, model, plot, or paper files outside `.gsd/` were modified
- [ ] No git commands (`git add`, `git commit`) were executed
</success_criteria>
