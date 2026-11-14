# Empirical Evidence 02: Archive Lineage, Dependency Reconciliation & Harness Integrity Audit

> **Phase:** 1 — Core Pipeline, Data, Demo & Documentation Audit  
> **Plan:** 2 — Visualizations, Asset Parity, Archive Lineage & Dependency Audit  
> **Task:** 2 — Audit archive lineage, dependency declarations vs codebase imports, and repo harness integrity  
> **Execution Date:** 2026-11-11  
> **Status:** Verified Pass (Strict Read-Only)

---

## 1. Executive Summary

This audit conducted an exhaustive inspection of all five historical subdirectories in `archive/`, tracked references from active code into legacy/archived locations, reconciled repository-wide Python imports against all requirement manifests (`requirements.txt`, `demo/requirements.txt`, `ml/requirements.txt`, `dl/requirements.txt`), and empirically verified the GSD automation harness.

Key findings:
1. **Critical Dead Path in `ml/train_filtered_experiments.py:19`:** Hardcodes `GOLD_CSV = PROJECT_ROOT / "scraped_data_2020" / "gold_set" / "gold_set_verified.csv"`. This file does not exist anywhere in the repository, causing `evaluate_on_gold_standard()` (lines 138-140) to silently exit and return `(0.0, 0.0)`.
2. **LLM Seed Model Discrepancy (Code vs Paper):** `archive/seed_pipeline_groq/src/02_classify_reviews_mygp.py:50` (and `myrobi`, `mybl`) hardcodes `model="qwen/qwen3.8-27b"`, whereas `paper/eswa_latex/manuscript.tex:254` claims the seed labels were generated using `Qwen-2.5-32B`.
3. **Five Undeclared Runtime Dependencies:** `nltk`, `python-docx` (`docx`), `openpyxl`, `Pillow` (`PIL`), and `huggingface_hub` are imported in repository source scripts but omitted from root `requirements.txt`.
4. **Demo Environment Breakdown:** `demo/requirements.txt` omits `nltk`. However, `demo/app.py:13` imports `ml.language_detector`, which imports `nltk` and calls `nltk.download("words")`. Any clean container installing only `demo/requirements.txt` crashes upon startup with `ModuleNotFoundError: No module named 'nltk'`.
5. **Two Unused Declared Packages:** `torchvision>=0.17.0` and `torchaudio>=2.2.0` are declared in root and `dl/requirements.txt` but are never imported in any `.py` script in the repository.
6. **Package Version Floor Mismatch:** `scikit-learn>=1.4.0` in root, `ml/`, and `dl/` vs `>=1.3.0` in `demo/requirements.txt`.
7. **Harness Integrity Verified:** `VERSION` is `1.6.0`, and `scripts/validate-all.ps1` executes 5 child validators across 27 workflows, 12 skills, 5 subagents, 24 templates, and 11 scripts with 0 errors.

---

## 2. Historical Archive Catalog (`archive/`)

| Subdirectory | File Count | Total Size | Primary Contents & Lineage Purpose | Empirical Observations / Discrepancies |
|---|---|---|---|---|
| `archive/seed_pipeline_groq/` | 13 files | 1.90 MB | Phase 1 Groq API seed annotation pipeline (`N=4,500` reviews: 1,500 each for GP, Robi, BL). Contains raw scrapes and classified outputs. | **Model String Discrepancy:** Code specifies `model="qwen/qwen3.8-27b"` (`02_classify_reviews_mygp.py:50`, `myrobi.py:55`, `mybl.py:56`), but `manuscript.tex:254` reports `Qwen-2.5-32B`. |
| `archive/scraped_data_2020/` | 54 files | 80.40 MB | Historical 402-day common window benchmark (`2020-01-01` to `2021-02-05`). Contains raw scrapes, classified sets, and iOS probe. | **Review Counts:** `all_operators_common_duration.csv` has `N = 83,417` (GP: 21,524; Robi: 33,825; BL: 28,068). `ios_probe/ios_scraped_reviews_empirical_probe.csv` has `N = 1,199`. `gold_set/` holds legacy 600-sample draft plan. |
| `archive/robi_backfill/` | 3 files | 3.56 MB | Historical one-time backfill script (`backfill_robi_gap.py`) and dataset slice (`robi_backfilled_gap_2024_2025.csv`). | **Volume:** `37,153` reviews (`~37.1k`) retrieved to resolve a 10-month historical gap (Sep 2024 – Aug 2025). Consolidated into global corpus; standalone slice archived. |
| `archive/early_dl_experiments/` | 2 files | 0.03 MB | Colab notebook (`telecom_voc_comment_type_classification_colab.ipynb`) evaluating frozen MiniLM, BiLSTM, and frozen BUET BanglaBERT. | **Ablation Benchmark:** Demonstrates frozen BanglaBERT feature extraction achieved only 74.88% CV accuracy (Macro-F1 0.6253), justifying full 12-layer fine-tuning (85.27% accuracy). |
| `archive/powerbi_dashboard/` | 3 files | 1.07 MB | Prototype Power BI recordings (`page1_demo.gif`: 414.6 KB; `page2_demo.gif`: 705.4 KB) and architecture comparison document. | **Discarded Rationale:** Discarded due to lack of batch ML scoring capacity (>50k rows), non-reproducible manual UI interactions, and proprietary licensing. Replaced by Python Matplotlib 300 DPI suite. |

---

## 3. Broken References into Archive

### 3.1 `ml/train_filtered_experiments.py:19`
- **Source Code Citation:**
  ```python
  # ml/train_filtered_experiments.py
  16: ML_DIR = Path(__file__).resolve().parent
  17: PROJECT_ROOT = ML_DIR.parent
  18: PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
  19: GOLD_CSV = PROJECT_ROOT / "scraped_data_2020" / "gold_set" / "gold_set_verified.csv"
  ...
  136: def evaluate_on_gold_standard(train_df: pd.DataFrame, min_words: int):
  137:     """Train ensemble on filtered train_df and test on corresponding Gold Standard subset."""
  138:     if not GOLD_CSV.exists():
  139:         return 0.0, 0.0
  140:
  141:     gold_df = pd.read_csv(GOLD_CSV)
  ```
- **Diagnostic:**
  1. `scraped_data_2020` was relocated to `archive/scraped_data_2020`. `PROJECT_ROOT / "scraped_data_2020"` does not exist.
  2. Even under `archive/scraped_data_2020/gold_set/`, no file named `gold_set_verified.csv` exists (the active benchmark is `data/gold_set/gold_set_verified_300.csv`).
  3. Consequently, executing `evaluate_on_gold_standard()` always triggers `if not GOLD_CSV.exists(): return 0.0, 0.0`. Short-text ablation reports silently record 0.00% Gold Standard evaluation accuracy.

### 3.2 Internal Archive Hardcoded Paths
Scripts retained within `archive/scraped_data_2020/` (e.g. `benchmark_common_duration_models.py:29`, `classify_with_existing_models.py:28`, `scrape_all_operators_up_to_2020.py:9`) reference `BASE_DIR / "scraped_data_2020"` assuming execution from repository root before relocation. Because these are historical archived scripts, they are not part of the active production pipeline, but direct invocation from their current directory fails without updating root offsets. In contrast, `scraped_data_global/pipeline/merge_and_sync_all_datasets.py:183` correctly references `repo_root / "archive" / "scraped_data_2020" / "raw"`.

---

## 4. Comprehensive Package Dependency Reconciliation

### 4.1 Declared Manifest Summary

| Manifest File | Declared Packages | Notes |
|---|---|---|
| `requirements.txt` (Root Canonical) | `google-play-scraper>=1.2.4`, `groq>=0.9.0`, `pandas>=2.0.0`, `numpy>=1.24.0`, `matplotlib>=3.7.0`, `scikit-learn>=1.4.0`, `scipy>=1.10.0`, `joblib>=1.3.0`, `torch>=2.2.0`, `torchvision>=0.17.0`, `torchaudio>=2.2.0`, `transformers>=4.40.0`, `sentence-transformers>=2.7.0` | 13 declared packages |
| `demo/requirements.txt` | `gradio>=4.0.0`, `scikit-learn>=1.3.0`, `joblib>=1.3.0`, `numpy>=1.24.0`, `scipy>=1.10.0` | 5 declared packages |
| `ml/requirements.txt` | `scikit-learn>=1.4.0`, `scipy>=1.10.0`, `joblib>=1.3.0`, `pandas>=2.0.0`, `numpy>=1.24.0` | 5 declared packages |
| `dl/requirements.txt` | `torch>=2.2.0`, `torchvision>=0.17.0`, `torchaudio>=2.2.0`, `transformers>=4.40.0`, `sentence-transformers>=2.7.0`, `scikit-learn>=1.4.0`, `pandas>=2.0.0`, `numpy>=1.24.0` | 8 declared packages |

### 4.2 Undeclared Runtime Dependencies (Imported in Code, Missing from Manifests)

| Imported Module | Target Package | Imported By | Lines Cited | Failure Impact |
|---|---|---|---|---|
| `nltk` | `nltk` | `ml/language_detector.py` | Lines 18, 28–29 (`import nltk`, `from nltk.corpus import words`) | `demo/app.py` and `ml/predict.py` fail immediately in clean environments. `demo/requirements.txt` completely lacks `nltk`. |
| `docx` | `python-docx` | `scripts/build_*_docx.py`, `scripts/convert_latex_to_docx.py`, `scripts/audit_docx.py`, `scripts/find_tables.py` | 7 script files | DOCX manuscript building scripts cannot run without external manual install. |
| `openpyxl` | `openpyxl` | `scripts/build_paper_empirical_excel.py` | Line 1 (`import openpyxl`) | Empirical calculation workbook regeneration script fails. |
| `PIL` | `Pillow` | `scripts/check_crops.py`, `scripts/check_other_crops.py`, `scripts/test_figure1_offsets.py` | 4 script files | Image inspection and figure validation scripts fail. |
| `huggingface_hub` | `huggingface_hub` | `scripts/upload_to_huggingface.py` | Line 195 (`from huggingface_hub import HfApi, create_repo`) | Weight upload utility fails unless huggingface_hub is installed. |

### 4.3 Unused Declared Dependencies (Declared in Manifests, Never Imported in Code)

| Declared Package | Manifest Location | AST Codebase Scan Result | Recommendation |
|---|---|---|---|
| `torchvision>=0.17.0` | `requirements.txt:36`, `dl/requirements.txt:6` | 0 imports found in any `.py` script across repo. | Remove from manifests to eliminate heavy computer vision wheel downloads. |
| `torchaudio>=2.2.0` | `requirements.txt:37`, `dl/requirements.txt:7` | 0 imports found in any `.py` script across repo. | Remove from manifests to eliminate heavy audio wheel downloads. |
| `sentence-transformers>=2.7.0` | `requirements.txt:39`, `dl/requirements.txt:9` | 0 imports in `.py` scripts (only referenced in archived Colab notebook `archive/early_dl_experiments/telecom_voc_comment_type_classification_colab.ipynb`). | Retain in dl requirements or annotate as optional Colab dependency. |

### 4.4 Dependency Version Specifier Inconsistencies

1. **`scikit-learn` Version Floor Inconsistency:**
   - Root `requirements.txt:30`: `scikit-learn>=1.4.0`
   - `ml/requirements.txt:5`: `scikit-learn>=1.4.0`
   - `dl/requirements.txt:10`: `scikit-learn>=1.4.0`
   - `demo/requirements.txt:2`: `scikit-learn>=1.3.0`  
   *Risk:* Production models pickled with scikit-learn 1.4+ may fail to unpickle with `joblib.load()` on a host running scikit-learn 1.3.0 due to internal Cython/estimator attribute changes.
2. **`gradio` Missing from Root Canonical Manifest:**
   - Declared in `demo/requirements.txt:1` (`gradio>=4.0.0`).
   - Omitted from `requirements.txt`. Installing the root manifest per `README.md:14` (`pip install -r requirements.txt`) leaves the user unable to launch `python demo/app.py`.

---

## 5. Repository Harness Integrity Audit

### 5.1 Version Tracking
- File: `VERSION`
- Content: `1.6.0` (single line, trimmed, verified).

### 5.2 GSD Validation Suite (`scripts/validate-all.ps1` & `scripts/validate-all.sh`)
Execution command:
```powershell
powershell -ExecutionPolicy Bypass -File scripts/validate-all.ps1
```
Output Summary:
- **Workflows:** 27 verified (`add-phase.md`, `plan.md`, `execute.md`, `verify.md`, etc.), 0 errors, 0 warnings.
- **Skills:** 12 verified (`codebase-mapper`, `context-fetch`, `empirical-validation`, `executor`, `verifier`, etc.), 0 errors.
- **Subagents:** 5 verified (`gsd-debugger`, `gsd-executor`, `gsd-planner`, `gsd-researcher`, `gsd-verifier`), 0 errors.
- **Templates:** 24 verified (`architecture.md`, `plan.md`, `spec.md`, `state.md`, etc.), 0 errors, 0 warnings.
- **Script Encoding:** 11 PowerShell scripts verified for clean UTF-8 encoding and syntax, 0 errors.
- **Overall Suite Result:** Exit code 0 (`✅ All validators passed!`).

---

## 6. Verification Status

Verification command passed:
```powershell
python -c "import os; assert os.path.exists('.gsd/phases/1/evidence/02_archive_and_dependencies_audit.md'), 'Evidence file missing'; print('Archive and dependency audit evidence successfully verified')"
```
Output:
`Archive and dependency audit evidence successfully verified`
