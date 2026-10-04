import os
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.naive_bayes import ComplementNB
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    f1_score,
    accuracy_score,
)
from sklearn.model_selection import StratifiedKFold, cross_validate
import joblib

# Paths setup
ML_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = ML_DIR.parent
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
MODELS_DIR = ML_DIR / "models"
REPORTS_DIR = ML_DIR / "reports"

MODELS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

VALID_CATEGORIES = [
    "General Appreciation / Other",
    "Offers & Data Packs",
    "App Login & Technical Bugs",
    "Network Speed & 4G Latency",
    "Billing & Airtime Deductions",
]


def load_category_dataset() -> pd.DataFrame:
    """Load and combine processed customer reviews with operational categories."""
    files = {
        "Grameenphone": PROCESSED_DATA_DIR / "mygp_classified_reviews.csv",
        "Banglalink": PROCESSED_DATA_DIR / "mybl_classified_reviews.csv",
        "Robi": PROCESSED_DATA_DIR / "myrobi_classified_reviews.csv",
    }

    dfs = []
    for operator, filepath in files.items():
        if not filepath.exists():
            raise FileNotFoundError(f"Processed file not found at: {filepath}")
        df = pd.read_csv(filepath)
        if "operator" not in df.columns:
            df["operator"] = operator
        dfs.append(df)

    combined_df = pd.concat(dfs, ignore_index=True)

    # Drop nulls
    combined_df = combined_df.dropna(subset=["review_text", "category"]).copy()
    combined_df["review_text"] = combined_df["review_text"].astype(str).str.strip()
    combined_df = combined_df[combined_df["review_text"].str.len() > 0].copy()

    # Clean categories
    combined_df["category"] = combined_df["category"].astype(str).str.strip()
    combined_df = combined_df[combined_df["category"].isin(VALID_CATEGORIES)].reset_index(drop=True)

    print(f"Loaded {len(combined_df)} cleaned reviews for category classification across 3 operators.")
    print("\nClass distribution:")
    for label, count in combined_df["category"].value_counts().items():
        pct = (count / len(combined_df)) * 100
        print(f"  - {label:32s}: {count:5d} ({pct:5.2f}%)")

    return combined_df


def get_feature_extractor() -> FeatureUnion:
    """
    Combined Sub-word Character N-Gram and Word N-Gram TF-IDF Feature Extractor.
    Captures phonetic Banglish spelling patterns as well as key domain terms
    like 'mb', 'offer', 'net', 'speed', 'login', 'taka', 'kete nei'.
    """
    return FeatureUnion([
        ("word_tfidf", TfidfVectorizer(
            ngram_range=(1, 2),
            min_df=2,
            sublinear_tf=True,
        )),
        ("char_tfidf", TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(3, 5),
            min_df=3,
            sublinear_tf=True,
        )),
    ])


def build_models():
    """Build baseline, logistic regression, calibrated LinearSVC, and ensemble pipelines."""
    feat = get_feature_extractor()

    clf_lr = LogisticRegression(
        class_weight="balanced",
        max_iter=1000,
        random_state=42,
    )
    clf_svc = CalibratedClassifierCV(
        LinearSVC(class_weight="balanced", random_state=42)
    )
    clf_cnb = ComplementNB(norm=True)

    models = {
        "Statistical Floor (Dummy - Most Frequent)": Pipeline([
            ("features", feat),
            ("classifier", DummyClassifier(strategy="most_frequent")),
        ]),
        "Primary Logistic Regression": Pipeline([
            ("features", feat),
            ("classifier", clf_lr),
        ]),
        "Challenger Calibrated LinearSVC": Pipeline([
            ("features", feat),
            ("classifier", clf_svc),
        ]),
        "Soft-Voting Ensemble (Hero Model)": Pipeline([
            ("features", feat),
            ("classifier", VotingClassifier(
                estimators=[("lr", clf_lr), ("svc", clf_svc), ("cnb", clf_cnb)],
                voting="soft",
                weights=[2, 2, 1],
            )),
        ]),
    }
    return models


def evaluate_models_cross_validation(df: pd.DataFrame):
    """Run 5-Fold Stratified Cross-Validation on Category classification."""
    X = df["review_text"]
    y = df["category"]

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scoring = {
        "macro_f1": "f1_macro",
        "weighted_f1": "f1_weighted",
        "accuracy": "accuracy",
    }

    results = {}
    models = build_models()

    print("\n" + "=" * 70)
    print("5-FOLD STRATIFIED CROSS-VALIDATION BENCHMARK (COMMENT TYPES / CATEGORIES)")
    print("=" * 70)

    for name, pipeline in models.items():
        print(f"\nEvaluating: {name} ...")
        scores = cross_validate(
            pipeline,
            X,
            y,
            cv=cv,
            scoring=scoring,
            n_jobs=-1,
            return_train_score=False,
        )

        mean_macro_f1 = np.mean(scores["test_macro_f1"])
        std_macro_f1 = np.std(scores["test_macro_f1"])
        mean_weighted_f1 = np.mean(scores["test_weighted_f1"])
        mean_acc = np.mean(scores["test_accuracy"])
        std_acc = np.std(scores["test_accuracy"])

        results[name] = {
            "mean_macro_f1": mean_macro_f1,
            "std_macro_f1": std_macro_f1,
            "mean_weighted_f1": mean_weighted_f1,
            "mean_acc": mean_acc,
            "std_acc": std_acc,
        }

        print(f"  --> Macro-F1    : {mean_macro_f1:.4f} (+/- {std_macro_f1:.4f})")
        print(f"  --> Weighted-F1 : {mean_weighted_f1:.4f}")
        print(f"  --> Accuracy    : {mean_acc * 100:.2f}% (+/- {std_acc * 100:.2f}%)")

    return results


def train_and_export_category_models(df: pd.DataFrame):
    """Train final category models on entire seed dataset and save to disk."""
    X = df["review_text"]
    y = df["category"]

    print("\n" + "=" * 70)
    print("TRAINING & EXPORTING PRODUCTION CATEGORY MODELS")
    print("=" * 70)

    models = build_models()

    # 1. Primary Logistic Regression
    lr_pipe = models["Primary Logistic Regression"]
    lr_pipe.fit(X, y)
    lr_path = MODELS_DIR / "category_logistic_regression.joblib"
    joblib.dump(lr_pipe, lr_path)
    print(f"Saved: {lr_path.name}")

    # 2. Challenger LinearSVC
    svc_pipe = models["Challenger Calibrated LinearSVC"]
    svc_pipe.fit(X, y)
    svc_path = MODELS_DIR / "category_linearsvc.joblib"
    joblib.dump(svc_pipe, svc_path)
    print(f"Saved: {svc_path.name}")

    # 3. Hero Soft-Voting Ensemble
    ensemble_pipe = models["Soft-Voting Ensemble (Hero Model)"]
    ensemble_pipe.fit(X, y)
    ensemble_path = MODELS_DIR / "category_voting_classifier.joblib"
    joblib.dump(ensemble_pipe, ensemble_path)
    print(f"Saved: {ensemble_path.name}")

    return ensemble_pipe


def generate_markdown_report(results: dict, df: pd.DataFrame, final_model):
    """Generate detailed evaluation report in markdown."""
    X = df["review_text"]
    y = df["category"]
    y_pred = final_model.predict(X)

    report_str = classification_report(y, y_pred, digits=4)
    cm = confusion_matrix(y, y_pred, labels=VALID_CATEGORIES)

    md_content = f"""# Operational Category (Comment Type) Classification Report

## Executive Summary
This report benchmarks Classical Machine Learning models for classifying customer feedback into **5 operational telecom categories** (Comment Types).
Trained on $N = {len(df):,d}$ multi-operator customer reviews across Grameenphone, Robi, and Banglalink.

## 5-Fold Stratified Cross-Validation Benchmark

| Model Architecture | Macro-F1 (Mean ± Std) | Weighted-F1 | Accuracy (Mean ± Std) | Status |
| :--- | :---: | :---: | :---: | :---: |
"""
    for name, m in results.items():
        status = "Baseline Floor" if "Dummy" in name else ("Hero Model" if "Ensemble" in name else "Candidate")
        md_content += f"| **{name}** | {m['mean_macro_f1']:.4f} ± {m['mean_macro_f1']:.4f} | {m['mean_weighted_f1']:.4f} | {m['mean_acc']*100:.2f}% ± {m['std_acc']*100:.2f}% | {status} |\n"

    md_content += f"""
## Final Hero Model (Soft-Voting Ensemble) Full Dataset Evaluation

```
{report_str}
```

## Category Confusion Matrix (Full Seed Corpus)

Categories order:
1. `General Appreciation / Other`
2. `Offers & Data Packs`
3. `App Login & Technical Bugs`
4. `Network Speed & 4G Latency`
5. `Billing & Airtime Deductions`

```
{cm}
```

## Deployed Artifacts
- **Primary Logistic Regression**: `ml/models/category_logistic_regression.joblib`
- **Challenger Calibrated LinearSVC**: `ml/models/category_linearsvc.joblib`
- **Soft-Voting Ensemble (Hero Model)**: `ml/models/category_voting_classifier.joblib`
"""
    report_file = REPORTS_DIR / "category_classification_report.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"\nReport generated at: {report_file}")


def test_sample_predictions(model):
    """Test sample real-world Bengali/Banglish reviews covering all 5 categories."""
    samples = [
        ("Network speed khub e baje, 4G thakleo net chole na", "Network Speed & 4G Latency"),
        ("Taka kete niyeche kintu MB dey nai, faltu system", "Billing & Airtime Deductions"),
        ("App open hocche na shudhu loading dekhasse otp ashe na", "App Login & Technical Bugs"),
        ("Offer gulo onek dam, kom dame bhalo data pack chai", "Offers & Data Packs"),
        ("Onek valo app, sob kichu sundor bhabe kora jay", "General Appreciation / Other"),
    ]

    print("\n" + "=" * 70)
    print("SAMPLE INFERENCE ON REAL-WORLD REVIEWS")
    print("=" * 70)
    for text, expected in samples:
        pred = model.predict([text])[0]
        probs = model.predict_proba([text])[0]
        conf = np.max(probs) * 100
        print(f"\nText     : \"{text}\"")
        print(f"Expected : {expected}")
        print(f"Predicted: {pred} (Confidence: {conf:.1f}%)")


if __name__ == "__main__":
    df = load_category_dataset()
    results = evaluate_models_cross_validation(df)
    hero_model = train_and_export_category_models(df)
    generate_markdown_report(results, df, hero_model)
    test_sample_predictions(hero_model)
