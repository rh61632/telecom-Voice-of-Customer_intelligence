"""
Script: scraper_worker.py
Purpose: High-throughput Google Play review scraper for a single operator using country='us'.
Default (full) mode: January 1, 2020 00:00:00 to today.
Incremental mode (--incremental): only fetches reviews newer than the most recent
  review already saved in the raw CSV, then appends and deduplicates by review_id.
Saves continuously to CSV and writes real-time progress to a JSON status file.
"""

import sys
import os
import time
import json
import argparse
import csv
from datetime import datetime
from pathlib import Path
from google_play_scraper import Sort, reviews

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
TARGET_DIR = PROJECT_ROOT / "scraped_data_global_2020_2026"
RAW_DIR = TARGET_DIR / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

START_DATE = datetime(2020, 1, 1, 0, 0, 0)
END_DATE   = datetime.now().replace(hour=23, minute=59, second=59, microsecond=0)

CONFIGS = {
    "gp": {
        "operator": "Grameenphone",
        "app_id": "com.portonics.mygp",
        "out_csv": RAW_DIR / "mygp_global_2020_to_sep2026.csv",
        "progress_json": TARGET_DIR / "progress_gp.json",
    },
    "bl": {
        "operator": "Banglalink",
        "app_id": "com.arena.banglalinkmela.app",
        "out_csv": RAW_DIR / "mybl_global_2020_to_sep2026.csv",
        "progress_json": TARGET_DIR / "progress_bl.json",
    },
    "robi": {
        "operator": "Robi",
        "app_id": "net.omobio.robisc",
        "out_csv": RAW_DIR / "myrobi_global_2020_to_sep2026.csv",
        "progress_json": TARGET_DIR / "progress_robi.json",
    },
}

FIELDNAMES = [
    "review_id",
    "user_name",
    "rating",
    "review_date",
    "review_text",
    "thumbs_up",
    "operator",
]


def update_progress(cfg, scraped_count, earliest_date, status="running", error=None):
    data = {
        "operator": cfg["operator"],
        "app_id": cfg["app_id"],
        "scraped_count": scraped_count,
        "earliest_date": earliest_date,
        "status": status,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    if error:
        data["error"] = str(error)
    try:
        with open(cfg["progress_json"], "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass


def get_existing_review_ids_and_cutoff(out_csv: Path):
    """Read existing CSV and return (set of review_ids, newest review datetime).

    Used in incremental mode to:
      1. Know where to stop fetching (stop when we hit a review older than cutoff).
      2. Deduplicate any overlap at the boundary after merging.
    """
    if not out_csv.exists():
        return set(), START_DATE

    import pandas as pd
    try:
        df = pd.read_csv(out_csv, usecols=["review_id", "review_date"], low_memory=False)
        df["review_date"] = pd.to_datetime(df["review_date"], errors="coerce")
        df = df.dropna(subset=["review_date"])
        if df.empty:
            return set(), START_DATE
        cutoff = df["review_date"].max().to_pydatetime()
        existing_ids = set(df["review_id"].dropna().astype(str).tolist())
        return existing_ids, cutoff
    except Exception as e:
        print(f"Warning: could not read existing CSV for incremental mode: {e}")
        return set(), START_DATE


def run_scraper(op_key: str, incremental: bool = False):
    if op_key not in CONFIGS:
        print(f"Unknown operator key: {op_key}. Choose from: gp, bl, robi")
        sys.exit(1)

    cfg = CONFIGS[op_key]
    op_name = cfg["operator"]
    app_id = cfg["app_id"]
    out_csv = cfg["out_csv"]

    # ── Determine effective start boundary ────────────────────────────────────
    if incremental and out_csv.exists():
        existing_ids, cutoff = get_existing_review_ids_and_cutoff(out_csv)
        effective_start = cutoff
        mode_label = f"INCREMENTAL (cutoff: {cutoff.strftime('%Y-%m-%d %H:%M:%S')})"
        print(f"  Found {len(existing_ids):,d} existing reviews. Will only fetch reviews newer than cutoff.")
    else:
        existing_ids = set()
        effective_start = START_DATE
        mode_label = f"FULL (from {START_DATE.strftime('%Y-%m-%d')})"

    print("=" * 70)
    print(f"STARTING SCRAPER: {op_name} ({app_id})")
    print(f"Mode          : {mode_label}")
    print(f"End Date      : {END_DATE.strftime('%Y-%m-%d')}")
    print(f"Output CSV    : {out_csv}")
    print("=" * 70)

    # ── Open CSV for writing ───────────────────────────────────────────────────
    # Incremental: open in append mode and collect new rows separately for dedup.
    # Full: overwrite from scratch.
    new_rows = []  # collected in memory; written + merged at end in incremental mode

    if not incremental:
        csv_file = open(out_csv, "w", encoding="utf-8", newline="")
        writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        writer.writeheader()
        csv_file.flush()
    else:
        csv_file = None  # will write at end
        writer = None

    token = None
    batch_num = 0
    scraped_count = 0
    earliest_date_str = "N/A"
    hit_start_boundary = False
    max_retries = 5
    empty_retries = 0

    update_progress(cfg, 0, earliest_date_str, status="running")

    try:
        while not hit_start_boundary:
            batch_num += 1
            batch = None
            retries = 0

            while retries < max_retries:
                try:
                    batch, token = reviews(
                        app_id,
                        lang="en",
                        country="us",
                        sort=Sort.NEWEST,
                        count=199,
                        continuation_token=token,
                    )
                    break
                except Exception as e:
                    retries += 1
                    print(f"[{op_name}] Warning: Retry {retries}/{max_retries} on batch {batch_num} due to: {e}")
                    time.sleep(2 * retries)

            if not batch:
                if token is not None and empty_retries < 5:
                    empty_retries += 1
                    print(f"[{op_name}] Empty batch (token active). Retrying in 3s (attempt {empty_retries}/5)...")
                    time.sleep(3)
                    continue
                else:
                    print(f"[{op_name}] Batch {batch_num}: 0 reviews or token exhausted.")
                    break
            empty_retries = 0

            valid_rows = []
            for r in batch:
                rev_dt = r.get("at")
                if not rev_dt:
                    continue

                # Skip future reviews beyond today
                if rev_dt > END_DATE:
                    continue

                # In incremental mode: stop when we reach the cutoff boundary
                if rev_dt <= effective_start:
                    hit_start_boundary = True
                    break

                row = {
                    "review_id": str(r.get("reviewId", "")),
                    "user_name": str(r.get("userName", "A Google user")),
                    "rating": int(r.get("score", 0)),
                    "review_date": rev_dt.strftime("%Y-%m-%d %H:%M:%S"),
                    "review_text": str(r.get("content", "")).strip(),
                    "thumbs_up": int(r.get("thumbsUpCount", 0)),
                    "operator": op_name,
                }
                valid_rows.append(row)

            if valid_rows:
                if incremental:
                    new_rows.extend(valid_rows)
                else:
                    writer.writerows(valid_rows)
                    csv_file.flush()
                scraped_count += len(valid_rows)
                earliest_date_str = valid_rows[-1]["review_date"][:10]

            if batch_num % 5 == 0 or hit_start_boundary:
                update_progress(cfg, scraped_count, earliest_date_str, status="running")
                print(f"[{op_name}] Batch {batch_num:4d} | New: {scraped_count:6,d} | Earliest: {earliest_date_str}")

            if hit_start_boundary:
                print(f"[{op_name}] Reached cutoff boundary ({effective_start.strftime('%Y-%m-%d')}). Stopping.")
                break

            if token is None:
                print(f"[{op_name}] Continuation token exhausted. Server ceiling reached.")
                break

            time.sleep(0.2)

        # ── Incremental merge & dedup ─────────────────────────────────────────
        if incremental and new_rows:
            import pandas as pd
            new_df = pd.DataFrame(new_rows, columns=FIELDNAMES)
            # Filter out any review_ids already in the existing file (boundary overlap)
            if existing_ids:
                new_df = new_df[~new_df["review_id"].astype(str).isin(existing_ids)]
            print(f"[{op_name}] Appending {len(new_df):,d} genuinely new reviews (after dedup).")
            if len(new_df) > 0:
                # Append to existing CSV
                new_df.to_csv(out_csv, mode="a", header=not out_csv.exists(), index=False)
        elif incremental and not new_rows:
            print(f"[{op_name}] No new reviews found since last scrape. Dataset is up to date.")

        status_final = "completed" if hit_start_boundary or token is None else "stopped"
        update_progress(cfg, scraped_count, earliest_date_str, status=status_final)
        mode_str = "incremental" if incremental else "full"
        print(f"\n✓ Finished {op_name} ({mode_str}): {scraped_count:,d} new reviews. Earliest new: {earliest_date_str}")

    except Exception as e:
        print(f"[{op_name}] Critical error: {e}")
        update_progress(cfg, scraped_count, earliest_date_str, status="error", error=e)
    finally:
        if csv_file:
            csv_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Google Play Single Operator Scraper")
    parser.add_argument("--operator", "-o", type=str, required=True, choices=["gp", "bl", "robi"])
    parser.add_argument(
        "--incremental", action="store_true",
        help=(
            "Only fetch reviews newer than the most recent review already in the raw CSV. "
            "Appends new rows and deduplicates by review_id. Much faster for routine refreshes."
        )
    )
    args = parser.parse_args()
    run_scraper(args.operator, incremental=args.incremental)

