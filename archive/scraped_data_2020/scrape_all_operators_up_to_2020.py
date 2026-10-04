import os
import sys
import time
from datetime import datetime
from pathlib import Path
import pandas as pd
from google_play_scraper import Sort, reviews

# STRICT REPOSITORY INTEGRITY: Everything is saved strictly in scraped_data_2020/
SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent if SCRIPT_DIR.name == "pipeline" else SCRIPT_DIR
RAW_DIR = BASE_DIR / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# Target Window: From January 1, 2020 00:00:00 up until September 30, 2026 23:59:59
START_DATE = datetime(2020, 1, 1, 0, 0, 0)
END_DATE = datetime(2026, 9, 30, 23, 59, 59)

OPERATORS = [
    {
        "name": "Grameenphone",
        "app_id": "com.portonics.mygp",
        "output_file": RAW_DIR / "mygp_scraped_2020_to_sep2026.csv",
    },
    {
        "name": "Banglalink",
        "app_id": "com.arena.banglalinkmela.app",
        "output_file": RAW_DIR / "mybl_scraped_2020_to_sep2026.csv",
    },
    {
        "name": "Robi",
        "app_id": "net.omobio.robisc",
        "output_file": RAW_DIR / "myrobi_scraped_2020_to_sep2026.csv",
    },
]


def format_review_row(r: dict, operator_name: str, rev_date: datetime) -> dict:
    """Format and map Google Play Store review item."""
    return {
        "user_name": str(r.get("userName", "A Google user")),
        "rating": int(r.get("score", 0)),
        "review_date": rev_date.strftime("%Y-%m-%d %H:%M:%S"),
        "review_text": str(r.get("content", "")).strip(),
        "thumbs_up": int(r.get("thumbsUpCount", 0)),
        "operator": operator_name,
    }


def scrape_operator(operator_info: dict, max_retries: int = 5):
    name = operator_info["name"]
    app_id = operator_info["app_id"]
    out_file = operator_info["output_file"]

    print("\n" + "=" * 70)
    print(f"SCRAPING OPERATOR: {name} ({app_id})")
    print(f"Target Window    : {START_DATE.strftime('%Y-%m-%d')} to {END_DATE.strftime('%Y-%m-%d')} (Up until Sept 2026)")
    print(f"Destination File : {out_file}")
    print("=" * 70)

    all_reviews = []
    token = None
    page = 0
    skipped_october_count = 0
    hit_start_boundary = False
    consecutive_empty = 0

    while True:
        page += 1
        retries = 0
        batch = None

        while retries < max_retries:
            try:
                batch, token = reviews(
                    app_id,
                    lang="en",
                    country="bd",
                    sort=Sort.NEWEST,
                    count=199,
                    continuation_token=token,
                )
                break
            except Exception as e:
                retries += 1
                wait_time = retries * 3
                print(f"  [Attempt {retries}/{max_retries}] API / Network error: {e}. Retrying in {wait_time}s...")
                time.sleep(wait_time)

        if not batch:
            consecutive_empty += 1
            print(f"  Page {page}: Received empty review batch. (Empty streak: {consecutive_empty})")
            if consecutive_empty >= 3 or (token and token.token is None):
                print(f"  [Stream Finished] No more reviews available from Google Play Store for {name}.")
                break
            time.sleep(2)
            continue
        else:
            consecutive_empty = 0

        # Filter reviews strictly within [START_DATE, END_DATE]
        for r in batch:
            rev_date = r.get("at")
            if not rev_date:
                continue

            # Ensure rev_date is a datetime object
            if isinstance(rev_date, str):
                try:
                    rev_date = datetime.fromisoformat(rev_date)
                except ValueError:
                    continue

            # 1. If review is newer than Sept 30, 2026 (e.g. October 2026), skip it
            if rev_date > END_DATE:
                skipped_october_count += 1
                continue

            # 2. If review is older than Jan 1, 2020, we have reached the past boundary
            if rev_date < START_DATE:
                hit_start_boundary = True
                break

            # 3. Valid review inside window: filter out ultra-short spam (< 3 characters)
            content = str(r.get("content", "")).strip()
            if len(content) >= 3:
                all_reviews.append(format_review_row(r, name, rev_date))

        oldest_in_batch = batch[-1].get("at")
        print(f"  Page {page:4d} | Batch: {len(batch):3d} | Kept (Window): {len(all_reviews):6d} | Skipped >Sep2026: {skipped_october_count:4d} | Oldest Batch Date: {oldest_in_batch}")

        # Checkpoint save every 5 pages (~1,000 reviews)
        if page % 5 == 0 and all_reviews:
            df_cp = pd.DataFrame(all_reviews)
            df_cp.to_csv(out_file, index=False)
            print(f"  >> Checkpoint saved: {len(df_cp)} reviews written to '{out_file.name}'")

        if hit_start_boundary:
            print(f"\n  [Target Boundary Reached] Encountered reviews prior to {START_DATE.strftime('%Y-%m-%d')}. Concluding scrape for {name}.")
            break

        if token is None or token.token is None:
            print(f"  [End of Stream] Google Play returned no further continuation token for {name}.")
            break

        # Polite delay to respect Google Play rate limits
        time.sleep(1.0)

    # Save final dataset for this operator
    df_final = pd.DataFrame(all_reviews)
    df_final.to_csv(out_file, index=False)
    print(f"\nFinished scraping {name}! Total reviews in window (2020 - Sep 2026): {len(df_final)}")
    if len(df_final) > 0:
        print(f"  Date range captured: {df_final['review_date'].min()} to {df_final['review_date'].max()}")
    return df_final


def main():
    combined_dfs = []
    for op in OPERATORS:
        df_op = scrape_operator(op)
        if len(df_op) > 0:
            combined_dfs.append(df_op)

    if combined_dfs:
        combined_df = pd.concat(combined_dfs, ignore_index=True)
        combined_file = RAW_DIR / "all_operators_scraped_2020_to_sep2026.csv"
        combined_df.to_csv(combined_file, index=False)

        print("\n" + "=" * 70)
        print("ALL OPERATOR SCRAPING COMPLETE")
        print(f"Total reviews saved across all operators: {len(combined_df)}")
        print(f"Combined dataset saved to: {combined_file}")
        print("=" * 70)
    else:
        print("\nNo reviews collected.")


if __name__ == "__main__":
    main()
