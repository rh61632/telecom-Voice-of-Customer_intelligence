# Phase 6 Research: ML/DL Provenance, Label Alignment, Portability & Gold Benchmark Remediation

**Phase:** 6 (`REM-03`, `REM-04`)  
**Discovery Level:** 3 (Comprehensive Empirical Verification)  
**Target Discrepancies:** `DISC-CRIT-01` (benchmarks), `DISC-CRIT-07`, `DISC-MAJ-01`, `DISC-MAJ-04` (code/docs), `DISC-MAJ-05`, `DISC-MAJ-06` (reports), `DISC-MAJ-19`, `DISC-MIN-07..13`, `DISC-HYG-06..08`  
**Constraint Alignment:** [`ADR-002`](../../DECISIONS.md#L8-L13), [`ADR-003`](../../DECISIONS.md#L14-L22) (preserve `.safetensors` weights and human annotations in `data/gold_set/blind_annotation_*.csv`; no unsolicited git commits)

---

## Executive Summary

All 4 research questions were resolved empirically against live disk artifacts (`torch 2.15.0+cpu`, `scikit-learn 1.9.1`, `joblib 1.6.0`, `pandas 2.3.2`, Python `3.15.1`):

1. **BanglaBERT Weights & Label Mapping (`Q1`):** The actual `model.safetensors` weights on disk (`dl/models/banglabert_finetuned_sentiment/model.safetensors` SHA256 `b566cc09e58f3649...`, 3-class `classifier.out_proj.bias` shape `[3]`; `dl/models/banglabert_finetuned_category/model.safetensors` SHA256 `dc85d60cf99eb9f8...`, 5-class `classifier.out_proj.bias` shape `[5]`) were trained by `dl/finetune_banglabert.py:54-66,288-317` invoked from `dl/telecom_voc_banglabert_finetuning_colab.ipynb:708`. **The uncommitted working-tree `config.json` files are RIGHT** (`0..2` Sentiment, `0: General .. 4: Billing` Category). **`cat_le.joblib` is NOT wrong for BiLSTM/MiniLM** (`0: App Login .. 4: Offers` alphabetical order used by `bilstm_category_model.pt` and `minilm_cat_head.joblib`), **but MUST NEVER be used with BanglaBERT**. **`banglabert_finetuned_models.zip`** contains identical `model.safetensors` bytes (`b566cc09...`, `dc85d60c...`) paired with **stale `LABEL_0..` `config.json` files** and must be repacked. `dl/predict_dl.py` currently does not support BanglaBERT at all.
2. **BiLSTM Vocabulary & Checkpoints (`Q2`):** `dl/models/bilstm_vocab.joblib` is a pickled Colab `__main__.Vocabulary` instance (`min_freq=2`, `word2idx` len `2,864`, `idx2word` len `2,864`). Both `dl/models/bilstm_sentiment_model.pt` (`embedding.weight (2864, 128)`, `fc.3.weight (3, 64)`) and `dl/models/bilstm_category_model.pt` (`embedding.weight (2864, 128)`, `fc.3.weight (5, 64)`) are raw `OrderedDict` `state_dict`s of **1-layer word-only** `HybridBiLSTMAttention` (no Char-CNN!) from `dl/telecom_voc_master_unified_colab.ipynb:486-590`, whereas `dl/models/bilstm_attention_model.pt` is a wrapped checkpoint dict (`['model_state_dict', 'vocab_word2idx', 'vocab_char2idx', 'label_map']`, `word_vocab=2,875`, `char_vocab=302`) from `dl/train_bilstm.py:380-387`. Exporting `dl/models/bilstm_vocab.json` + using a shared `Vocabulary` class + safe `pickle.Unpickler` fallback makes `bilstm_vocab` portable without breaking `classify_global_dataset.py`, `merge_and_sync_all_datasets.py`, or any `.pt` weights. `dl/train_bilstm_category.py:311-312,344-345` has a `+1` off-by-one vocab size bug and implements `BiLSTMWithAttention` (incompatible with `bilstm_category_model.pt` on disk).
3. **Classical ML Provenance & Reports (`Q3`):** Of the 9 `.joblib` files in `ml/models/`, 7 were built locally (`sklearn 1.9.1`, `0` warnings) and 2 (`category_voting_classifier.joblib` with `34` warnings and `sentiment_voting_classifier.joblib` with `28` warnings) were imported from Google Colab (`sklearn 1.6.1`, `dl/telecom_voc_master_unified_colab.ipynb:295-410`). Neither `ml/train_category.py` nor `ml/train_ensemble.py` matches those Colab pipelines; `ml/train_filtered_experiments.py:19,138-139` silently returns `(0.0, 0.0)` due to a dead `g600` path; `ml/language_detector.py:153` silently lowers the documented `70%` threshold to `60%` (affecting `133` seed reviews); and every ML report in `ml/reports/` has stale `N=4,499`, `g600` prose/table contradictions, `2016–2026` vs `2014–2026` date drift, or `14` dropped Symbolic reviews.
4. **Gold Standard `g600` Retirement & `BLIND_106` Preservation (`Q4`):** `data/gold_set/comprehensive_benchmark_table.md:28-38` and `data/gold_set/gold_standard_evaluation_report.md:7-86,132-144` leak `g600` (`archive/scraped_data_2020/gold_set/archived_600_plan/gold_set_verified.csv`, $N=600$) verbatim, including `200/200/200` operator splits, `82.00% / 0.6781`, the $3\times 3$ confusion matrix summing to $600$, and qualitative quotes (`VOC_0035`, `VOC_0014`, `VOC_0010`) absent from active `g300`. Rebuilding strictly from `blind_annotation_300_annotator1.csv` ($N=300$; 100/100/100) and dual-human consensus ($N=182$ sentiment, $N=187$ category — noting $N=182$ contains `0` `Neutral` ground-truth rows), adding `operator="Grameenphone"` to `data/processed/mygp_classified_reviews.csv`, anonymizing `calculate_agreement.py` and markdown links, and adding a disambiguation note in `ANNOTATION_RULEBOOK.md` cleanly retires `g600` while preserving `BLIND_106` verbatim per [`ADR-003`](../../DECISIONS.md#L21).

---

## Question 1: True BanglaBERT Class Mappings (`0..4` Category, `0..2` Sentiment) & Config/Encoder Alignment

### 1.1 Proof of Exact Trained Integer Mappings in `model.safetensors`

1. **Training Script Definition (`dl/finetune_banglabert.py:54-66`):**
   - Sentiment (`lines 54-58`): `SENTIMENT_LABEL_MAP = {"Negative": 0, "Neutral": 1, "Positive": 2}`.
   - Category (`lines 60-66`): `CATEGORY_LABEL_MAP = {"General Appreciation / Other": 0, "Offers & Data Packs": 1, "App Login & Technical Bugs": 2, "Network Speed & 4G Latency": 3, "Billing & Airtime Deductions": 4}`.
   - Label encoding (`lines 196, 274`): `labels = np.array([label_map[item] for item in df[task]])`.
   - Root cause of `LABEL_0..` default (`lines 219-222, 288-291`): `AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=num_classes)` did **not** pass `id2label` or `label2id`, so `model.save_pretrained(out_dir)` (`line 316`) wrote Hugging Face defaults `"0": "LABEL_0"`, etc.
2. **Colab Execution Trace (`dl/telecom_voc_banglabert_finetuning_colab.ipynb`):**
   - Cell 4 (`line 708`) executed `!python dl/finetune_banglabert.py --task both --epochs 4 --batch_size 32 --lr 2e-5`.
   - FutureWarning lines captured in Colab stdout (`lines 264, 266, 670, 672`) match exact line numbers in local `dl/finetune_banglabert.py:232, 151, 300`, proving identical training code generated the saved checkpoints.
   - Cell 6 (`lines 922-964`) immediately loaded `dl/models/banglabert_finetuned_sentiment` and `dl/models/banglabert_finetuned_category` and mapped argmax logits using `SENT_MAP` (`line 922`) and `CAT_MAP` (`lines 923-929`, identical to `CATEGORY_LABEL_MAP`), producing accurate category predictions (`lines 895-911`): `"MB kete nilo..."` $\to$ `Network Speed & 4G Latency (84.0%)`, `"Update er por theke OTP..."` $\to$ `App Login & Technical Bugs (91.1%)`, `"Onk shundor app shob offer e discount pai"` $\to$ `Offers & Data Packs (86.4%)`.
   - Cell 6 (`line 905`) misclassified `"Onk shundor app shob offer e discount pai"` as `Negative (94.7%)` (`DISC-MIN-08`), which is a Latin-script Banglish out-of-domain failure mode (other negative reviews `"MB kete nilo..."`, `"Update er por..."`, `"4G connection..."` all predicted `Negative` at `97.4%–97.6%`), not a swapped sentiment index.
3. **Safetensors Tensor Header & Zip Parity Verification:**
   - Binary inspection of `model.safetensors` confirmed `classifier.out_proj.bias` shape `[3]` / `classifier.out_proj.weight` `[3, 768]` (`dl/models/banglabert_finetuned_sentiment/model.safetensors`) and `classifier.out_proj.bias` shape `[5]` / `classifier.out_proj.weight` `[5, 768]` (`dl/models/banglabert_finetuned_category/model.safetensors`).
   - SHA256 checksums of `model.safetensors` on disk vs inside `banglabert_finetuned_models.zip` (821,497,087 bytes, created in Colab Cell 7 `lines 1080-1095`) are **byte-for-byte identical**:
     - Sentiment: `b566cc09e58f3649` (`442,502,748` bytes).
     - Category: `dc85d60cf99eb9f8` (`442,508,900` bytes).

### 1.2 Verdict Table: What Is Right vs Wrong

| Artifact | Observed State (`file:line`) | Verdict | Exact Action Required |
|---|---|---|---|
| `dl/models/banglabert_finetuned_sentiment/config.json` | Working tree (`lines 15-27`): `0: Negative, 1: Neutral, 2: Positive` (patched from `HEAD` `LABEL_0..`) | **RIGHT** | Preserve working-tree mapping (`git diff dl/models/` shows the exact fix). |
| `dl/models/banglabert_finetuned_category/config.json` | Working tree (`lines 15-31`): `0: General, 1: Offers, 2: App Login, 3: Network, 4: Billing` (patched from `HEAD` `LABEL_0..`) | **RIGHT** | Preserve working-tree mapping. |
| `banglabert_finetuned_models.zip` | Contains identical `model.safetensors` (`b566cc09...`, `dc85d60c...`) + **pre-patch `LABEL_0..` `config.json`s** (plus LF `tokenizer.json` / `tokenizer_config.json`) | **WRONG (`DISC-HYG-06`)** | Repack `banglabert_finetuned_models.zip` from `dl/models/banglabert_finetuned_{sentiment,category}/` (including only the 4 canonical files each: `config.json`, `model.safetensors`, `tokenizer.json`, `tokenizer_config.json`, with LF line endings or current disk files — exclude any `README.md` if generated). |
| `dl/models/sent_le.joblib` | `sklearn 1.6.1` `LabelEncoder`: `['Negative', 'Neutral', 'Positive']` (`0..2`) | **RIGHT (for BiLSTM/MiniLM; matches BanglaBERT Sentiment)** | **Do not modify.** Needed intact by `classify_global_dataset.py:91,185` and `merge_and_sync_all_datasets.py:90,170`. |
| `dl/models/cat_le.joblib` | `sklearn 1.6.1` `LabelEncoder`: `['App Login & Technical Bugs', 'Billing & Airtime Deductions', 'General Appreciation / Other', 'Network Speed & 4G Latency', 'Offers & Data Packs']` (`0..4`, alphabetical) | **RIGHT for BiLSTM & MiniLM; INCOMPATIBLE with BanglaBERT (`DISC-CRIT-07`)** | **Do not modify.** `bilstm_category_model.pt` (`telecom_voc_master_unified_colab.ipynb:539,583,594`), `minilm_cat_head.joblib`, `classify_global_dataset.py:92,186`, and `merge_and_sync_all_datasets.py:91,171` depend on alphabetical order. Never pass BanglaBERT category logits through `cat_le.inverse_transform()` (corrupts 4/5 classes: only index `3` coincides). Always decode BanglaBERT via `model.config.id2label` or `CATEGORY_LABEL_MAP`. |
| `dl/finetune_banglabert.py` | Missing `id2label`/`label2id` in `from_pretrained()` (`lines 219-222,288-291`); appends only 85/15 test split (`lines 321-326`) leaving 5-fold CV unpersisted; prints `2 operators` (`line 348`) due to missing `operator` in `mygp_classified_reviews.csv` | **DEFECTIVE** | Pass `id2label={v: k for k, v in label_map.items()}, label2id=label_map` in both `from_pretrained()` calls; log 5-fold CV summary into `dl/reports/banglabert_finetuning_report.txt` (using overwrite `"w"` at run start or structured per-task sections rather than unbounded `"a"` appends); add `if "operator" not in df.columns` fallback or fix `mygp_classified_reviews.csv` (see Q4). |
| `dl/predict_dl.py` | Only handles `--model bilstm` (`bilstm_attention_model.pt`) and `--model transformer` (`minilm_transformer_head.pt`) for Sentiment; lacks BanglaBERT and Colab BiLSTM support (`lines 103-115`) | **INCOMPLETE (`DISC-MAJ-19`)** | Add CLI choices/options for BanglaBERT (`banglabert_finetuned_{sentiment,category}` reading `config.json` `id2label`) and Colab BiLSTM (`bilstm_{sentiment,category}_model.pt`), plus `ImportError` guard for `transformers` (`line 68`). |
| `scripts/upload_to_huggingface.py` | Hardcodes Category `0.8527` CV Acc paired with `0.8032` F1 (`lines 145-147,164`) instead of 5-fold CV Macro-F1 `0.7624` (`dl/README.md:76`, `banglabert_finetuned` Colab stdout `line 649`); held-out test (`N=675`) F1 is `0.8023` (`dl/reports/banglabert_finetuning_report.txt:30`) | **STALE METRICS** | Reconcile YAML/prose F1 in `scripts/upload_to_huggingface.py:147,164` to `0.7624` (5-fold CV) and note held-out test split `87.11% / 0.8023` separately if cited; keep `DISC-MIN-08` Banglish limitation documented. |

---

## Question 2: BiLSTM Checkpoints, `bilstm_vocab.joblib` Structure, Loaders & Portability Design

### 2.1 Exact On-Disk Structure of `bilstm_vocab.joblib` and All 4 `.pt` Checkpoints

Empirical inspection (`torch.load(..., map_location='cpu', weights_only=False)` and mock-unpickling `dl/models/bilstm_vocab.joblib`):

| Artifact (`dl/models/`) | Exact Disk Structure | Architecture / Producer | Vocab & Output Dimensions |
|---|---|---|---|
| `bilstm_vocab.joblib` | Pickled `__main__.Vocabulary` instance (`min_freq=2`, `word2idx` len=`2,864`, `idx2word` len=`2,864`, `'<pad>': 0`, `'<unk>': 1`) | Colab Cell 6–7 (`dl/telecom_voc_master_unified_colab.ipynb:451-471,535,592`) | `2,864` words; `transform(text, max_len=40)` (`str(text).lower().split()[:40]`, `<unk>=1`, zero-padded to 40) |
| `bilstm_sentiment_model.pt` | Raw `OrderedDict` `state_dict` (16 tensors): `embedding.weight (2864, 128)`, 1-layer BiLSTM `bilstm.*_l0` (`input=128, hidden=128`), `attention.{w,v}`, `fc.{1,3}` with `fc.3.weight (3, 64)` | Colab Cell 7 (`dl/telecom_voc_master_unified_colab.ipynb:486-504,575-578`): `HybridBiLSTMAttention` (**word-only, 1-layer, no Char-CNN**) | `vocab_size=2,864`, `num_classes=3` (decoded via `sent_le.joblib`) |
| `bilstm_category_model.pt` | Raw `OrderedDict` `state_dict` (16 tensors): `embedding.weight (2864, 128)`, 1-layer BiLSTM `bilstm.*_l0`, `attention.{w,v}`, `fc.{1,3}` with `fc.3.weight (5, 64)` | Colab Cell 7 (`dl/telecom_voc_master_unified_colab.ipynb:486-504,586-589`): `HybridBiLSTMAttention` (**word-only, 1-layer, no Char-CNN**) | `vocab_size=2,864`, `num_classes=5` (decoded via `cat_le.joblib`) |
| `bilstm_attention_model.pt` | Dict `['model_state_dict', 'vocab_word2idx', 'vocab_char2idx', 'label_map']`: `word_embedding.weight (2875, 128)`, `char_embedding.weight (302, 32)`, `char_conv.weight (64, 32, 3)`, 2-layer BiLSTM (`l0` input `192`, `l1` input `256`), `attention.{proj,query}`, `classifier.{0,3}` with `classifier.3.weight (3, 128)` | Local `dl/train_bilstm.py:173-256,368-387`: `BiLSTMWithAttention` (**Word + Char-CNN, 2-layer**) | `word_vocab=2,875`, `char_vocab=302`, `num_classes=3` (`LABEL_MAP`: Neg=0, Neu=1, Pos=2) |
| `minilm_transformer_head.pt` | Dict `['model_name', 'head_state_dict', 'label_map']` (`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`, `{'Negative': 0, 'Neutral': 1, 'Positive': 2}`) | Local `dl/train_transformer.py:78-98,234-240` | `384 -> 128 -> 64 -> 3` |

### 2.2 Loader Matrix & Architectural Mismatches

| Script | What It Loads (`file:line`) | How It Loads `Vocabulary` | Compatibility / Defect |
|---|---|---|---|
| `scraped_data_global/pipeline/classify_global_dataset.py` | `bilstm_vocab.joblib`, `sent_le.joblib`, `cat_le.joblib`, `bilstm_sentiment_model.pt`, `bilstm_category_model.pt` (`lines 90-102`) | Defines duplicate `class Vocabulary` at top level (`lines 24-34`), calls `joblib.load(dl_dir / "bilstm_vocab.joblib")` (`line 90`), uses `len(vocab.word2idx)` (`lines 95,100`) and `vocab.transform(t)` (`line 178`). | Works **only** when executed as `__main__`; crashes with `AttributeError` if `load_all_models()` is imported from another module. |
| `scraped_data_global/pipeline/merge_and_sync_all_datasets.py` | Same 5 DL artifacts (`lines 89-99`) | Duplicate `class Vocabulary` (`lines 32-42`), `joblib.load(dl_dir / "bilstm_vocab.joblib")` (`line 89`), `vocab.transform(t)` (`line 163`). | Same `__main__` pickle fragility + code duplication (`lines 32-113` duplicated verbatim from `classify_global_dataset.py:24-117`). |
| `dl/predict_dl.py` | `bilstm_attention_model.pt` (`lines 28-45`) and `minilm_transformer_head.pt` (`lines 67-81`) | Rebuilds `dl.train_bilstm.Vocabulary` from `ckpt["vocab_word2idx"]` and `ckpt["vocab_char2idx"]` (`lines 35-37`). | Does not load `bilstm_vocab.joblib` or `bilstm_{sentiment,category}_model.pt` or BanglaBERT; `load_transformer()` (`line 68`) crashes unhandled when `transformers` is not installed (`ModuleNotFoundError`). |
| `dl/train_bilstm.py` | Trains & writes `bilstm_attention_model.pt` (`lines 368-387`) | Saves `vocab_word2idx` & `vocab_char2idx` dicts directly inside `.pt` (`lines 382-383`) using `word_vocab_size=len(vocab.word2idx)` (`line 369`). | Cleanly embeds vocab dicts; matches `bilstm_attention_model.pt` on disk. |
| `dl/train_bilstm_category.py` | Trains `BiLSTMWithAttention` (Word+Char-CNN 2-layer) and writes `bilstm_category_model.pt` + `bilstm_category_vocab.json` (`lines 310-355`) | Uses `Vocabulary.to_dict()` / `from_dict()` (`lines 132-146`) and writes JSON (`lines 352-354`). | **2 Bugs (`DISC-HYG-07`):** (1) `lines 311-312, 344-345` pass `len(vocab.word2idx) + 1` and `len(vocab.char2idx) + 1`, allocating an unused extra embedding row since `0` (`<pad>`) and `1` (`<unk>`) are already inside `len()`; (2) `bilstm_category_vocab.json` does not exist on disk because `bilstm_category_model.pt` on disk came from Colab (`HybridBiLSTMAttention`), **NOT** `train_bilstm_category.py`! Re-running `train_bilstm_category.py` as-is would overwrite `dl/models/bilstm_category_model.pt` with a `BiLSTMWithAttention` dict checkpoint and **break `classify_global_dataset.py:101` & `merge_and_sync_all_datasets.py:98`**. |

### 2.3 Portable `bilstm_vocab` Design (Zero Breaking Changes)

To resolve `DISC-MAJ-19` without breaking `classify_global_dataset.py`, `merge_and_sync_all_datasets.py`, or any `.pt` weights:
1. **Export JSON Vocabulary (`dl/models/bilstm_vocab.json`):** Extract directly from `dl/models/bilstm_vocab.joblib` (with `__main__.Vocabulary` shim during one-time export) into a pure-JSON artifact:
   - Keys: `{"min_freq": 2, "max_len": 40, "word2idx": <exact 2,864-entry dict>, "idx2word": <exact 2,864-entry str-keyed dict>}`.
   - Exact length `len(word2idx) == 2864` preserves `HybridBiLSTMAttention(2864, ...)` tensor compatibility with `bilstm_sentiment_model.pt` and `bilstm_category_model.pt`.
   - **Keep `dl/models/bilstm_vocab.joblib` on disk** (or document `.joblib` as legacy Colab export superseded by `.json`) so any external legacy script running as `__main__` does not lose the file, while updating all repo loaders to prefer `bilstm_vocab.json`.
2. **Create a Shared Importable Module (e.g., `dl/bilstm_artifacts.py`):**
   - Define `Vocabulary` (with `transform(self, text, max_len=40)` matching `classify_global_dataset.py:30-33` character-for-character, plus `from_json()` / `to_dict()`), `BahdanauAttention`, and `HybridBiLSTMAttention`.
   - Provide `load_bilstm_vocab(dl_dir: Path)`: loads `dl_dir / "bilstm_vocab.json"` first; if missing, falls back to `dl_dir / "bilstm_vocab.joblib"` using a custom `pickle.Unpickler` overriding `find_class(self, module, name)` to map `("__main__", "Vocabulary") -> Vocabulary` (zero `__main__` monkey-patching required!).
   - Provide `load_label_encoder_classes(...)` or read `.joblib` encoders cleanly (still needed for `sent_le.joblib` and `cat_le.joblib`).
3. **Update All Consumers:**
   - Update `scraped_data_global/pipeline/classify_global_dataset.py:24-103` and `scraped_data_global/pipeline/merge_and_sync_all_datasets.py:32-100` to import `Vocabulary`, `HybridBiLSTMAttention`, and `load_bilstm_vocab` from `dl.bilstm_artifacts` (with `sys.path` insert for `repo_root` so running from subdirectories works). Verify identical outputs on sample strings before/after!
   - Update `dl/train_bilstm_category.py`: fix `+1` off-by-one (`lines 311-312, 344-345` $\to$ `len(vocab.word2idx)`, `len(vocab.char2idx)`), and save to a non-colliding checkpoint name (e.g. `bilstm_category_charcnn_model.pt` + `bilstm_category_charcnn_vocab.json` OR add explicit warning/CLI flag `--output`) so running `train_bilstm_category.py` does not silently overwrite the Colab `HybridBiLSTMAttention` `bilstm_category_model.pt` required by `classify_global_dataset.py`!
   - Update `dl/predict_dl.py`:
     - Guard `from transformers import ...` with `try/except ImportError` printing an actionable message (`pip install -r dl/requirements.txt`) instead of crashing with an unhandled traceback (`DISC-MAJ-19`).
     - Support `--model` choices covering `bilstm` (`bilstm_attention_model.pt`), `bilstm-colab` / `bilstm-sentiment` & `bilstm-category` (`bilstm_{sentiment,category}_model.pt` + `bilstm_vocab.json`), `transformer` (`minilm_transformer_head.pt`), and `banglabert` (`banglabert_finetuned_{sentiment,category}` using `model.config.id2label`, never `cat_le.joblib`).
   - Update `dl/README.md`:
     - Remove false `Char-CNN` / `sub-word token embeddings` claims for Colab `HybridBiLSTMAttention` (`lines 12, 62, 78`); distinguish Colab word-only `HybridBiLSTMAttention` (`bilstm_{sentiment,category}_model.pt`, `bilstm_vocab.json`) from local `dl/train_bilstm.py` Word+Char-CNN (`bilstm_attention_model.pt`).
     - Reconcile metrics (`lines 61-62, 75, 77`) clearly between Colab `telecom_voc_master_unified_colab.ipynb` outputs (Sentiment MiniLM `82.33% / 0.7475`, Sentiment BiLSTM `81.50% / 0.7180` fallback, Category Ensemble `87.33% / 0.7791`, Category MiniLM `80.56% / 0.7103`) and local/archived benchmark tables (`87.44% / 0.7845` from `N=4,499` local `train_category.py`; `86.00% / 0.7809` & `84.02% / 0.7525` in `results.txt`).
     - Fix absolute local machine URIs `file:///home/ratul/...` (`lines 12, 19, 24`) to relative links and document `bilstm_vocab.json` (`line 89`).
   - Update `dl/reports/results.txt`:
     - Replace stale commit `60cf0f4` / `2,773 / 1,238 / 489` counts (`lines 4, 11-13`) with verified live seed counts (`2,774 / 1,238 / 488`, $N=4,500$), remove references to unexecuted `dl/telecom_voc_deep_learning_colab.ipynb` and non-existent `dl/models/colab_bilstm_attention.pt` (`lines 58-59`), and reconcile `BiLSTM + Char-CNN` / MiniLM metrics to match actual on-disk artifacts (`DISC-MIN-07`).

---

## Question 3: Classical ML Training Scripts vs Deployed `.joblib` Models, Language Detector & `ml/reports/*`

### 3.1 Exact Diff Matrix: `ml/train_*.py` vs `ml/models/*.joblib`

All 9 `.joblib` files in `ml/models/` were deserialized and inspected under `scikit-learn 1.9.1`:

| `.joblib` Artifact | `sklearn` Ver / Warnings | Exact Feature & Classifier Parameters on Disk | Local Script Origin & Exact Diffs |
|---|---|---|---|
| `category_voting_classifier.joblib` *(Prod Hero)* | **1.6.1** (`34` warnings) | `FeatureUnion`: `word` `(1,2)` `min_df=2` `max_features=12000` (`4,843` terms); `char` **`analyzer='char'`** `(3,5)` **`min_df=2`** **`max_features=25000`** (`25,000` terms); Total $V=29,843$, mean `nnz=109.72`. `VotingClassifier` step `'classifier'`, `weights=[2.0, 2.5, 1.0]`: `lr(C=2.5)`, `lsvc(Calibrated(LinearSVC(C=1.0, max_iter=2000), cv=3))`, `cnb(alpha=0.5, norm=False)`. | **NOT `ml/train_category.py`!** Imported from `dl/telecom_voc_master_unified_colab.ipynb:295-410`. `ml/train_category.py:78-135` differs on **all 7 parameters**: `word max_features=None` (`4,842`), `char_wb` (`min_df=3`, `max_features=None`, `16,355`), `C=1.0`, `cv=None (5)`, `ComplementNB(norm=True, alpha=1.0)`, `weights=[2, 2, 1]`. |
| `sentiment_voting_classifier.joblib` *(Prod Global)* | **1.6.1** (`28` warnings) | Same Colab `FeatureUnion` (`4,843 + 25,000 = 29,843` features). `VotingClassifier` step `'classifier'`, `weights=[2.0, 2.5, 1.0]`: `lr(C=2.0)`, `lsvc(cv=3, max_iter=2000)`, `cnb(alpha=0.5, norm=False)`. | **NOT `ml/train_ensemble.py`!** Imported from `dl/telecom_voc_master_unified_colab.ipynb:295-331`. Used by `classify_global_dataset.py:78` & `merge_and_sync_all_datasets.py:82`. |
| `ensemble_voting_classifier.joblib` *(CLI/Demo Hero)* | `1.9.1` (`0` warnings) | Single `TfidfVectorizer(analyzer='char_wb', ngram_range=(2,5), min_df=3)` (`18,027` features); `VotingClassifier` step `'voting'`, `weights=[2, 2, 1]`, `lr(C=1.0)`, `svc(cv=None)`, `cnb(alpha=1.0, norm=True)`. | Exact match to `ml/train_ensemble.py:46-103`. Loaded by `ml/predict.py:21` and `demo/app.py:17`! *(Note runtime split: `ml/predict.py` / `demo/app.py` use `ensemble_voting_classifier.joblib`, whereas the 661k global corpus uses `sentiment_voting_classifier.joblib`!)* |
| `category_logistic_regression.joblib`, `category_linearsvc.joblib` | `1.9.1` (`0` warnings) | `FeatureUnion`: `word (1,2) min_df=2` (`4,842`) + `char_wb (3,5) min_df=3` (`16,355`) = `21,197` features; `LR(C=1.0)` / `Calibrated(LinearSVC, cv=None)`. | Exact match to `ml/train_category.py:78-125,202-213`. |
| `primary_logistic_regression.joblib`, `challenger_linearsvc.joblib` | `1.9.1` (`0` warnings) | `char_wb (2,5) min_df=3` (`18,027` features). | Exact match to `ml/train_sentiment.py:67-99,163-190`. |
| `category_ensemble_filtered_min3words.joblib`, `sentiment_ensemble_filtered_min3words.joblib` | `1.9.1` (`0` warnings) | `FeatureUnion`: `word (1,2) min_df=2` (`4,770`) + `char_wb (3,5) min_df=3` (`16,053`) = `20,823` features; `weights=[2, 2, 1]`, `LR(C=1.0)`, `cv=None`, `CNB(norm=True)`. | Exact match to `ml/train_filtered_experiments.py:50-65,157-179`. |

### 3.2 Empirical 5-Fold Stratified CV Benchmarks (`N = 4,500`, `seed=42`) vs Reports

| Script / Config | Task | Macro-F1 (Mean $\pm$ Std) | Weighted-F1 | Accuracy (Mean $\pm$ Std) | Report Claim (`file:line`) |
|---|---|---|---|---|---|
| `ml/train_category.py` (Local `Dummy`) | Cat | `0.1511 ± 0.0001` | `0.4584` | `60.69% ± 0.04%` | `category_classification_report.md:11`: `0.1511 ± 0.0000 | 0.4583 | 60.68% ± 0.03%` (`N=4,499`) |
| `ml/train_category.py` (Local `LR`) | Cat | `0.7756 ± 0.0171` | `0.8675` | `86.36% ± 1.09%` | `category_classification_report.md:12`: `0.7781 ± 0.0175 | 0.8682 | 86.44% ± 1.13%` (`N=4,499`) |
| `ml/train_category.py` (Local `LinearSVC`) | Cat | `0.7690 ± 0.0177` | `0.8681` | `87.16% ± 0.63%` | `category_classification_report.md:13`: `0.7687 ± 0.0195 | 0.8676 | 87.09% ± 1.01%` (`N=4,499`) |
| `ml/train_category.py` (Local `Ensemble`) | Cat | **`0.7892 ± 0.0166`** | **`0.8774`** | **`87.78% ± 0.65%`** | `category_classification_report.md:14` & `category_benchmark_summary.csv:2`: `0.7845 ± 0.0190 | 0.8738 | 87.44% ± 0.88%` (`N=4,499`) |
| `ml/train_category.py` (`CNB(norm=True)` alone) | Cat | `0.6304 ± 0.0148` | `0.7779` | `79.20%` | *(Manuscript Table 2 `manuscript.tex:278` overstated as `0.7418`, `DISC-MAJ-09`)* |
| **Colab Category Config** (`category_voting_classifier.joblib`) | Cat | **`0.7794 ± 0.0146`** | **`0.8717`** | **`87.33% ± 0.81%`** | Colab notebook `line 351-364` (pooled OOF): `0.7791 | 0.8717 | 87.33%` |
| **Colab `CNB(alpha=0.5, norm=False)` alone** | Cat | `0.6934 ± 0.0191` | `0.8160` | `81.47%` | *(Not in `ml/reports/`)* |
| `ml/train_sentiment.py` (`Dummy`) | Sent | `0.2542 ± 0.0001` | `0.4702` | `61.64% ± 0.04%` | `ml/README.md:38`: `0.2542 ± 0.0001 | 61.62% ± 0.05%` (`N=4,499`) |
| `ml/train_sentiment.py` (`LR`) | Sent | `0.7779 ± 0.0229` | `0.8641` | `85.87% ± 1.80%` | `ml/README.md:39`: `0.7796 ± 0.0182 | 85.96% ± 1.36%` (`N=4,499`) |
| `ml/train_sentiment.py` (`LinearSVC`) | Sent | `0.7798 ± 0.0147` | `0.8740` | `87.64% ± 0.93%` | `ml/README.md:40`: `0.7852 ± 0.0142 | 87.89% ± 0.93%` (`N=4,499`) |
| `ml/train_ensemble.py` (`ensemble_voting_classifier`) | Sent | `0.7820 ± 0.0213` | `0.8753` | `87.84% ± 1.13%` | *(Not documented in `ml/README.md`)* |
| **Colab Sentiment Config** (`sentiment_voting_classifier`) | Sent | `0.7688 ± 0.0186` | `0.8690` | `87.44% ± 1.31%` | Colab notebook `line 1072`: `0.7684 | 87.47%` |

**Additional `ml/train_category.py` & `category_classification_report.md` Defects:**
- `ml/train_category.py:247`: Prints `{m['mean_macro_f1']:.4f} ± {m['mean_macro_f1']:.4f}` instead of `{m['std_macro_f1']:.4f}` (`DISC-MIN-10`).
- `ml/reports/category_classification_report.md:5,33,37-39,53-57`: Hardcodes $N=4,499$, `General` support `2730` (live is `2,731`), full-fit metrics `0.9898 / 0.9866` (live deployed `category_voting_classifier.joblib` on $N=4,500$ achieves `0.9900` Acc / `0.9883` Macro-F1 / `0.9805` Macro-P / `0.9965` Macro-R; confusion matrix `[[2687, 15, 8, 19, 2], [1, 787, 0, 0, 0], [0, 0, 400, 0, 0], [0, 0, 0, 364, 0], [0, 0, 0, 0, 217]]`).
- **Actionable Decision for `train_category.py` / `train_ensemble.py` (`REM-04`):**
  - Align `ml/train_category.py:78-135` with the **deployed Colab `category_voting_classifier.joblib` pipeline** (`word 12k + char 25k, weights=[2.0, 2.5, 1.0], LR C=2.5, LinearSVC cv=3 max_iter=2000, CNB alpha=0.5, norm=False` + `class_weight="balanced"`), fix `line 247` (`std_macro_f1`), and preserve/inject the `Google Colab GPU Benchmark` section cleanly (matching `category_benchmark_summary.csv` and `N=4,500`!).
  - Note: Check whether `ml/train_ensemble.py` should stay targeting `ensemble_voting_classifier.joblib` (which `ml/predict.py:21` and `demo/app.py:17` load) OR also document/reproduce `sentiment_voting_classifier.joblib` — **do NOT break `ml/predict.py` / `demo/app.py`**, and document both `ensemble_voting_classifier.joblib` (local CLI/demo, `0.7820 / 87.84%`) and `sentiment_voting_classifier.joblib` (Colab global corpus, `0.7688 / 87.44%`) clearly in `ml/README.md`!
  - Fix `ml/reports/category_benchmark_summary.csv`: `line 2` (`0.784467..., 0.874413...`) is from the old `N=4,499` local run; update row 2 to live `N=4,500` (`0.7794, 0.8733` for deployed Colab Ensemble or `0.7892, 0.8778` if local, matching `category_classification_report.md`!). *(Note: Phase 8 will synchronize `manuscript.tex` Table 2 to these reconciled values under `REM-07`.)*

### 3.3 `ml/train_filtered_experiments.py` & `ml/reports/short_text_filtering_ablation_study.md`

Exact live execution comparison (`N=4,500`, `N=3,887`, `N=2,286`):

| Setting (`min_words`) | Live Seed $N$ (%) | Report `short_text_...md:12-14` | Live Cat F1 / Acc | Live Sent F1 / Acc | Leaked `g600` F1 / Acc (Matches Report!) | Active `g300` F1 / Acc ($N$) | Active Consensus F1 / Acc ($N$) |
|---|---|---|---|---|---|---|---|
| Full (`1`) | `4,500` (`100.0%`) | `4,499` (`100.0%`) | `0.7892` / `87.78%` | `0.7914` / `88.22%` | `0.6737` / `80.17%` ($N=600$) | `0.5571` / `82.00%` ($N=300$) | `0.4725` / `85.71%` ($N=182$) |
| Filtered (`3`) | `3,887` (`86.4%`) | `3,886` (`86.4%`) | `0.7803` / `85.95%` | `0.7822` / `87.37%` | `0.7318` / `77.54%` ($N=187$) | `0.5632` / `67.65%` ($N=68$) | `0.4727` / `66.67%` ($N=33$) |
| Aggressive (`5`) | `2,286` (`50.8%`) | `2,285` (`50.8%`) | `0.7498` / `80.05%` | `0.7825` / `84.78%` | `0.6989` / `70.94%` ($N=117$) | `0.7556` / `82.05%` ($N=39$) | `0.9488` / `95.00%` ($N=20$) |

**Exact Deficiencies Found:**
1. `ml/train_filtered_experiments.py:19`: Dead `GOLD_CSV` (`scraped_data_2020/gold_set/gold_set_verified.csv`) + `lines 138-139` silent `return 0.0, 0.0` + `lines 152-153` `gold_sentiment` column (`DISC-MAJ-01`). Fix to `PROJECT_ROOT / "data" / "gold_set" / "blind_annotation_300_annotator1.csv"`, raise `FileNotFoundError` if missing, and evaluate against `sentiment_label`.
2. `ml/train_filtered_experiments.py:204-213` & `ml/reports/short_text_filtering_ablation_study.md:18-27`: Prose hardcodes stale `g600` char-only numbers (`0.6781 -> 0.7436`, `+6.55% to +7.80%`) and stale per-class `N=4,499` metrics (`Billing 64.82% -> 67.38%`, `App Login 74.45% -> 76.26%`, `Offers 0.8309 -> 0.8326`), whereas live OOF `N=4,500 -> N=3,887` (`get_ensemble_pipeline()`) yields `Billing` Precision `64.08% -> 66.15%`, `App Login` Precision `75.24% -> 76.77%`, `Offers` F1 `0.8403 -> 0.8331`. Both script and report must compute and format real live numbers dynamically (`DISC-MIN-11`).
3. `ml/reports/short_text_filtering_ablation_study.md:19,37`: Fix malformed `(≥ 3$ words)` to `($\ge 3$ words)`. (Also note in the report why `min_words >= 3` on `g300` reduces $N$ from `300` to `68` because 77.3% of `g300` reviews are 1–2 words!)

### 3.4 `ml/language_detector.py`, `global_language_distribution.md` & `linguistic_subcohort_report.md`

1. **`ml/language_detector.py:6,86,147-156` (`DISC-MIN-12`):**
   - `dominance_threshold` is initialized to `0.70` (`line 86`), citing Gambäck & Das (2016) ($\ge 70\%$ dominance, `line 6`), **but `line 153` executes `elif english_ratio >= 0.60: lang = "English"`** whenever `banglish_matches == 0`, while `line 147` (`banglish_ratio >= 0.15`) is redundant before `line 151` (`elif banglish_matches > 0:`).
   - **Empirical Impact on `N=4,500`:** Exactly **`133`** reviews have `banglish_matches == 0` and `0.60 <= english_ratio < 0.70` (examples: `'Veary High price'`, `'I LOVE MYGP❤️‍🩹'`, `'low rate plz'`, `'too much expesive'`).
   - **Two Valid Remediation Options (Pick One Explicitly in Plan):**
     - *Option A (Enforce Strict 70% Threshold):* Remove `lines 153-154` (and simplify `lines 147-156` to `if banglish_matches > 0: ... elif english_ratio >= self.dominance_threshold: ... else: Romanized Banglish`), then **re-run** `scripts/evaluate_linguistic_subcohorts.py` and `scripts/compute_global_language_distribution.py` so `ml/reports/*` and `data/processed/all_operators_classified_with_language.csv` match (and note downstream `paper/eswa_latex/manuscript.tex:334-367` Table 4 / counts will update in Phase 8).
     - *Option B (Preserve Existing `3,005 / 509,887` Partitions & Document Heuristic):* Keep the `0.60` typo-tolerance fallback for zero-Banglish Latin text and update `ml/language_detector.py:6,86,146-156` docstrings/comments to explicitly document the `0.70` CMI primary criterion + `0.60` zero-Banglish typo-tolerance fallback (eliminating redundant `line 147`). *(Note: `DISCREPANCY_REPORT.md:360` explicitly permits either: "Align implementation with Gambäck & Das 70% threshold or update documentation.")*
2. **`ml/reports/global_language_distribution.md:3` & `scripts/compute_global_language_distribution.py:116` (`DISC-MIN-13`):**
   - Both write `(2016–2026)`, whereas `ml/reports/global_language_distribution.json:90-152` and `all_operators_classified_global.csv` cover **2014–2026** (`183` reviews in 2014, `910` in 2015, `2,119` in 2016). Fix both script line 116 and markdown line 3 to `(2014–2026)` (plus add a year breakdown summary or clarify full corpus `2014–2026`).
3. **`scripts/evaluate_linguistic_subcohorts.py` & `ml/reports/linguistic_subcohort_report.md` (`DISC-MAJ-06`):**
   - `evaluate_linguistic_subcohorts.py:156` / `linguistic_subcohort_report.md:5`: Fix `$N = 4,499$` $\to$ `$N = 4,500$`.
   - `evaluate_linguistic_subcohorts.py:104-109`: Add `("Symbolic / Emoticons", df[df["language"] == "Symbolic / Emoticons"])` to `cohorts` so rows sum to `4,500` (`1,091 + 390 + 3,005 + 14 = 4,500`; on `N=14` Symbolic reviews, existing `all_operators_classified_with_language.csv` shows `Cat Acc(CV)=100.0%`, `Sent Acc(CV)=92.86%`, `Cat Acc(Fit)=100.0%`, noting single-class/small-$N$ support).
   - `evaluate_linguistic_subcohorts.py:81`: Sentiment CV currently loops over `cv.split(X, y_cat)` instead of `cv.split(X, y_sent)`. Split `cv.split(X, y_sent)` into a separate loop for `sent_oof` so sentiment folds are properly stratified!
4. **`ml/README.md`:**
   - `line 23`: `(~10.9%)` $\to$ `(10.84%, 488/4,500)`.
   - `lines 38-40`: Update `N=4,499` metrics (`0.2542 / 61.62%`, `0.7796 / 85.96%`, `0.7852 / 87.89%`) to live `N=4,500` (`0.2542 ± 0.0001 / 61.64% ± 0.04%`, `0.7779 ± 0.0229 / 85.87% ± 1.80%`, `0.7798 ± 0.0147 / 87.64% ± 0.93%`) and add `train_ensemble.py` (`0.7820 ± 0.0213 / 87.84% ± 1.13%`), `train_category.py`, `train_filtered_experiments.py`, and note Colab vs local models.

---

## Question 4: Retiring `g600` Leakage & Preserving Human Annotations (`BLIND_106`)

### 4.1 Ground Truth Schema & Active Gold Cohorts

1. **`data/processed/mygp_classified_reviews.csv` (`DISC-MIN-09`):**
   - Currently has 8 columns: `['user_name', 'rating', 'review_date', 'review_text', 'thumbs_up', 'category', 'sentiment', 'english_summary']` (`1,500` rows, `0` nulls).
   - Both `mybl_classified_reviews.csv` and `myrobi_classified_reviews.csv` have 9 columns with `operator` at column index 5 (between `thumbs_up` and `category`).
   - **Exact Edit:** Insert column `operator` = `"Grameenphone"` at column index 5 (`1,500` rows) without altering any existing text, rating, date, or labels.
2. **Active Gold Files (Immutable per [`ADR-003`](../../DECISIONS.md#L21)):**
   - `data/gold_set/blind_annotation_300_annotator1.csv`: `300` rows (`100` GP, `100` BL, `100` Robi), `0` nulls in `sentiment_label` (`258 Pos / 23 Neg / 19 Neu`) and `category_label` (`268 Gen / 13 Off / 9 Bill / 5 App / 5 Net`).
   - `data/gold_set/blind_annotation_200_annotator2.csv`: `200` rows (`67` GP, `67` BL, `66` Robi), `0` nulls in `sentiment_label` (`184 Pos / 16 Neg / 0 Neu`), **`4` nulls in `category_label`** (`BLIND_004`, `BLIND_051`, `BLIND_042`, `BLIND_495`), leaving `196` valid category pairs.
   - **Verified Inter-Annotator Agreement:** Sentiment ($N=200$): `91.00%` (`182/200`), $\kappa = 0.5762$ (`GP: 89.55% / 0.6921`, `BL: 94.03% / 0.4846`, `Robi: 89.39% / 0.3400`). Category ($N=196$): `95.41%` (`187/196`), $\kappa = 0.7694$.
   - **Consensus Subsets:**
     - Sentiment Consensus ($N=182$): **`169 Positive, 13 Negative, 0 Neutral`** (because Annotator 2 assigned `0` `Neutral` labels across all 200 rows — `gold_standard_evaluation_report.md:112-116`). **Crucial statistical consequence:** Any model predicting $\ge 1$ `Neutral` on $N=182$ receives $F_1(\text{Neutral}) = 0.0$, depressing 3-class Macro-F1; therefore BOTH 3-class Macro-F1 and 2-class Macro-F1 (Neg, Pos) + Raw Accuracy + Weighted-F1 should be reported!
     - Category Consensus ($N=187$): `171 Gen / 8 Off / 4 Bill / 2 Net / 2 App`.

### 4.2 Verified Active Benchmarks Replacing `g600`

All models evaluated directly on active `g300` ($N=300$) and consensus ($N=182$ / $N=187$) — zero `g600` leakage:

| Task & Model | `g300` ($N=300$) Acc / Macro-F1 / Wtd-F1 / $\kappa$ | Consensus ($N=182$ Sent / $N=187$ Cat) Acc / Macro-F1 (3-cls or 5-cls) / 2-cls F1 / $\kappa$ |
|---|---|---|
| **Sent:** `ensemble_voting_classifier.joblib` *(Local CLI/Demo)* | `89.00%` / `0.6089` / `0.8820` / `0.5150` | `91.21%` / `0.4589` *(2-cls: `0.6884`)* / `0.3253` |
| **Sent:** `sentiment_voting_classifier.joblib` *(Colab Global Prod)* | `83.67%` / `0.5625` / `0.8638` / `0.4670` | `87.91%` / `0.4769` *(2-cls: `0.7153`)* / `0.4031` |
| **Sent:** `challenger_linearsvc.joblib` | `89.00%` / `0.6330` / `0.8862` / `0.5366` | `91.21%` / `0.4519` / `0.3233` *(Note: `README.md:379` claims `92.31%` — verify against `sentiment_linearsvc` or typo!)* |
| **Sent:** `primary_logistic_regression.joblib` | `82.67%` / `0.5836` / `0.8577` / `0.4624` | `85.71%` / `0.4560` / `0.3569` |
| **Sent:** `bilstm_attention_model.pt` *(Word+Char-CNN)* | `79.67%` / `0.5790` / `0.8409` | `80.77%` / `0.4624` |
| **Sent:** `bilstm_sentiment_model.pt` *(Colab Word-only)* | `78.67%` / `0.5364` / `0.8297` | `80.22%` / `0.4232` |
| **Sent:** Star-Rating Heuristic (`1-2★=Neg, 3★=Neu, 4-5★=Pos`) | `86.67%` / `0.5438` / `0.8539` / `0.4244` | `92.86%` / `0.5282` / `0.5593` |
| **Cat:** `category_voting_classifier.joblib` *(Colab Prod)* | `91.33%` / `0.4919` / `0.9098` / `0.5046` | `94.12%` / `0.5166` / `0.5403` |
| **Cat:** `category_linearsvc.joblib` | `91.00%` / `0.4904` / `0.9051` / `0.4679` | `94.12%` / `0.5166` / `0.5403` |
| **Cat:** `category_logistic_regression.joblib` | `89.33%` / `0.4760` / `0.8985` / `0.4385` | `92.51%` / `0.5181` / `0.5077` |
| **Cat:** `bilstm_category_model.pt` *(Colab Word-only)* | `91.33%` / `0.5154` / `0.9132` | `94.12%` / `0.6153` |

*Per-Operator on Active `g300` ($N=100$ each):*
- **Grameenphone ($N=100$):** `ensemble_voting` `82.0% (0.540)` | `sentiment_voting` `78.0% (0.561)` | `SVC` `82.0% (0.610)` | `LR` `76.0% (0.544)` | `BiLSTM_att` `73.0% (0.558)` | `BiLSTM_col` `73.0% (0.518)`.
- **Robi ($N=100$):** `ensemble_voting` `91.0% (0.608)` | `sentiment_voting` `86.0% (0.475)` | `SVC` `91.0% (0.608)` | `LR` `86.0% (0.584)` | `BiLSTM_att` `84.0% (0.532)` | `BiLSTM_col` `83.0% (0.511)`.
- **Banglalink ($N=100$):** `ensemble_voting` `94.0% (0.709)` | `sentiment_voting` `87.0% (0.641)` | `SVC` `94.0% (0.709)` | `LR` `86.0% (0.634)` | `BiLSTM_att` `82.0% (0.635)` | `BiLSTM_col` `80.0% (0.603)`.

*Active Rogan-Gladen Parameters (Negative vs Non-Negative on `g300`, $N=300$):*
- `ensemble_voting_classifier`: `TP=12, FN=11, TN=270, FP=7` $\implies$ **`Se = 0.5217, Sp = 0.9747`**.
- `sentiment_voting_classifier`: `TP=11, FN=12, TN=269, FP=8` $\implies$ **`Se = 0.4783, Sp = 0.9711`**.
- (Contrast leaked `g600`: `Se = 54/76 = 0.711` from `pred_ensemble` + `Sp = 494/524 = 0.942` from `pred_bilstm`!)

*Active `g300` Qualitative Case Studies (Replacing Leaked `g600` Quotes `VOC_0035`, `VOC_0014`, `VOC_0010` — note `"লোট পাটের জন্য সেরা রে"` and `"ভালো"` (1★) do not exist in `g300`!):*
- 5★ Negative / Rating Mismatch (`g300`): `BLIND_085` (5★, GP, `"মাই জিপি অ্যাপসে ঢুকতে পারতেছি না 😂😂"`, Human `Negative`, Ensemble `Positive` / Colab `Neutral`) or `BLIND_098` / `BLIND_314`; `BLIND_111` (5★, GP, `"khali tk besi 🫠"`, Human `Negative`, both models `Negative`).
- 1★ Positive (`g300`): `BLIND_238` (1★, BL, `"Mashallah, very beautiful."`, Human `Positive`, both models `Positive`); `BLIND_173`, `BLIND_188`, `BLIND_254`.
- Banglish Contraction (`g300`): `BLIND_325` (5★, BL, `"nc app"`, Human `Positive`).

### 4.3 Exact Edits Needed Across Every Target File (Question 4 Checklist)

1. **`data/processed/mygp_classified_reviews.csv` (`DISC-MIN-09`):**
   - Insert `operator="Grameenphone"` at column index 5 so schema matches `mybl_classified_reviews.csv` and `myrobi_classified_reviews.csv` (`9` columns, `1,500` rows, `0` nulls).
2. **`data/gold_set/calculate_agreement.py` (`DISC-HYG-08`):**
   - Anonymize docstring (`line 3`), candidate lists (`lines 35, 37, 43, 45` — drop `_ratul`/`_friend` or map solely to `blind_annotation_300_annotator1.csv` / `blind_annotation_200_annotator2.csv`), variable names (`ratul_*`/`friend_*` $\to$ `ann1_*`/`ann2_*`), and all stdout prints (`lines 73-78, 111-112, 139, 143, 154, 188`) to `"Annotator 1"` and `"Annotator 2"`.
   - Enhance script to also print the per-operator breakdown (`GP 67, BL 67, Robi 66`) so `comprehensive_benchmark_table.md` and `gold_standard_evaluation_report.md` tables are 100% programmatically reproduced.
3. **`data/gold_set/comprehensive_benchmark_table.md` (`DISC-CRIT-01`):**
   - Keep Section 1 (Inter-Annotator Agreement: `91.00% / 0.5762`, `95.41% / 0.7694`, per-operator `0.6921 / 0.4846 / 0.3400`).
   - Completely replace Section 2 (`lines 26-37`, leaked `g600` `82.00% / 0.6781`, etc.) with active `g300` ($N=300$) + Consensus ($N=182$ / $N=187$) benchmark tables for **both** Sentiment and Category models (and BiLSTM/Star-Rating baselines from §4.2 above), clearly distinguishing `ensemble_voting_classifier` vs `sentiment_voting_classifier` and explaining the 0-Neutral artifact in $N=182$.
   - Fix Section 3 (`lines 42-43`): `Primary Annotator (Ratul)` / `blind_annotation_300_ratul.csv` $\to$ `Primary Annotator (Annotator 1)` / [`blind_annotation_300_annotator1.csv`](blind_annotation_300_annotator1.csv); `Secondary Annotator (Friend)` / `blind_annotation_200_friend.csv` $\to$ `Secondary Annotator (Annotator 2)` / [`blind_annotation_200_annotator2.csv`](blind_annotation_200_annotator2.csv).
4. **`data/gold_set/gold_standard_evaluation_report.md` (`DISC-CRIT-01`, `DISC-HYG-08`):**
   - Header (`lines 4-8`): Remove `200 reviews per operator` and `50% Consensus / 30% Disagreements / 20% Low-Confidence` (`g600` metadata); replace with `100 reviews per operator` (random stratified draw from common window Aug 2025 – Sep 2026 with zero seed overlap), anonymized `Annotator 1` ($N=300$) and `Annotator 2` ($N=200$).
   - Line 14: Fix links (`blind_annotation_300_annotator1.csv`, `blind_annotation_200_annotator2.csv`), fix broken relative path `archived_600_plan/README.md` $\to$ `../../archive/scraped_data_2020/gold_set/archived_600_plan/README.md` (and explicitly clarify that early `g600` prototype numbers were retired in favor of active $N=300$ / $N=200$).
   - Sections 1–3 (`lines 16-59`): Retire ALL `g600` tables, `200/200/200` breakdown, and $600$-row confusion matrix; replace with verified $N=300$ (`100/100/100`) Sentiment & Category tables, $3\times 3$ confusion matrix on $N=300$ (`[[12,3,8],[5,5,9],[2,6,250]]` for `ensemble_voting_classifier` and `[[11,12,0],[8,7,4],[0,25,233]]` for `sentiment_voting_classifier`), consensus ($N=182$ / $N=187$), and active Rogan-Gladen sensitivity/specificity (`Se=0.5217, Sp=0.9747` / `Se=0.4783, Sp=0.9711`).
   - Section 4 (`lines 62-86`): Replace the three leaked `g600` quotes (`লোট পাটের জন্য সেরা রে`, `ভালো` 1★, `nc app 🫠`) with verified `g300` examples (`BLIND_085` 5★ Negative, `BLIND_238` 1★ `"Mashallah, very beautiful."`, `BLIND_325` `"nc app"`).
   - Section 5 (`lines 89-129`): Replace `Ratul` / `Friend` / `_ratul` / `_friend` (`lines 91, 110, 113-115, 120-128`) with `Annotator 1` / `Annotator 2` and `Ann1_*`; also document the `[BLIND_106]` boundary case (`"Good but price is some high"`: `Ann1: Negative / Billing & Airtime Deductions` vs `Ann2: Positive / General Appreciation / Other`).
   - Section 6 (`lines 132-144`): Retire `82.00% / 0.6781` (`line 137`) and `"stress-test set composed of hard disagreements"` (`line 141`), replace with active $N=300$ / consensus figures, and fix missing opening `$` on `κ = 0.5762$` and `κ = 0.7694$` (`line 139` $\to$ `$\kappa = 0.5762$` and `$\kappa = 0.7694$`).
5. **`data/gold_set/ANNOTATION_RULEBOOK.md` (`DISC-HYG-08` while preserving `BLIND_106`):**
   - **Do NOT edit `blind_annotation_300_annotator1.csv` or `blind_annotation_200_annotator2.csv`** (`ADR-003`).
   - In Section 2 (`lines 104-110`) and Cheat Sheet (`line 122`), add an explicit **Edge-Case Disambiguation Note (`[BLIND_106]` / `[BLIND_111]`):** clarify that explicit data-pack/tariff pricing complaints (*"MB package dam beshi"*) map to `Offers & Data Packs`, whereas generic uncontextualized cost complaints (*"Good but price is some high"*, `[BLIND_106]`; *"khali tk besi"*, `[BLIND_111]`) sit on the `Billing & Airtime Deductions` vs `Offers & Data Packs` boundary and historical blind annotations in `blind_annotation_*.csv` are preserved verbatim without post-hoc modification.
6. **`data/README.md` (`DISC-HYG-08`):**
   - `lines 23-24`: Replace `blind_annotation_300_ratul.csv` and `blind_annotation_200_friend.csv` with `blind_annotation_300_annotator1.csv` and `blind_annotation_200_annotator2.csv`.
   - `line 25`: Fix broken math `κ = 0.7694$` $\to$ `Sentiment $\kappa = 0.5762$, Category $\kappa = 0.7694$`.
   - *(Note: also check if `README.md:381` from Phase 5 needs a 1-line fix: `Naive Star-Rating Baseline` currently lists `80.17% | 84.62% | 0.4102` from `g600` instead of active `g300` `86.67% | 92.86% | 0.4244`, and `README.md:379` lists `92.31%` vs `91.21%` for `challenger_linearsvc` on $N=182$. Recommend fixing in Phase 6 or Phase 7! Also check `archive/scraped_data_2020/gold_set/archived_600_plan/README.md` if archival note wording should be left untouched or have `../blind_annotation_*_annotator*.csv` links noted.)*

---

## Unknowns & Cross-Phase Boundaries

- **BanglaBERT Live Inference Locally:** `transformers` and `safetensors` Python packages are not installed in the local Python `3.15.1` environment (`{'torch': True, 'transformers': False, 'safetensors': False}`), so full local forward passes of `csebuetnlp/banglabert` cannot run locally without installing `dl/requirements.txt` (`SPEC.md` Non-Goal: avoid installing cloud-only packages globally unless needed). Integer class order was nevertheless proven 100% from the exact training script lines matching Colab FutureWarnings, Colab Cell 6 inference stdout, tensor shapes, and SHA256 zip parity.
- **Manuscript/Paper & Statistical Test Script Edits Deferred:** `paper/eswa_latex/*`, `paper/telecommunications_policy_latex/*`, `scripts/build_paper_empirical_excel.py`, and `scripts/compute_statistical_tests.py` belong to Phases 7–9 (`REM-05`..`REM-08`) and were not modified.
