# Empirical Evidence 02: BanglaBERT Working-Tree Diff, Zip Archive SHA256 Parity, and Hugging Face Metadata Audit

**Audit Timestamp:** 2026-11-11  
**Auditor:** GSD Phase 2 Executor (`ADR-001` Read-Only Audit)  
**Target Artifacts:**
- `dl/models/banglabert_finetuned_sentiment/config.json`
- `dl/models/banglabert_finetuned_category/config.json`
- `banglabert_finetuned_models.zip` (821,497,087 bytes)
- `scripts/upload_to_huggingface.py`
- `dl/models/cat_le.joblib`

---

## 1. Uncommitted Git Working-Tree Diff on `config.json`

The git working tree contains uncommitted modifications to the Hugging Face configuration files in both fine-tuned BanglaBERT model directories:
1. `dl/models/banglabert_finetuned_sentiment/config.json`
2. `dl/models/banglabert_finetuned_category/config.json`

### 1.1 Exact Git Diff Analysis

The diff reflects an in-place patch to replace Hugging Face's default anonymous class tags (`"LABEL_0"`, `"LABEL_1"`, etc.) with semantic string labels.

#### Sentiment Model Configuration Diff:
```diff
diff --git a/dl/models/banglabert_finetuned_sentiment/config.json b/dl/models/banglabert_finetuned_sentiment/config.json
index 22ad47f..3b336c8 100644
--- a/dl/models/banglabert_finetuned_sentiment/config.json
+++ b/dl/models/banglabert_finetuned_sentiment/config.json
@@ -13,17 +13,17 @@
   "hidden_dropout_prob": 0.1,
   "hidden_size": 768,
   "id2label": {
-    "0": "LABEL_0",
-    "1": "LABEL_1",
-    "2": "LABEL_2"
+    "0": "Negative",
+    "1": "Neutral",
+    "2": "Positive"
   },
   "initializer_range": 0.02,
   "intermediate_size": 3072,
   "is_decoder": false,
   "label2id": {
-    "LABEL_0": 0,
-    "LABEL_1": 1,
-    "LABEL_2": 2
+    "Negative": 0,
+    "Neutral": 1,
+    "Positive": 2
   },
   "layer_norm_eps": 1e-12,
   "max_position_embeddings": 512,
```

#### Category Model Configuration Diff:
```diff
diff --git a/dl/models/banglabert_finetuned_category/config.json b/dl/models/banglabert_finetuned_category/config.json
index 9601c0b..da359c9 100644
--- a/dl/models/banglabert_finetuned_category/config.json
+++ b/dl/models/banglabert_finetuned_category/config.json
@@ -13,21 +13,21 @@
   "hidden_dropout_prob": 0.1,
   "hidden_size": 768,
   "id2label": {
-    "0": "LABEL_0",
-    "1": "LABEL_1",
-    "2": "LABEL_2",
-    "3": "LABEL_3",
-    "4": "LABEL_4"
+    "0": "General Appreciation / Other",
+    "1": "Offers & Data Packs",
+    "2": "App Login & Technical Bugs",
+    "3": "Network Speed & 4G Latency",
+    "4": "Billing & Airtime Deductions"
   },
   "initializer_range": 0.02,
   "intermediate_size": 3072,
   "is_decoder": false,
   "label2id": {
-    "LABEL_0": 0,
-    "LABEL_1": 1,
-    "LABEL_2": 2,
-    "LABEL_3": 3,
-    "LABEL_4": 4
+    "General Appreciation / Other": 0,
+    "Offers & Data Packs": 1,
+    "App Login & Technical Bugs": 2,
+    "Network Speed & 4G Latency": 3,
+    "Billing & Airtime Deductions": 4
   },
   "layer_norm_eps": 1e-12,
   "max_position_embeddings": 512,
```

### 1.2 Origin & Cause of the Uncommitted Change
When training BanglaBERT via [`dl/finetune_banglabert.py:219-222`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/finetune_banglabert.py#L219-L222), the model was initialized with:
```python
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=num_classes,
)
```
Because `id2label` and `label2id` dictionaries were **not passed** to `AutoModelForSequenceClassification.from_pretrained()`, the Hugging Face `transformers` library defaulted to generating `"0": "LABEL_0"`, `"1": "LABEL_1"`, etc.

Later, on November 8, 2026, an editor manually patched `config.json` on disk to insert the mapping defined in [`dl/finetune_banglabert.py:54-66`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/finetune_banglabert.py#L54-L66) (`SENTIMENT_LABEL_MAP` and `CATEGORY_LABEL_MAP`), but did not commit the change to git.

### 1.3 Operational Hazard: Label Index Ordering Divergence Across Models
An empirical check was conducted on the category label ordering between BanglaBERT and the classical ML / BiLSTM label encoder [`dl/models/cat_le.joblib`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/models/cat_le.joblib):

| Class Index | BanglaBERT `config.json` Order | `cat_le.joblib` (scikit-learn `LabelEncoder`) Order |
|:---:|:---|:---|
| **0** | **General Appreciation / Other** | **App Login & Technical Bugs** |
| **1** | **Offers & Data Packs** | **Billing & Airtime Deductions** |
| **2** | **App Login & Technical Bugs** | **General Appreciation / Other** |
| **3** | Network Speed & 4G Latency | Network Speed & 4G Latency |
| **4** | **Billing & Airtime Deductions** | **Offers & Data Packs** |

**Critical System Risk:**
Only index 3 (`Network Speed & 4G Latency`) is consistent between the two representations. If downstream deployment code or an evaluation pipeline passes raw integer predictions or logits from BanglaBERT into `cat_le.inverse_transform()`, **80% of categories will be corrupted**:
- A BanglaBERT prediction of `0` (`General Appreciation`) would be decoded by `cat_le` as `App Login & Technical Bugs`.
- A BanglaBERT prediction of `1` (`Offers & Data Packs`) would be decoded as `Billing & Airtime Deductions`.
- A BanglaBERT prediction of `2` (`App Login & Technical Bugs`) would be decoded as `General Appreciation / Other`.
- A BanglaBERT prediction of `4` (`Billing & Airtime Deductions`) would be decoded as `Offers & Data Packs`.

---

## 2. Empirical Verification of `banglabert_finetuned_models.zip`

The archive [`banglabert_finetuned_models.zip`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/banglabert_finetuned_models.zip) sits in the repository root ($821,497,087$ bytes, timestamped `2026-10-19 20:34:39`). A read-only verification was executed using Python `zipfile` and `hashlib`.

### 2.1 Archive Structure & File Inventory
The zip archive contains exactly 8 files organized into two directories, corresponding to the two models:
1. `banglabert_finetuned_sentiment/`
   - `model.safetensors` ($442,502,748$ bytes)
   - `tokenizer.json` ($1,032,103$ bytes)
   - `tokenizer_config.json` ($412$ bytes)
   - `config.json` ($993$ bytes)
2. `banglabert_finetuned_category/`
   - `model.safetensors` ($442,508,900$ bytes)
   - `tokenizer.json` ($1,032,103$ bytes)
   - `tokenizer_config.json` ($412$ bytes)
   - `config.json` ($1,069$ bytes)

### 2.2 SHA256 Checksum Parity on `model.safetensors`
To ensure that the uncompressed disk checkpoints have not suffered bit rot or tampering, SHA256 hashes of the safetensors weights inside the zip and on disk were computed and compared:

| Artifact | Size (Bytes) | SHA256 Checksum Prefix | Parity Result |
|---|---|---|:---:|
| `dl/models/banglabert_finetuned_sentiment/model.safetensors` | 442,502,748 | `b566cc09e58f3649...` | **EXACT MATCH (`True`)** |
| `dl/models/banglabert_finetuned_category/model.safetensors` | 442,508,900 | `dc85d60cf99eb9f8...` | **EXACT MATCH (`True`)** |

**Conclusion:** The neural network weights on disk are byte-for-byte identical to the weights stored in `banglabert_finetuned_models.zip`.

### 2.3 Tokenizer Configuration Byte Discrepancy (CRLF vs LF)
- Disk file `dl/models/banglabert_finetuned_sentiment/tokenizer.json` has $1,064,266$ bytes, whereas inside the zip it is $1,032,103$ bytes.
- Similarly, `tokenizer_config.json` is $428$ bytes on disk vs $412$ bytes in the zip.
- **Empirical Check:** Converting CRLF (`\r\n`) to LF (`\n`) yielded identical bytes (`True`), and parsing both files with `json.loads()` yielded strictly identical JSON dictionaries. The difference is purely Windows git checkout newline conversion (`core.autocrlf`).

### 2.4 Pre-Patch State of `config.json` in Zip Archive
Inspection of `config.json` extracted directly from the zip revealed:
```json
// banglabert_finetuned_sentiment/config.json (inside zip)
"id2label": {
  "0": "LABEL_0",
  "1": "LABEL_1",
  "2": "LABEL_2"
}

// banglabert_finetuned_category/config.json (inside zip)
"id2label": {
  "0": "LABEL_0",
  "1": "LABEL_1",
  "2": "LABEL_2",
  "3": "LABEL_3",
  "4": "LABEL_4"
}
```
This confirms that `banglabert_finetuned_models.zip` was generated by Colab Cell 12 on October 19, 2026, **prior** to the November 8 label patch. The zip file contains the unpatched `LABEL_0` configuration files.

---

## 3. Audit of `scripts/upload_to_huggingface.py`

Inspection of [`scripts/upload_to_huggingface.py`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/scripts/upload_to_huggingface.py) revealed several reporting discrepancies and mutating side effects:

### 3.1 Hardcoded Metric Inconsistency in Model Cards
Lines 143-165 define the auto-generated YAML metadata and Markdown for the category model:
```yaml
    metrics:
    - type: accuracy
      value: 0.8527
    - type: f1
      value: 0.8032
---
# Performance: **85.27% Cross-Validation Accuracy** | **0.8032 Macro-F1**
```
- **Contradiction:** The 5-fold cross-validation Macro-F1 achieved by BanglaBERT for Category classification was **`0.7624`**, as documented in `dl/README.md:76`, `master_unified_colab.ipynb:1095`, and `early_dl_experiments/README.md:27`.
- **Origin of `0.8032`:** In [`dl/reports/banglabert_finetuning_report.txt:30`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/reports/banglabert_finetuning_report.txt#L30), the 85/15 held-out test split ($N=675$) scored Macro-F1 of `0.8023`. The upload script incorrectly pairs the 5-fold CV accuracy (`85.27%`) with the single test split macro-F1 (`0.8032`), inflating the advertised cross-validation performance by **+4.08% F1**.

### 3.2 File-Mutating & Network Side Effects
1. **Uncommitted Working-Tree Mutation:**
   Lines 245-247 write generated `README.md` files directly into `dl/models/banglabert_finetuned_{sentiment,category}/`:
   ```python
   readme_path = local_dir / "README.md"
   with open(readme_path, "w", encoding="utf-8") as f:
       f.write(r["readme"])
   ```
   Executing `upload_to_huggingface.py` would create two new untracked/modified files in the working directory.
2. **Network Dependency:**
   Lines 200-213 import `huggingface_hub`, prompt for interactive API tokens, and push models over the public network. Under `ADR-001`, this script is classified as mutating/network-dependent and must not be run during the audit.
