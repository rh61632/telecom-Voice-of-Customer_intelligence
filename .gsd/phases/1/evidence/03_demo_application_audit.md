# Empirical Evidence: Interactive Demo Application Audit (`demo/app.py`)

## 1. Executive Summary & Audit Overview

This audit performs a strict read-only examination of the Gradio interactive web application located in `demo/app.py` and its configuration in `demo/requirements.txt`. The demo application provides an interactive decision-support interface allowing real-time classification of Bengali, Banglish, and English telecom reviews with confidence gauges, class probability distributions, and operational subsystem attribution.

This audit evaluates four key areas:
1. **Component Wiring & UI Output Mapping Defect:** Identification of an unrendered UI component (`out_cat`) caused by omitted return variables and incomplete callback output lists.
2. **Training Corpus Claim Inaccuracy:** Discrepancy between stated training volume ($N = 655,649$) and empirical ground truth ($N = 4,500$).
3. **Paper Title Leakage & Academic Decoupling:** Markdown footer metadata citation of the research paper title in relation to commit `4d5aaad` and repository decoupling.
4. **Runtime Dependency Gaps & Model Loading Architecture:** Analysis of `demo/requirements.txt` vs actual runtime import chains (`nltk` omission) and model artifact loading.

---

## 2. Component Wiring & UI Output Mapping Defect

### 2.1 Code Trace & Root Cause Analysis

In `demo/app.py`, the user interface instantiates a dedicated display textbox for the operational category prediction at line 97:

```python
# demo/app.py:93-98
with gr.Column(scale=1):
    with gr.Row():
        out_lang = gr.Textbox(label="Detected Language / Modality", interactive=False)
        out_sent = gr.Textbox(label="Sentiment Polarity", interactive=False)
    
    out_cat = gr.Textbox(label="Operational Domain", interactive=False)
```

Within the prediction callback function `analyze_review`, the operational category text string and confidence percentage are explicitly computed at line 38:

```python
# demo/app.py:34-38
res = predict_sentiment(review_text, sentiment_model, model_name, category_model)

lang_badge = f"{res['language']} {'(Code-Mixed)' if res['is_code_mixed'] else ''}"
sentiment_label = f"{res['sentiment']} ({res['confidence'] * 100:.1f}%)"
category_label = f"{res['category']} ({res['category_confidence'] * 100:.1f}%)"
```

However, the return statements in `analyze_review` return only 5 values, completely omitting `category_label`:

```python
# demo/app.py:30-31 (Empty input early return)
if not review_text or not review_text.strip():
    return "N/A", "N/A", {}, {}, "Please enter a customer review."

# demo/app.py:54 (Standard prediction return)
return lang_badge, sentiment_label, res["probabilities"], cat_probs, diagnostic_summary
```

Correspondingly, the Gradio event listener on line 105 registers only 5 target output widgets, omitting `out_cat`:

```python
# demo/app.py:105-109
submit_btn.click(
    fn=analyze_review,
    inputs=[input_text],
    outputs=[out_lang, out_sent, out_sent_probs, out_cat_probs, out_diag]
)
```

### 2.2 Empirical Impact & Bug Manifestation

| Output Index | Callback Return Value | Registered Output Widget | Resulting UI Behavior |
|:---:|:---|:---|:---|
| 1 | `lang_badge` (str) | `out_lang` (`gr.Textbox`) | Correctly shows detected language / modality |
| 2 | `sentiment_label` (str) | `out_sent` (`gr.Textbox`) | Correctly shows sentiment polarity with confidence |
| **MISSING** | **`category_label`** (str) | **`out_cat`** (`gr.Textbox`) | **PERMANENTLY BLANK (`""`) in web UI** |
| 3 | `res["probabilities"]` (dict) | `out_sent_probs` (`gr.Label`) | Correctly displays top-3 sentiment probabilities |
| 4 | `cat_probs` (dict) | `out_cat_probs` (`gr.Label`) | Correctly displays top-5 operational probabilities |
| 5 | `diagnostic_summary` (str) | `out_diag` (`gr.Markdown`) | Correctly displays architectural triage markdown |

**Consequence:** While the probability distribution for operational categories renders properly in `out_cat_probs` (`gr.Label`), the prominent single-line summary textbox `out_cat` (`"Operational Domain"`) remains permanently unpopulated on all classifications.

### 2.3 Proposed Fix

To resolve this defect, two lines in `demo/app.py` require surgical updating:

1. Update `analyze_review`:
   - Line 31: `return "N/A", "N/A", "N/A", {}, {}, "Please enter a customer review."`
   - Line 54: `return lang_badge, sentiment_label, category_label, res["probabilities"], cat_probs, diagnostic_summary`
2. Update `submit_btn.click`:
   - Line 108: `outputs=[out_lang, out_sent, out_cat, out_sent_probs, out_cat_probs, out_diag]`

---

## 3. Training Corpus Claim Inaccuracy

### 3.1 Headline Claim

In `demo/app.py:63-69`, the markdown banner at the top of the interface states:

```python
# demo/app.py:63-69
with gr.Blocks(title="Telecom VoC Intelligence", css=custom_css, theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 📱 Telecom Voice-of-Customer (VoC) Intelligence & Cross-Layer Diagnostics
        ### High-Throughput Multilingual Customer Intelligence for Telecommunications Self-Care Apps
        *Trained on 655,649 longitudinal customer reviews across Grameenphone, Robi Axiata, and Banglalink (2016–2026).*
        """
    )
```

### 3.2 Reconciliation Against Ground Truth

| Metric | Stated in `demo/app.py:67` | Empirical Truth in Codebase | Source of Ground Truth |
|:---|:---:|:---:|:---|
| **Ensemble Training Samples ($N$)** | `655,649` reviews | **`4,500`** reviews | `data/processed/{mygp,myrobi,mybl}_classified_reviews.csv` |
| **Model Nature** | Stated as "Trained on" | Trained on curated seed; inference run on 655k | `ml/train_ensemble.py`, `ml/train_category_models.py` |
| **655,649 Role** | Described as training set | Common-window longitudinal **inference** corpus | `scraped_data_global/classified/common_duration_summary.json` |

**Analysis:**
The claim *"Trained on 655,649 longitudinal customer reviews..."* is factually incorrect. The production machine learning models (`ensemble_voting_classifier.joblib` and `category_voting_classifier.joblib`) were trained on $N = 4,500$ LLM/human-labeled seed reviews (1,500 reviews per operator). The $655,649$ reviews constitute the unlabeled/evaluated Google Play Store multi-year production dataset that was *scored by* the models, not used to train them.

**Recommended Correction:**
Update line 67 to:
`*Inference evaluated across 655,649 longitudinal customer reviews (2016–2026); Core ensemble trained on N=4,500 curated seed reviews with human gold-standard validation.*`

---

## 4. Paper Title Leakage & Academic Decoupling

### 4.1 Markdown Citation in Demo

In `demo/app.py:111-117`, the interface footer renders:

```python
# demo/app.py:111-117
gr.Markdown(
    """
    ---
    **Research Paper:** *“With Great Reviews Comes Great Responsibility: An Intelligent Decision Support System for Telecommunications Voice-of-the-Customer Diagnostics and Cross-Layer Subsystem Decoupling”*  
    **Replication Codebase:** [GitHub Repository](https://github.com/rh61632/telecom-Voice-of-Customer_intelligence) | **Model Weights:** [Hugging Face Hub](https://huggingface.co/models?search=telecom-voc-banglabert)
    """
)
```

### 4.2 Decoupling Policy & Anonymity Audit

1. **Commit `4d5aaad` Context:**
   - Commit `4d5aaad` decoupled research paper deliverables by reorganizing academic manuscripts into `paper/` and establishing double-blind compliance.
   - In `demo/app.py`, the exact full academic title of the initial manuscript is exposed in plaintext.
2. **Public vs Blinded Presentation:**
   - The paper itself in `paper/eswa_latex/manuscript.tex` underwent a title revision to:
     * *“An Intelligent Decision Support System for Telecommunications Voice-of-the-Customer Diagnostics and Cross-Layer Subsystem Decoupling”*
     (dropping the playful *"With Great Reviews Comes Great Responsibility"* prefix for peer-reviewed journal submission).
   - The demo application retains the earlier, informal working title.
   - For public portfolio deployment, this linkage is beneficial for academic attribution; however, for double-blind peer review submission, this title exposure links the public repository `rh61632` directly with the manuscript.

---

## 5. Runtime Dependencies & Model Loading Verification

### 5.1 Dependency Analysis (`demo/requirements.txt`)

`demo/requirements.txt` specifies:
```text
gradio>=4.0.0
scikit-learn>=1.3.0
joblib>=1.3.0
numpy>=1.24.0
scipy>=1.10.0
```

However, tracing the import graph of `demo/app.py`:
1. `demo/app.py:13` imports `from ml.language_detector import detector`.
2. `ml/language_detector.py:18` imports `from nltk.corpus import words`.
3. `ml/language_detector.py:28-29` executes `import nltk` and `nltk.download("words", quiet=True)`.

**Critical Gap:** `nltk` is **absent** from `demo/requirements.txt`.
If an engineer or automated deployment container (e.g., Hugging Face Spaces Docker container) installs only `demo/requirements.txt`, launching `demo/app.py` triggers an immediate runtime exception:
`ModuleNotFoundError: No module named 'nltk'`

Furthermore, `demo/app.py` requires `pandas` (imported via `ml.feature_engineering` in `ml.predict`), which is also omitted from `demo/requirements.txt`.

### 5.2 Model Loading Verification

In `demo/app.py:16-19`:
```python
sentiment_model, model_name = load_model("ensemble")
category_model = load_category_model()
```

- `load_model("ensemble")` resolves to `ml/models/ensemble_voting_classifier.joblib` (3.98 MB, verified present on disk).
- `load_category_model()` resolves to `ml/models/category_voting_classifier.joblib` (8.52 MB, verified present on disk).
- Both models load successfully when scikit-learn is present and compatible.
- Note: Both models loaded here are the **unfiltered** full models ($N = 4,499$), not the short-text filtered models (`sentiment_ensemble_filtered_min3words.joblib`, `category_ensemble_filtered_min3words.joblib`).

---

## 6. Summary of Actionable Discrepancies

| ID | Issue | Location | Severity | Action Required |
|---|---|---|---|---|
| **DEMO-01** | `out_cat` textbox never populated | `demo/app.py:31,54,108` | High (UI Functionality) | Add `category_label` to returns & `out_cat` to click outputs |
| **DEMO-02** | Stated training size ($655,649$) conflates training with evaluation corpus | `demo/app.py:67` | Medium (Factual Accuracy) | Clarify: 655k evaluated, 4,500 trained |
| **DEMO-03** | Missing runtime dependencies | `demo/requirements.txt` | High (Deployment Blocker) | Add `nltk>=3.8` and `pandas>=2.0.0` |
| **DEMO-04** | Title discrepancy vs active ESWA manuscript | `demo/app.py:114` | Low (Documentation Drift) | Synchronize title with active manuscript |
