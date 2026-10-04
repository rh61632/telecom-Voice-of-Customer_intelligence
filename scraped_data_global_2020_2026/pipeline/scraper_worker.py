"""
Script: scraper_worker.py
Purpose: High-throughput Google Play review scraper for a single operator using country='us'.
Target window: January 1, 2020 00:00:00 to September 30, 2026 23:59:59.
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
END_DATE = datetime(2026, 9, 30, 23, 59, 59)

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


def run_scraper(op_key: str):
    if op_key not in CONFIGS:
        print(f"Unknown operator key: {op_key}. Choose from: gp, bl, robi")
        sys.exit(1)

    cfg = CONFIGS[op_key]
    op_name = cfg["operator"]
    app_id = cfg["app_id"]
    out_csv = cfg["out_csv"]

    print("=" * 70)
    print(f"STARTING GLOBAL SCRAPER: {op_name} ({app_id})")
    print(f"Target Window : {START_DATE.strftime('%Y-%m-%d')} to {END_DATE.strftime('%Y-%m-%d')}")
    print(f"Output CSV    : {out_csv}")
    print("=" * 70)

    # Initialize CSV if not exists or start fresh
    csv_file = open(out_csv, "w", encoding="utf-8", newline="")
    writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
    writer.writeheader()
    csv_file.flush()

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
                    print(f"[{op_name}] Empty batch received (token active). Retrying in 3s (attempt {empty_retries}/5)...")
                    time.sleep(3)
                    continue
                else:
                    print(f"[{op_name}] Batch {batch_num}: Returned 0 reviews or token exhausted.")
                    break
            empty_retries = 0

            valid_rows = []
            for r in batch:
                rev_dt = r.get("at")
                if not rev_dt:
                    continue

                # Skip anything in October 2026 or later
                if rev_dt > END_DATE:
                    continue

                # If review is older than 2020-01-01, we reached the start boundary!
                if rev_dt < START_DATE:
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
                writer.writerows(valid_rows)
                csv_file.flush()
                scraped_count += len(valid_rows)
                earliest_date_str = valid_rows[-1]["review_date"][:10]

            if batch_num % 5 == 0 or hit_start_boundary:
                update_progress(cfg, scraped_count, earliest_date_str, status="running")
                print(f"[{op_name}] Batch {batch_num:4d} | Total: {scraped_count:6,d} | Earliest: {earliest_date_str}")

            if hit_start_boundary:
                print(f"[{op_name}] Reached Jan 1, 2020 start boundary! Stopping.")
                break

            if token is None:
                print(f"[{op_name}] Continuation token is None. Server ceiling reached.")
                break

            time.sleep(0.2)

        status_final = "completed" if hit_start_boundary or token is None else "stopped"
        update_progress(cfg, scraped_count, earliest_date_str, status=status_final)
        print(f"\n✓ Finished {op_name}: {scraped_count:,d} reviews collected. Earliest: {earliest_date_str}")

    except Exception as e:
        print(f"[{op_name}] Critical error: {e}")
        update_progress(cfg, scraped_count, earliest_date_str, status="error", error=e)
    finally:
        csv_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Google Play Single Operator Scraper")
    parser.add_argument("--operator", "-o", type=str, required=True, choices=["gp", "bl", "robi"])
    args = parser.parse_args()
    run_scraper(args.operator)
