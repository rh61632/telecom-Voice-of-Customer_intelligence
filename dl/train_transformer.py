import math
import os
from pathlib import Path
import random
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report, f1_score, accuracy_score
from transformers import AutoTokenizer, AutoModel

# Reproducibility
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)

DL_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DL_DIR.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"
MODELS_DIR = DL_DIR / "models"
REPORTS_DIR = DL_DIR / "reports"

MODELS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
LABEL_MAP = {"Negative": 0, "Neutral": 1, "Positive": 2}
INV_LABEL_MAP = {v: k for k, v in LABEL_MAP.items()}


def mean_pooling(model_output, attention_mask):
    """Mean pooling to extract sentence representation from token embeddings."""
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


def load_dataset() -> pd.DataFrame:
    files = {
        "Grameenphone": DATA_DIR / "mygp_classified_reviews.csv",
        "Banglalink": DATA_DIR / "mybl_classified_reviews.csv",
        "Robi": DATA_DIR / "myrobi_classified_reviews.csv",
    }
    dfs = []
    for op, path in files.items():
        if not path.exists():
            raise FileNotFoundError(f"Missing dataset at {path}")
        df = pd.read_csv(path)
        if "operator" not in df.columns:
            df["operator"] = op
        dfs.append(df)
        
    combined = pd.concat(dfs, ignore_index=True)
    combined = combined.dropna(subset=["review_text", "sentiment"]).copy()
    combined["review_text"] = combined["review_text"].astype(str).str.strip()
    combined = combined[combined["review_text"].str.len() > 0]
    combined = combined[combined["sentiment"].isin(LABEL_MAP.keys())].reset_index(drop=True)
    combined["label"] = combined["sentiment"].map(LABEL_MAP)
    return combined


class EmbeddingFeatureDataset(Dataset):
    def __init__(self, embeddings, labels):
        self.embeddings = torch.tensor(embeddings, dtype=torch.float32)
        self.labels = torch.tensor(labels, dtype=torch.long)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return self.embeddings[idx], self.labels[idx]


class MultilingualClassificationHead(nn.Module):
    """
    Classification head built on top of 384-dimensional MiniLM embeddings.
    Uses LayerNorm, GELU, and Dropout for regularization.
    """
    def __init__(self, in_features=384, hidden_dim=128, num_classes=3, dropout=0.3):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_features, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, 64),
            nn.LayerNorm(64),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(64, num_classes),
        )

    def forward(self, x):
        return self.net(x)


def extract_all_embeddings(texts, batch_size=32):
    """Extract sentence embeddings using the pretrained multilingual transformer."""
    print(f"\nLoading transformer: {MODEL_NAME} ...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    transformer = AutoModel.from_pretrained(MODEL_NAME)
    transformer.eval()

    all_embeddings = []
    total = len(texts)
    print(f"Extracting embeddings for {total} reviews on CPU (batch size {batch_size})...")

    with torch.no_grad():
        for i in range(0, total, batch_size):
            batch_texts = texts[i : i + batch_size]
            encoded = tokenizer(
                batch_texts,
                padding=True,
                truncation=True,
                max_length=96,
                return_tensors="pt",
            )
            out = transformer(**encoded)
            pooled = mean_pooling(out, encoded["attention_mask"])
            # Normalize embeddings to unit sphere
            normalized = F.normalize(pooled, p=2, dim=1)
            all_embeddings.append(normalized.cpu().numpy())
            
            if (i // batch_size) % 20 == 0 or (i + batch_size) >= total:
                print(f"  Processed {min(i + batch_size, total)}/{total} reviews...")

    embeddings_matrix = np.vstack(all_embeddings)
    print(f"Extracted feature matrix shape: {embeddings_matrix.shape}")
    return embeddings_matrix, tokenizer, transformer


def train_head_epoch(model, loader, optimizer, criterion):
    model.train()
    total_loss = 0.0
    for x, y in loader:
        optimizer.zero_grad()
        logits = model(x)
        loss = criterion(logits, y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * len(y)
    return total_loss / len(loader.dataset)


def eval_head(model, loader):
    model.eval()
    all_preds = []
    all_labels = []
    all_probs = []
    with torch.no_grad():
        for x, y in loader:
            logits = model(x)
            probs = F.softmax(logits, dim=-1)
            preds = torch.argmax(probs, dim=-1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(y.cpu().numpy())
            all_probs.extend(probs.cpu().numpy())
            
    macro_f1 = f1_score(all_labels, all_preds, average="macro")
    acc = accuracy_score(all_labels, all_preds)
    return macro_f1, acc


def run_cross_validation(embeddings, labels, n_splits=5, epochs=15, batch_size=32):
    """5-Fold Stratified Cross Validation on Transformer Head."""
    print("=" * 65)
    print("RUNNING 5-FOLD STRATIFIED CV: PRETRAINED MULTILINGUAL MINILM")
    print("=" * 65)
    
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=SEED)
    fold_f1_scores = []
    fold_acc_scores = []

    class_counts = pd.Series(labels).value_counts().sort_index().values
    weights = torch.tensor([len(labels) / (len(class_counts) * c) for c in class_counts], dtype=torch.float32)

    for fold, (train_idx, val_idx) in enumerate(skf.split(embeddings, labels), 1):
        train_ds = EmbeddingFeatureDataset(embeddings[train_idx], labels[train_idx])
        val_ds = EmbeddingFeatureDataset(embeddings[val_idx], labels[val_idx])

        train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
        val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False)

        head = MultilingualClassificationHead(in_features=embeddings.shape[1])
        optimizer = torch.optim.AdamW(head.parameters(), lr=2e-3, weight_decay=1e-3)
        criterion = nn.CrossEntropyLoss(weight=weights)

        best_f1 = 0.0
        best_acc = 0.0
        for ep in range(1, epochs + 1):
            train_head_epoch(head, train_loader, optimizer, criterion)
            val_f1, val_acc = eval_head(head, val_loader)
            if val_f1 > best_f1:
                best_f1 = val_f1
                best_acc = val_acc

        print(f"Fold {fold}/{n_splits} -> Best Macro-F1: {best_f1:.4f} | Accuracy: {best_acc:.4f}")
        fold_f1_scores.append(best_f1)
        fold_acc_scores.append(best_acc)

    mean_f1 = np.mean(fold_f1_scores)
    std_f1 = np.std(fold_f1_scores)
    mean_acc = np.mean(fold_acc_scores)
    std_acc = np.std(fold_acc_scores)

    print("-" * 65)
    print(f"MiniLM Transformer CV Macro-F1 : {mean_f1:.4f} (±{std_f1:.4f})")
    print(f"MiniLM Transformer CV Accuracy : {mean_acc:.4f} (±{std_acc:.4f})")
    print("=" * 65)
    return {"mean_macro_f1": mean_f1, "std_macro_f1": std_f1, "mean_acc": mean_acc, "std_acc": std_acc}


def train_final_transformer_head(embeddings, labels, epochs=15, batch_size=32):
    print("\nFitting final Multilingual MiniLM Classification Head on all data...")
    dataset = EmbeddingFeatureDataset(embeddings, labels)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    class_counts = pd.Series(labels).value_counts().sort_index().values
    weights = torch.tensor([len(labels) / (len(class_counts) * c) for c in class_counts], dtype=torch.float32)

    head = MultilingualClassificationHead(in_features=embeddings.shape[1])
    optimizer = torch.optim.AdamW(head.parameters(), lr=2e-3, weight_decay=1e-3)
    criterion = nn.CrossEntropyLoss(weight=weights)

    for ep in range(1, epochs + 1):
        loss = train_head_epoch(head, loader, optimizer, criterion)
        if ep % 5 == 0 or ep == epochs:
            print(f"  Epoch {ep:2d}/{epochs} - Loss: {loss:.4f}")

    checkpoint = {
        "model_name": MODEL_NAME,
        "head_state_dict": head.state_dict(),
        "label_map": LABEL_MAP,
    }
    model_path = MODELS_DIR / "minilm_transformer_head.pt"
    torch.save(checkpoint, model_path)
    print(f"Saved Transformer Head to: {model_path}")
    return head


if __name__ == "__main__":
    df = load_dataset()
    embeddings, tokenizer, transformer = extract_all_embeddings(df["review_text"].tolist())
    cv_res = run_cross_validation(embeddings, df["label"].values)
    final_head = train_final_transformer_head(embeddings, df["label"].values)
