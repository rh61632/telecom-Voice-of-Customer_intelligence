# Plan 2.1 Summary: Deep Learning Notebooks, Training Scripts, Checkpoints, and Runtime Audit

**Plan:** `2/1-PLAN.md`  
**Phase:** 2 — ML/DL Models, Gold Standard & Empirical Audit Scripts  
**Timestamp:** 2026-11-11  
**Execution Mode:** Strictly Read-Only under [`ADR-001`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/.gsd/DECISIONS.md) & [`ADR-002`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/.gsd/DECISIONS.md)  
**Git Commits:** None (`ADR-001` prohibits git commits / project file mutations)

---

## 1. Executive Summary

Plan 2.1 completed a comprehensive, read-only empirical audit across all Deep Learning assets in `dl/` and `archive/early_dl_experiments/`. The audit systematically verified 4 Jupyter notebooks against 5 local Python training/inference scripts, 2 benchmark report files, documentation (`dl/README.md`), and the Hugging Face model upload script (`scripts/upload_to_huggingface.py`).

In addition, the uncommitted git working-tree diff on fine-tuned BanglaBERT `config.json` was analyzed, byte-level and SHA256 parity with `banglabert_finetuned_models.zip` was verified, and all serialized PyTorch `.pt` checkpoints, Joblib models, pickling bugs, and CLI inference routines were empirically tested under Python 3.15.1.

All 3 tasks defined in `2/1-PLAN.md` completed with passing verification commands. Zero project source, model, notebook, or data files outside `.gsd/` were modified.

---

## 2. Key Findings & Discrepancies Cataloged

### 2.1 Dataset Scope and Class Distribution Contradictions
- **Ground Truth Counts ($N=4,500$):** Active processed reviews across all three operators (`data/processed/my{gp,bl,robi}_classified_reviews.csv`) total $N=4,500$ (2,774 Positive / 1,238 Negative / 488 Neutral; 2,731 General / 788 Offers / 400 App / 364 Network / 217 Billing).
- **Stale Report File ([`dl/reports/results.txt`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/reports/results.txt)):** Cites commit `60cf0f4` reporting $2,773 / 1,238 / 489$, claims generation by `dl/telecom_voc_deep_learning_colab.ipynb` (which is unexecuted on disk), and points to missing checkpoint `dl/models/colab_bilstm_attention.pt`.

### 2.2 BanglaBERT Colab Defects and Metric Divergence
- **Missing `operator` Column in MyGP:** In [`dl/telecom_voc_banglabert_finetuning_colab.ipynb:225`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/telecom_voc_banglabert_finetuning_colab.ipynb#L225), `finetune_banglabert.py` printed `"Loaded ground-truth dataset: 4,500 reviews across 2 operators."` because `mygp_classified_reviews.csv` lacks the `operator` column (`NaN`).
- **Live Misclassification:** In Cell 10 ([`line 905`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/telecom_voc_banglabert_finetuning_colab.ipynb#L905)), fine-tuned BanglaBERT misclassified the positive review `"Onk shundor app shob offer e discount pai"` as `Negative (94.7% confidence)`.
- **Category 5-Fold CV F1 Discrepancy:**
  - `dl/README.md:76`, `master_unified_colab.ipynb:1095`, and `early_dl_experiments/README.md:27` report **`85.27% CV Accuracy / 0.7624 Macro-F1`**.
  - [`scripts/upload_to_huggingface.py:145-147,164`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/scripts/upload_to_huggingface.py#L145-L147) hardcodes **`85.27% Accuracy / 0.8032 Macro-F1`**, combining the 5-fold CV accuracy with the single 85/15 held-out test split F1 score (`0.8023` in `banglabert_finetuning_report.txt:30`).
- **Omitted 5-Fold CV Persistence:** [`dl/finetune_banglabert.py:321-326`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/finetune_banglabert.py#L321-L326) opens `dl/reports/banglabert_finetuning_report.txt` in `"a"` mode and only writes the 85/15 held-out test split ($N=675$), leaving 5-fold CV results entirely absent from disk reports.

### 2.3 Other Metric Contradictions
- **Sentiment MiniLM:** [`dl/README.md:61`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/README.md#L61) reports `82.33% / 0.7475` (scikit-learn `LogisticRegression` in `master_unified_colab.ipynb:1051`), contradicting [`dl/reports/results.txt:23`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/reports/results.txt#L23) (`86.00% / 0.7809` from PyTorch `TransformerClassifier`).
- **Sentiment BiLSTM:** [`dl/README.md:62`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/README.md#L62) reports `81.50% / 0.7180` (hardcoded fallback in `master_unified_colab.ipynb:1088`), contradicting [`dl/reports/results.txt:21`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/reports/results.txt#L21) (`84.02% / 0.7525`).
- **Category Ensemble & MiniLM:** [`dl/README.md:75,77`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/README.md#L75) reports `87.44% / 0.7845` and `81.15% / 0.7247` (from archived `category_benchmark_summary.csv`), while the Colab run that produced the committed disk models scored `87.33% / 0.7791` and `80.56% / 0.7103`.

### 2.4 Architecture Advertising vs Implementation Discrepancy
- Documentation in [`dl/README.md:12,62`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/README.md#L12) and [`dl/telecom_voc_master_unified_colab.ipynb:24`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/telecom_voc_master_unified_colab.ipynb#L24) advertises `Hybrid BiLSTM + Attention + Char-CNN`.
- In reality, Cell 9 ([`master_unified_colab.ipynb:486-504`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/telecom_voc_master_unified_colab.ipynb#L486-L504)) implements a **word-only** `HybridBiLSTMAttention` with zero Char-CNN logic.

### 2.5 BanglaBERT Uncommitted Diff & Zip Parity
- **Uncommitted Diff:** On November 8, 2026, `config.json` was modified in both model directories to map anonymous Hugging Face tags (`LABEL_0..`) to human-readable strings.
- **Label Index Alignment Hazard:** BanglaBERT `config.json` uses non-alphabetical indexing (`0: General`, `1: Offers`, `2: App Login`, `3: Network`, `4: Billing`), which conflicts directly with the alphabetical indexing in [`dl/models/cat_le.joblib`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/models/cat_le.joblib) (`0: App Login`, `1: Billing`, `2: General`, `3: Network`, `4: Offers`).
- **Zip Parity:** SHA256 verification proved `model.safetensors` inside `banglabert_finetuned_models.zip` is byte-for-byte identical to the files on disk (`b566cc09e58f...` sentiment, `dc85d60cf99e...` category). The zip archive contains the unpatched `LABEL_0` configuration files.

### 2.6 Serialized Checkpoints & Runtime Compatibility
- **PyTorch Checkpoints:** Deserialization of all 4 `.pt` files succeeded with dummy forward passes producing expected tensor shapes: `bilstm_attention_model.pt` -> `(1, 3)`, `minilm_transformer_head.pt` -> `(1, 3)`, `bilstm_sentiment_model.pt` -> `(1, 3)`, and `bilstm_category_model.pt` -> `(1, 5)`.
- **Fatal Pickle Coupling:** Direct `joblib.load("dl/models/bilstm_vocab.joblib")` crashes with `AttributeError: module '__main__' has no attribute 'Vocabulary'`, because the object was pickled from Colab's interactive `__main__` namespace.
- **Scikit-Learn Version Warnings:** `minilm_sent_head.joblib`, `minilm_cat_head.joblib`, `sent_le.joblib`, and `cat_le.joblib` raise `InconsistentVersionWarning` (pickled with `1.6.1`, loaded under `1.9.1`).
- **CLI Inference:**
  - `python dl/predict_dl.py --model bilstm --text "valo service"` succeeded with exit code 0 (74.48% Positive).
  - `python dl/predict_dl.py --model transformer --text "valo service"` failed with exit code 1 (`ModuleNotFoundError: No module named 'transformers'`).
  - `predict_dl.py` lacks CLI flags for BanglaBERT and the Colab BiLSTM checkpoints.

---

## 3. Tasks Completed

| Task | Name | Verification Output | Status |
|---|---|---|:---:|
| 1 | Audit DL notebooks vs local scripts, report files, and documentation metrics | Verified `.gsd/phases/2/evidence/01_dl_notebooks_and_scripts_audit.md` (Length > 1000, contains notebook name, exit code 0) | **PASS** |
| 2 | Audit BanglaBERT uncommitted diff, zip archive SHA256 parity, and Hugging Face metadata | Verified `.gsd/phases/2/evidence/01_banglabert_diff_and_zip_audit.md` (Length > 1000, contains zip archive name, exit code 0) | **PASS** |
| 3 | Empirically verify PyTorch checkpoints, Joblib unpickling, and CLI inference under Python 3.15.1 | Executed `python dl/predict_dl.py --model bilstm --text "valo service"` (exit code 0, Positive 74.48%); generated `.gsd/phases/2/evidence/01_dl_checkpoints_runtime_audit.md` and `1-SUMMARY.md` | **PASS** |

---

## 4. Artifacts Produced

1. [`.gsd/phases/2/evidence/01_dl_notebooks_and_scripts_audit.md`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/.gsd/phases/2/evidence/01_dl_notebooks_and_scripts_audit.md): Systematic comparative audit table and line-by-line citations across all 4 notebooks, 5 training scripts, 2 reports, and documentation.
2. [`.gsd/phases/2/evidence/01_banglabert_diff_and_zip_audit.md`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/.gsd/phases/2/evidence/01_banglabert_diff_and_zip_audit.md): Complete analysis of the working-tree git diff on `config.json`, SHA256 parity proofs for `banglabert_finetuned_models.zip`, label index alignment hazard with `cat_le.joblib`, and Hugging Face upload script defects.
3. [`.gsd/phases/2/evidence/01_dl_checkpoints_runtime_audit.md`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/.gsd/phases/2/evidence/01_dl_checkpoints_runtime_audit.md): Empirical Python 3.15.1 verification of PyTorch `.pt` models, reproduction of the fatal `bilstm_vocab.joblib` pickle coupling crash, scikit-learn version warnings, and CLI inference runs.
4. [`.gsd/phases/2/1-SUMMARY.md`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/.gsd/phases/2/1-SUMMARY.md): This summary document.

---

## 5. Compliance with Project Decisions

- **`ADR-001` (Read-Only & No-Git-Commit):** Confirmed. No files outside `.gsd/` were modified. No git commits or staging operations were executed.
- **`ADR-002` (Sequential `inherit` Workspace):** Confirmed. Execution occurred in the main repository workspace with full visibility into the true disk and git working tree state.
