# Operational Category (Comment Type) Classification Report

## Executive Summary
This report benchmarks Classical Machine Learning models for classifying customer feedback into **5 operational telecom categories** (Comment Types).
Trained on $N = 4,500$ multi-operator customer reviews across Grameenphone, Robi, and Banglalink.

## 5-Fold Stratified Cross-Validation Benchmark (Classical ML)

| Model Architecture | Macro-F1 (Mean ± Std) | Weighted-F1 | Accuracy (Mean ± Std) | Status |
| :--- | :---: | :---: | :---: | :---: |
| **Statistical Floor (Dummy - Most Frequent)** | 0.1511 ± 0.0001 | 0.4584 | 60.69% ± 0.04% | Baseline Floor |
| **Primary Logistic Regression** | 0.7845 ± 0.0135 | 0.8730 | 87.16% ± 0.86% | Candidate |
| **Challenger Calibrated LinearSVC** | 0.7664 ± 0.0160 | 0.8654 | 86.91% ± 0.74% | Candidate |
| **Soft-Voting Ensemble (Hero Model)** | **0.7794 ± 0.0146** | **0.8717** | **87.33% ± 0.81%** | **Hero Model** |

## Google Colab GPU Benchmark (Multi-Paradigm Comparison)
Trained and verified on Google Colab with NVIDIA T4 GPU across 5-Fold Stratified CV:

| Model Paradigm | Macro-F1 | Accuracy | Key Strengths / Characteristics |
| :--- | :---: | :---: | :--- |
| 🏆 **Soft-Voting Ensemble ML** | **0.7794** | **87.33%** | Best overall; sub-word n-grams capture domain tokens (`mb`, `otp`, `taka`) |
| 🚀 **Multilingual MiniLM Transformer Head** | 0.7247 | 81.15% | High multilingual cross-lingual density (384-dim) |
| 🧠 **Hybrid BiLSTM + Attention (GPU)** | 0.7106 | 80.84% | Strong sequential modeling with Char-CNN morphology |
| 🇧🇩 **BUET BanglaBERT Head** | 0.6253 | 74.88% | Native Bengali representations; sensitive to Romanized Banglish |

## Final Hero Model (Soft-Voting Ensemble) Full Dataset Evaluation

```
                              precision    recall  f1-score   support

  App Login & Technical Bugs     0.9804    1.0000    0.9901       400
Billing & Airtime Deductions     0.9909    1.0000    0.9954       217
General Appreciation / Other     0.9996    0.9839    0.9917      2731
  Network Speed & 4G Latency     0.9504    1.0000    0.9746       364
         Offers & Data Packs     0.9813    0.9987    0.9899       788

                    accuracy                         0.9900      4500
                   macro avg     0.9805    0.9965    0.9883      4500
                weighted avg     0.9903    0.9900    0.9900      4500
```

## Category Confusion Matrix (Full Seed Corpus)

Categories order:
1. `General Appreciation / Other`
2. `Offers & Data Packs`
3. `App Login & Technical Bugs`
4. `Network Speed & 4G Latency`
5. `Billing & Airtime Deductions`

```
[[2687   15    8   19    2]
 [   1  787    0    0    0]
 [   0    0  400    0    0]
 [   0    0    0  364    0]
 [   0    0    0    0  217]]
```

## Deployed Artifacts
- **Primary Logistic Regression**: `ml/models/category_logistic_regression.joblib`
- **Challenger Calibrated LinearSVC**: `ml/models/category_linearsvc.joblib`
- **Soft-Voting Ensemble (Hero Model)**: `ml/models/category_voting_classifier.joblib`
