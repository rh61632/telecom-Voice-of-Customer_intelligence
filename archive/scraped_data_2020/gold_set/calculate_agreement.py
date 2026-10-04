"""
Script: calculate_agreement.py
Purpose: Compute Cohen's Kappa and inter-annotator agreement between Ratul and second annotator (Friend).
"""

from pathlib import Path
import pandas as pd
from sklearn.metrics import cohen_kappa_score, confusion_matrix

GOLD_DIR = Path(__file__).resolve().parent
RATUL_CSV = GOLD_DIR / "blind_annotation_600_ratul.csv"
FRIEND_CSV = GOLD_DIR / "blind_annotation_200_friend.csv"


def evaluate_agreement():
    print("=" * 70)
    print("      INTER-ANNOTATOR AGREEMENT & COHEN'S KAPPA EVALUATION")
    print("=" * 70)

    if not RATUL_CSV.exists() or not FRIEND_CSV.exists():
        print("Missing annotation CSV files.")
        return

    df_r = pd.read_csv(RATUL_CSV)
    df_f = pd.read_csv(FRIEND_CSV)

    merged = pd.merge(
        df_r[["sample_id", "operator", "rating", "review_text", "sentiment_label"]],
        df_f[["sample_id", "sentiment_label"]],
        on="sample_id",
        suffixes=("_ratul", "_friend"),
    )

    # Filter to annotated rows
    r_valid = df_r["sentiment_label"].fillna("").astype(str).str.strip()
    f_valid = df_f["sentiment_label"].fillna("").astype(str).str.strip()

    r_annotated_count = (r_valid != "").sum()
    f_annotated_count = (f_valid != "").sum()

    m_r = merged["sentiment_label_ratul"].fillna("").astype(str).str.strip()
    m_f = merged["sentiment_label_friend"].fillna("").astype(str).str.strip()
    annotated = merged[(m_r != "") & (m_f != "")].copy()

    total_paired = len(annotated)
    if total_paired == 0:
        print("No overlapping reviews have been annotated by both annotators yet.")
        print(f"Ratul completed : {r_annotated_count} / {len(df_r)}")
        print(f"Friend completed: {f_annotated_count} / {len(df_f)}")
        return

    print(f"Total overlapping reviews evaluated: {total_paired} / {len(merged)}")

    y_ratul = annotated["sentiment_label_ratul"]
    y_friend = annotated["sentiment_label_friend"]

    # Compute Agreement & Kappa
    raw_agreement = (y_ratul == y_friend).mean() * 100
    kappa = cohen_kappa_score(y_ratul, y_friend)

    print(f"\n📊 RESULTS:")
    print(f"  • Raw Percentage Agreement : {raw_agreement:.2f}%")
    print(f"  • Cohen's Kappa (κ)         : {kappa:.4f}")

    # Interpret Kappa
    if kappa > 0.80:
        interp = "Near Perfect Agreement"
    elif kappa > 0.60:
        interp = "Substantial Agreement"
    elif kappa > 0.40:
        interp = "Moderate Agreement"
    else:
        interp = "Fair / Slight Agreement"
    print(f"  • Interpretation            : {interp}")

    labels = ["Positive", "Neutral", "Negative"]
    cm = confusion_matrix(y_ratul, y_friend, labels=labels)
    cm_df = pd.DataFrame(cm, index=[f"Ratul_{l}" for l in labels], columns=[f"Friend_{l}" for l in labels])
    print(f"\nConfusion Matrix:\n{cm_df}")

    # Disagreements
    disagreements = annotated[y_ratul != y_friend]
    if len(disagreements) > 0:
        print(f"\nDisagreements ({len(disagreements)} cases):")
        for _, row in disagreements.head(10).iterrows():
            print(f"  [{row['sample_id']}] Ratul: {row['sentiment_label_ratul']} vs Friend: {row['sentiment_label_friend']}")
            print(f"    Rating: {row['rating']}★ | \"{row['review_text']}\"\n")


if __name__ == "__main__":
    evaluate_agreement()
