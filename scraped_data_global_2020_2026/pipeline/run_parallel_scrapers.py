"""
Script: run_parallel_scrapers.py
Purpose: Master launcher to run Google Play scrapers for Grameenphone, Banglalink,
         and Robi concurrently in 3 parallel processes.
"""

import sys
import os
import subprocess
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PYTHON_BIN = PROJECT_ROOT / "dl" / ".venv" / "bin" / "python"
if not PYTHON_BIN.exists():
    PYTHON_BIN = sys.executable

WORKER_SCRIPT = PROJECT_ROOT / "scraped_data_global_2020_2026" / "pipeline" / "scraper_worker.py"


def main():
    print("=" * 70)
    print("LAUNCHING 3 PARALLEL SCRAPERS (Grameenphone, Banglalink, Robi)")
    print(f"Target: Jan 1, 2020 to Sep 30, 2026 | Location: US Global Endpoint")
    print("=" * 70)

    operators = ["gp", "bl", "robi"]
    processes = {}

    for op in operators:
        cmd = [str(PYTHON_BIN), str(WORKER_SCRIPT), "--operator", op]
        p = subprocess.Popen(cmd)
        processes[op] = p
        print(f"  ✓ Spawned worker for: {op.upper()} (PID: {p.pid})")

    print("\nAll 3 scrapers are running concurrently in the background.")
    print("Waiting for all workers to complete...\n")

    # Monitor until all are done
    while True:
        alive = {op: p.poll() is None for op, p in processes.items()}
        if not any(alive.values()):
            print("\n🎉 All 3 operator scrapers have finished execution!")
            break
        time.sleep(2)


if __name__ == "__main__":
    main()
