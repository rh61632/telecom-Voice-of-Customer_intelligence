"""
Script: generate_blind_samples.py
Purpose:
  1. Check for data leakage against the 4,500 training seed reviews and strictly exclude any overlap.
  2. Draw a balanced, blind sample of 600 reviews (200 Grameenphone, 200 Banglalink, 200 Robi) for Ratul.
  3. Draw a stratified random subsample of 200 reviews from those 600 for Ratul's friend (for Cohen's Kappa).
  4. Hide all model suggestions and scrub PII (user_name, etc.) to eliminate confirmation bias.
"""

from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
COMMON_CSV = PROJECT_ROOT / "scraped_data_2020" / "common_duration" / "classified_all_operators_pretrained.csv"
TRAIN_DIR = PROJECT_ROOT / "data" / "processed"
GOLD_DIR = PROJECT_ROOT / "scraped_data_2020" / "gold_set"
GOLD_DIR.mkdir(parents=True, exist_ok=True)

RATUL_600_CSV = GOLD_DIR / "blind_annotation_600_ratul.csv"
FRIEND_200_CSV = GOLD_DIR / "blind_annotation_200_friend.csv"


def generate_blind_datasets():
    print("=" * 70)
    print("GENERATING ZERO-LEAKAGE BLIND ANNOTATION DATASETS")
    print("=" * 70)

    # 1. Load training seed reviews to prevent leakage
    train_files = list(TRAIN_DIR.glob("*_classified_reviews.csv"))
    train_texts = set()
    for f in train_files:
        df_train = pd.read_csv(f)
        if "review_text" in df_train.columns:
            cleaned = df_train["review_text"].dropna().astype(str).str.strip().str.lower()
            train_texts.update(cleaned)
    print(f"Loaded {len(train_texts):,d} unique training seed reviews to exclude.")

    # 2. Load Common Duration Dataset
    if not COMMON_CSV.exists():
        raise FileNotFoundError(f"Missing {COMMON_CSV}")
    
    df_all = pd.read_csv(COMMON_CSV)
    print(f"Loaded {len(df_all):,d} total reviews from common duration window.")

    # 3. Filter out training seed overlap
    df_all["clean_text_check"] = df_all["review_text"].dropna().astype(str).str.strip().str.lower()
    leakage_mask = df_all["clean_text_check"].isin(train_texts)
    print(f"Excluded {leakage_mask.sum():,d} reviews that overlap with training seed data.")
    clean_pool = df_all[~leakage_mask].copy()
    print(f"Available unseen candidate pool: {len(clean_pool):,d} reviews.")

    # 4. Stratified random sampling: 200 per operator = 600 reviews
    rng = np.random.default_rng(42)
    ratul_samples = []
    
    for op in ["Grameenphone", "Banglalink", "Robi"]:
        op_pool = clean_pool[clean_pool["operator"] == op]
        sampled_op = op_pool.sample(n=200, random_state=42)
        ratul_samples.append(sampled_op)

    ratul_df = pd.concat(ratul_samples, ignore_index=True)
    # Shuffle to intermix operators so annotator doesn't see a single block of one operator
    ratul_df = ratul_df.sample(frac=1.0, random_state=42).reset_index(drop=True)
    ratul_df["sample_id"] = [f"BLIND_{i+1:03d}" for i in range(len(ratul_df))]

    # 5. Prepare blind fields (No model predictions, No PII)
    ratul_df["sentiment_label"] = ""
    ratul_df["category_label"] = ""
    ratul_df["annotator_notes"] = ""

    out_cols = [
        "sample_id",
        "operator",
        "rating",
        "review_date",
        "review_text",
        "sentiment_label",
        "category_label",
        "annotator_notes",
    ]

    ratul_df_clean = ratul_df[out_cols].copy()
    ratul_df_clean.to_csv(RATUL_600_CSV, index=False)
    print(f"\n✓ Saved Ratul's 600 Blind Dataset: {RATUL_600_CSV}")
    print(f"  Distribution: {ratul_df_clean['operator'].value_counts().to_dict()}")

    # 6. Sample 200 from the 600 for Ratul's friend (stratified ~67 GP, 67 BL, 66 Robi)
    friend_samples = []
    for op, n_req in [("Grameenphone", 67), ("Banglalink", 67), ("Robi", 66)]:
        op_subset = ratul_df_clean[ratul_df_clean["operator"] == op]
        sampled_friend_op = op_subset.sample(n=n_req, random_state=101)
        friend_samples.append(sampled_friend_op)

    friend_df = pd.concat(friend_samples, ignore_index=True)
    # Shuffle friend dataset too, keeping exact sample_id for exact 1-to-1 join
    friend_df = friend_df.sample(frac=1.0, random_state=101).reset_index(drop=True)
    friend_df.to_csv(FRIEND_200_CSV, index=False)
    print(f"\n✓ Saved Friend's 200 Blind Dataset: {FRIEND_200_CSV}")
    print(f"  Distribution: {friend_df['operator'].value_counts().to_dict()}")
    print("=" * 70)


if __name__ == "__main__":
    generate_blind_datasets()
