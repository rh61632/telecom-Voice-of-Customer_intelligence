#!/usr/bin/env python3
"""
Script: finetune_banglabert.py
Purpose: Full end-to-end fine-tuning of BUET BanglaBERT (csebuetnlp/banglabert)
         for Multilingual Telecom VoC Sentiment Analysis and Operational Category Classification.

Unlike a frozen feature extractor (which only trains a shallow linear head on static embeddings),
this script propagates gradients through all 12 transformer layers (110M parameters),
enabling BanglaBERT to adapt its self-attention representations to telecom domain vocabulary,
Romanized Banglish tokens, and customer complaint nuances.

Supported Tasks:
  - 'sentiment': 3 Classes (Negative, Neutral, Positive)
  - 'category' : 5 Classes (Offers & Data Packs, App Login & Technical Bugs,
                           Network Speed & 4G Latency, Billing & Airtime Deductions,
                           General Appreciation / Other)
  - 'both'     : Trains and evaluates both tasks sequentially.

Usage:
  python dl/finetune_banglabert.py --task both --epochs 4 --batch_size 32
"""

import os
import sys
import time
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.metrics import classification_report, f1_score, accuracy_score
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    get_linear_schedule_with_warmup,
)

# Set up project root and artifact directories
REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_PROCESSED_PRIMARY = REPO_ROOT / "data" / "processed"
DATA_PROCESSED_ARCHIVE = REPO_ROOT / "archive" / "seed_pipeline_groq" / "data" / "processed"
MODELS_DIR = REPO_ROOT / "dl" / "models"
REPORTS_DIR = REPO_ROOT / "dl" / "reports"

MODELS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

MODEL_NAME = "csebuetnlp/banglabert"
SEED = 42

SENTIMENT_LABEL_MAP = {
    "Negative": 0,
    "Neutral": 1,
    "Positive": 2,
}

CATEGORY_LABEL_MAP = {
    "General Appreciation / Other": 0,
    "Offers & Data Packs": 1,
    "App Login & Technical Bugs": 2,
    "Network Speed & 4G Latency": 3,
    "Billing & Airtime Deductions": 4,
}


def set_seed(seed=SEED):
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def load_dataset() -> pd.DataFrame:
    """Load the 4,500 curated ground-truth reviews across GP, Robi, and Banglalink."""
    data_dir = DATA_PROCESSED_PRIMARY if DATA_PROCESSED_PRIMARY.exists() else DATA_PROCESSED_ARCHIVE
    if not data_dir.exists():
        raise FileNotFoundError(f"Could not locate processed data at {DATA_PROCESSED_PRIMARY} or {DATA_PROCESSED_ARCHIVE}")

    files = [
        data_dir / "mygp_classified_reviews.csv",
        data_dir / "myrobi_classified_reviews.csv",
        data_dir / "mybl_classified_reviews.csv",
    ]

    dfs = []
    for f in files:
        if f.exists():
            dfs.append(pd.read_csv(f))

    if not dfs:
        raise FileNotFoundError("No review CSV files found to load.")

    df = pd.concat(dfs, ignore_index=True)
    df = df.dropna(subset=["review_text", "sentiment", "category"]).copy()
    df["review_text"] = df["review_text"].astype(str).str.strip()
    df = df[df["review_text"].str.len() > 0]
    df = df[df["category"] != "Unclassified"].reset_index(drop=True)
    return df


class VoCDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length=96):
        self.texts = list(texts)
        self.labels = list(labels)
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = int(self.labels[idx])
        encoding = self.tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=self.max_length,
            return_tensors="pt",
        )
        return {
            "input_ids": encoding["input_ids"].squeeze(0),
            "attention_mask": encoding["attention_mask"].squeeze(0),
            "label": torch.tensor(label, dtype=torch.long),
        }


def compute_class_weights(labels, num_classes, device):
    """Inverse frequency class weights to balance minority categories and neutral sentiment."""
    counts = np.bincount(labels, minlength=num_classes)
    total = len(labels)
    # Smooth to avoid extreme multipliers
    weights = total / (num_classes * np.maximum(counts, 1).astype(float))
    return torch.tensor(weights, dtype=torch.float, device=device)


def train_epoch(model, dataloader, optimizer, scheduler, criterion, device, scaler=None):
    model.train()
    total_loss = 0.0

    for batch in dataloader:
        optimizer.zero_grad()
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["label"].to(device)

        if scaler is not None:
            with torch.amp.autocast(device_type=device.type):
                outputs = model(input_ids=input_ids, attention_mask=attention_mask)
                loss = criterion(outputs.logits, labels)
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
        else:
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            loss = criterion(outputs.logits, labels)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()

        scheduler.step()
        total_loss += loss.item() * len(labels)

    return total_loss / len(dataloader.dataset)


def evaluate(model, dataloader, device):
    model.eval()
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for batch in dataloader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["label"].to(device)

            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            preds = torch.argmax(outputs.logits, dim=-1)

            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    macro_f1 = f1_score(all_labels, all_preds, average="macro", zero_division=0)
    acc = accuracy_score(all_labels, all_preds)
    return macro_f1, acc, all_labels, all_preds


def run_cv_experiment(df, task, label_map, args, device, tokenizer):
    """Run 5-Fold Stratified Cross Validation to rigorously benchmark BanglaBERT."""
    inv_label_map = {v: k for k, v in label_map.items()}
    num_classes = len(label_map)
    labels = np.array([label_map[item] for item in df[task]])
    texts = df["review_text"].values

    skf = StratifiedKFold(n_splits=args.folds, shuffle=True, random_state=SEED)
    fold_f1_scores = []
    fold_acc_scores = []

    print("\n" + "=" * 75)
    print(f"STARTING {args.folds}-FOLD CV FULL FINE-TUNING: BUET BanglaBERT")
    print(f"Task: {task.upper()} ({num_classes} Classes) | Epochs: {args.epochs} | Batch: {args.batch_size}")
    print(f"Device: {device.type.upper()} ({torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'})")
    print("=" * 75)

    for fold, (train_idx, val_idx) in enumerate(skf.split(texts, labels), 1):
        print(f"\n--- Fold {fold}/{args.folds} (Train: {len(train_idx)}, Val: {len(val_idx)}) ---")

        train_ds = VoCDataset(texts[train_idx], labels[train_idx], tokenizer, max_length=args.max_length)
        val_ds = VoCDataset(texts[val_idx], labels[val_idx], tokenizer, max_length=args.max_length)

        train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True)
        val_loader = DataLoader(val_ds, batch_size=args.batch_size * 2, shuffle=False)

        # Re-initialize clean model from pretrained checkpoint for each fold
        model = AutoModelForSequenceClassification.from_pretrained(
            MODEL_NAME,
            num_labels=num_classes,
        ).to(device)

        class_weights = compute_class_weights(labels[train_idx], num_classes, device)
        criterion = nn.CrossEntropyLoss(weight=class_weights)

        optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=0.01)
        total_steps = len(train_loader) * args.epochs
        warmup_steps = int(total_steps * 0.1)
        scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=warmup_steps, num_training_steps=total_steps)

        scaler = torch.amp.GradScaler(device_type=device.type) if device.type == "cuda" else None

        best_val_f1 = 0.0
        best_val_acc = 0.0

        for epoch in range(1, args.epochs + 1):
            t0 = time.time()
            train_loss = train_epoch(model, train_loader, optimizer, scheduler, criterion, device, scaler)
            val_f1, val_acc, _, _ = evaluate(model, val_loader, device)
            elapsed = time.time() - t0

            if val_f1 > best_val_f1:
                best_val_f1 = val_f1
                best_val_acc = val_acc
                marker = "⭐ (Best)"
            else:
                marker = ""

            print(f"  Epoch {epoch:2d}/{args.epochs} | Loss: {train_loss:.4f} | Val F1: {val_f1:.4f} | Val Acc: {val_acc*100:.2f}% | {elapsed:.1f}s {marker}")

        print(f"✓ Fold {fold} Complete -> Macro-F1: {best_val_f1:.4f} | Accuracy: {best_val_acc*100:.2f}%")
        fold_f1_scores.append(best_val_f1)
        fold_acc_scores.append(best_val_acc)

    mean_f1 = np.mean(fold_f1_scores)
    std_f1 = np.std(fold_f1_scores)
    mean_acc = np.mean(fold_acc_scores)
    std_acc = np.std(fold_acc_scores)

    print("\n" + "=" * 75)
    print(f"BUET BanglaBERT {task.upper()} 5-FOLD CV SUMMARY:")
    print(f"  Macro-F1 : {mean_f1:.4f} ± {std_f1:.4f}")
    print(f"  Accuracy : {mean_acc*100:.2f}% ± {std_acc*100:.2f}%")
    print("=" * 75)

    return mean_f1, mean_acc, fold_f1_scores, fold_acc_scores


def train_production_checkpoint(df, task, label_map, args, device, tokenizer):
    """Train final production weights on full dataset with a held-out test split, and save model."""
    inv_label_map = {v: k for k, v in label_map.items()}
    num_classes = len(label_map)
    labels = np.array([label_map[item] for item in df[task]])
    texts = df["review_text"].values

    train_texts, test_texts, train_labels, test_labels = train_test_split(
        texts, labels, test_size=0.15, random_state=SEED, stratify=labels
    )

    print(f"\nTraining Final Production Model for {task.upper()} (Train: {len(train_texts)}, Test: {len(test_texts)})...")
    train_ds = VoCDataset(train_texts, train_labels, tokenizer, max_length=args.max_length)
    test_ds = VoCDataset(test_texts, test_labels, tokenizer, max_length=args.max_length)

    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True)
    test_loader = DataLoader(test_ds, batch_size=args.batch_size * 2, shuffle=False)

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=num_classes,
    ).to(device)

    class_weights = compute_class_weights(train_labels, num_classes, device)
    criterion = nn.CrossEntropyLoss(weight=class_weights)

    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=0.01)
    total_steps = len(train_loader) * args.epochs
    warmup_steps = int(total_steps * 0.1)
    scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=warmup_steps, num_training_steps=total_steps)
    scaler = torch.amp.GradScaler(device_type=device.type) if device.type == "cuda" else None

    for epoch in range(1, args.epochs + 1):
        loss = train_epoch(model, train_loader, optimizer, scheduler, criterion, device, scaler)
        f1, acc, _, _ = evaluate(model, test_loader, device)
        print(f"  Epoch {epoch}/{args.epochs} - Loss: {loss:.4f} | Test F1: {f1:.4f} | Test Acc: {acc*100:.2f}%")

    # Final detailed classification report on held-out test split
    _, _, y_true, y_pred = evaluate(model, test_loader, device)
    target_names = [inv_label_map[i] for i in range(num_classes)]
    report_str = classification_report(y_true, y_pred, target_names=target_names, digits=4)
    print("\n--- FINAL TEST SPLIT CLASSIFICATION REPORT ---")
    print(report_str)

    # Save fine-tuned checkpoint
    out_dir = MODELS_DIR / f"banglabert_finetuned_{task}"
    model.save_pretrained(out_dir)
    tokenizer.save_pretrained(out_dir)
    print(f"✓ Saved Fine-Tuned BanglaBERT ({task}) to: {out_dir}")

    # Append to results report file
    report_file = REPORTS_DIR / "banglabert_finetuning_report.txt"
    with open(report_file, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*70}\nBUET BanglaBERT Fine-Tuned Report: {task.upper()}\nDate: {time.ctime()}\n{'='*70}\n")
        f.write(report_str)
        f.write("\n")

    return model


def main():
    parser = argparse.ArgumentParser(description="BUET BanglaBERT Full End-to-End Fine-Tuning")
    parser.add_argument("--task", type=str, default="both", choices=["sentiment", "category", "both"])
    parser.add_argument("--epochs", type=int, default=4, help="Number of fine-tuning epochs per fold")
    parser.add_argument("--batch_size", type=int, default=32, help="Batch size (reduce to 16 if low GPU memory)")
    parser.add_argument("--lr", type=float, default=2e-5, help="Learning rate for AdamW")
    parser.add_argument("--max_length", type=int, default=96, help="Maximum token length")
    parser.add_argument("--folds", type=int, default=5, help="Number of cross-validation folds")
    parser.add_argument("--skip_cv", action="store_true", help="Skip 5-fold CV and train single production model")
    args = parser.parse_args()

    set_seed(SEED)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Active Device: {device.type.upper()}")
    if device.type == "cuda":
        print(f"GPU Hardware: {torch.cuda.get_device_name(0)}")

    df = load_dataset()
    print(f"Loaded ground-truth dataset: {len(df):,d} reviews across {df['operator'].nunique()} operators.")

    print(f"Loading tokenizer: {MODEL_NAME}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    tasks_to_run = ["sentiment", "category"] if args.task == "both" else [args.task]

    for task in tasks_to_run:
        label_map = SENTIMENT_LABEL_MAP if task == "sentiment" else CATEGORY_LABEL_MAP

        if not args.skip_cv:
            run_cv_experiment(df, task, label_map, args, device, tokenizer)

        train_production_checkpoint(df, task, label_map, args, device, tokenizer)

    print("\n🎉 ALL BANGLABERT FINE-TUNING PIPELINES COMPLETED SUCCESSFULLY!")


if __name__ == "__main__":
    main()
