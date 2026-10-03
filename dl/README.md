# 📡 Telecom VoC Deep Learning on Google Colab

This folder contains the complete Deep Learning pipeline and an end-to-end, GPU-accelerated **Google Colab notebook**: [`telecom_voc_deep_learning_colab.ipynb`](file:///home/ratul/Github/telecom-Voice-of-Customer_intelligence/dl/telecom_voc_deep_learning_colab.ipynb).

---

## 🚀 How to Run in Google Colab

### Option 1: Direct Upload (Fastest)
1. Navigate to [Google Colab](https://colab.research.google.com).
2. Click **Upload** and select [`dl/telecom_voc_deep_learning_colab.ipynb`](file:///home/ratul/Github/telecom-Voice-of-Customer_intelligence/dl/telecom_voc_deep_learning_colab.ipynb).
3. In Colab, switch to a free GPU:
   * **Runtime** ➔ **Change runtime type** ➔ Select **T4 GPU** ➔ Click **Save**.
4. Run all cells (`Runtime` ➔ `Run all` or `Ctrl + F9`).

### Option 2: Via GitHub URL
Once your changes are pushed to GitHub, open directly via this link:
```text
https://colab.research.google.com/github/rh61632/telecom-Voice-of-Customer_intelligence/blob/main/dl/telecom_voc_deep_learning_colab.ipynb
```

---

## 🧠 Notebook Capabilities

1. **Hardware Detection**: Automatically detects GPU (T4/V100/A100) or CPU and sets PyTorch device.
2. **Automated Setup**: Clones the repository, installs dependencies, and prepares all 4,500 reviews across Grameenphone, Banglalink, and Robi.
3. **Model 1: BiLSTM with Self-Attention & Char-CNN**:
   * Evaluates 5-fold cross-validation on GPU in seconds.
   * Dual word + character convolutions handle phonetic Banglish, Bengali script, and English.
4. **Model 2: Multilingual Transformer (MiniLM)**:
   * Extracts dense multilingual embeddings on GPU in batches.
   * Trains a regularized classification head with 5-fold CV.
5. **Interactive Prediction**:
   * Test any custom review in real-time with visual probability bars.
6. **Model Checkpointing & Download**:
   * Save `.pt` checkpoints directly to local browser download or Google Drive.
