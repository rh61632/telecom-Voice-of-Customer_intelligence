# Phase 6 Plan 1: Deep Learning Checkpoints, Portability & Documentation Remediation Summary

**Phase:** 6  
**Plan:** 1-PLAN.md  
**Status:** complete  
**Execution Mode:** `inherit` workspace, zero git commits (`ADR-003`)  
**Timestamp:** 2026-11-11  

---

## 1. Executive Summary

Plan 6.1 remediated deep learning model packaging, provenance, and loader portability without modifying or overwriting deployed model weights (`.safetensors`, `.pt`) or label encoders (`.joblib`):
1. **BanglaBERT Packaging**: Repacked `banglabert_finetuned_models.zip` from working-tree models so bundled `config.json` files contain the explicit class label order (`0: Negative .. 2: Positive` and `0: General Appreciation / Other .. 4: Billing & Airtime Deductions`) while preserving byte-for-byte identical `model.safetensors` SHA256 hashes (`b566cc09...` for Sentiment, `dc85d60c...` for Category).
2. **Fine-Tuning Script & Hugging Face Hub Card**: Updated `dl/finetune_banglabert.py` with explicit `id2label`/`label2id` constructor arguments, operator presence fallback handling in `load_dataset()`, and structured 5-fold CV logging to `dl/reports/banglabert_finetuning_report.txt`. Reconciled `scripts/upload_to_huggingface.py` Category 5-fold CV Macro-F1 from `0.8032` to the true empirical `0.7624`, documented the held-out test split ($N=675$: `87.11%` Accuracy / `0.8023` Macro-F1), and added the Latin-script Banglish out-of-domain limitation note (`DISC-MIN-08`).
3. **BiLSTM Portability & Pipeline Loaders**: Eliminated the pickled `__main__.Vocabulary` fragility by exporting `dl/models/bilstm_vocab.json` (2,864 tokens, `min_freq=2`, `max_len=40`) and implementing `dl/bilstm_artifacts.py` (`Vocabulary`, `BahdanauAttention`, `HybridBiLSTMAttention`, `load_bilstm_vocab`). Updated `scraped_data_global/pipeline/classify_global_dataset.py` and `merge_and_sync_all_datasets.py` to import from `dl.bilstm_artifacts`.
4. **Local Category Training & Collision Prevention**: In `dl/train_bilstm_category.py`, eliminated the `+1` off-by-one vocabulary bug (`word_vocab_size` and `char_vocab_size`) and redirected default checkpoint exports to `dl/models/bilstm_category_charcnn_model.pt` with a warning, preventing inadvertent clobbering of the deployed Colab word-only `HybridBiLSTMAttention` checkpoint.
5. **Unified Inference CLI & Documentation Reconciliation**: Updated `dl/predict_dl.py` to support all 6 model choices (`bilstm`, `transformer`, `bilstm-colab-sentiment`, `bilstm-colab-category`, `banglabert-sentiment`, `banglabert-category`) with an `ImportError` guard when `transformers` is unavailable. Reconciled `dl/README.md` and `dl/reports/results.txt` to remove stale commit references, reflect live $N=4,500$ seed counts (`2,774 / 1,238 / 488`), and distinguish word-only from Char-CNN architectures.

---

## 2. Tasks Completed & Empirical Evidence

### Task 1: Repack banglabert_finetuned_models.zip and align dl/finetune_banglabert.py & upload_to_huggingface.py
- **Files Modified:**
  - `banglabert_finetuned_models.zip`
  - `dl/finetune_banglabert.py`
  - `scripts/upload_to_huggingface.py`
- **Actions Taken:**
  - Repacked `banglabert_finetuned_models.zip` containing verified `config.json` files and exact SHA256 `model.safetensors` files:
    - Sentiment: `b566cc09e58f3649437763caa58586914792951af6fb651b1f6f50c1c02daa30`
    - Category: `dc85d60cf99eb9f832a8df23cffcfa81b9ce94f0c44110d542dc13ea59616054`
  - In `dl/finetune_banglabert.py`:
    - Updated `load_dataset()` with per-file fallback operator logic (`Grameenphone`, `Robi`, `Banglalink`) to prevent missing operator column issues.
    - Added `id2label` and `label2id` mappings to `AutoModelForSequenceClassification.from_pretrained(...)` in both `run_cv_experiment` and `train_production_checkpoint`.
    - Added structured 5-fold CV report logging to `dl/reports/banglabert_finetuning_report.txt`.
  - In `scripts/upload_to_huggingface.py`:
    - Reconciled Category 5-fold CV Macro-F1 to `0.7624` (lines 147 and 164) and documented the held-out test split results (`87.11%` Accuracy / `0.8023` Macro-F1).
    - Added out-of-domain limitation notes regarding Romanized Banglish (`DISC-MIN-08`).
- **Verification Command:**
  ```powershell
  python -c "import zipfile, json, hashlib; z=zipfile.ZipFile('banglabert_finetuned_models.zip'); c_cat=json.loads(z.read('banglabert_finetuned_category/config.json')); c_sent=json.loads(z.read('banglabert_finetuned_sentiment/config.json')); assert c_cat['id2label']['0'] == 'General Appreciation / Other', 'Category 0 mismatch'; assert c_cat['id2label']['4'] == 'Billing & Airtime Deductions', 'Category 4 mismatch'; assert c_sent['id2label']['0'] == 'Negative', 'Sentiment 0 mismatch'; h_sent=hashlib.sha256(z.read('banglabert_finetuned_sentiment/model.safetensors')).hexdigest(); h_cat=hashlib.sha256(z.read('banglabert_finetuned_category/model.safetensors')).hexdigest(); assert h_sent.startswith('b566cc09'), f'Sent hash mismatch: {h_sent}'; assert h_cat.startswith('dc85d60c'), f'Cat hash mismatch: {h_cat}'; print('✓ Zip repack and config verification passed!')"
  ```
- **Output:** `✓ Zip repack and config verification passed!`

---

### Task 2: Create shared dl/bilstm_artifacts.py, export bilstm_vocab.json, and update pipeline loaders
- **Files Created / Modified:**
  - `dl/models/bilstm_vocab.json` (Created)
  - `dl/bilstm_artifacts.py` (Created)
  - `scraped_data_global/pipeline/classify_global_dataset.py` (Modified)
  - `scraped_data_global/pipeline/merge_and_sync_all_datasets.py` (Modified)
  - `dl/train_bilstm_category.py` (Modified)
- **Actions Taken:**
  - Exported `dl/models/bilstm_vocab.json` containing 2,864 tokens with `min_freq: 2`, `max_len: 40`, `word2idx`, and `idx2word` mappings.
  - Authored `dl/bilstm_artifacts.py` defining `Vocabulary`, `BahdanauAttention`, `HybridBiLSTMAttention`, and `load_bilstm_vocab()` with seamless fallback to legacy `.joblib` via an unpickler shim.
  - Replaced duplicate inlined definitions in `scraped_data_global/pipeline/classify_global_dataset.py` and `merge_and_sync_all_datasets.py` with imports from `dl.bilstm_artifacts`.
  - In `dl/train_bilstm_category.py`, fixed `len(vocab.word2idx) + 1` and `len(vocab.char2idx) + 1` off-by-one index sizing, redirected default model save path to `dl/models/bilstm_category_charcnn_model.pt`, and added CLI arguments `--output_model` and `--output_vocab`.
- **Verification Command:**
  ```powershell
  python -c "import sys, torch; from pathlib import Path; sys.path.insert(0, '.'); from dl.bilstm_artifacts import load_bilstm_vocab, HybridBiLSTMAttention; import joblib; dl_dir = Path('dl/models'); vocab = load_bilstm_vocab(dl_dir); assert len(vocab.word2idx) == 2864, f'Vocab size: {len(vocab.word2idx)}'; cat_le = joblib.load(dl_dir / 'cat_le.joblib'); model = HybridBiLSTMAttention(len(vocab.word2idx), len(cat_le.classes_)); model.load_state_dict(torch.load(dl_dir / 'bilstm_category_model.pt', map_location='cpu')); model.eval(); x = torch.tensor([vocab.transform('net slow problem')]); out = model(x); assert out.shape == (1, 5), f'Unexpected shape: {out.shape}'; print('✓ bilstm_artifacts and bilstm_vocab.json verification passed!')"
  ```
- **Output:** `✓ bilstm_artifacts and bilstm_vocab.json verification passed!`

---

### Task 3: Enhance dl/predict_dl.py with multi-architecture CLI and reconcile DL docs & results.txt
- **Files Modified:**
  - `dl/predict_dl.py`
  - `dl/README.md`
  - `dl/reports/results.txt`
- **Actions Taken:**
  - Rewrote `dl/predict_dl.py` to support 6 distinct architectures:
    - `--model bilstm` (Local Word + Char-CNN BiLSTM)
    - `--model transformer` (Local MiniLM head)
    - `--model bilstm-colab-sentiment` (Colab word-only BiLSTM sentiment)
    - `--model bilstm-colab-category` (Colab word-only BiLSTM category)
    - `--model banglabert-sentiment` (BUET BanglaBERT fine-tuned sentiment)
    - `--model banglabert-category` (BUET BanglaBERT fine-tuned category)
  - Added clean `ImportError` guards providing clear instructions when optional heavy packages (e.g. `transformers`) are absent.
  - Reconciled `dl/README.md`:
    - Replaced absolute `file:///home/ratul/...` URLs with relative links.
    - Removed false Char-CNN / sub-word claims for the Colab 1-layer word-only `HybridBiLSTMAttention` checkpoints.
    - Reconciled metrics across leaderboards and added the `DISC-MIN-08` out-of-domain Banglish limitation note.
    - Documented `dl/models/bilstm_vocab.json` and portability architecture.
  - Reconciled `dl/reports/results.txt`:
    - Removed stale commit `60cf0f4` and non-existent `colab_bilstm_attention.pt` path.
    - Updated class counts to verified live ground truth: Positive 2,774, Negative 1,238, Neutral 488 ($N = 4,500$).
    - Clarified architecture distinctions (`DISC-MIN-07`).
- **Verification Command:**
  ```powershell
  python dl/predict_dl.py --model bilstm-colab-category -t "net kub slow 4g pai na"
  ```
- **Output:**
  ```text
  =================================================================
  Model Architecture : Colab Word-Only Hybrid BiLSTM + Attention (Operational Category)
  Target Task        : Operational Category
  Input Review       : net kub slow 4g pai na
  Predicted Class    : Network Speed & 4G Latency
  Confidence         : 99.85%
  Class Probabilities:
    - App Login & Technical Bugs      :   0.00%
    - Billing & Airtime Deductions    :   0.00%
    - General Appreciation / Other    :   0.12%
    - Network Speed & 4G Latency      :  99.85%
    - Offers & Data Packs             :   0.02%
  =================================================================
  ```

---

## 3. Discrepancy Invariants & Must-Haves Verification

| Invariant / Metric | Expected | Observed | Status |
| :--- | :--- | :--- | :--- |
| `banglabert_finetuned_sentiment` weights SHA256 | `b566cc09e58f3649...` | `b566cc09e58f3649...` | ✅ Pass (Exact match) |
| `banglabert_finetuned_category` weights SHA256 | `dc85d60cf99eb9f8...` | `dc85d60cf99eb9f8...` | ✅ Pass (Exact match) |
| Zip `config.json` category class 0 | `General Appreciation / Other` | `General Appreciation / Other` | ✅ Pass (Exact match) |
| Zip `config.json` category class 4 | `Billing & Airtime Deductions` | `Billing & Airtime Deductions` | ✅ Pass (Exact match) |
| `bilstm_vocab.json` size & min_freq | 2,864 tokens, min_freq=2 | 2,864 tokens, min_freq=2 | ✅ Pass (Exact match) |
| `bilstm_artifacts.py` unpickler-free load | Shape `(1, 5)` tensor | Shape `(1, 5)` tensor | ✅ Pass (Exact match) |
| `train_bilstm_category.py` vocab indexing | Zero `+ 1` off-by-one | Removed | ✅ Pass (Exact match) |
| `train_bilstm_category.py` output path | `bilstm_category_charcnn_model.pt` | `bilstm_category_charcnn_model.pt` | ✅ Pass (Non-colliding) |
| `results.txt` ground truth class distribution | 2,774 / 1,238 / 488 ($N=4,500$) | 2,774 / 1,238 / 488 ($N=4,500$) | ✅ Pass (Empirically verified) |
| `dl/README.md` absolute paths | Zero `file:///home/ratul` links | 0 remaining | ✅ Pass (Clean relative links) |
| ADR-003 Commit Constraint | Zero git commits created | 0 commits | ✅ Pass |

---

## 4. Remediation Diffs Summary

- `banglabert_finetuned_models.zip`: Repacked with verified `config.json` mappings and bit-identical safetensors weights.
- `dl/finetune_banglabert.py`: Added `id2label`/`label2id` model parameters, per-operator fallback in dataset loading, and structured 5-fold CV logging.
- `scripts/upload_to_huggingface.py`: Aligned Category CV F1 to `0.7624`, test split to `0.8023`, and added Banglish limitation notes.
- `dl/models/bilstm_vocab.json`: Portable JSON vocabulary containing 2,864 words.
- `dl/bilstm_artifacts.py`: Centralized neural components and unpickler-free loader.
- `scraped_data_global/pipeline/classify_global_dataset.py`: Switched to `dl.bilstm_artifacts`.
- `scraped_data_global/pipeline/merge_and_sync_all_datasets.py`: Switched to `dl.bilstm_artifacts`.
- `dl/train_bilstm_category.py`: Fixed vocab off-by-one bug and decoupled checkpoint export path.
- `dl/predict_dl.py`: Multi-architecture inference CLI with `ImportError` guards.
- `dl/README.md`: Reconciled architecture descriptions, metrics, relative URLs, and Banglish limitations.
- `dl/reports/results.txt`: Synced class distribution counts and architecture context.
