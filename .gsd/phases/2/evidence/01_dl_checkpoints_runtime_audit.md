# Empirical Evidence 03: PyTorch Checkpoints, Joblib Deserialization, and CLI Inference Runtime Audit

**Audit Timestamp:** 2026-11-11  
**Auditor:** GSD Phase 2 Executor (`ADR-001` Read-Only Audit)  
**Python Runtime:** Python `3.15.1`, PyTorch `2.15.0+cpu`, scikit-learn `1.9.1`, joblib `1.6.0`  
**Target Artifacts:**
- `dl/models/bilstm_attention_model.pt`
- `dl/models/minilm_transformer_head.pt`
- `dl/models/bilstm_sentiment_model.pt`
- `dl/models/bilstm_category_model.pt`
- `dl/models/bilstm_vocab.joblib`
- `dl/models/minilm_sent_head.joblib`
- `dl/models/minilm_cat_head.joblib`
- `dl/models/sent_le.joblib`
- `dl/models/cat_le.joblib`
- `dl/predict_dl.py`

---

## 1. PyTorch Checkpoints (`.pt`) Deserialization & Forward-Pass Verification

All four `.pt` files under `dl/models/` were deserialized and verified using safe, read-only Python code (`torch.load(..., weights_only=False, map_location="cpu")`). Synthetic tensor inputs were routed through instantiated network architectures to verify forward-pass compatibility.

| Checkpoint File | Checkpoint Structure & Metadata | Target Architecture | Synthetic Input Shape | Output Logits Shape | Runtime Status |
|---|---|---|:---:|:---:|:---:|
| `bilstm_attention_model.pt` | Dictionary: `['model_state_dict', 'vocab_word2idx', 'vocab_char2idx', 'label_map']`. `word_vocab` = 2,875, `char_vocab` = 302, `label_map` = 3 classes. | `BiLSTMWithAttention` (2-layer BiLSTM + Char-CNN + Bahdanau Attention from `dl/train_bilstm.py`) | Words: `(1, 15)`<br>Chars: `(1, 15, 12)` | `(1, 3)` | **PASS** (`rc=0`) |
| `minilm_transformer_head.pt` | Dictionary: `['model_name', 'head_state_dict', 'label_map']`. `model_name` = `"paraphrase-multilingual-MiniLM-L12-v2"`, `label_map` = 3 classes. | `MultilingualClassificationHead` (MLP: 384 $\rightarrow$ 128 $\rightarrow$ 64 $\rightarrow$ 3 with LayerNorm & GELU from `dl/train_transformer.py`) | Dense: `(1, 384)` | `(1, 3)` | **PASS** (`rc=0`) |
| `bilstm_sentiment_model.pt` | Raw `OrderedDict` (`state_dict` directly dumped from Colab `telecom_voc_master_unified_colab.ipynb`, 16 parameter tensors). | `HybridBiLSTMAttention` (Word-only 1-layer BiLSTM + Bahdanau Attention, `vocab_size=2864`, `embed_dim=128`, `hidden_dim=128`, `num_classes=3`) | Words: `(1, 20)` | `(1, 3)` | **PASS** (`rc=0`) |
| `bilstm_category_model.pt` | Raw `OrderedDict` (`state_dict` directly dumped from Colab `telecom_voc_master_unified_colab.ipynb`, 16 parameter tensors). | `HybridBiLSTMAttention` (Word-only 1-layer BiLSTM + Bahdanau Attention, `vocab_size=2864`, `embed_dim=128`, `hidden_dim=128`, `num_classes=5`) | Words: `(1, 20)` | `(1, 5)` | **PASS** (`rc=0`) |

### Key Architectural Finding
The checkpoint `dl/models/bilstm_category_model.pt` is **not** produced by standalone script [`dl/train_bilstm_category.py`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/train_bilstm_category.py). Standalone script `train_bilstm_category.py:342-348` saves a dictionary wrapper with keys `['model_state_dict', 'word_vocab_size', 'char_vocab_size', 'num_classes', 'label_map']`, whereas the file on disk is an unwrapped `collections.OrderedDict` matching the word-only `HybridBiLSTMAttention` trained in Google Colab `telecom_voc_master_unified_colab.ipynb:580`.

---

## 2. Joblib Deserialization & the `bilstm_vocab.joblib` Coupling Failure

### 2.1 Fatal Coupling Bug: `AttributeError: module '__main__' has no attribute 'Vocabulary'`
Attempting direct deserialization of [`dl/models/bilstm_vocab.joblib`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/models/bilstm_vocab.joblib) using `joblib.load()` crashes immediately:

```text
Exception Type: AttributeError
Exception Message: module '__main__' has no attribute 'Vocabulary'
```

### 2.2 Root Cause Analysis
During pickle serialization in Python, instances of custom classes store a reference to the defining module and class name (`module.__dict__['Vocabulary']`). The file `bilstm_vocab.joblib` was exported from Cell 10 of Google Colab notebook [`dl/telecom_voc_master_unified_colab.ipynb`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/telecom_voc_master_unified_colab.ipynb), where `class Vocabulary` was defined interactively in the notebook's global `__main__` namespace rather than imported from a reusable package/module.

Consequently, any standalone script, API server, or evaluation pipeline that attempts to call `joblib.load("dl/models/bilstm_vocab.joblib")` without first monkey-patching or defining `Vocabulary` in its own `__main__` namespace will crash fatally.

### 2.3 Verification with Injected Mock
When a mock definition is injected into `sys.modules['__main__'].Vocabulary`, `joblib.load()` succeeds:
- **Object Type:** `<class '__main__.Vocabulary'>`
- **Internal Dictionary Keys:** `['min_freq', 'word2idx', 'idx2word']`
- **Vocabulary Size:** $2,864$ words

---

## 3. Scikit-Learn Joblib Models & Label Encoders Audit

Deserializing `minilm_sent_head.joblib`, `minilm_cat_head.joblib`, `sent_le.joblib`, and `cat_le.joblib` under scikit-learn `1.9.1` surfaced version drift warnings and verified downstream inference:

### 3.1 Provenance & `InconsistentVersionWarning`
```text
InconsistentVersionWarning: Trying to unpickle estimator LogisticRegression from version 1.6.1 when using version 1.9.1.
InconsistentVersionWarning: Trying to unpickle estimator LabelEncoder from version 1.6.1 when using version 1.9.1.
```
All four objects were pickled under **scikit-learn `1.6.1`** (in Google Colab `telecom_voc_master_unified_colab.ipynb`).

### 3.2 Evaluation of Deserialized Objects
1. `dl/models/minilm_sent_head.joblib`:
   - Type: `LogisticRegression(C=1.5, max_iter=1000)`
   - Classes: `['Negative', 'Neutral', 'Positive']`
   - Test inference on random 384-dimensional vector succeeded: output = `['Neutral']`.
2. `dl/models/minilm_cat_head.joblib`:
   - Type: `LogisticRegression(C=2.0, max_iter=1000)`
   - Classes: `['App Login & Technical Bugs', 'Billing & Airtime Deductions', 'General Appreciation / Other', 'Network Speed & 4G Latency', 'Offers & Data Packs']`
   - Test inference on random 384-dimensional vector succeeded: output = `['Offers & Data Packs']`.
3. `dl/models/sent_le.joblib`:
   - Type: `LabelEncoder`
   - Classes: `['Negative', 'Neutral', 'Positive']`
4. `dl/models/cat_le.joblib`:
   - Type: `LabelEncoder`
   - Classes: `['App Login & Technical Bugs', 'Billing & Airtime Deductions', 'General Appreciation / Other', 'Network Speed & 4G Latency', 'Offers & Data Packs']` (Alphabetical order).

---

## 4. CLI Inference Audit (`dl/predict_dl.py`)

Inference via the command-line interface [`dl/predict_dl.py`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/predict_dl.py) was empirically tested on Python 3.15.1.

### 4.1 BiLSTM Inference Test (`--model bilstm`)
**Command:**
```powershell
python dl/predict_dl.py --model bilstm --text "valo service"
```
**Captured Output:**
```text
==================================================
Model        : BiLSTM with Self-Attention
Input Review : valo service
Sentiment    : Positive
Confidence   : 74.48%
Probabilities:
  - Negative:   6.69%
  - Neutral :  18.83%
  - Positive:  74.48%
==================================================
```
**Result:** **SUCCESS (`exit code 0`)**. Model loads `bilstm_attention_model.pt` correctly and performs inference within ~1.2 seconds.

### 4.2 Transformer Inference Test (`--model transformer`)
**Command:**
```powershell
python dl/predict_dl.py --model transformer --text "valo service"
```
**Captured Stderr:**
```text
Traceback (most recent call last):
  File "dl\predict_dl.py", line 143, in <module>
    main()
  File "dl\predict_dl.py", line 113, in main
    tokenizer, transformer, head = load_transformer()
  File "dl\predict_dl.py", line 68, in load_transformer
    from transformers import AutoTokenizer, AutoModel
ModuleNotFoundError: No module named 'transformers'
```
**Result:** **CRASH (`exit code 1`)**. The local environment does not have the Hugging Face `transformers` package installed, preventing execution of the transformer inference pipeline.

### 4.3 Missing CLI Support for Other Models
Inspection of `dl/predict_dl.py` lines 99-106 shows:
```python
parser.add_argument(
    "--model",
    type=str,
    choices=["bilstm", "transformer"],
    default="bilstm",
    help="Model to use for prediction (bilstm or transformer)",
)
```
The script provides no flags or implementations to run inference on:
1. `dl/models/banglabert_finetuned_sentiment`
2. `dl/models/banglabert_finetuned_category`
3. `dl/models/bilstm_sentiment_model.pt`
4. `dl/models/bilstm_category_model.pt`
5. `dl/models/minilm_cat_head.joblib`
