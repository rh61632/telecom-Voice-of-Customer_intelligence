# 🗄️ Archived: Early Deep Learning & Frozen Head Baseline Experiments

> **Status: ARCHIVED / SUPERSEDED** (October 2026)  
> The active transformer pipeline is BUET BanglaBERT **Full End-to-End Fine-Tuning** located in [`dl/finetune_banglabert.py`](../../dl/finetune_banglabert.py) and [`dl/telecom_voc_banglabert_finetuning_colab.ipynb`](../../dl/telecom_voc_banglabert_finetuning_colab.ipynb).

---

## 📌 Overview

This archive preserves the initial preliminary deep learning experiments conducted prior to implementing end-to-end transformer fine-tuning.

### Archived Files
- **`telecom_voc_comment_type_classification_colab.ipynb`**:  
  Initial Colab exploration for 5-class operational category classification using:
  1. Multilingual MiniLM embeddings (`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`) + MLP head.
  2. PyTorch BiLSTM + Bahdanau attention.
  3. **BUET BanglaBERT as a Frozen Feature Extractor (`csebuetnlp/banglabert`)**: 
     In this experiment, the 12 transformer encoder layers were frozen (`torch.no_grad()`), and only a shallow 2-layer MLP head was trained on static 768-dimensional embeddings.

---

## 📊 Empirical Findings & Why It Was Superseded

| Model Architecture | Approach | 5-Fold CV Accuracy | Macro-F1 | Status |
| :--- | :--- | :---: | :---: | :--- |
| **BUET BanglaBERT (Frozen Head)** | Static 768-dim embeddings + 2-layer MLP | **74.88%** | **0.6253** | ❌ Underperformed Classical Ensemble (87.44%) |
| **BUET BanglaBERT (Fine-Tuned)** | Full 12-layer backpropagation (`dl/finetune_banglabert.py`) | **85.27%** | **0.7624** | 🏆 **+10.39% leap** over frozen baseline |

### Why Frozen Feature Extraction Failed
Pre-trained BanglaBERT representations were trained primarily on formal Bengali web text (Wikipedia, news articles). When presented with customer reviews containing:
- Heavy phonetic Romanized Bengali ("Banglish") like *"MB er dam beshi"*, *"balance kete niyeche"*, *"faltu network"*,
- Telecom domain abbreviations (*"VAS"*, *"OTP"*, *"4G"*),

a frozen feature extractor cannot adapt its sub-word token attention weights to these out-of-domain patterns. 

By propagating gradients through all 12 transformer layers during **end-to-end fine-tuning**, the model adapted its internal self-attention heads to telecom domain vocabulary, increasing category accuracy from **74.88% to 85.27%** and achieving state-of-the-art sentiment accuracy of **91.60%**.

The frozen head setup is preserved here purely as an academic ablation baseline.
