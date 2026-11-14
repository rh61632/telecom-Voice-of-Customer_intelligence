# Plan 1.3 Summary: Documentation, Live Demo & Working-Tree Drift Audit

**Phase:** 1 - Core Pipeline, Data, Demo & Documentation Audit  
**Plan:** `3-PLAN.md` (Plan 3 of 3)  
**Status:** Completed  
**Execution Mode:** Strictly Read-Only Audit (`ADR-001`, `ADR-002`)  
**Date:** 2026-11-11  

---

## 1. Executive Summary

Plan 1.3 audited the Gradio interactive demo application in `demo/app.py`, checked dependency completeness in `demo/requirements.txt`, reconciled all published metrics, scorecards, badges, and roadmap items in `README.md`, `data/README.md`, and `TODO.txt` against underlying ground-truth data, and comprehensively cataloged all 39 pre-existing uncommitted modified tracked files and untracked artifacts composing the working-tree drift.

All tasks were executed in strict read-only compliance with `ADR-001` and `ADR-002`: no project code, data, model, or paper files outside `.gsd/` were altered, and no `git add` or `git commit` commands were issued.

---

## 2. Completed Tasks

| Task | Objective | Evidence Artifact | Status |
|---|---|---|---|
| **Task 1** | Audit `demo/app.py` UI wiring, runtime imports, and demo documentation | `.gsd/phases/1/evidence/03_demo_application_audit.md` | **PASSED** |
| **Task 2** | Audit `README.md`, `data/README.md`, `TODO.txt`, and catalog working-tree drift | `.gsd/phases/1/evidence/03_documentation_and_drift_audit.md` | **PASSED** |

---

## 3. Key Findings & Discrepancy Catalog

### 3.1 Demo Application UI Component Wiring Bug (`demo/app.py`)
- **Unrendered Category Textbox (`out_cat`):**
  - Line 97 defines `out_cat = gr.Textbox(label="Operational Domain", interactive=False)`.
  - Line 38 calculates `category_label = f"{res['category']} ({res['category_confidence'] * 100:.1f}%)"`.
  - Line 31 (empty input fallback) returns 5 elements: `"N/A", "N/A", {}, {}, "Please enter a customer review."`.
  - Line 54 (prediction return) returns 5 elements: `lang_badge, sentiment_label, res["probabilities"], cat_probs, diagnostic_summary`. `category_label` is completely omitted from both return statements.
  - Line 108 registers 5 outputs: `outputs=[out_lang, out_sent, out_sent_probs, out_cat_probs, out_diag]`. `out_cat` is omitted from the callback output list.
  - **Empirical Consequence:** In the live web UI, the "Operational Domain" textbox remains permanently blank (`""`) on all inputs.
  - **Fix:** Add `category_label` to return tuples and `out_cat` to the `outputs` list in `submit_btn.click`.

### 3.2 Demo Training Claim Inaccuracy & Paper Title Leakage
- **Training Volume Exaggeration (`demo/app.py:67`):**
  - Banner claims: `*Trained on 655,649 longitudinal customer reviews across Grameenphone, Robi Axiata, and Banglalink (2016–2026).*`
  - Ground Truth: The production ensemble was trained on $N = 4,500$ seed reviews (`data/processed/`), while $655,649$ is the size of the unscored/scored evaluation corpus. Conflating inference evaluation corpus size with training size is a major factual inaccuracy.
- **Paper Working Title Exposure (`demo/app.py:114`):**
  - Line 114 cites: `**Research Paper:** *“With Great Reviews Comes Great Responsibility: An Intelligent Decision Support System for Telecommunications Voice-of-the-Customer Diagnostics and Cross-Layer Subsystem Decoupling”*`
  - While paper deliverables were restructured in `paper/`, `demo/app.py` preserves the earlier, informal manuscript working title rather than the peer-reviewed submission title.

### 3.3 Demo Runtime Dependency Gaps (`demo/requirements.txt`)
- `demo/requirements.txt` specifies `gradio`, `scikit-learn`, `joblib`, `numpy`, and `scipy`.
- `demo/app.py` imports `ml.language_detector`, which imports `nltk.corpus.words` and executes `nltk.download("words")`.
- `demo/app.py` also imports `ml.predict`, which requires `pandas`.
- **Deployment Hazard:** Deploying the demo in a clean virtual environment or container installing only `demo/requirements.txt` triggers an immediate crash: `ModuleNotFoundError: No module named 'nltk'`.

### 3.4 Documentation Metric Reconciliation & Internal Inconsistency
- **Scorecard vs Ground Truth:** The `README.md:43-56` Performance Scorecard matches `scraped_data_global/classified/common_duration_summary.json` exactly:
  - Total: 655,649 reviews (GP: 320,140, Robi: 198,378, BL: 137,131).
  - Pos/Neu/Neg shares: GP (77.0% / 10.9% / 12.1%), Robi (77.9% / 10.2% / 12.0%), BL (70.4% / 12.3% / 17.3%), Industry (75.9% / 10.9% / 13.2%).
  - Net Sentiment Score (NSS): GP (+64.9%), Robi (+65.9%), BL (+53.0%), Industry (+62.7%).
- **Internal Inconsistency (`README.md:416`):**
  - Section 6.3 states: `* **Common Period NSS:** +53.1% (137,131 reviews)`.
  - Contradicts Section 1 Scorecard (`+53.0%`) and ground truth JSON (`53.04%`).
  - Cause: Residual rounding from legacy 3,716-day window ($53.05\%$).
- **Badge Ambiguity (`README.md:20`):**
  - Displays `Cohen's Kappa: κ = 0.77 (Substantial)` which represents Operational Category ($\kappa = 0.7694$), obscuring Sentiment Kappa ($\kappa = 0.5762$, Moderate).

### 3.5 `TODO.txt` Roadmap Reconciliation
- **Item 1 (Model Hub Hosting):** `scripts/upload_to_huggingface.py` exists and `dl/models/` configs are updated; Hub push remains pending.
- **Item 2 (Gold Standard Expansion):** Accurately marked `[COMPLETED]` with exact matching metrics against `gold_standard_evaluation_report.md`.
- **Item 3 (Filtered vs Unfiltered):** Ablation study and filtered models exist; line 63 contains a stale reference to `"The 398k production corpus"`.
- **Item 4 (Web Demo):** Marked open/pending despite `demo/app.py` having already been built with Gradio.
- **Item 5 (Model Calibration):** Pending; calibration plot does not exist.

### 3.6 Working-Tree Git Drift Categorization (39 Modified Files)
The 39 tracked files modified in the working tree cluster into four operational groups:
1. **Common Window Shift (2016-07-28 -> 2016-08-01, 3,716 -> 3,713 Days, 655,670 -> 655,649 Reviews):** 7 files (`README.md`, `data/README.md`, `common_duration_summary.json`, `global_multi_year_intelligence_report.md`, `merge_and_sync_all_datasets.py`, `generate_global_visualizations.py`, `audit_project_integrity.py`).
2. **Visualization Regeneration:** 30 binary PNG plots (15 in `assets/plots/`, 15 in `scraped_data_global/plots/`) re-rendered at 300 DPI reflecting the new window boundaries.
3. **Model Config Label Mappings:** 2 JSON files (`dl/models/banglabert_finetuned_{sentiment,category}/config.json`) mapped from generic labels to semantic class names for Hub publishing.
4. **Paper Path Restructuring:** 2 script files (`scripts/build_paper_empirical_excel.py`, `scripts/generate_two_panel_figure.py`) updated to reference `paper/`.

---

## 4. Verification & Proof Captured

1. `python -c "import os; assert os.path.exists('.gsd/phases/1/evidence/03_demo_application_audit.md')"`: **PASS**
2. `python -c "import os; assert os.path.exists('.gsd/phases/1/evidence/03_documentation_and_drift_audit.md')"`: **PASS**
3. `git status -s`: Tracked working tree remained 100% untouched; only `.gsd/` files written (`ADR-001`).

---

## 5. Phase 1 Completion Status

With Plan 1.3 completed:
- `1-PLAN.md`: Scraping, merging, and NSS telemetry pipeline audited.
- `2-PLAN.md`: Assets, plots, archived artifacts, and dependencies audited.
- `3-PLAN.md`: Demo app wiring, documentation scorecards, and git drift audited.
- Phase 1 core pipeline and documentation audit is now complete and ready for independent verification via `gsd-verifier`.
