import os
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
import joblib

# Paths setup (strictly confined to ml/ directory and reading from data/processed)
ML_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = ML_DIR.parent
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
MODELS_DIR = ML_DIR / "models"
REPORTS_DIR = ML_DIR / "reports"

MODELS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def load_dataset() -> pd.DataFrame:
    """Load and combine processed customer reviews from all three operators."""
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
    
    # Drop rows where review_text or sentiment is null/empty
    combined_df = combined_df.dropna(subset=["review_text", "sentiment"]).copy()
    combined_df["review_text"] = combined_df["review_text"].astype(str).str.strip()
    combined_df = combined_df[combined_df["review_text"].str.len() > 0].copy()
    
    # Standardize sentiment labels
    combined_df["sentiment"] = combined_df["sentiment"].astype(str).str.strip()
    valid_sentiments = {"Positive", "Negative", "Neutral"}
    combined_df = combined_df[combined_df["sentiment"].isin(valid_sentiments)].reset_index(drop=True)

    print(f"Loaded {len(combined_df)} total cleaned reviews across 3 operators.")
    print("Class distribution:")
    for label, count in combined_df["sentiment"].value_counts().items():
        pct = (count / len(combined_df)) * 100
        print(f"  - {label}: {count} ({pct:.2f}%)")

    return combined_df


def get_tfidf_vectorizer() -> TfidfVectorizer:
    """Create Character N-Gram TF-IDF Feature Extractor."""
    return TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(2, 5),
        min_df=3,
        sublinear_tf=True,
    )


def build_models():
    """Build baseline, primary, and challenger pipelines."""
    models = {
        "Statistical Floor (Dummy - Most Frequent)": Pipeline([
            ("tfidf", get_tfidf_vectorizer()),
            ("classifier", DummyClassifier(strategy="most_frequent")),
        ]),
        "Primary (Balanced Logistic Regression)": Pipeline([
            ("tfidf", get_tfidf_vectorizer()),
            ("classifier", LogisticRegression(
                class_weight="balanced",
                max_iter=1000,
                random_state=42,
            )),
        ]),
        "Challenger (Balanced LinearSVC)": Pipeline([
            ("tfidf", get_tfidf_vectorizer()),
            ("classifier", LinearSVC(
                class_weight="balanced",
                random_state=42,
            )),
        ]),
    }
    return models


def evaluate_models_cross_validation(df: pd.DataFrame):
    """Run 5-Fold Stratified Cross Validation and print Macro-F1 comparison."""
    X = df["review_text"]
    y = df["sentiment"]

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scoring = {
        "macro_f1": "f1_macro",
        "weighted_f1": "f1_weighted",
        "accuracy": "accuracy",
    }

    results = {}
    models = build_models()

    print("\n" + "=" * 60)
    print("5-FOLD STRATIFIED CROSS-VALIDATION BENCHMARK")
    print("=" * 60)

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
        mean_acc = np.mean(scores["test_accuracy"])
        std_acc = np.std(scores["test_accuracy"])

        results[name] = {
            "mean_macro_f1": mean_macro_f1,
            "std_macro_f1": std_macro_f1,
            "mean_accuracy": mean_acc,
            "std_accuracy": std_acc,
            "raw_scores": scores["test_macro_f1"],
        }

        print(f"  Macro-F1 : {mean_macro_f1:.4f} (±{std_macro_f1:.4f})")
        print(f"  Accuracy : {mean_acc:.4f} (±{std_acc:.4f})")
        print(f"  Folds    : {[round(s, 4) for s in scores['test_macro_f1']]}")

    return results


def train_and_export_final_model(df: pd.DataFrame):
    """Train primary model on full dataset and export model artifact."""
    X = df["review_text"]
    y = df["sentiment"]

    print("\n" + "=" * 60)
    print("TRAINING FINAL PRIMARY LOGISTIC REGRESSION MODEL")
    print("=" * 60)

    primary_pipeline = Pipeline([
        ("tfidf", get_tfidf_vectorizer()),
        ("classifier", LogisticRegression(
            class_weight="balanced",
            max_iter=1000,
            random_state=42,
        )),
    ])

    primary_pipeline.fit(X, y)
    
    model_path = MODELS_DIR / "primary_logistic_regression.joblib"
    joblib.dump(primary_pipeline, model_path)
    print(f"Model successfully saved to: {model_path}")

    # Also train and save challenger model
    challenger_pipeline = Pipeline([
        ("tfidf", get_tfidf_vectorizer()),
        ("classifier", LinearSVC(
            class_weight="balanced",
            random_state=42,
        )),
    ])
    challenger_pipeline.fit(X, y)
    challenger_path = MODELS_DIR / "challenger_linearsvc.joblib"
    joblib.dump(challenger_pipeline, challenger_path)
    print(f"Challenger model saved to: {challenger_path}")

    return primary_pipeline


def test_sample_predictions(model):
    """Test the trained primary pipeline with various sample queries."""
    sample_texts = [
        "Network speed khub e baje, 4G thakleo kono kaje ase na",  # Banglish Negative
        "খুব সুন্দর এবং সহজ অ্যাপ, অনেক সুবিধা পাই",             # Bengali Positive
        "Good application but data pack price is too high",       # English Mixed/Neutral-Negative
        "Emergency internet option its very very good services", # English Positive
        "faltu service kono kajer na akdom useless",              # Banglish Negative
        "App open hocche na shudhu loading dekhasse",             # Banglish Negative (Login bug)
        "মোটামুটি চলে তবে আরও উন্নতি দরকার",                       # Bengali Neutral
    ]

    print("\n" + "=" * 60)
    print("SAMPLE PREDICTIONS (PRIMARY LOGISTIC REGRESSION)")
    print("=" * 60)

    for text in sample_texts:
        pred_label = model.predict([text])[0]
        probs = model.predict_proba([text])[0]
        prob_dict = {cls: round(prob, 4) for cls, prob in zip(model.classes_, probs)}
        print(f"\nReview : \"{text}\"")
        print(f"Prediction : {pred_label}")
        print(f"Probabilities : {prob_dict}")


if __name__ == "__main__":
    df = load_dataset()
    cv_results = evaluate_models_cross_validation(df)
    primary_model = train_and_export_final_model(df)
    test_sample_predictions(primary_model)
