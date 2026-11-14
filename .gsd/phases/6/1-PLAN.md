---
phase: 6
plan: 1
wave: 1
depends_on: []
files_modified:
  - banglabert_finetuned_models.zip
  - dl/finetune_banglabert.py
  - scripts/upload_to_huggingface.py
  - dl/bilstm_artifacts.py
  - dl/models/bilstm_vocab.json
  - scraped_data_global/pipeline/classify_global_dataset.py
  - scraped_data_global/pipeline/merge_and_sync_all_datasets.py
  - dl/train_bilstm_category.py
  - dl/predict_dl.py
  - dl/README.md
  - dl/reports/results.txt
autonomous: true
gap_closure: false

must_haves:
  truths:
    - "Working-tree BanglaBERT config.json files and label encoders remain intact with true trained integer class order matching model.safetensors"
    - "banglabert_finetuned_models.zip contains identical model.safetensors bytes paired with verified working-tree config.json files"
    - "dl/finetune_banglabert.py passes explicit id2label and label2id, logs structured 5-fold CV results, and includes operator presence fallback"
    - "dl/bilstm_artifacts.py and dl/models/bilstm_vocab.json provide clean, portable unpickler-free loading with exact tensor compatibility"
    - "classify_global_dataset.py and merge_and_sync_all_datasets.py produce bit-for-bit identical predictions using shared bilstm_artifacts"
    - "dl/train_bilstm_category.py fixes the +1 off-by-one bug and saves to a non-colliding checkpoint preventing clobbering of Colab HybridBiLSTMAttention"
    - "dl/predict_dl.py supports all DL architectures with an ImportError guard for transformers, and DL documentation accurately separates Word-only from Char-CNN models"
  artifacts:
    - "dl/models/bilstm_vocab.json with exactly 2,864 vocabulary words and min_freq=2"
    - "dl/bilstm_artifacts.py defining Vocabulary, BahdanauAttention, HybridBiLSTMAttention, and load_bilstm_vocab"
    - "banglabert_finetuned_models.zip containing verified config.json files and byte-identical model.safetensors weights"
---

# Plan 6.1: Deep Learning Checkpoints, Portability & Documentation Remediation

## Objective
Remediate deep learning model packaging, provenance, and loader portability: repack `banglabert_finetuned_models.zip` so its `config.json` files match the working-tree integer mapping (`0: Negative, 1: Neutral, 2: Positive` and `0: General Appreciation / Other .. 4: Billing & Airtime Deductions`) without mutating `.safetensors` weights or `cat_le.joblib`; eliminate the pickled `__main__.Vocabulary` fragility by exporting `dl/models/bilstm_vocab.json` and a shared `dl/bilstm_artifacts.py` module for `classify_global_dataset.py` and `merge_and_sync_all_datasets.py`; fix `dl/train_bilstm_category.py`'s `+1` off-by-one bug and checkpoint collision; add unified CLI inference and `ImportError` guarding in `dl/predict_dl.py`; and reconcile DL documentation and reports (`dl/README.md`, `dl/reports/results.txt`, `scripts/upload_to_huggingface.py`).

## Context
Load these files for context:
- `.gsd/SPEC.md`
- `.gsd/REQUIREMENTS.md` (`REM-03`)
- `.gsd/DECISIONS.md` (`ADR-002`, `ADR-003`)
- `.gsd/phases/6/RESEARCH.md`
- `dl/finetune_banglabert.py`
- `dl/train_bilstm_category.py`
- `dl/predict_dl.py`
- `scraped_data_global/pipeline/classify_global_dataset.py`
- `scraped_data_global/pipeline/merge_and_sync_all_datasets.py`

## Tasks

<task type="auto">
  <name>Repack banglabert_finetuned_models.zip and align dl/finetune_banglabert.py & upload_to_huggingface.py</name>
  <files>
    banglabert_finetuned_models.zip
    dl/finetune_banglabert.py
    scripts/upload_to_huggingface.py
  </files>
  <action>
    1. Repack `banglabert_finetuned_models.zip` at repo root:
       - Keep working-tree `dl/models/banglabert_finetuned_{sentiment,category}/config.json` intact (they already map `0..2` sentiment and `0..4` category correctly; do NOT revert them to HEAD's `LABEL_0..`).
       - Keep `dl/models/sent_le.joblib` and `dl/models/cat_le.joblib` intact (they are required by BiLSTM/MiniLM).
       - Pack `banglabert_finetuned_models.zip` from `dl/models/banglabert_finetuned_sentiment` and `dl/models/banglabert_finetuned_category`. Include exactly 4 files per model: `config.json`, `model.safetensors`, `tokenizer.json`, and `tokenizer_config.json`.
       - Verify that `model.safetensors` in the newly packed zip has identical SHA256 checksums to disk (`b566cc09...` for sentiment and `dc85d60c...` for category) and that the bundled `config.json` files contain the explicit class label mappings (`Negative/Neutral/Positive` and `General Appreciation / Other` .. `Billing & Airtime Deductions`).
    2. Update `dl/finetune_banglabert.py`:
       - In `run_cv_experiment` and `train_production_checkpoint` (lines 219-222 and 288-291), pass `id2label={v: k for k, v in label_map.items()}` and `label2id=label_map` to `AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=num_classes, id2label=id2label, label2id=label2id)` so saved checkpoints never emit default `LABEL_0..`.
       - In `load_dataset()`: add an operator presence check so if `operator` column is missing in any input file (e.g. `mygp_classified_reviews.csv`), assign fallback operator based on filename (`Grameenphone`, `Robi`, or `Banglalink`) before concatenating, preventing `NaN` in `df["operator"]`.
       - In `run_cv_experiment`: log structured 5-fold CV results (per-fold macro-F1, accuracy, and overall mean ± std) to `dl/reports/banglabert_finetuning_report.txt` (opening with `"w"` at start of run or task section, preventing unconstrained appending).
    3. Update `scripts/upload_to_huggingface.py`:
       - Reconcile Category F1 from `0.8032` to `0.7624` (lines 147 and 164) matching the true 5-fold CV Macro-F1 (`dl/README.md:76` and Colab output `line 649`).
       - Explicitly document that held-out test split ($N=675$) achieves `87.11%` Accuracy / `0.8023` Macro-F1.
       - Retain and highlight the Latin-script Banglish out-of-domain limitation note (`DISC-MIN-08`).

    AVOID: Reverting `dl/models/banglabert_finetuned_{sentiment,category}/config.json` to git HEAD (`LABEL_0..`).
    AVOID: Changing `cat_le.joblib` (alphabetical order is required by BiLSTM and MiniLM).
    USE: Exact byte preservation of `model.safetensors` in zip archive.
  </action>
  <verify>
    python -c "import zipfile, json, hashlib; z=zipfile.ZipFile('banglabert_finetuned_models.zip'); c_cat=json.loads(z.read('banglabert_finetuned_category/config.json')); c_sent=json.loads(z.read('banglabert_finetuned_sentiment/config.json')); assert c_cat['id2label']['0'] == 'General Appreciation / Other', 'Category 0 mismatch'; assert c_cat['id2label']['4'] == 'Billing & Airtime Deductions', 'Category 4 mismatch'; assert c_sent['id2label']['0'] == 'Negative', 'Sentiment 0 mismatch'; h_sent=hashlib.sha256(z.read('banglabert_finetuned_sentiment/model.safetensors')).hexdigest(); h_cat=hashlib.sha256(z.read('banglabert_finetuned_category/model.safetensors')).hexdigest(); assert h_sent.startswith('b566cc09'), f'Sent hash mismatch: {h_sent}'; assert h_cat.startswith('dc85d60c'), f'Cat hash mismatch: {h_cat}'; print('✓ Zip repack and config verification passed!')"
  </verify>
  <done>
    banglabert_finetuned_models.zip contains valid config.json label mappings and byte-for-byte identical model.safetensors weights; dl/finetune_banglabert.py has id2label/label2id parameters and operator fallback; upload_to_huggingface.py reports 0.7624 5-fold CV F1.
  </done>
</task>

<task type="auto">
  <name>Create shared dl/bilstm_artifacts.py, export bilstm_vocab.json, and update pipeline loaders</name>
  <files>
    dl/bilstm_artifacts.py
    dl/models/bilstm_vocab.json
    scraped_data_global/pipeline/classify_global_dataset.py
    scraped_data_global/pipeline/merge_and_sync_all_datasets.py
    dl/train_bilstm_category.py
  </files>
  <action>
    1. Export `dl/models/bilstm_vocab.json`:
       - Deserialize `dl/models/bilstm_vocab.joblib` using an unpickler shim that maps `__main__.Vocabulary` to a minimal class with `word2idx` and `idx2word`.
       - Write `dl/models/bilstm_vocab.json` with keys `min_freq: 2`, `max_len: 40`, `word2idx` (2,864 items), and `idx2word` (2,864 items with string integer keys).
       - Ensure `dl/models/bilstm_vocab.joblib` remains on disk for backward compatibility.
    2. Create `dl/bilstm_artifacts.py`:
       - Define `Vocabulary`:
         - `__init__(self, min_freq=2, word2idx=None, idx2word=None)`
         - `transform(self, text, max_len=40)`: produces identical token sequence `[self.word2idx.get(w, 1) for w in str(text).lower().split()[:max_len]] + [0] * (max_len - len(seq))`
         - `from_json(cls, json_path)` and `to_dict(self)`
       - Define `BahdanauAttention(nn.Module)`: matches `classify_global_dataset.py:36-45`
       - Define `HybridBiLSTMAttention(nn.Module)`: matches `classify_global_dataset.py:48-73` (1-layer word-only BiLSTM + attention + FC layers)
       - Define `load_bilstm_vocab(dl_dir: Path)`:
         - Checks for `bilstm_vocab.json` first. If present, returns `Vocabulary.from_json(json_path)`.
         - If JSON missing, falls back to `bilstm_vocab.joblib` using a custom `pickle.Unpickler` that overrides `find_class(module, name)` to map `("__main__", "Vocabulary") -> Vocabulary`.
    3. Update `scraped_data_global/pipeline/classify_global_dataset.py` and `scraped_data_global/pipeline/merge_and_sync_all_datasets.py`:
       - Replace inlined `class Vocabulary`, `BahdanauAttention`, and `HybridBiLSTMAttention` with imports from `dl.bilstm_artifacts` (using `sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))` so `dl` is importable).
       - Replace direct `joblib.load(dl_dir / "bilstm_vocab.joblib")` with `load_bilstm_vocab(dl_dir)`.
       - Test that BiLSTM outputs on test inputs produce bit-identical probabilities before and after the change.
    4. Update `dl/train_bilstm_category.py`:
       - Fix the `+1` off-by-one bug in lines 311-312 and 344-345: change `len(vocab.word2idx) + 1` to `len(vocab.word2idx)` and `len(vocab.char2idx) + 1` to `len(vocab.char2idx)`.
       - Change output checkpoint name default from `bilstm_category_model.pt` to `bilstm_category_charcnn_model.pt` (and vocab to `bilstm_category_charcnn_vocab.json`), and add an explicit docstring / CLI argument `--output_model` with a warning that `dl/models/bilstm_category_model.pt` is the deployed word-only Colab `HybridBiLSTMAttention` model and must not be overwritten.

    AVOID: Overwriting `dl/models/bilstm_category_model.pt` or `dl/models/bilstm_sentiment_model.pt`.
    AVOID: Modifying `sent_le.joblib` or `cat_le.joblib`.
    USE: Safe custom unpickler fallback for legacy `.joblib` files.
  </action>
  <verify>
    python -c "import sys, torch; from pathlib import Path; sys.path.insert(0, '.'); from dl.bilstm_artifacts import load_bilstm_vocab, HybridBiLSTMAttention; import joblib; dl_dir = Path('dl/models'); vocab = load_bilstm_vocab(dl_dir); assert len(vocab.word2idx) == 2864, f'Vocab size: {len(vocab.word2idx)}'; cat_le = joblib.load(dl_dir / 'cat_le.joblib'); model = HybridBiLSTMAttention(len(vocab.word2idx), len(cat_le.classes_)); model.load_state_dict(torch.load(dl_dir / 'bilstm_category_model.pt', map_location='cpu')); model.eval(); x = torch.tensor([vocab.transform('net slow problem')]); out = model(x); assert out.shape == (1, 5), f'Unexpected shape: {out.shape}'; print('✓ bilstm_artifacts and bilstm_vocab.json verification passed!')"
  </verify>
  <done>
    dl/models/bilstm_vocab.json exists with 2,864 words; dl/bilstm_artifacts.py exports Vocabulary and model classes; classify_global_dataset.py and merge_and_sync_all_datasets.py import from bilstm_artifacts; dl/train_bilstm_category.py has +1 off-by-one fixed and non-colliding default output.
  </done>
</task>

<task type="auto">
  <name>Enhance dl/predict_dl.py with multi-architecture CLI and reconcile DL docs & results.txt</name>
  <files>
    dl/predict_dl.py
    dl/README.md
    dl/reports/results.txt
  </files>
  <action>
    1. Update `dl/predict_dl.py`:
       - Add `try / except ImportError` around `transformers` imports in `load_transformer()` and any BanglaBERT loader with an informative error message directing the user to `pip install -r dl/requirements.txt` or to select `--model bilstm` / `--model bilstm-colab`.
       - Support `--model` options:
         - `bilstm` (local Word+Char-CNN `bilstm_attention_model.pt`)
         - `transformer` (local MiniLM head `minilm_transformer_head.pt`)
         - `bilstm-colab-sentiment` (Colab word-only `bilstm_sentiment_model.pt` + `bilstm_vocab.json` + `sent_le.joblib`)
         - `bilstm-colab-category` (Colab word-only `bilstm_category_model.pt` + `bilstm_vocab.json` + `cat_le.joblib`)
         - `banglabert-sentiment` (loads `dl/models/banglabert_finetuned_sentiment` using its `config.json` `id2label`)
         - `banglabert-category` (loads `dl/models/banglabert_finetuned_category` using its `config.json` `id2label`, NEVER `cat_le.joblib`)
       - Add `--task` argument or unified dispatch so predicting sentiment or category is straightforward.
    2. Reconcile `dl/README.md`:
       - Remove false Char-CNN / sub-word claims for the Colab `HybridBiLSTMAttention` models (`lines 12, 62, 78`). Clearly distinguish the 1-layer word-only `HybridBiLSTMAttention` (Colab `bilstm_{sentiment,category}_model.pt`) from the local Word+Char-CNN `BiLSTMWithAttention` (`dl/train_bilstm.py`).
       - Reconcile metrics: Colab outputs (Sentiment MiniLM `82.33% / 0.7475`, Sentiment BiLSTM `81.50% / 0.7180`, Category Ensemble `87.33% / 0.7791`, Category MiniLM `80.56% / 0.7103`, BanglaBERT Sentiment `88.40% / 0.8173`, BanglaBERT Category `85.27% / 0.7624` 5-fold CV and `87.11% / 0.8023` test).
       - Replace absolute local URIs `file:///home/ratul/...` (lines 12, 19, 24) with clean relative links.
       - Document `dl/models/bilstm_vocab.json` and portability architecture.
       - Document the BanglaBERT Latin-script Banglish out-of-domain limitation (`DISC-MIN-08`).
    3. Reconcile `dl/reports/results.txt`:
       - Replace stale commit `60cf0f4` and `2,773 / 1,238 / 489` counts (lines 4, 11-13) with verified live seed counts `2,774 / 1,238 / 488` ($N=4,500$).
       - Remove references to unexecuted `dl/telecom_voc_deep_learning_colab.ipynb` and non-existent `colab_bilstm_attention.pt` (lines 58-59).
       - Accurately report on-disk BiLSTM and MiniLM metrics (`DISC-MIN-07`).

    AVOID: Reverting `config.json` files or modifying model weights.
    USE: Clean exception handling so CLI runs smoothly even if transformers is absent.
  </action>
  <verify>
    python dl/predict_dl.py --model bilstm-colab-category -t "net kub slow 4g pai na"
  </verify>
  <done>
    dl/predict_dl.py classifies input via bilstm-colab-category without error; dl/README.md accurately describes Colab word-only vs Char-CNN architectures and removes file:///home/ratul links; dl/reports/results.txt reflects verified live N=4,500 counts (2,774 / 1,238 / 488).
  </done>
</task>

## Must-Haves
After all tasks complete, verify:
- [ ] Working-tree `dl/models/banglabert_finetuned_{sentiment,category}/config.json` files match true trained class label order
- [ ] `banglabert_finetuned_models.zip` contains identical `model.safetensors` SHA256 hashes and updated `config.json` files
- [ ] `dl/models/bilstm_vocab.json` exists with 2,864 items and `dl/bilstm_artifacts.py` loads both JSON and legacy `.joblib` safely
- [ ] `scraped_data_global/pipeline/classify_global_dataset.py` and `merge_and_sync_all_datasets.py` import `dl.bilstm_artifacts`
- [ ] `dl/train_bilstm_category.py` has no off-by-one bug and defaults to a non-colliding checkpoint path
- [ ] `dl/predict_dl.py` handles `--model bilstm-colab-category` and `--model bilstm-colab-sentiment` seamlessly
- [ ] `dl/README.md` and `dl/reports/results.txt` accurately reflect live architectures, metrics, and $N=4,500$ seed counts

## Success Criteria
- [ ] All tasks verified passing with single-command PowerShell checks
- [ ] Zero changes to `.safetensors` or `.pt` weight tensors
- [ ] No git commits created (`ADR-003`)
