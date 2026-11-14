---
milestone: Project & Paper Discrepancy Remediation
version: 2.0.0
updated: 2026-11-11T12:55:00+06:00
---

# Roadmap

> **Current Phase:** 9 - Cross-Venue Deliverables, Workbook & Final System Verification
> **Status:** executing

## Must-Haves (from SPEC v2.0.0)

- [x] Milestone v1.0.0 Audit Complete (Phases 1–4 verified 40/40, 55 discrepancies cataloged)
- [x] Phase 5: Data pipeline, telemetry JSONs, demo UI, dependencies, README & TODO fixed and verified
- [x] Phase 6: ML/DL scripts, label mappings, gold benchmarks & reports fixed and verified
- [x] Phase 7: Statistical ground-truth script, `audit_project_integrity.py`, legacy scripts & GSD validators fixed and verified
- [x] Phase 8: Publication figures, ESWA LaTeX manuscripts, BibTeX & compiled PDFs fixed and verified
- [ ] Phase 9: Cross-venue deliverables (Excel workbook, Telecom Policy, HTML), cleanup & full end-to-end re-verification complete

---

## Completed Milestone v1.0.0 Phases (Audit)

- ✅ **Phase 1:** Core Pipeline, Data, Demo & Documentation Audit (`3/3` plans, `12/12` verified)
- ✅ **Phase 2:** ML/DL Models, Gold Standard & Empirical Audit Scripts (`3/3` plans, `9/9` verified)
- ✅ **Phase 3:** Research Paper & Cross-Venue Deliverables Audit (`3/3` plans, `13/13` verified)
- ✅ **Phase 4:** Cross-Artifact Quantitative Reconciliation & Synthesis (`2/2` plans, `6/6` verified)

---

## Milestone v2.0.0 Phases (Remediation)

### Phase 5: Data Pipeline, Telemetry JSONs, Demo UI & Dependencies Remediation
**Status:** ✅ Complete (Verified 20/20 must-haves -> `.gsd/phases/5/VERIFICATION.md`)
**Objective:** Preserve 12 raw columns in scraper/merge, fix `run_parallel_scrapers.py` & `sync_post_classification.py` (`2016-08-01`, `N=655,649`), regenerate telemetry JSONs/MD, fix `demo/app.py` (`out_cat`, banner, dependencies), align all `requirements.txt`, and fix `README.md` / `TODO.txt`.
**Requirements:** REM-01, REM-02
**Depends on:** Phase 4 (Audit Complete)

**Plans:**
- [x] Plan 5.1: Remediate raw scrapers, resolve Robi null review_id safely, and regenerate telemetry JSONs/MD
- [x] Plan 5.2: Wire Gradio `out_cat` callback, update banner/title, and reconcile dependency manifests
- [x] Plan 5.3: Reconcile `README.md` and `TODO.txt` without paper references

---

### Phase 6: ML/DL Models, Label Mappings, Gold Standard & Reports Remediation
**Status:** ✅ Complete (Verified 16/16 must-haves -> `.gsd/phases/6/VERIFICATION.md`)
**Objective:** Verify BanglaBERT true trained index order and align `config.json` / `cat_le.joblib` / zip archive, fix `bilstm_vocab` portability & DL scripts/reports, fix `ml/train_filtered_experiments.py` & `ml/train_category.py` & `ml/language_detector.py` & `ml/reports/*`, and rebuild active `N=300`/`N=200` gold benchmarks.
**Requirements:** REM-03, REM-04
**Depends on:** Phase 5

**Plans:**
- [x] Plan 6.1: Remediate DL portability (`bilstm_vocab.json` + `dl/bilstm_artifacts.py`), fix `train_bilstm_category`/`finetune_banglabert`/`predict_dl`, repack zip, and align `dl/README` & `results.txt`
- [x] Plan 6.2: Align `ml/train_category`, fix `train_filtered_experiments` & `language_detector`, re-run linguistic subcohorts, and update `ml/reports/*` & `ml/README.md`
- [x] Plan 6.3: Add `operator` column to mygp seed CSV, anonymize `calculate_agreement.py`, retire `g600` leakage across `gold_set/*`, and sync `README.md` gold benchmark table

---

### Phase 7: Statistical Ground Truth, Integrity Tooling & Script Hygiene Remediation
**Status:** ✅ Complete (Verified 36/36 must-haves -> `.gsd/phases/7/VERIFICATION.md`)
**Objective:** Implement `scripts/compute_statistical_tests.py` to compute canonical live metrics for all paper tables/tests/shocks/case studies, complete `scripts/audit_project_integrity.py` (Modules 2, 3, 7), clean/fix stale scripts in `scripts/`, convert `.sh` CRLF->LF, and anchor `validate-*.ps1`.
**Requirements:** REM-05
**Depends on:** Phase 6

**Plans:**
- [x] Plan 7.1: Implement & run canonical `scripts/compute_statistical_tests.py` generating `paper_empirical_ground_truth.json` and companion MD
- [x] Plan 7.2: Retire 28 legacy scripts to `archive/legacy_scripts/`, repair verify scripts in-place, and complete all 8 modules in `scripts/audit_project_integrity.py`
- [x] Plan 7.3: Convert `scripts/*.sh` CRLF->LF, extend `validate-encoding`, and anchor `scripts/validate-*.ps1` with `$PSScriptRoot` and frontmatter regexes

---

### Phase 8: Publication Figures, Active ESWA Manuscript & Compiled PDFs Remediation
**Status:** ✅ Complete (24/24 must-haves verified in `.gsd/phases/8/VERIFICATION.md`)
**Objective:** Regenerate clean `figure0`–`figure4` PNGs, retire/fix brittle `reconstruct_master_manuscript.py`, fix all empirical, architectural, structural, BibTeX, and formatting discrepancies across `paper/eswa_latex/*`, and compile clean ESWA PDFs synced to `paper/*.pdf`.
**Requirements:** REM-06, REM-07
**Depends on:** Phase 7

**Plans:**
- [x] Plan 8.1: Regenerate clean publication figures (`figure0`–`figure4`) free of bitmap prefixes and clipping, align `figure3` to 3.75% threshold, and sync SHA256 hashes across venues and aliases
- [x] Plan 8.2: Archive legacy patchers, fix `references.bib`, `title_page.tex`, `compute_statistical_tests.py:818`, and align `manuscript.tex` & `manuscript_twocolumn.tex` to 100% empirical ground truth
- [x] Plan 8.3: Compile ESWA PDFs with strict log/page checks (`<=35` / `<=15` pages), verify SHA256 sync, and validate `audit_project_integrity.py` with Checks 1–3 cleared

---

### Phase 9: Cross-Venue Deliverables, Workbook & Final System Verification
**Status:** ✅ Complete (26/26 must-haves verified in `.gsd/phases/9/VERIFICATION.md`)
**Objective:** Generate `paper/JBA_Manuscript_Empirical_Calculations.xlsx`, fix `paper/telecommunications_policy_latex/` & recompile PDFs, fix & rebuild `paper/{index,paper}.html`, remove scratch artifacts, and run full post-remediation integrity & verifier checks.
**Requirements:** REM-08
**Depends on:** Phase 8

**Plans:**
- [x] Plan 9.1: Remediate `build_paper_empirical_excel.py` and generate canonical `paper/JBA_Manuscript_Empirical_Calculations.xlsx`
- [x] Plan 9.2: Remediate `paper/telecommunications_policy_latex/` (compile in-place) and `scripts/build_paper_html.py` (`index.html`/`paper.html`)
- [x] Plan 9.3: Fix `demo/app.py:54`, clean workspace scratch/patchers, run full system verification battery, and author `.gsd/AUDIT_v2.md`
- [x] Plan 9.4: Close HTML deliverable gaps (Table 4 shock recovery, HUD count synchronization, reference pruning) and re-verify Phase 9 (26/26 PASS)

---

## Progress Summary (v2.0.0)

| Phase | Status | Plans | Complete |
|---|---|---|---|
| 5 | ✅ | 3/3 | 2026-11-11 |
| 6 | ✅ | 3/3 | 2026-11-11 |
| 7 | ✅ | 3/3 | 2026-11-11 |
| 8 | ✅ | 3/3 | 2026-11-12 |
| 9 | ✅ | 4/4 | 2026-11-14 |

---

*Last updated: 2026-11-14*
