# REQUIREMENTS.md

## Milestone v1.0.0 — Audit (Complete)

| ID | Requirement | Source | Phase | Status |
|---|---|---|---|---|
| REQ-01..REQ-08 | Full codebase, ML/DL, paper & cross-reconciliation audit | SPEC v1.0.0 | Phases 1–4 | Complete (40/40 verified) |

## Milestone v2.0.0 — Remediation

| ID | Requirement | Target Discrepancies | Phase | Status |
|---|---|---|---|---|
| REM-01 | Preserve 12 raw columns in scraper/merge, fix `run_parallel_scrapers.py` interpreter, standardize `2016-08-01` (`N=655,649`) in `sync_post_classification.py` & regenerate `yearly_intelligence_trends.json` / `common_duration_summary.json` / `global_multi_year_intelligence_report.md`, check `myrobi_global.csv` null/dup handling | `DISC-CRIT-08`, `DISC-MAJ-16`, `DISC-MIN-06`, `DISC-HYG-01`, `DISC-HYG-05` | Phase 5 | Complete (Phase 5 VERIFICATION.md) |
| REM-02 | Fix `demo/app.py` (`out_cat` wiring, training banner, paper title alignment), sync all `requirements.txt` manifests, update `README.md` scorecard/badges & `TODO.txt` | `DISC-MAJ-03`, `DISC-MAJ-08`, `DISC-MIN-14..17`, `DISC-HYG-02`, `DISC-HYG-03` | Phase 5 | Complete (Phase 5 VERIFICATION.md) |
| REM-03 | Verify true BanglaBERT trained index order & align `dl/models/banglabert_finetuned_*/config.json` vs `cat_le.joblib` / `sent_le.joblib` & zip archive; fix `bilstm_vocab` JSON portability, `dl/train_bilstm_category.py` off-by-one, `dl/predict_dl.py`, `dl/README.md`, `dl/reports/results.txt` | `DISC-CRIT-07`, `DISC-MAJ-04` (code/docs), `DISC-MAJ-19`, `DISC-MIN-07..09`, `DISC-HYG-06`, `DISC-HYG-07` | Phase 6 | Complete (Phase 6 VERIFICATION.md) |
| REM-04 | Fix `ml/train_filtered_experiments.py` (`GOLD_CSV`), align `ml/train_category.py` (`mean±std`, Colab pipeline parity), `ml/language_detector.py`, `ml/reports/*`, `data/processed/mygp_classified_reviews.csv` `operator`, and rebuild `data/gold_set/*` strictly from active `N=300`/`N=200` (retiring `g600` leakage, anonymizing `calculate_agreement.py`, handling `[BLIND_106]` note) | `DISC-CRIT-01` (benchmarks), `DISC-MAJ-01`, `DISC-MAJ-05`, `DISC-MAJ-06` (reports), `DISC-MIN-10..13`, `DISC-HYG-08` | Phase 6 | Complete (Phase 6 VERIFICATION.md) |
| REM-05 | Build `scripts/compute_statistical_tests.py` producing ground-truth CV, paired $t$-tests, McNemar, active Rogan-Gladen, `V`/`d`, Table 3/4/5/6/7/8 & Case Studies 1–2 empirical JSON; complete `scripts/audit_project_integrity.py` Modules 2/3/7; resolve broken/stale scripts in `scripts/`; fix `.sh` CRLF & `validate-*.ps1` | `DISC-CRIT-01..05` (stats), `DISC-MAJ-07`, `DISC-MAJ-09`, `DISC-MAJ-10`, `DISC-HYG-09`, `DISC-HYG-10` | Phase 7 | Complete (Phase 7 VERIFICATION.md) |
| REM-06 | Regenerate clean `figure0`–`figure4` PNGs (no dual numbering, no clipping, coherent Figure 3 quadrants, dual alias sync in `generate_two_panel_figure.py`) across `paper/figures/`, `paper/eswa_latex/figures/`, `paper/telecommunications_policy_latex/figures/` | `DISC-MAJ-13`, `DISC-HYG-04` | Phase 8 | Complete |
| REM-07 | Fix `scripts/reconstruct_master_manuscript.py` & `paper/eswa_latex/*` (`manuscript.tex`, `manuscript_twocolumn.tex`, `title_page.tex`, `highlights.txt`, `references.bib`): remove markdown syntax, fix Table 1/2/3/4/5/6/7/8, Case Studies 1 & 2, architecture/LLM claims, ARPU/SAC, overfull boxes, BibTeX years & orphans, `rh61632` URL, and recompile ESWA PDFs cleanly to `paper/*.pdf` | `DISC-CRIT-01..06`, `DISC-MAJ-02`, `DISC-MAJ-04..06`, `DISC-MAJ-09..12`, `DISC-MAJ-17`, `DISC-MIN-01..05` | Phase 8 | Complete |
| REM-08 | Fix & run `scripts/build_paper_empirical_excel.py` -> `paper/JBA_Manuscript_Empirical_Calculations.xlsx`; fix `paper/telecommunications_policy_latex/` Eq 9, review counts & recompile PDFs; fix `scripts/build_paper_html.py` & rebuild `paper/{index,paper}.html`; clean scratch files; verify full end-to-end integrity (`AUDIT_v2.md`) | `DISC-MAJ-14`, `DISC-MAJ-15`, `DISC-MIN-18`, clean workspace verification | Phase 9 | Complete (Phase 9 VERIFICATION.md) |

---

*Last updated: 2026-11-14*
