"""
Utility: prepare_gold_set.py
Purpose: Create an intelligent candidate sample for human Gold Standard annotation
         and provide an interactive terminal voting tool to easily verify reviews.
"""

import sys
import argparse
from pathlib import Path
import pandas as pd
import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
SCRAPED_DIR = SCRIPT_DIR.parent if SCRIPT_DIR.name == "pipeline" else SCRIPT_DIR
COMMON_DIR = SCRAPED_DIR / "common_duration"
GOLD_DIR = SCRAPED_DIR / "gold_set"
GOLD_DIR.mkdir(parents=True, exist_ok=True)

INPUT_CSV = COMMON_DIR / "classified_all_operators_pretrained.csv"
CANDIDATES_CSV = GOLD_DIR / "gold_set_candidates.csv"
VERIFIED_CSV = GOLD_DIR / "gold_set_verified.csv"


def generate_candidate_sample(sample_size=600):
    print("=" * 70)
    print("GENERATING GOLD STANDARD CANDIDATE DATASET")
    print("=" * 70)

    if not INPUT_CSV.exists():
        print(f"Error: {INPUT_CSV} not found! Run classification first.")
        sys.exit(1)

    df = pd.read_csv(INPUT_CSV)
    print(f"Loaded {len(df):,d} classified reviews.")

    # Identify agreement & disagreement
    df["models_agree"] = (
        (df["pred_ensemble"] == df["pred_logistic"])
        & (df["pred_ensemble"] == df["pred_linearsvc"])
        & (df["pred_ensemble"] == df["pred_bilstm"])
    )
    df["is_edge_case"] = ~df["models_agree"]
    df["low_conf"] = df["conf_ensemble"] < 0.65

    print(f"  - Full 4-Model Agreement : {df['models_agree'].sum():,d} ({df['models_agree'].mean()*100:.1f}%)")
    print(f"  - Model Disagreements    : {df['is_edge_case'].sum():,d} ({df['is_edge_case'].mean()*100:.1f}%)")
    print(f"  - Low Confidence (<65%)  : {df['low_conf'].sum():,d} ({df['low_conf'].mean()*100:.1f}%)")

    # Stratified candidate sampling per operator
    per_op = sample_size // 3
    sampled_dfs = []

    for op in ["Grameenphone", "Banglalink", "Robi"]:
        op_df = df[df["operator"] == op]

        # 50% Consensus cases (high confidence)
        n_agree = int(per_op * 0.50)
        agree_sub = op_df[op_df["models_agree"]].sample(n=min(n_agree, len(op_df[op_df["models_agree"]])), random_state=42)

        # 30% Disagreement edge cases
        n_disagree = int(per_op * 0.30)
        disagree_pool = op_df[op_df["is_edge_case"]]
        disagree_sub = disagree_pool.sample(n=min(n_disagree, len(disagree_pool)), random_state=42)

        # 20% Low-confidence cases
        n_low = per_op - len(agree_sub) - len(disagree_sub)
        low_pool = op_df[op_df["low_conf"] & ~op_df.index.isin(agree_sub.index) & ~op_df.index.isin(disagree_sub.index)]
        if len(low_pool) > 0:
            low_sub = low_pool.sample(n=min(n_low, len(low_pool)), random_state=42)
        else:
            low_sub = op_df.sample(n=n_low, random_state=42)

        sampled_dfs.extend([agree_sub, disagree_sub, low_sub])

    candidates = pd.concat(sampled_dfs, ignore_index=True)
    candidates = candidates.sample(frac=1.0, random_state=42).reset_index(drop=True)
    candidates["review_id"] = [f"VOC_{i+1:04d}" for i in range(len(candidates))]

    candidates["gold_sentiment"] = ""  # Left blank for human annotator
    candidates["annotator_notes"] = ""

    output_cols = [
        "review_id",
        "operator",
        "rating",
        "review_date",
        "review_text",
        "pred_ensemble",
        "conf_ensemble",
        "pred_bilstm",
        "pred_logistic",
        "models_agree",
        "gold_sentiment",
        "annotator_notes",
    ]

    candidates[output_cols].to_csv(CANDIDATES_CSV, index=False)
    print(f"\nSaved {len(candidates)} candidate reviews to: {CANDIDATES_CSV.name}")
    print(f"Candidates per operator: {candidates['operator'].value_counts().to_dict()}")
    return candidates


def run_interactive_annotator():
    print("=" * 70)
    print("INTERACTIVE GOLD STANDARD ANNOTATION TOOL")
    print("=" * 70)

    # Check if verified progress exists, otherwise start from candidates
    if VERIFIED_CSV.exists():
        df = pd.read_csv(VERIFIED_CSV)
        print(f"Resuming from existing progress: {VERIFIED_CSV.name}")
    elif CANDIDATES_CSV.exists():
        df = pd.read_csv(CANDIDATES_CSV)
        print(f"Starting fresh from: {CANDIDATES_CSV.name}")
    else:
        print("Candidates CSV not found. Generating now...")
        df = generate_candidate_sample()

    # Ensure sentiment columns can store strings without LossySetitemError
    df["gold_sentiment"] = df["gold_sentiment"].astype(object)
    if "annotator_notes" in df.columns:
        df["annotator_notes"] = df["annotator_notes"].astype(object)

    total = len(df)
    labeled_count = (df["gold_sentiment"].fillna("").astype(str).str.strip() != "").sum()
    print(f"Status: {labeled_count}/{total} reviews already verified.\n")
    print("Controls:")
    print("  [1] Vote Negative")
    print("  [2] Vote Neutral")
    print("  [3] Vote Positive")
    print("  [Enter] Accept Ensemble Suggestion (shown in brackets)")
    print("  [b] Back / Undo previous review")
    print("  [s] Skip this review")
    print("  [edit <num>] Jump to edit a specific review (e.g. 'edit 99')")
    print("  [q] Save & Quit\n")

    val_map = {"1": "Negative", "2": "Neutral", "3": "Positive"}

    # Start at the first unvoted review
    idx = 0
    while idx < total:
        val = str(df.at[idx, "gold_sentiment"]).strip()
        if val in ("", "nan"):
            break
        idx += 1

    history = []

    while idx < total:
        row = df.iloc[idx]
        review_id = row.get("review_id", f"REV_{idx+1}")
        operator = row["operator"]
        rating = row["rating"]
        text = str(row["review_text"])
        ens_pred = row["pred_ensemble"]
        ens_conf = float(row["conf_ensemble"]) if pd.notnull(row.get("conf_ensemble")) else 0.0
        lstm_pred = row["pred_bilstm"]
        is_agree = row.get("models_agree", True)
        current_vote = str(row.get("gold_sentiment", "")).strip()
        if current_vote == "nan":
            current_vote = ""

        print("-" * 70)
        status_tag = f" [Current Vote: {current_vote}]" if current_vote else ""
        print(f"[{review_id}] ({idx+1}/{total}) | Operator: {operator} | Rating: {rating} ★{status_tag}")
        print(f"Text: \"{text}\"")
        lr_pred = row.get("pred_logistic", "N/A")
        if not is_agree:
            print(f"⚠️  DISAGREEMENT: Ensemble={ens_pred} ({ens_conf*100:.1f}%) | BiLSTM={lstm_pred} | LogReg={lr_pred}")
        else:
            print(f"✓  All Models Agree: {ens_pred} (Confidence: {ens_conf*100:.1f}%)")

        default_suggestion = ens_pred if not current_vote else current_vote

        while True:
            choice = input(f"Vote [1:Neg, 2:Neu, 3:Pos, Enter={default_suggestion}, b:Back, s:Skip, q:Quit]: ").strip()
            choice_lower = choice.lower()

            if choice_lower == "q":
                df.to_csv(VERIFIED_CSV, index=False)
                new_count = (df["gold_sentiment"].fillna("").astype(str).str.strip() != "").sum()
                print(f"\nProgress saved to {VERIFIED_CSV.name} ({new_count}/{total} verified). Goodbye!")
                return
            elif choice_lower == "b":
                if history:
                    idx = history.pop()
                    print(f"\n⏪ Stepping back to Review {idx + 1}...")
                    break
                elif idx > 0:
                    idx -= 1
                    print(f"\n⏪ Stepping back to Review {idx + 1}...")
                    break
                else:
                    print("Already at the very first review.")
            elif choice_lower.startswith("edit "):
                target = choice_lower.replace("edit", "").strip()
                try:
                    target_idx = int(target) - 1
                    if 0 <= target_idx < total:
                        history.append(idx)
                        idx = target_idx
                        print(f"\n🎯 Jumping to Review {idx + 1}...")
                        break
                    else:
                        print(f"Review number must be between 1 and {total}.")
                except ValueError:
                    print("Invalid review number. Usage: edit 99")
            elif choice_lower == "s":
                print("Skipped.")
                history.append(idx)
                idx += 1
                break
            elif choice == "":
                # Accept suggestion
                df.at[idx, "gold_sentiment"] = default_suggestion
                print(f"Voted: {default_suggestion} ✓")
                history.append(idx)
                idx += 1
                break
            elif choice in val_map:
                vote = val_map[choice]
                df.at[idx, "gold_sentiment"] = vote
                print(f"Voted: {vote} ✓")
                history.append(idx)
                idx += 1
                break
            else:
                print("Invalid input. Type 1, 2, 3, b (back), s (skip), q (quit), or press Enter.")

        # Auto-save every 10 annotations
        if len(history) % 10 == 0:
            df.to_csv(VERIFIED_CSV, index=False)

    df.to_csv(VERIFIED_CSV, index=False)
    final_count = (df["gold_sentiment"].fillna("").astype(str).str.strip() != "").sum()
    print(f"\nAll done! {final_count}/{total} reviews verified in '{VERIFIED_CSV.name}'.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gold Standard Dataset Manager")
    parser.add_argument("--interactive", "-i", action="store_true", default=True, help="Launch interactive CLI voting tool (Default)")
    parser.add_argument("--generate", "-g", action="store_true", help="Re-generate fresh candidate sample")
    parser.add_argument("--sample-size", "-s", type=int, default=600, help="Candidate sample size (default: 600)")
    args = parser.parse_args()

    if args.generate:
        generate_candidate_sample(sample_size=args.sample_size)
    else:
        run_interactive_annotator()
