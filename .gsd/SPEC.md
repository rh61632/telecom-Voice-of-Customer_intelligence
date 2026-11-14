# SPEC.md — Project Specification (v2.0.0 Remediation Milestone)

> **Status**: `FINALIZED`
>
> **Planning Lock**: Cleared for remediation planning and execution (`ADR-003`).

## Vision
Remediate all 55 cataloged discrepancies across the **Telecom Voice-of-Customer (VoC) Intelligence** codebase, data/telemetry pipeline, ML/DL models and reports, verification tooling, active *Expert Systems with Applications* (ESWA) manuscript and PDFs, and secondary venue/web/Excel deliverables, bringing the entire repository and research paper into 100% empirical, reproducible alignment under the full GSD pipeline (`PLAN -> EXECUTE -> VERIFY -> AUDIT`).

## Goals
1. **Pipeline, Demo & Dependency Remediation (Phase 5)** — Preserve all 12 raw columns in scrapers/merge, standardize `2016-08-01` (`N=655,649`) across sync scripts and JSON/MD summaries, fix `demo/app.py` (`out_cat`, banner, requirements), align dependency manifests, and reconcile `README.md` / `TODO.txt`.
2. **ML/DL Provenance, Label Alignment & Gold Benchmark Remediation (Phase 6)** — Verify and fix BanglaBERT `config.json` label indices against true trained class order, fix `ml/train_filtered_experiments.py`, resolve BiLSTM JSON vocab / `train_bilstm_category.py` / `predict_dl.py` loading issues, align `ml/` / `dl/` training scripts & reports, and rebuild gold benchmarks strictly on active `N=300` / `N=200` consensus (retiring `g600` leakage).
3. **Statistical Ground Truth & Integrity Tooling Remediation (Phase 7)** — Build a canonical reproducible statistical/econometric reconciliation script (`scripts/compute_statistical_tests.py`) computing exact 5-fold CV, paired $t$-tests, McNemar, active Rogan-Gladen parameters, Table 3 & 4 metrics, 122-month non-overlapping Era NSS, all 35 modern shocks, Case Studies 1 & 2, and Priority Matrix stats; complete `scripts/audit_project_integrity.py` (Modules 2, 3, 7); archive/fix broken legacy scripts; fix `.sh` line endings and `.ps1` validators.
4. **Figures & Active ESWA Manuscript/PDF Remediation (Phase 8)** — Regenerate clean publication figures (`figure0`–`figure4`) free of dual headers, clipping, and quadrant contradictions; repair `scripts/reconstruct_master_manuscript.py` (or clean direct templating); eliminate every critical/major/minor discrepancy in `paper/eswa_latex/` (`manuscript.tex`, `manuscript_twocolumn.tex`, `title_page.tex`, `highlights.txt`, `references.bib`); recompile PDFs cleanly with zero errors/overfull warnings and sync to `paper/*.pdf`.
5. **Cross-Venue Deliverables & Final Full-System Audit (Phase 9)** — Regenerate `paper/JBA_Manuscript_Empirical_Calculations.xlsx` from active ground truth, fix `paper/telecommunications_policy_latex/` (Eq 9, counts, PDF recompile) and `paper/*.html` (`build_paper_html.py` KaTeX escapes, HUD word count, July 2016 exclusion), clean temporary LaTeX artifacts, and run full empirical verification across codebase and paper.

## Non-Goals (Out of Scope)
- Re-scraping Google Play or mutating historical `N=655,649` / `N=4,500` / `N=300` human labels.
- Creating unsolicited git commits or pushing to GitHub / Hugging Face Hub.
- Installing cloud-only packages (`gradio`, `transformers`, `groq`) globally unless needed, though all code/imports/requirements must be syntactically verified and tested against available packages.

## Constraints
- **Empirical Integrity (`ADR-003`):** Every reported number in code, reports, tables, figures, and LaTeX must match executed Python output on live workspace data. Unsubstantiated external commercial numbers (`28% ARPU`, `3.5x–5.0x SAC`) must be removed or replaced with strictly evidenced qualitative/literature-grounded statements.
- **Sequential `inherit` Workspace (`ADR-002`):** Sequential execution in parent workspace.
- **PowerShell Discipline:** One command per invocation (no `&&` or `||`).

## Success Criteria
- [ ] All 8 Critical discrepancies (`DISC-CRIT-01..08`) resolved and verified empirically.
- [ ] All 19 Major, 18 Minor, and 10 Hygiene discrepancies (`DISC-MAJ-01..19`, `DISC-MIN-01..18`, `DISC-HYG-01..10`) resolved or explicitly documented if external/untrainable locally.
- [ ] `scripts/audit_project_integrity.py` (all 8 modules) and `scripts/validate-all.ps1` pass cleanly (`rc=0`).
- [ ] Active ESWA PDFs compile cleanly (`0` undefined refs/citations, `0` overfull equations/URLs, `0` raw markdown tokens) and match `paper/*.pdf`.
- [ ] Every remediation phase (Phases 5–9) independently verified by `gsd-verifier` and summarized in `.gsd/AUDIT_v2.md`.

---

*Last updated: 2026-11-11*
