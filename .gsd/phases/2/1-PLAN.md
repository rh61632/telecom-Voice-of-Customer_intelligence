---
phase: 2
plan: 1
wave: 1
depends_on: []
files_modified:
  - .gsd/phases/2/evidence/01_dl_notebooks_and_scripts_audit.md
  - .gsd/phases/2/evidence/01_banglabert_diff_and_zip_audit.md
  - .gsd/phases/2/evidence/01_dl_checkpoints_runtime_audit.md
  - .gsd/phases/2/1-SUMMARY.md
autonomous: true
user_setup: []

must_haves:
  truths:
    - "All 4 DL Jupyter notebooks are systematically compared against local dl/*.py training scripts, reports, dl/README.md, and Hugging Face card metadata"
    - "Uncommitted git diff on dl/models/banglabert_finetuned_*/config.json and exact relationship with banglabert_finetuned_models.zip are empirically verified"
    - "PyTorch .pt checkpoints, Joblib models, bilstm_vocab.joblib unpickling crash, and CLI inference with predict_dl.py are empirically tested under Python 3.15.1"
  artifacts:
    - ".gsd/phases/2/evidence/01_dl_notebooks_and_scripts_audit.md"
    - ".gsd/phases/2/evidence/01_banglabert_diff_and_zip_audit.md"
    - ".gsd/phases/2/evidence/01_dl_checkpoints_runtime_audit.md"
    - ".gsd/phases/2/1-SUMMARY.md"
  key_links:
    - "BanglaBERT label mappings in config.json link to dl/finetune_banglabert.py and downstream pipeline inference in demo/app.py"
    - "BiLSTM checkpoint architecture links to dl/train_bilstm.py and dl/telecom_voc_master_unified_colab.ipynb cell definitions"
---

# Plan 2.1: DL Scripts, Colab Notebooks, BanglaBERT/BiLSTM Checkpoints & Reports Audit

<objective>
Audit all Deep Learning artifacts across `dl/` and `archive/early_dl_experiments/` under `ADR-001` (strictly read-only on project/paper/data files; zero git commits). Compare the 4 Jupyter notebooks against local training scripts and reports, audit the uncommitted git diff on BanglaBERT `config.json` against `banglabert_finetuned_models.zip`, and empirically test deserialization and forward-pass execution of `.pt` and `.joblib` checkpoints under Python 3.15.1.
</objective>

<context>
Load for context:
- .gsd/SPEC.md
- .gsd/REQUIREMENTS.md
- .gsd/DECISIONS.md
- .gsd/phases/2/RESEARCH.md
- dl/telecom_voc_master_unified_colab.ipynb
- dl/telecom_voc_banglabert_finetuning_colab.ipynb
- dl/telecom_voc_deep_learning_colab.ipynb
- archive/early_dl_experiments/telecom_voc_comment_type_classification_colab.ipynb
- dl/finetune_banglabert.py
- dl/train_bilstm.py
- dl/train_bilstm_category.py
- dl/train_transformer.py
- dl/predict_dl.py
- dl/reports/banglabert_finetuning_report.txt
- dl/reports/results.txt
- dl/README.md
- scripts/upload_to_huggingface.py
</context>

<tasks>

<task type="auto">
  <name>Audit DL notebooks vs local scripts, report files, and documentation metrics</name>
  <files>
    .gsd/phases/2/evidence/01_dl_notebooks_and_scripts_audit.md
  </files>
  <action>
    Perform an in-depth comparative audit across all 4 Jupyter notebooks (`dl/*.ipynb` and `archive/early_dl_experiments/*.ipynb`), local training scripts (`dl/*.py`), reports (`dl/reports/*`), documentation (`dl/README.md`), and upload metadata (`scripts/upload_to_huggingface.py`).

    Steps:
    1. Parse and compare dataset scope and sample counts across all notebooks and scripts: document that while seed datasets contain `N=4,500` reviews (`2,774 Pos / 1,238 Neg / 488 Neu`; `2,731 Gen / 788 Off / 400 App / 364 Net / 217 Bill`), `dl/reports/results.txt:4-32` is stale from commit `60cf0f4` reporting `2,773 / 1,238 / 489` and targeting missing `colab_bilstm_attention.pt`.
    2. Audit `dl/telecom_voc_banglabert_finetuning_colab.ipynb`:
       - Cite lines 206-225 where `finetune_banglabert.py` printed `"across 2 operators"` because `data/processed/mygp_classified_reviews.csv` lacks an `operator` column (parsed as `NaN`).
       - Cite Cell 10 (line 905) where fine-tuned BanglaBERT misclassified the positive review `"Onk shundor app shob offer e discount pai"` as `Negative (94.7% confidence)`.
       - Cite Cell 6 output truncation and verify that 5-fold CV summary was omitted from `dl/reports/banglabert_finetuning_report.txt` (which only logged 85/15 held-out split `N=675`: Sent `89.78% / 0.8324`, Cat `87.11% / 0.8023`).
    3. Document macro-F1 and accuracy contradictions:
       - Category BanglaBERT 5-fold CV: `dl/README.md:76`, `archive/early_dl_experiments/README.md:27`, and `master_unified_colab.ipynb:1095` report `85.27% / 0.7624`, whereas `scripts/upload_to_huggingface.py:145-147` hardcodes `85.27% / 0.8032`.
       - Sentiment MiniLM: `dl/README.md:61` reports `82.33% / 0.7475` (Logistic Regression head in `master_unified_colab.ipynb`), contradicting `dl/reports/results.txt:23` (`86.00% / 0.7809` from PyTorch TransformerClassifier).
       - Sentiment BiLSTM: `dl/README.md:62` reports `81.50% / 0.7180` (hardcoded string in `master_unified_colab.ipynb:1088` where Cell 10 omitted BiLSTM CV), contradicting `dl/reports/results.txt:21` (`84.02% / 0.7525`).
       - Category Ensemble & MiniLM: `dl/README.md:75,77` reports `87.44% / 0.7845` and `81.15% / 0.7247` (from archived `category_benchmark_summary.csv`), whereas the Colab run that generated disk models scored `87.33% / 0.7791` and `80.56% / 0.7103`.
    4. Audit architecture discrepancy in `master_unified_colab.ipynb`: Cell 0 and `dl/README.md:12` advertise `Hybrid BiLSTM + Attention + Char-CNN`, but Cell 9 (lines 486-504) implements a word-only `HybridBiLSTMAttention` with no Char-CNN layers.
    5. Document script defects:
       - `dl/train_bilstm_category.py:311-312`: off-by-one padding size `len(vocab.word2idx) + 1`; missing output artifacts `bilstm_category_vocab.json` and `dl_bilstm_category_report.md`.
       - `dl/finetune_banglabert.py:322`: report file opened with `mode="a"` instead of `"w"`, causing silent accumulation across runs.
       - `archive/.../telecom_voc_comment_type_classification_colab.ipynb`: broken GitHub Colab badge (line 17), corrupted regex `r"(.)\u0001{2,}"` (line 121), and epoch-mismatch bug pairing `best_f1` with final-epoch accuracy outside training loop (lines 372-375, 482-486, 561-565).
    6. Write comprehensive audit table and analysis to `.gsd/phases/2/evidence/01_dl_notebooks_and_scripts_audit.md`.

    AVOID: Re-running Colab notebooks or mutating any files under `dl/` or `archive/`.
    USE: Read-only static analysis and AST/JSON parsing of `.ipynb` and `.py` files.
  </action>
  <verify>
    powershell -Command "if ((Select-String -Path .gsd/phases/2/evidence/01_dl_notebooks_and_scripts_audit.md -Pattern 'telecom_voc_master_unified_colab.ipynb' -Quiet) -and ((Get-Item .gsd/phases/2/evidence/01_dl_notebooks_and_scripts_audit.md).Length -gt 1000)) { exit 0 } else { exit 1 }"
  </verify>
  <done>
    Evidence document 01_dl_notebooks_and_scripts_audit.md exists with exact file:line citations for all 4 notebooks, 5 training scripts, 2 reports, and documentation contradictions.
  </done>
</task>

<task type="auto">
  <name>Audit BanglaBERT uncommitted diff, zip archive SHA256 parity, and Hugging Face metadata</name>
  <files>
    .gsd/phases/2/evidence/01_banglabert_diff_and_zip_audit.md
  </files>
  <action>
    Inspect the uncommitted git working-tree changes on BanglaBERT model directories, verify byte-level parity with `banglabert_finetuned_models.zip`, and audit the Hugging Face upload script.

    Steps:
    1. Inspect the uncommitted `git diff` on `dl/models/banglabert_finetuned_sentiment/config.json` and `dl/models/banglabert_finetuned_category/config.json` without modifying git state:
       - Record exact modifications: default Hugging Face `"LABEL_0".."LABEL_2"` and `"LABEL_0".."LABEL_4"` replaced with human-readable labels matching `SENTIMENT_LABEL_MAP` and `CATEGORY_LABEL_MAP` in `dl/finetune_banglabert.py:54-66`.
       - Document index alignment hazard: `banglabert_finetuned_category/config.json` uses custom semantic ordering (`0: General`, `1: Offers`, `2: App Login`, `3: Network`, `4: Billing`), which differs from the alphabetical order used by `dl/models/cat_le.joblib` (`0: App Login`, `1: Billing`, `2: General`, `3: Network`, `4: Offers`).
    2. Inspect `banglabert_finetuned_models.zip` (821.5 MB) using a read-only Python script (`zipfile` and `hashlib`):
       - Compare internal archive structure against `dl/models/banglabert_finetuned_{sentiment,category}/`.
       - Verify SHA256 hashes of `model.safetensors` in zip vs on disk (`b566cc09e58f...` for sentiment, `dc85d60cf99e...` for category) to prove model weights are byte-for-byte identical.
       - Verify that `tokenizer.json` and `tokenizer_config.json` differ only by CRLF vs LF line endings.
       - Document that `config.json` in the zip contains the original unpatched `LABEL_0..` mappings, confirming the zip is an unpatched pre-export archive.
    3. Audit `scripts/upload_to_huggingface.py:145-167`:
       - Document model card generation, hardcoded F1 metrics (`0.8032` cat vs `0.7624` in notebooks/reports), and the mutating side effect of writing `README.md` into model directories if executed.
    4. Compile findings into `.gsd/phases/2/evidence/01_banglabert_diff_and_zip_audit.md`.

    AVOID: Extracting or unpacking `banglabert_finetuned_models.zip` over disk files, running `scripts/upload_to_huggingface.py`, or executing any git commands.
    USE: Read-only Python zip inspection and hashlib verification.
  </action>
  <verify>
    powershell -Command "if ((Select-String -Path .gsd/phases/2/evidence/01_banglabert_diff_and_zip_audit.md -Pattern 'banglabert_finetuned_models.zip' -Quiet) -and ((Get-Item .gsd/phases/2/evidence/01_banglabert_diff_and_zip_audit.md).Length -gt 1000)) { exit 0 } else { exit 1 }"
  </verify>
  <done>
    Evidence document 01_banglabert_diff_and_zip_audit.md details exact config.json diffs, zip archive SHA256 matches, label ordering differences, and Hugging Face upload script discrepancies.
  </done>
</task>

<task type="auto">
  <name>Empirically verify PyTorch checkpoints, Joblib unpickling, and CLI inference under Python 3.15.1</name>
  <files>
    .gsd/phases/2/evidence/01_dl_checkpoints_runtime_audit.md
    .gsd/phases/2/1-SUMMARY.md
  </files>
  <action>
    Execute safe, read-only Python 3.15.1 verification of all serialized PyTorch `.pt` checkpoints, DL `.joblib` helper models, and CLI inference script `dl/predict_dl.py`.

    Steps:
    1. Write and execute a read-only Python script to test deserialization of all 4 `.pt` files using `torch.load(..., weights_only=False)`:
       - `dl/models/bilstm_attention_model.pt` (full model checkpoint with architecture and weights)
       - `dl/models/minilm_transformer_head.pt` (MLP head weights)
       - `dl/models/bilstm_sentiment_model.pt` (raw state_dict from Colab)
       - `dl/models/bilstm_category_model.pt` (raw state_dict from Colab)
       Run synthetic tensor forward passes through instantiated models to verify output tensor shapes `(1, 3)` and `(1, 5)`.
    2. Test unpickling of `dl/models/bilstm_vocab.joblib`:
       - Demonstrate and document the fatal pickling coupling error: direct `joblib.load()` crashes with `AttributeError: module '__main__' has no attribute 'Vocabulary'`, and explain why (the object was serialized from a Colab notebook `__main__` namespace).
       - Verify successful load when `class Vocabulary` is mock-defined in `__main__`.
    3. Test unpickling of `dl/models/minilm_sent_head.joblib`, `minilm_cat_head.joblib`, `sent_le.joblib`, and `cat_le.joblib`:
       - Record scikit-learn `InconsistentVersionWarning` (`1.6.1` -> `1.9.1`).
       - Verify `.predict()` on dummy embedding vectors.
    4. Test CLI inference with `dl/predict_dl.py`:
       - Execute `python dl/predict_dl.py --model bilstm --text "valo service"` and capture stdout (successful execution, ~71.5% Negative prediction).
       - Execute `python dl/predict_dl.py --model transformer --text "valo service"` and capture stderr (`ModuleNotFoundError: No module named 'transformers'`), verifying the absence of the `transformers` runtime package.
       - Note that `predict_dl.py` lacks CLI flags for `banglabert_finetuned_*` or `bilstm_{sentiment,category}_model.pt`.
    5. Write findings to `.gsd/phases/2/evidence/01_dl_checkpoints_runtime_audit.md` and synthesize the overall Plan 2.1 summary in `.gsd/phases/2/1-SUMMARY.md`.

    AVOID: Modifying any `.pt` or `.joblib` files, creating git commits, or installing new packages globally.
    USE: Read-only Python 3.15.1 execution and structured markdown reporting.
  </action>
  <verify>
    python dl/predict_dl.py --model bilstm --text "valo service"
  </verify>
  <done>
    All 4 .pt checkpoints and DL .joblib files verified under Python 3.15.1, bilstm_vocab.joblib coupling bug reproduced, predict_dl.py behavior recorded, and 1-SUMMARY.md generated.
  </done>
</task>

</tasks>

<verification>
After all tasks, verify:
- [ ] Evidence document `01_dl_notebooks_and_scripts_audit.md` documents all 4 notebooks vs local scripts, reports, and documentation
- [ ] Evidence document `01_banglabert_diff_and_zip_audit.md` documents BanglaBERT config diffs and zip SHA256 parity
- [ ] Evidence document `01_dl_checkpoints_runtime_audit.md` documents PyTorch and Joblib deserialization and predict_dl.py CLI tests
- [ ] Summary file `1-SUMMARY.md` is complete with all observed discrepancies
</verification>

<success_criteria>
- [ ] All 3 tasks verified passing
- [ ] Must-haves confirmed
- [ ] Zero project source or paper files modified outside `.gsd/`
- [ ] Zero git commits created
</success_criteria>
