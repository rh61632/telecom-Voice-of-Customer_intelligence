import math
import os
from pathlib import Path
import re
import json
import random
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report, f1_score, accuracy_score

# Set random seeds for reproducibility
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)

# Paths
DL_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DL_DIR.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"
MODELS_DIR = DL_DIR / "models"
REPORTS_DIR = DL_DIR / "reports"

MODELS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

LABEL_MAP = {
    "General Appreciation / Other": 0,
    "Offers & Data Packs": 1,
    "App Login & Technical Bugs": 2,
    "Network Speed & 4G Latency": 3,
    "Billing & Airtime Deductions": 4,
}
INV_LABEL_MAP = {v: k for k, v in LABEL_MAP.items()}


def clean_text(text: str) -> str:
    """Normalize text while preserving Bangla script, English, and Banglish."""
    text = str(text).strip()
    text = re.sub(r"(.)\1{2,}", r"\1\1", text)
    text = re.sub(r"\s+", " ", text)
    return text.lower()


def load_dataset() -> pd.DataFrame:
    """Load and merge category data from all 3 telecom operators."""
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
    combined = combined.dropna(subset=["review_text", "category"]).copy()
    combined["clean_text"] = combined["review_text"].apply(clean_text)
    combined = combined[combined["clean_text"].str.len() > 0]
    combined = combined[combined["category"].isin(LABEL_MAP.keys())].reset_index(drop=True)
    combined["label"] = combined["category"].map(LABEL_MAP)
    return combined


class Vocabulary:
    """Word and Character dual vocabulary builder."""
    def __init__(self, max_words=10000, min_word_freq=2, max_chars=300):
        self.max_words = max_words
        self.min_word_freq = min_word_freq
        self.max_chars = max_chars
        
        self.pad_token = "<pad>"
        self.unk_token = "<unk>"
        
        self.word2idx = {self.pad_token: 0, self.unk_token: 1}
        self.char2idx = {self.pad_token: 0, self.unk_token: 1}
        self.idx2word = {0: self.pad_token, 1: self.unk_token}

    def fit(self, texts):
        word_counts = {}
        char_counts = {}
        for text in texts:
            words = text.split()
            for w in words:
                word_counts[w] = word_counts.get(w, 0) + 1
            for c in text:
                char_counts[c] = char_counts.get(c, 0) + 1
        
        sorted_words = sorted(
            [w for w, cnt in word_counts.items() if cnt >= self.min_word_freq],
            key=lambda w: word_counts[w],
            reverse=True
        )[:self.max_words]
        
        for w in sorted_words:
            if w not in self.word2idx:
                idx = len(self.word2idx)
                self.word2idx[w] = idx
                self.idx2word[idx] = w

        sorted_chars = sorted(char_counts.keys(), key=lambda c: char_counts[c], reverse=True)[:self.max_chars]
        for c in sorted_chars:
            if c not in self.char2idx:
                self.char2idx[c] = len(self.char2idx)

    def encode(self, text, max_words=64, max_word_chars=16):
        words = text.split()[:max_words]
        word_ids = [self.word2idx.get(w, 1) for w in words]
        
        char_matrix = []
        for w in words:
            c_ids = [self.char2idx.get(c, 1) for c in w[:max_word_chars]]
            c_ids += [0] * (max_word_chars - len(c_ids))
            char_matrix.append(c_ids)
            
        pad_len = max_words - len(word_ids)
        word_ids += [0] * pad_len
        char_matrix += [[0] * max_word_chars for _ in range(pad_len)]
        
        return word_ids, char_matrix

    def to_dict(self):
        return {
            "word2idx": self.word2idx,
            "char2idx": self.char2idx,
            "max_words": self.max_words,
            "min_word_freq": self.min_word_freq,
        }

    @classmethod
    def from_dict(cls, d):
        v = cls(max_words=d["max_words"], min_word_freq=d["min_word_freq"])
        v.word2idx = d["word2idx"]
        v.char2idx = d["char2idx"]
        v.idx2word = {int(v_idx): k for k, v_idx in v.word2idx.items()}
        return v


class TelecomReviewDataset(Dataset):
    def __init__(self, texts, labels, vocab, max_words=64, max_word_chars=16):
        self.labels = labels
        self.encoded_words = []
        self.encoded_chars = []
        for text in texts:
            w_ids, c_ids = vocab.encode(text, max_words, max_word_chars)
            self.encoded_words.append(w_ids)
            self.encoded_chars.append(c_ids)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return (
            torch.tensor(self.encoded_words[idx], dtype=torch.long),
            torch.tensor(self.encoded_chars[idx], dtype=torch.long),
            torch.tensor(self.labels[idx], dtype=torch.long),
        )


class Attention(nn.Module):
    """Additive Self-Attention layer."""
    def __init__(self, hidden_dim):
        super().__init__()
        self.proj = nn.Linear(hidden_dim, hidden_dim)
        self.query = nn.Linear(hidden_dim, 1, bias=False)

    def forward(self, h, mask=None):
        energy = torch.tanh(self.proj(h))
        scores = self.query(energy).squeeze(-1)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
        weights = F.softmax(scores, dim=-1)
        context = torch.bmm(weights.unsqueeze(1), h).squeeze(1)
        return context, weights


class BiLSTMWithAttention(nn.Module):
    """
    Hybrid Word + Character-CNN BiLSTM with Additive Self-Attention
    Configured for 5 operational categories.
    """
    def __init__(
        self,
        word_vocab_size,
        char_vocab_size,
        word_emb_dim=128,
        char_emb_dim=32,
        char_cnn_filters=64,
        char_kernel_size=3,
        lstm_hidden_dim=128,
        lstm_layers=2,
        num_classes=5,
        dropout=0.3,
    ):
        super().__init__()
        self.word_embedding = nn.Embedding(word_vocab_size, word_emb_dim, padding_idx=0)
        self.char_embedding = nn.Embedding(char_vocab_size, char_emb_dim, padding_idx=0)
        self.char_conv = nn.Conv1d(
            in_channels=char_emb_dim,
            out_channels=char_cnn_filters,
            kernel_size=char_kernel_size,
            padding=char_kernel_size // 2,
        )
        combined_dim = word_emb_dim + char_cnn_filters
        self.dropout = nn.Dropout(dropout)
        self.bilstm = nn.LSTM(
            input_size=combined_dim,
            hidden_size=lstm_hidden_dim,
            num_layers=lstm_layers,
            bidirectional=True,
            batch_first=True,
            dropout=dropout if lstm_layers > 1 else 0.0,
        )
        self.attention = Attention(lstm_hidden_dim * 2)
        self.classifier = nn.Sequential(
            nn.Linear(lstm_hidden_dim * 2, 128),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(128, num_classes),
        )

    def forward(self, word_ids, char_ids):
        batch_size, seq_len = word_ids.size()
        w_emb = self.word_embedding(word_ids)

        c_flat = char_ids.view(batch_size * seq_len, -1)
        c_emb = self.char_embedding(c_flat).transpose(1, 2)
        c_conv = F.relu(self.char_conv(c_emb))
        c_pooled, _ = torch.max(c_conv, dim=-1)
        c_feat = c_pooled.view(batch_size, seq_len, -1)

        x = torch.cat([w_emb, c_feat], dim=-1)
        x = self.dropout(x)

        lstm_out, _ = self.bilstm(x)
        mask = (word_ids != 0)
        context, _ = self.attention(lstm_out, mask=mask)
        logits = self.classifier(context)
        return logits


def train_epoch(model, dataloader, optimizer, criterion):
    model.train()
    total_loss = 0.0
    for w_ids, c_ids, labels in dataloader:
        optimizer.zero_grad()
        logits = model(w_ids, c_ids)
        loss = criterion(logits, labels)
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), max_norm=5.0)
        optimizer.step()
        total_loss += loss.item() * len(labels)
    return total_loss / len(dataloader.dataset)


def evaluate(model, dataloader):
    model.eval()
    all_preds = []
    all_labels = []
    all_probs = []
    with torch.no_grad():
        for w_ids, c_ids, labels in dataloader:
            logits = model(w_ids, c_ids)
            probs = F.softmax(logits, dim=-1)
            preds = torch.argmax(probs, dim=-1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
            all_probs.extend(probs.cpu().numpy())
            
    macro_f1 = f1_score(all_labels, all_preds, average="macro", zero_division=0)
    acc = accuracy_score(all_labels, all_preds)
    return macro_f1, acc, np.array(all_preds), np.array(all_labels), np.array(all_probs)


def train_and_export_category_bilstm(df: pd.DataFrame, epochs=8, batch_size=32):
    """Train BiLSTM category model on full dataset with validation split and export."""
    print("=" * 70)
    print("TRAINING PRODUCTION BiLSTM + ATTENTION MODEL (5 OPERATIONAL CATEGORIES)")
    print("=" * 70)

    # 85/15 train/val split
    skf = StratifiedKFold(n_splits=7, shuffle=True, random_state=SEED)
    train_idx, val_idx = next(skf.split(df, df["label"]))
    
    train_df = df.iloc[train_idx]
    val_df = df.iloc[val_idx]

    vocab = Vocabulary()
    vocab.fit(train_df["clean_text"].tolist())

    train_ds = TelecomReviewDataset(train_df["clean_text"].tolist(), train_df["label"].tolist(), vocab)
    val_ds = TelecomReviewDataset(val_df["clean_text"].tolist(), val_df["label"].tolist(), vocab)

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False)

    class_counts = train_df["label"].value_counts().sort_index().values
    weights = torch.tensor([len(train_df) / (len(class_counts) * c) for c in class_counts], dtype=torch.float32)

    model = BiLSTMWithAttention(
        word_vocab_size=len(vocab.word2idx) + 1,
        char_vocab_size=len(vocab.char2idx) + 1,
        num_classes=5,
    )

    criterion = nn.CrossEntropyLoss(weight=weights)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)

    best_val_f1 = 0.0
    best_state = None

    for epoch in range(1, epochs + 1):
        loss = train_epoch(model, train_loader, optimizer, criterion)
        val_f1, val_acc, _, _, _ = evaluate(model, val_loader)
        print(f"Epoch {epoch:2d}/{epochs:2d} | Train Loss: {loss:.4f} | Val F1: {val_f1:.4f} | Val Acc: {val_acc*100:.2f}%")
        if val_f1 > best_val_f1:
            best_val_f1 = val_f1
            best_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}

    # Load best weights
    model.load_state_dict(best_state)

    # Final evaluation on val set
    val_f1, val_acc, val_preds, val_targets, _ = evaluate(model, val_loader)
    target_names = [INV_LABEL_MAP[i] for i in range(5)]
    rep = classification_report(val_targets, val_preds, target_names=target_names, digits=4)
    print("\nFinal Validation Classification Report:")
    print(rep)

    # Save model
    model_path = MODELS_DIR / "bilstm_category_model.pt"
    torch.save({
        "model_state_dict": model.state_dict(),
        "word_vocab_size": len(vocab.word2idx) + 1,
        "char_vocab_size": len(vocab.char2idx) + 1,
        "num_classes": 5,
        "label_map": LABEL_MAP,
    }, model_path)
    print(f"Model saved to: {model_path}")

    # Save vocabulary
    vocab_path = MODELS_DIR / "bilstm_category_vocab.json"
    with open(vocab_path, "w", encoding="utf-8") as f:
        json.dump(vocab.to_dict(), f, indent=2, ensure_ascii=False)
    print(f"Vocabulary saved to: {vocab_path}")

    # Save Markdown report
    md_report = f"""# Deep Learning BiLSTM Category Classification Report

## Model Architecture
- **Embedding**: Dual Word (128-dim) + Char-CNN (64 filters) Representation
- **Sequence Modeling**: 2-Layer Bidirectional LSTM (hidden dim = 128)
- **Pooling**: Additive Bahdanau Attention Mechanism
- **Output**: 5 Operational Category Classes with CrossEntropyLoss class weighting

## Validation Results
- **Validation Macro-F1**: `{val_f1:.4f}`
- **Validation Accuracy**: `{val_acc * 100:.2f}%`

```
{rep}
```
"""
    rep_path = REPORTS_DIR / "dl_bilstm_category_report.md"
    with open(rep_path, "w", encoding="utf-8") as f:
        f.write(md_report)
    print(f"Report saved to: {rep_path}")


if __name__ == "__main__":
    df = load_dataset()
    train_and_export_category_bilstm(df, epochs=8)
