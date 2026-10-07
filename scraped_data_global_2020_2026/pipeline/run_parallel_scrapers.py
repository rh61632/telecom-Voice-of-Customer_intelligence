"""
Script: run_parallel_scrapers.py
Purpose: Master launcher to run Google Play scrapers for Grameenphone, Banglalink,
         and Robi concurrently in 3 parallel processes.

Usage:
  Full scrape (first-time or reset):
    python run_parallel_scrapers.py

  Incremental update (only new reviews since last scrape):
    python run_parallel_scrapers.py --incremental
"""

import sys
import os
import argparse
import subprocess
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PYTHON_BIN = PROJECT_ROOT / "dl" / ".venv" / "bin" / "python"
if not PYTHON_BIN.exists():
    PYTHON_BIN = sys.executable

WORKER_SCRIPT = PROJECT_ROOT / "scraped_data_global_2020_2026" / "pipeline" / "scraper_worker.py"


def main():
    parser = argparse.ArgumentParser(description="Launch parallel scrapers for all 3 operators.")
    parser.add_argument(
        "--incremental", action="store_true",
        help=(
            "Only fetch reviews newer than the most recent review already saved. "
            "Appends and deduplicates. Much faster for routine monthly refreshes."
        )
    )
    args = parser.parse_args()
    mode = "INCREMENTAL" if args.incremental else "FULL"

    print("=" * 70)
    print(f"LAUNCHING 3 PARALLEL SCRAPERS — Mode: {mode}")
    print(f"Operators: Grameenphone, Banglalink, Robi  |  Endpoint: US Global")
    print("=" * 70)

    operators = ["gp", "bl", "robi"]
    processes = {}

    for op in operators:
        cmd = [str(PYTHON_BIN), str(WORKER_SCRIPT), "--operator", op]
        if args.incremental:
            cmd.append("--incremental")
        p = subprocess.Popen(cmd)
        processes[op] = p
        print(f"  ✓ Spawned {mode} worker for: {op.upper()} (PID: {p.pid})")

    print("\nAll 3 scrapers are running concurrently in the background.")
    print("Waiting for all workers to complete...\n")

    # Monitor until all are done
    while True:
        alive = {op: p.poll() is None for op, p in processes.items()}
        if not any(alive.values()):
            print("\n🎉 All 3 operator scrapers have finished execution!")
            break
        time.sleep(2)

    if args.incremental:
        print("\nNext step: run merge_and_sync_all_datasets.py to classify new reviews.")
        print("Then update the 'Data Last Scraped' badge in README.md.")


if __name__ == "__main__":
    main()

