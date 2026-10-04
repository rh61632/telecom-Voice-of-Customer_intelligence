# Operational Category (Comment Type) Classification Report

## Executive Summary
This report benchmarks Classical Machine Learning models for classifying customer feedback into **5 operational telecom categories** (Comment Types).
Trained on $N = 4,499$ multi-operator customer reviews across Grameenphone, Robi, and Banglalink.

## 5-Fold Stratified Cross-Validation Benchmark (Classical ML)

| Model Architecture | Macro-F1 (Mean ± Std) | Weighted-F1 | Accuracy (Mean ± Std) | Status |
| :--- | :---: | :---: | :---: | :---: |
| **Statistical Floor (Dummy - Most Frequent)** | 0.1511 ± 0.0000 | 0.4583 | 60.68% ± 0.03% | Baseline Floor |
| **Primary Logistic Regression** | 0.7781 ± 0.0175 | 0.8682 | 86.44% ± 1.13% | Candidate |
| **Challenger Calibrated LinearSVC** | 0.7687 ± 0.0195 | 0.8676 | 87.09% ± 1.01% | Candidate |
| **Soft-Voting Ensemble (Hero Model)** | **0.7845 ± 0.0190** | **0.8738** | **87.44% ± 0.88%** | **Hero Model** |

## Google Colab GPU Benchmark (Multi-Paradigm Comparison)
Trained and verified on Google Colab with NVIDIA T4 GPU across 5-Fold Stratified CV:

| Model Paradigm | Macro-F1 | Accuracy | Key Strengths / Characteristics |
| :--- | :---: | :---: | :--- |
| 🏆 **Soft-Voting Ensemble ML** | **0.7845** | **87.44%** | Best overall; sub-word n-grams capture domain tokens (`mb`, `otp`, `taka`) |
| 🚀 **Multilingual MiniLM Transformer Head** | 0.7247 | 81.15% | High multilingual cross-lingual density (384-dim) |
| 🧠 **Hybrid BiLSTM + Attention (GPU)** | 0.7106 | 80.84% | Strong sequential modeling with Char-CNN morphology |
| 🇧🇩 **BUET BanglaBERT Head** | 0.6253 | 74.88% | Native Bengali representations; sensitive to Romanized Banglish |

## Final Hero Model (Soft-Voting Ensemble) Full Dataset Evaluation

```
                              precision    recall  f1-score   support

  App Login & Technical Bugs     0.9828    1.0000    0.9913       400
Billing & Airtime Deductions     0.9775    1.0000    0.9886       217
General Appreciation / Other     1.0000    0.9842    0.9921      2730
  Network Speed & 4G Latency     0.9453    0.9973    0.9706       364
         Offers & Data Packs     0.9837    0.9975    0.9905       788

                    accuracy                         0.9898      4499
                   macro avg     0.9779    0.9958    0.9866      4499
                weighted avg     0.9901    0.9898    0.9898      4499

```

## Category Confusion Matrix (Full Seed Corpus)

Categories order:
1. `General Appreciation / Other`
2. `Offers & Data Packs`
3. `App Login & Technical Bugs`
4. `Network Speed & 4G Latency`
5. `Billing & Airtime Deductions`

```
[[2687   13    7   21    2]
 [   0  786    0    0    2]
 [   0    0  400    0    0]
 [   0    0    0  363    1]
 [   0    0    0    0  217]]
```

## Deployed Artifacts
- **Primary Logistic Regression**: `ml/models/category_logistic_regression.joblib`
- **Challenger Calibrated LinearSVC**: `ml/models/category_linearsvc.joblib`
- **Soft-Voting Ensemble (Hero Model)**: `ml/models/category_voting_classifier.joblib`
