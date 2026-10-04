"""
Interactive Blind Review Annotator
Purpose: Annotate customer reviews without unintentional bias (model suggestions are hidden).
Features:
  - 100% blind (model predictions hidden).
  - Explicit keystroke required (no accept-with-Enter shortcut).
  - Auto-saves after every review.
  - Resume from where you left off.
  - Back/Skip/Quit options.
"""

import sys
import argparse
import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_CSV = PROJECT_ROOT / "scraped_data_2020" / "gold_set" / "blind_annotation_600_ratul.csv"

SENTIMENT_MAP = {
    "1": "Positive",
    "2": "Neutral",
    "3": "Negative",
}

CATEGORY_MAP = {
    "1": "Billing & Airtime Deductions",
    "2": "App Login & Technical Bugs",
    "3": "Network Speed & 4G Latency",
    "4": "Offers & Data Packs",
    "5": "General Appreciation / Other",
}


def load_dataset(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        rows = list(reader)
    
    # Ensure standard columns exist
    for col in ["sentiment_label", "category_label", "annotator_notes"]:
        if col not in fieldnames:
            fieldnames.append(col)
        for r in rows:
            if col not in r:
                r[col] = ""
    return fieldnames, rows


def save_dataset(file_path: Path, fieldnames, rows):
    with open(file_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def run_annotator(file_path: Path):
    if not file_path.exists():
        print(f"Error: Target file not found at {file_path}")
        sys.exit(1)

    fieldnames, rows = load_dataset(file_path)
    total = len(rows)

    # Find first unannotated row
    unannotated_indices = [
        i for i, r in enumerate(rows)
        if not r.get("sentiment_label") or not r["sentiment_label"].strip()
    ]
    
    if not unannotated_indices:
        print("\n🎉 Congratulations! All reviews in this file have been annotated.")
        print(f"File: {file_path}")
        print("\nSummary of annotations:")
        counts = {}
        for r in rows:
            s = r.get("sentiment_label", "").strip()
            if s:
                counts[s] = counts.get(s, 0) + 1
        for s, c in sorted(counts.items()):
            print(f"  {s}: {c}")
        return

    curr_idx = unannotated_indices[0]

    print("=" * 70)
    print("      BLIND TELECOM VoC ANNOTATION TOOL (ZERO MODEL BIAS)")
    print("=" * 70)
    print(f"File: {file_path.name}")
    print(f"Total reviews: {total} | Completed: {total - len(unannotated_indices)} | Remaining: {len(unannotated_indices)}")
    print("=" * 70)
    print("Controls:")
    print("  [1] Positive   [2] Neutral   [3] Negative")
    print("  [b] Back       [s] Skip      [q] Save & Quit")
    print("=" * 70)

    while curr_idx < total:
        row = rows[curr_idx]
        done_count = sum(1 for r in rows if r.get("sentiment_label") and r["sentiment_label"].strip())
        pct = (done_count / total) * 100

        try:
            r_val = int(row.get("rating", 3))
        except (ValueError, TypeError):
            r_val = 3
        stars = "★" * r_val + "☆" * (5 - r_val)

        print(f"\n--- [{curr_idx + 1}/{total}] (Completed: {done_count}/{total} - {pct:.1f}%) ---")
        print(f"Sample ID : {row.get('sample_id', '')}  |  Operator: {row.get('operator', '')}")
        print(f"Rating    : {row.get('rating', '')}★ ({stars})  |  Date: {row.get('review_date', '')}")
        print(f"Review    : \"{row.get('review_text', '')}\"")
        current_s = row.get("sentiment_label", "").strip()
        current_c = row.get("category_label", "").strip()
        if current_s:
            print(f"Current   : Sentiment: {current_s} | Category: {current_c}")
        print("-" * 70)

        # 1. Sentiment Input
        while True:
            choice = input("Sentiment [1=Pos, 2=Neu, 3=Neg, b=Back, s=Skip, q=Quit] > ").strip().lower()

            if choice in ("q", "quit", "exit"):
                save_dataset(file_path, fieldnames, rows)
                print(f"\n✓ Progress saved to {file_path.name}. Exiting.")
                return

            if choice == "b":
                if curr_idx > 0:
                    curr_idx -= 1
                    break
                else:
                    print("Already at the very first review.")
                    continue

            if choice == "s":
                curr_idx += 1
                break

            if choice in SENTIMENT_MAP:
                sentiment = SENTIMENT_MAP[choice]
                
                # 2. Optional Category Input
                print("\nOptional Category:")
                print("  [1] Billing & Deductions  [2] App Bugs/Login  [3] Network/Speed")
                print("  [4] Offers & Data Packs   [5] General Praise/Other  [Enter to skip]")
                cat_choice = input("Category [1-5 or Enter] > ").strip()
                category = CATEGORY_MAP.get(cat_choice, "")

                # 3. Optional Notes
                notes = ""
                if choice == "2" or (r_val == 5 and choice == "3"):
                    notes_in = input("Notes/Reason (optional, Enter to skip) > ").strip()
                    if notes_in:
                        notes = notes_in

                # Save into row dict
                row["sentiment_label"] = sentiment
                if category:
                    row["category_label"] = category
                if notes:
                    row["annotator_notes"] = notes

                # Persist to disk immediately
                save_dataset(file_path, fieldnames, rows)
                curr_idx += 1
                break
            else:
                print("Invalid input! Please press 1 (Pos), 2 (Neu), 3 (Neg), b (Back), or q (Quit).")

    print("\n🎉 All reviews in this dataset have been annotated!")
    print(f"File saved: {file_path}")


def resolve_target_file(arg_file: str = None) -> Path:
    if arg_file:
        p = Path(arg_file)
        if p.exists():
            return p
        print(f"Error: Specified file does not exist: {arg_file}")
        sys.exit(1)

    # 1. Look in current working directory
    for name in ["blind_annotation_200_friend.csv", "blind_annotation_600_ratul.csv"]:
        cwd_candidate = Path.cwd() / name
        if cwd_candidate.exists():
            return cwd_candidate

    # 2. Look beside this script file
    script_dir = Path(__file__).resolve().parent
    for name in ["blind_annotation_200_friend.csv", "blind_annotation_600_ratul.csv"]:
        beside_candidate = script_dir / name
        if beside_candidate.exists():
            return beside_candidate

    # 3. Look in repo structure
    for name in ["blind_annotation_600_ratul.csv", "blind_annotation_200_friend.csv"]:
        repo_candidate = PROJECT_ROOT / "scraped_data_2020" / "gold_set" / name
        if repo_candidate.exists():
            return repo_candidate

    # 4. Look for any .csv in current working directory
    cwd_csvs = list(Path.cwd().glob("*.csv"))
    if cwd_csvs:
        return cwd_csvs[0]

    print("Error: Could not find any annotation CSV file.")
    print("Please specify the file path: python annotate_blind.py --file <path_to_csv>")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Blind Review Annotation CLI Tool")
    parser.add_argument(
        "--file", "-f",
        type=str,
        default=None,
        help="Path to CSV to annotate (auto-detected if omitted)",
    )
    args = parser.parse_args()
    target_file = resolve_target_file(args.file)
    run_annotator(target_file)


if __name__ == "__main__":
    main()
