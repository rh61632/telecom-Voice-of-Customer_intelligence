# 📡 Telecom VoC Deep Learning & Colab Suites

This folder contains the complete Deep Learning pipeline and **GPU-accelerated Google Colab notebooks**:

### 🏆 1. Master Unified Colab Suite (All ML + DL Models in One File)
* [**`telecom_voc_master_unified_colab.ipynb`**](file:///home/ratul/Github/telecom-Voice-of-Customer_intelligence/dl/telecom_voc_master_unified_colab.ipynb): **Complete All-in-One Suite**. Trains and benchmarks **both Sentiment Analysis and Operational Comment Types** across Classical Soft-Voting Ensembles, Hybrid BiLSTM+Attention (PyTorch), and Multilingual Sentence Transformers with automated 1-click model download.
  * **Direct Colab Link**:
    ```text
    https://colab.research.google.com/github/rh61632/telecom-Voice-of-Customer_intelligence/blob/main/dl/telecom_voc_master_unified_colab.ipynb
    ```

### Specialized Single-Task Notebooks
2. [**`telecom_voc_deep_learning_colab.ipynb`**](file:///home/ratul/Github/telecom-Voice-of-Customer_intelligence/dl/telecom_voc_deep_learning_colab.ipynb): Focused **Sentiment Classification** (Positive, Neutral, Negative).
3. [**`telecom_voc_comment_type_classification_colab.ipynb`**](file:///home/ratul/Github/telecom-Voice-of-Customer_intelligence/dl/telecom_voc_comment_type_classification_colab.ipynb): Focused **Comment Type / Operational Category** (5 Classes).

---

## 🚀 How to Run in Google Colab (Free GPU)

### 1. Comment Type / Operational Category Classification Notebook
* **Direct Colab Link**:
  ```text
  https://colab.research.google.com/github/rh61632/telecom-Voice-of-Customer_intelligence/blob/main/dl/telecom_voc_comment_type_classification_colab.ipynb
  ```
* **Or Upload Directly**:
  1. Go to [Google Colab](https://colab.research.google.com).
  2. Click **Upload** ➔ Select `dl/telecom_voc_comment_type_classification_colab.ipynb`.
  3. Ensure GPU is enabled: **Runtime** ➔ **Change runtime type** ➔ **T4 GPU** ➔ **Save**.
  4. Run all cells (`Runtime` ➔ `Run all`).

### 2. Sentiment Classification Notebook
* **Direct Colab Link**:
  ```text
  https://colab.research.google.com/github/rh61632/telecom-Voice-of-Customer_intelligence/blob/main/dl/telecom_voc_deep_learning_colab.ipynb
  ```

---

## 🧠 Notebook Capabilities

1. **Zero Local Compute**: Everything trains in the cloud on free Google Colab Nvidia T4 GPUs.
2. **Automated Setup**: Clones the repository, installs dependencies, and prepares all 4,499 operational reviews across Grameenphone, Banglalink, and Robi.
3. **4-Paradigm Benchmark (5-Fold Stratified CV)**:
   - 🏆 **Soft-Voting Ensemble ML**: Dual Char (3-5) + Word (1-2) TF-IDF + Logistic Regression + LinearSVC + ComplementNB.
   - 🧠 **Hybrid BiLSTM + Bahdanau Attention**: Dual Word + Char-CNN embeddings with inverse class weighting.
   - 🚀 **Multilingual MiniLM Transformer**: 384-dimensional dense semantic sentence representations.
   - 🇧🇩 **BUET BanglaBERT**: 768-dimensional native Bengali contextual representations.
4. **Live Interactive Testing**: Test any custom Banglish or Bengali review in real time.
5. **Model Checkpointing & Download**: Automatically packages trained models into a zip file and triggers a browser download.
