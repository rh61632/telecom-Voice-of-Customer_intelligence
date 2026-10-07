"""
Script: backfill_robi_gap.py
Purpose: Fair multi-rating backfill scraper for Robi (net.omobio.robisc) across
all 5 star ratings (1, 2, 3, 4, 5) to recover the 10-month historical gap
between September 17, 2024 and August 23, 2025.

Methodological Fairness Guarantee:
- Queries all 5 star ratings individually with identical parameters (lang='en', country='us', Sort.NEWEST).
- Retains only reviews within [2024-09-16 00:00:00, 2025-08-25 23:59:59].
- Preserves natural Google Play Store rating distributions without sampling or filtering bias.
- Deduplicates strictly against existing reviews by review_id and (review_date, review_text, user_name).
"""

import sys
import os
import time
import csv
from datetime import datetime
from pathlib import Path
import pandas as pd
from google_play_scraper import reviews, Sort

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
RAW_DIR = REPO_ROOT / "scraped_data_global_2020_2026" / "raw"
ROBI_RAW = RAW_DIR / "myrobi_global_2020_to_sep2026.csv"
BACKFILL_OUT = RAW_DIR / "robi_backfilled_gap_2024_2025.csv"

APP_ID = "net.omobio.robisc"
OPERATOR = "Robi"

START_DATE = datetime(2024, 9, 16, 0, 0, 0)
END_DATE = datetime(2025, 8, 25, 23, 59, 59)

FIELDNAMES = [
    "review_id",
    "user_name",
    "rating",
    "review_date",
    "review_text",
    "thumbs_up",
    "operator",
]


def fetch_star_stream(score: int, max_batches: int = 350):
    print(f"\n--- Fetching Rating {score} Stars (Fair Stream) ---")
    collected = []
    token = None
    batch_num = 0
    t0 = time.time()

    while batch_num < max_batches:
        batch_num += 1
        batch = None
        retries = 0

        while retries < 5:
            try:
                batch, token = reviews(
                    APP_ID,
                    lang="en",
                    country="us",
                    sort=Sort.NEWEST,
                    filter_score_with=score,
                    count=199,
                    continuation_token=token,
                )
                break
            except Exception as e:
                retries += 1
                time.sleep(1.5 * retries)

        if not batch:
            print(f"  [Score {score}] Batch {batch_num}: Empty batch or token exhausted.")
            break

        hit_past_boundary = False
        in_window_count = 0

        for r in batch:
            rev_dt = r.get("at")
            if not rev_dt:
                continue

            if rev_dt > END_DATE:
                continue

            if rev_dt < START_DATE:
                hit_past_boundary = True
                continue

            in_window_count += 1
            row = {
                "review_id": str(r.get("reviewId", "")),
                "user_name": str(r.get("userName", "A Google user")),
                "rating": int(score),
                "review_date": rev_dt.strftime("%Y-%m-%d %H:%M:%S"),
                "review_text": str(r.get("content", "")).strip(),
                "thumbs_up": int(r.get("thumbsUpCount", 0)),
                "operator": OPERATOR,
            }
            collected.append(row)

        if batch_num % 10 == 0 or hit_past_boundary:
            earliest = batch[-1]["at"].strftime("%Y-%m-%d")
            print(f"  [Score {score}] Batch {batch_num:3d} | Reached: {earliest} | Window revs: {len(collected):,d}")

        if hit_past_boundary:
            print(f"  [Score {score}] Reached past start date ({START_DATE.strftime('%Y-%m-%d')}) at batch {batch_num}. Done!")
            break

        if not token:
            print(f"  [Score {score}] Token exhausted at batch {batch_num}.")
            break

        time.sleep(0.05)

    print(f"  [Score {score}] Finished in {time.time()-t0:.1f}s: {len(collected):,d} reviews in window.")
    return collected


def main():
    print("=" * 75)
    print("ROBI HISTORICAL GAP BACKFILL (FAIR 5-STAR COVERAGE)")
    print(f"Window: {START_DATE.strftime('%Y-%m-%d')} to {END_DATE.strftime('%Y-%m-%d')}")
    print("=" * 75)

    # 1. Fetch each star rating
    all_new_reviews = []
    star_counts = {}

    for score in [1, 2, 3, 4, 5]:
        max_b = 320 if score == 5 else 40
        star_reviews = fetch_star_stream(score, max_batches=max_b)
        star_counts[score] = len(star_reviews)
        all_new_reviews.extend(star_reviews)

    print("\n" + "=" * 75)
    print("BACKFILL EXTRACTION SUMMARY ACROSS ALL 5 RATINGS")
    print("=" * 75)
    total_fetched = len(all_new_reviews)
    for score in [1, 2, 3, 4, 5]:
        cnt = star_counts[score]
        pct = (cnt / total_fetched * 100) if total_fetched > 0 else 0
        print(f"  Rating {score} Star: {cnt:6,d} reviews ({pct:5.1f}%)")
    print(f"  Total Fetched : {total_fetched:6,d} reviews")

    if total_fetched == 0:
        print("No reviews fetched. Exiting.")
        return

    # 2. Convert to DataFrame
    df_new = pd.DataFrame(all_new_reviews)
    df_new["review_date"] = pd.to_datetime(df_new["review_date"])

    # Save isolated backfilled slice
    df_new.to_csv(BACKFILL_OUT, index=False)
    print(f"\n✓ Saved raw backfilled slice to: {BACKFILL_OUT.name}")

    # 3. Load existing raw Robi CSV
    print(f"\nLoading existing Robi raw dataset: {ROBI_RAW.name}...")
    df_existing = pd.read_csv(ROBI_RAW, low_memory=False)
    df_existing["review_date"] = pd.to_datetime(df_existing["review_date"], errors="coerce")
    initial_len = len(df_existing)

    # 4. Merge and strict deduplication
    print(f"Existing reviews: {initial_len:,d}")
    combined = pd.concat([df_existing, df_new], ignore_index=True)
    combined = combined.drop_duplicates(subset=["operator", "review_date", "review_text", "user_name"])
    if "review_id" in combined.columns:
        # Also drop duplicates where review_id is valid and non-empty
        valid_id_mask = combined["review_id"].notna() & (combined["review_id"] != "")
        valid_ids = combined[valid_id_mask].drop_duplicates(subset=["review_id"])
        invalid_ids = combined[~valid_id_mask]
        combined = pd.concat([valid_ids, invalid_ids], ignore_index=True)
        combined = combined.drop_duplicates(subset=["operator", "review_date", "review_text", "user_name"])

    # Sort descending by date
    combined = combined.sort_values("review_date", ascending=False).reset_index(drop=True)
    final_len = len(combined)
    added = final_len - initial_len

    print(f"Merged & Deduplicated: {final_len:,d} total reviews (+{added:,d} net new reviews added)")

    # 5. Overwrite raw Robi dataset
    combined.to_csv(ROBI_RAW, index=False)
    print(f"🎉 Updated {ROBI_RAW.name} with complete historical continuity!")

    # 6. Verify monthly continuity
    combined["ym"] = combined["review_date"].dt.to_period("M")
    print("\nUpdated Robi monthly review counts around backfilled window (2024-06 to 2025-10):")
    counts = combined["ym"].value_counts().sort_index().loc["2024-06":"2025-10"]
    for ym, count in counts.items():
        print(f"  {ym}: {count:5,d} reviews")


if __name__ == "__main__":
    main()

