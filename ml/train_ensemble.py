import os
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.naive_bayes import ComplementNB
from sklearn.ensemble import VotingClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, cross_validate
import joblib

ML_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = ML_DIR.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"
MODELS_DIR = ML_DIR / "models"
REPORTS_DIR = ML_DIR / "reports"

MODELS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def load_dataset() -> pd.DataFrame:
    files = {
        "Grameenphone": DATA_DIR / "mygp_classified_reviews.csv",
        "Banglalink": DATA_DIR / "mybl_classified_reviews.csv",
        "Robi": DATA_DIR / "myrobi_classified_reviews.csv",
    }
    dfs = []
    for op, path in files.items():
        d = pd.read_csv(path)
        if "operator" not in d.columns:
            d["operator"] = op
        dfs.append(d)
        
    df = pd.concat(dfs, ignore_index=True)
    df = df.dropna(subset=["review_text", "sentiment"]).copy()
    df["review_text"] = df["review_text"].astype(str).str.strip()
    df = df[df["review_text"].str.len() > 0]
    df = df[df["sentiment"].isin(["Positive", "Negative", "Neutral"])].reset_index(drop=True)
    return df


def build_ensemble_pipeline():
    tfidf = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(2, 5),
        min_df=3,
        sublinear_tf=True,
    )
    
    clf1 = LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42)
    clf2 = CalibratedClassifierCV(LinearSVC(class_weight="balanced", random_state=42))
    clf3 = ComplementNB(norm=True)
    
    ensemble = Pipeline([
        ("tfidf", tfidf),
        ("voting", VotingClassifier(
            estimators=[("lr", clf1), ("svc", clf2), ("cnb", clf3)],
            voting="soft",
            weights=[2, 2, 1],
        ))
    ])
    return ensemble


def evaluate_and_train():
    df = load_dataset()
    X = df["review_text"]
    y = df["sentiment"]
    
    print("=" * 65)
    print("5-FOLD STRATIFIED CV: SOFT-VOTING ENSEMBLE ML")
    print("=" * 65)
    
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    ensemble = build_ensemble_pipeline()
    
    scores = cross_validate(
        ensemble,
        X,
        y,
        cv=cv,
        scoring={"f1_macro": "f1_macro", "accuracy": "accuracy"},
        n_jobs=-1,
    )
    
    f1_mean = np.mean(scores["test_f1_macro"])
    f1_std = np.std(scores["test_f1_macro"])
    acc_mean = np.mean(scores["test_accuracy"])
    acc_std = np.std(scores["test_accuracy"])
    
    print(f"Ensemble Macro-F1 : {f1_mean:.4f} (±{f1_std:.4f})")
    print(f"Ensemble Accuracy : {acc_mean * 100:.2f}% (±{acc_std * 100:.2f}%)")
    print(f"Folds Macro-F1    : {[round(s, 4) for s in scores['test_f1_macro']]}")
    
    print("\nFitting final model on all 4,500 reviews...")
    ensemble.fit(X, y)
    out_path = MODELS_DIR / "ensemble_voting_classifier.joblib"
    joblib.dump(ensemble, out_path)
    print(f"Ensemble model saved to: {out_path}")
    return ensemble


if __name__ == "__main__":
    evaluate_and_train()
