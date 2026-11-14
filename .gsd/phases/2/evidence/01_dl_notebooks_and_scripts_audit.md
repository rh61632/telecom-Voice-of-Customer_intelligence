# Empirical Evidence 01: Deep Learning Notebooks, Training Scripts, Reports, and Documentation Audit

**Audit Timestamp:** 2026-11-11  
**Auditor:** GSD Phase 2 Executor (`ADR-001` Read-Only Audit)  
**Scope:** `dl/*.ipynb`, `archive/early_dl_experiments/*.ipynb`, `dl/*.py`, `dl/reports/*`, `dl/README.md`, `scripts/upload_to_huggingface.py`

---

## 1. Executive Summary

A systematic comparative audit was performed across all 4 Deep Learning Jupyter notebooks, 5 standalone Python training/inference scripts, 2 benchmark report files, documentation (`dl/README.md`), and the Hugging Face model card upload script (`scripts/upload_to_huggingface.py`).

Key findings include:
1. **Dataset Class Distribution & Split Contradictions:** Active processed data across the three operators (`data/processed/my{gp,bl,robi}_classified_reviews.csv`) totals $N=4,500$ (2,774 Positive / 1,238 Negative / 488 Neutral; 2,731 General / 788 Offers / 400 App / 364 Network / 217 Billing). In contrast, [`dl/reports/results.txt`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/reports/results.txt) is stale from commit `60cf0f4` reporting $N=4,500$ with $2,773 / 1,238 / 489$, referencing a missing GPU checkpoint `colab_bilstm_attention.pt`.
2. **Missing `operator` Column & Misclassification in BanglaBERT Notebook:** In [`dl/telecom_voc_banglabert_finetuning_colab.ipynb:225`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/telecom_voc_banglabert_finetuning_colab.ipynb#L225), `finetune_banglabert.py` printed `"across 2 operators"` because `mygp_classified_reviews.csv` lacks an `operator` column. In Cell 10 ([`line 905`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/telecom_voc_banglabert_finetuning_colab.ipynb#L905)), fine-tuned BanglaBERT misclassified the positive Banglish review `"Onk shundor app shob offer e discount pai"` as `Negative (94.7% confidence)`.
3. **Macro-F1 & Accuracy Figure Conflicts:**
   - **Category BanglaBERT 5-Fold CV:** [`dl/README.md:76`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/README.md#L76), [`archive/early_dl_experiments/README.md:27`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/archive/early_dl_experiments/README.md#L27), and [`dl/telecom_voc_master_unified_colab.ipynb:1095`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/telecom_voc_master_unified_colab.ipynb#L1095) report `85.27% / 0.7624`, but [`scripts/upload_to_huggingface.py:145-147,164`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/scripts/upload_to_huggingface.py#L145-L147) hardcodes `85.27% / 0.8032` (mixing the 5-fold CV accuracy with the 85/15 held-out test split F1 from [`dl/reports/banglabert_finetuning_report.txt:30`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/reports/banglabert_finetuning_report.txt#L30)).
   - **Sentiment MiniLM:** [`dl/README.md:61`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/README.md#L61) reports `82.33% / 0.7475` (Logistic Regression head in `master_unified_colab.ipynb`), contradicting [`dl/reports/results.txt:23`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/reports/results.txt#L23) (`86.00% / 0.7809` from PyTorch `TransformerClassifier`).
   - **Sentiment BiLSTM:** [`dl/README.md:62`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/README.md#L62) reports `81.50% / 0.7180` (hardcoded fallback string in `master_unified_colab.ipynb:1088` where Cell 10 omitted BiLSTM CV), contradicting [`dl/reports/results.txt:21`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/reports/results.txt#L21) (`84.02% / 0.7525`).
   - **Category Ensemble & MiniLM:** [`dl/README.md:75,77`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/README.md#L75) reports `87.44% / 0.7845` and `81.15% / 0.7247` (from archived `category_benchmark_summary.csv`), whereas the Colab run that generated the disk models scored `87.33% / 0.7791` and `80.56% / 0.7103`.
4. **Architecture Advertising Discrepancy:** [`dl/telecom_voc_master_unified_colab.ipynb:24`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/telecom_voc_master_unified_colab.ipynb#L24) and [`dl/README.md:12,62`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/README.md#L12) advertise `Hybrid BiLSTM + Attention + Char-CNN`, but Cell 9 ([`lines 486-504`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/telecom_voc_master_unified_colab.ipynb#L486-L504)) implements a **word-only** `HybridBiLSTMAttention` with **no** Char-CNN layers.
5. **Script Defects:**
   - [`dl/train_bilstm_category.py:311-312`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/train_bilstm_category.py#L311-L312): off-by-one padding size `len(vocab.word2idx) + 1`; missing output artifacts `bilstm_category_vocab.json` and `dl_bilstm_category_report.md`.
   - [`dl/finetune_banglabert.py:322`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/finetune_banglabert.py#L322): report file opened with `mode="a"` instead of `"w"`, causing silent accumulation across runs.
   - [`archive/.../telecom_voc_comment_type_classification_colab.ipynb`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/archive/early_dl_experiments/telecom_voc_comment_type_classification_colab.ipynb): broken GitHub Colab badge (`line 17`), corrupted regex `r"(.)\u0001{2,}"` (`line 121`), and epoch-mismatch bug pairing `best_f1` with final-epoch accuracy outside the training loop (`lines 372-375, 482-486, 561-565`).

---

## 2. Comprehensive Inventory & Comparison Matrix

| Artifact | Task(s) | Dataset Scope & Counts | Model Architecture & Hyperparameters | Execution State & Exported Artifacts | Metrics Recorded |
|---|---|---|---|---|---|
| [`dl/telecom_voc_master_unified_colab.ipynb`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/telecom_voc_master_unified_colab.ipynb) (19 cells) | Sentiment (3-class) + Operational Category (5-class) | $N=4,500$ (Sent: 2,774 Pos / 1,238 Neg / 488 Neu; Cat: 2,731 Gen / 788 Off / 400 App / 364 Net / 217 Bill, lines 185-232) | **ML Ensembles** (lines 295-399): `FeatureUnion(word 1-2 min_df=2 max=12k, char 3-5 min_df=2 max=25k)`, `LR(C=2.0 sent / 2.5 cat, balanced)`, `CalibratedClassifierCV(LinearSVC(C=1.0), cv=3)`, `ComplementNB(alpha=0.5)`, `weights=[2.0, 2.5, 1.0]`. **BiLSTM** (lines 486-590): word-only `HybridBiLSTMAttention` (`vocab=2864, min_freq=2, max_len=40, embed=128, hidden=128, BahdanauAttention, Dropout(0.4), epochs=7 sent / 8 cat, bs=64, AdamW lr=1e-3, wd=1e-4`, full-fit only). **MiniLM** (lines 1005-1035): `paraphrase-multilingual-MiniLM-L12-v2` (`bs=128`) + `LR(C=1.5 sent / 2.0 cat)`. | **Executed** on Tesla T4 (PyTorch 2.11.0+cu130). Exports `telecom_voc_all_models_colab.zip` (14.80 MB, lines 1262-1350): `sentiment_voting_classifier.joblib`, `category_voting_classifier.joblib`, `bilstm_{sentiment,category}_model.pt`, `bilstm_vocab.joblib`, `sent_le.joblib`, `cat_le.joblib`, `minilm_{sent,cat}_head.joblib`. | **5-fold CV:** ML Sent `87.47% / 0.7684` (line 331); ML Cat `87.33% / 0.7791` (line 421); MiniLM Sent `82.33% / 0.7475` (line 1051); MiniLM Cat `80.56% / 0.7103` (line 1054). **Hardcoded** in Cell 14 (lines 1085-1097): BanglaBERT (`91.60% / 0.8598` sent, `85.27% / 0.7624` cat), BiLSTM (`81.50% / 0.7180` sent, `80.84% / 0.7106` cat). |
| [`dl/telecom_voc_banglabert_finetuning_colab.ipynb`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/telecom_voc_banglabert_finetuning_colab.ipynb) (13 cells) | Sentiment (3-class) & Category (5-class) | $N=4,500$ (61.64% Pos, 27.51% Neg, 10.84% Neu; line 225 prints `"across 2 operators"` because `mygp` lacks `operator`) | Runs CLI `!python dl/finetune_banglabert.py --task both --epochs 4 --batch_size 32 --lr 2e-5` (line 281). Architecture: `csebuetnlp/banglabert` (110M), `max_length=96`, 5-fold Stratified CV + final 85/15 held-out split ($N=675$). | **Executed** on Tesla T4 (PyTorch 2.11.0+cu130). Cell 10 tests 4 sample reviews (lines 890-930). Cell 12 packs `banglabert_finetuned_models.zip` (821.5 MB, line 1094). | Cell 8 prints `dl/reports/banglabert_finetuning_report.txt` (85/15 held-out split $N=675$: Sent `89.78% / 0.8324`, Cat `87.11% / 0.8023`). Cell 6 output truncated before 5-fold CV summary. |
| [`dl/telecom_voc_deep_learning_colab.ipynb`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/telecom_voc_deep_learning_colab.ipynb) (21 cells) | Sentiment (3-class) | $N=4,500$ (`MIN_WORDS=1`, line 95) | **Ensemble** (lines 147-166): `char_wb (2,5) min_df=3`, `LR + CalibratedLinearSVC + CNB(norm=True)`, `weights=[2,2,1]`. **BiLSTM+Char-CNN** (lines 278-352): `word_dim=128, char_dim=32, char_filters=64, lstm_dim=128, 2 layers, dropout=0.3, epochs=8, bs=32, lr=1e-3`. **Frozen MiniLM** (lines 395-470) & **Frozen BanglaBERT** (lines 524-580): `max_length=96, mean pooling, MLP(384->128->64->3 / 768->256->64->3, LayerNorm+GELU, dropout=0.3, epochs=15, bs=32, lr=2e-3, wd=1e-3)`. | **Unexecuted** (zero cell execution counts, zero outputs saved). Targets missing `dl/models/colab_bilstm_attention.pt` (line 760), `ml/models/ensemble_voting_classifier.joblib`, `dl/reports/results.txt`. | Hardcodes Dummy (`0.2542 / 61.62%`) and Char N-Gram LogReg (`0.7796 / 85.96%`) (lines 623-624). |
| [`archive/early_dl_experiments/telecom_voc_comment_type_classification_colab.ipynb`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/archive/early_dl_experiments/telecom_voc_comment_type_classification_colab.ipynb) (21 cells) | Category (5-class) | $N=4,499$ in headers/comments (lines 109, 137) | **Ensemble** (lines 178-193): `word (1,2) min_df=2` + `char_wb (3,5) min_df=3`, `LR + CalibratedLinearSVC + CNB(norm=True)`, `weights=[2,2,1]`. **BiLSTM+Char-CNN** (lines 288-353): 2-layer 128, `epochs=8, bs=64, lr=2e-3`. **Frozen MiniLM (384) & Frozen BanglaBERT (768)** (lines 403-563): `max_length=128, bs=128`, `TransformerHead(in->256->128->5, BatchNorm1d+ReLU, dropout=0.3/0.2), epochs=14, lr=1e-3, wd=1e-4`. | **Unexecuted** (zero saved cell outputs). Exports `category_voting_classifier.joblib` & `category_benchmark_summary.csv` (lines 677-681). | Exact floats saved in `ml/reports/category_benchmark_summary.csv:2-5`: Ensemble `0.7845 / 87.44%`, MiniLM `0.7247 / 81.15%`, BiLSTM `0.7106 / 80.84%`, Frozen BanglaBERT `0.6253 / 74.88%`. |
| [`dl/finetune_banglabert.py`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/finetune_banglabert.py) (368 lines) | Sentiment, Category, Both | $N=4,500$ (`mygp` lacks `operator` column; lines 76-101) | `csebuetnlp/banglabert`, `--epochs 4 --batch_size 32 --lr 2e-5 --max_length 96 --folds 5`, `AdamW(wd=0.01)`, 10% linear warmup, inverse-freq `CrossEntropyLoss` (lines 224-230, 331-339). | Saves `dl/models/banglabert_finetuned_{sentiment,category}/` (lines 315-317); appends (`mode="a"`, line 322) test split report to `dl/reports/banglabert_finetuning_report.txt`. | Prints 5-fold CV to stdout only; report file logs only 85/15 held-out split ($N=675$): Sent `89.78% / 0.8324`, Cat `87.11% / 0.8023`. |
| [`dl/train_bilstm.py`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/train_bilstm.py) (395 lines) | Sentiment (3-class) | $N=4,500$ (lines 46-68) | `BiLSTMWithAttention` (Word 128 + Char-CNN 64, 2-layer BiLSTM 128, dropout=0.3), `epochs=8, bs=32, lr=1e-3, wd=1e-4, ReduceLROnPlateau` (lines 173-226, 394-395). | Saves dict checkpoint `dl/models/bilstm_attention_model.pt` (lines 380-387). | No report file written. |
| [`dl/train_bilstm_category.py`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/train_bilstm_category.py) (382 lines) | Category (5-class) | $N=4,500$ (lines 50-72) | Same `BiLSTMWithAttention` (`num_classes=5`), single 85/15 split (`StratifiedKFold(n_splits=7)` fold 1, lines 292-293), `epochs=8, bs=32, lr=1e-3`. | Targets `bilstm_category_model.pt` (dict), `bilstm_category_vocab.json`, `dl/reports/dl_bilstm_category_report.md` (lines 341-377). | **Disk artifacts do NOT match this script** (`bilstm_category_vocab.json` & `.md` missing; `.pt` on disk is Colab `HybridBiLSTMAttention`). |
| [`dl/train_transformer.py`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/train_transformer.py) (249 lines) | Sentiment (3-class) | $N=4,500$ (lines 42-63) | Frozen `paraphrase-multilingual-MiniLM-L12-v2` (`max_length=96, bs=32`) + `MultilingualClassificationHead(384->128->64->3, LayerNorm+GELU, dropout=0.3)`, `epochs=15, lr=2e-3, wd=1e-3` (lines 78-98, 168-242). | Saves `dl/models/minilm_transformer_head.pt` (lines 239-240). | No report file written. |
| [`dl/predict_dl.py`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/predict_dl.py) (143 lines) | CLI Sentiment Inference | — | Supports `--model {bilstm, transformer}` (line 104). | Reads `bilstm_attention_model.pt` (line 30) or `minilm_transformer_head.pt` (line 70). | Does **not** support `banglabert_finetuned_*` or `bilstm_{sentiment,category}_model.pt`. |

---

## 3. Detailed Audit Findings & Citations

### 3.1 Dataset Scope and Stale Results Report
- **Active Seed Distribution ($N=4,500$):**
  - Positive: 2,774 (61.64%)
  - Negative: 1,238 (27.51%)
  - Neutral: 488 (10.84%)
  - Operational Category: General Appreciation: 2,731 (60.69%), Offers: 788 (17.51%), App Login: 400 (8.89%), Network: 364 (8.09%), Billing: 217 (4.82%).
- **Stale Colab Run in [`dl/reports/results.txt`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/reports/results.txt):**
  - Line 4 cites git commit `60cf0f4` (before commit `3e453d0` fixed the class label in `mygp_classified_reviews.csv`).
  - Lines 11-13 report: Positive: 2,773 (61.62%), Negative: 1,238 (27.51%), Neutral: 489 (10.87%).
  - Line 58 claims to be generated by `dl/telecom_voc_deep_learning_colab.ipynb` (which has 0 execution outputs on disk).
  - Line 59 points to `dl/models/colab_bilstm_attention.pt`, which does **not exist** on disk.

### 3.2 BanglaBERT Fine-Tuning Colab Audit (`dl/telecom_voc_banglabert_finetuning_colab.ipynb`)
- **Missing `operator` Column (Lines 206–225):**
  In Cell 4, when loading datasets, `data/processed/mygp_classified_reviews.csv` lacked the `operator` column (parsed as `NaN`). As a result, the operator unique list evaluated to `[nan, 'Robi', 'Banglalink']` (`nunique() == 2`), prompting the script to print:
  ```
  Loaded ground-truth dataset: 4,500 reviews across 2 operators.
  ```
- **Positive Sample Misclassified as 94.7% Negative in Cell 10 (Line 905):**
  In Cell 10, the interactive prediction block tested four sample queries. Sample 3:
  ```
  INPUT REVIEW: "Onk shundor app shob offer e discount pai"
  PREDICTED SENTIMENT : Negative (94.7% confidence)
  PREDICTED CATEGORY  : Offers & Data Packs (86.4% confidence)
  ```
  The input text is unambiguously positive ("Very beautiful app, I get discounts on all offers"), yet the fine-tuned model assigned 94.7% probability to `Negative`.
- **Cell 6 Truncation and Missing 5-Fold CV Persistence:**
  In Cell 6, execution output displays Fold 1 through Fold 5 and prints:
  ```
  Macro-F1 : 0.7624 ± 0.0163
  Accuracy : 85.27% ± 1.14%
  ```
  However, [`dl/finetune_banglabert.py:321-326`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/finetune_banglabert.py#L321-L326) only writes the final held-out test split ($N=675$) classification report to `dl/reports/banglabert_finetuning_report.txt` (Sent: `89.78% / 0.8324`, Cat: `87.11% / 0.8023`). The 5-fold CV summary was never saved to disk and is completely absent from the report file.

### 3.3 Metric Contradictions Across README, Notebooks, and Hugging Face Card
1. **Category BanglaBERT 5-Fold Macro-F1 Divergence:**
   - [`dl/README.md:76`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/README.md#L76), [`archive/early_dl_experiments/README.md:27`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/archive/early_dl_experiments/README.md#L27), and [`dl/telecom_voc_master_unified_colab.ipynb:1095`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/telecom_voc_master_unified_colab.ipynb#L1095) record **`85.27% CV Accuracy / 0.7624 Macro-F1`**.
   - [`scripts/upload_to_huggingface.py:145-147,164`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/scripts/upload_to_huggingface.py#L145-L147) hardcodes **`85.27% Cross-Validation Accuracy | 0.8032 Macro-F1`**.
   - **Root Cause:** The author combined the 5-fold CV accuracy (`85.27%`) with the single 85/15 held-out test split F1 score (`0.8023` $\approx$ `0.8032` in `banglabert_finetuning_report.txt:30`) when authoring the Hugging Face model card template.
2. **Sentiment MiniLM Discrepancy:**
   - [`dl/README.md:61`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/README.md#L61) reports `82.33% / 0.7475` (produced by a scikit-learn `LogisticRegression(C=1.5)` head in `master_unified_colab.ipynb:1051-1052`).
   - [`dl/reports/results.txt:23`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/reports/results.txt#L23) reports `86.00% / 0.7809` (produced by a PyTorch `TransformerClassifier` MLP head in `telecom_voc_deep_learning_colab.ipynb:420-435`).
3. **Sentiment BiLSTM Discrepancy:**
   - [`dl/README.md:62`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/README.md#L62) reports `81.50% / 0.7180` (hardcoded fallback string in `master_unified_colab.ipynb:1088` because Cell 10 omitted cross-validation for BiLSTM).
   - [`dl/reports/results.txt:21`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/reports/results.txt#L21) reports `84.02% / 0.7525`.
4. **Category Ensemble & MiniLM:**
   - [`dl/README.md:75,77`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/README.md#L75) reports Ensemble `87.44% / 0.7845` and MiniLM `81.15% / 0.7247` (copied from `ml/reports/category_benchmark_summary.csv:2-3` produced by the early archived notebook).
   - The actual Colab run in `master_unified_colab.ipynb:421,1054` that produced the models committed on disk (`ml/models/category_voting_classifier.joblib` and `dl/models/minilm_cat_head.joblib`) scored **`87.33% / 0.7791`** and **`80.56% / 0.7103`**.

### 3.4 Architecture Discrepancy: Word-Only vs Char-CNN
- **Documentation Claim:** [`dl/README.md:12,62`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/README.md#L12) and [`dl/telecom_voc_master_unified_colab.ipynb:24`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/telecom_voc_master_unified_colab.ipynb#L24) advertise:
  > `Hybrid BiLSTM + Attention + Char-CNN`
- **Actual Implementation in `master_unified_colab.ipynb:486-504`:**
  ```python
  class HybridBiLSTMAttention(nn.Module):
      def __init__(self, vocab_size, num_classes, embed_dim=128, hidden_dim=128):
          super().__init__()
          self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
          self.bilstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True, bidirectional=True)
          self.attention = BahdanauAttention(hidden_dim * 2)
          self.fc = nn.Sequential(...)
  ```
  There is **zero** character embedding or Char-CNN convolution logic in `HybridBiLSTMAttention`. It is a single-layer bidirectional LSTM operating strictly on word tokens. (In contrast, standalone script [`dl/train_bilstm.py:173-226`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/train_bilstm.py#L173-L226) does implement `BiLSTMWithAttention` having Char-CNN branches).

### 3.5 Training Script Defects
1. **`dl/train_bilstm_category.py:311-312` Off-By-One Padding:**
   `word_vocab_size=len(vocab.word2idx) + 1`. Because `<pad>` (index 0) and `<unk>` (index 1) are already counted inside `len(vocab.word2idx)`, adding `+1` allocates an extra, unindexed embedding vector.
2. **Missing Output Artifacts:**
   [`dl/train_bilstm_category.py:352,374`](file:///c:/Users/user/Ratul/project/telecom-Voice-of-Customer_intelligence/dl/train_bilstm_category.py#L352) specifies paths `dl/models/bilstm_category_vocab.json` and `dl/reports/dl_bilstm_category_report.md`. Neither file exists on disk.
3. **`dl/finetune_banglabert.py:322` Append Mode Accumulation:**
   Opening `dl/reports/banglabert_finetuning_report.txt` in `"a"` mode appends every execution to the end of the file instead of refreshing it.
4. **`archive/early_dl_experiments/telecom_voc_comment_type_classification_colab.ipynb`:**
   - **Broken Colab Badge (Line 10):** Points to non-existent URL `.../blob/main/dl/telecom_voc_comment_type_classification_colab.ipynb`.
   - **Corrupted Regex (Line 121):** `re.sub(r"(.)\u0001{2,}", r"\u0001\u0001", text)` contains an ASCII Start-of-Heading control character (`\x01`) rather than a backreference `\1`.
   - **Validation Epoch Mismatch Bug (Lines 372-376, 482-486, 561-565):**
     `if f1 > best_f1: best_f1 = f1` updates `best_f1` across epochs, but `acc = accuracy_score(targets, preds)` is executed outside the epoch loop, pairing the peak macro-F1 with the final epoch's validation accuracy.
