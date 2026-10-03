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

LABEL_MAP = {"Negative": 0, "Neutral": 1, "Positive": 2}
INV_LABEL_MAP = {v: k for k, v in LABEL_MAP.items()}


def clean_text(text: str) -> str:
    """Normalize text while preserving Bangla script, English, and Banglish."""
    text = str(text).strip()
    # Normalize excessive repeated characters (e.g. "faltuuuu" -> "faltuu")
    text = re.sub(r"(.)\1{2,}", r"\1\1", text)
    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)
    return text.lower()


def load_dataset() -> pd.DataFrame:
    """Load and merge data from all 3 telecom operators."""
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
    combined["clean_text"] = combined["review_text"].apply(clean_text)
    combined = combined[combined["clean_text"].str.len() > 0]
    combined = combined[combined["sentiment"].isin(LABEL_MAP.keys())].reset_index(drop=True)
    combined["label"] = combined["sentiment"].map(LABEL_MAP)
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
        
        # Sort words by frequency
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
        
        # Matrix of char IDs: [max_words, max_word_chars]
        char_matrix = []
        for w in words:
            c_ids = [self.char2idx.get(c, 1) for c in w[:max_word_chars]]
            c_ids += [0] * (max_word_chars - len(c_ids))
            char_matrix.append(c_ids)
            
        # Pad word_ids and char_matrix
        pad_len = max_words - len(word_ids)
        word_ids += [0] * pad_len
        char_matrix += [[0] * max_word_chars for _ in range(pad_len)]
        
        return word_ids, char_matrix


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
        # h: [batch_size, seq_len, hidden_dim]
        energy = torch.tanh(self.proj(h))
        scores = self.query(energy).squeeze(-1) # [batch_size, seq_len]
        
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
            
        weights = F.softmax(scores, dim=-1) # [batch_size, seq_len]
        context = torch.bmm(weights.unsqueeze(1), h).squeeze(1) # [batch_size, hidden_dim]
        return context, weights


class BiLSTMWithAttention(nn.Module):
    """
    Hybrid Word + Character-CNN BiLSTM with Additive Self-Attention
    Tailored specifically for phonetic Banglish, Bangla script, and English.
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
        num_classes=3,
        dropout=0.3,
    ):
        super().__init__()
        # Word Embeddings
        self.word_embedding = nn.Embedding(word_vocab_size, word_emb_dim, padding_idx=0)
        
        # Char Embeddings + 1D Conv for sub-word morphology (Banglish spelling invariance)
        self.char_embedding = nn.Embedding(char_vocab_size, char_emb_dim, padding_idx=0)
        self.char_conv = nn.Conv1d(
            in_channels=char_emb_dim,
            out_channels=char_cnn_filters,
            kernel_size=char_kernel_size,
            padding=char_kernel_size // 2,
        )
        
        combined_dim = word_emb_dim + char_cnn_filters
        self.dropout = nn.Dropout(dropout)
        
        # Bidirectional LSTM
        self.bilstm = nn.LSTM(
            input_size=combined_dim,
            hidden_size=lstm_hidden_dim,
            num_layers=lstm_layers,
            bidirectional=True,
            batch_first=True,
            dropout=dropout if lstm_layers > 1 else 0.0,
        )
        
        # Attention Pooling
        self.attention = Attention(lstm_hidden_dim * 2)
        
        # Classification Head
        self.classifier = nn.Sequential(
            nn.Linear(lstm_hidden_dim * 2, 128),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(128, num_classes),
        )

    def forward(self, word_ids, char_ids):
        # word_ids: [batch_size, seq_len]
        # char_ids: [batch_size, seq_len, word_char_len]
        batch_size, seq_len, word_char_len = char_ids.shape
        
        # 1. Word representations
        w_emb = self.word_embedding(word_ids) # [batch_size, seq_len, word_emb_dim]
        
        # 2. Char CNN representations
        c_flat = char_ids.view(batch_size * seq_len, word_char_len)
        c_emb = self.char_embedding(c_flat).transpose(1, 2) # [batch * seq, char_emb_dim, word_char_len]
        c_conv = F.relu(self.char_conv(c_emb))
        c_pooled, _ = torch.max(c_conv, dim=-1) # [batch * seq, char_cnn_filters]
        c_feat = c_pooled.view(batch_size, seq_len, -1)
        
        # 3. Concatenate Word + Char features
        x = torch.cat([w_emb, c_feat], dim=-1)
        x = self.dropout(x)
        
        # 4. BiLSTM
        lstm_out, _ = self.bilstm(x) # [batch_size, seq_len, 2 * hidden_dim]
        
        # 5. Attention Pooling
        mask = (word_ids != 0)
        context, _ = self.attention(lstm_out, mask=mask)
        
        # 6. Final logits
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
            
    macro_f1 = f1_score(all_labels, all_preds, average="macro")
    acc = accuracy_score(all_labels, all_preds)
    return macro_f1, acc, np.array(all_preds), np.array(all_labels), np.array(all_probs)


def run_cross_validation(df: pd.DataFrame, n_splits=5, epochs=10, batch_size=32):
    """5-Fold Stratified Cross Validation on BiLSTM with Attention."""
    print("=" * 65)
    print("RUNNING 5-FOLD STRATIFIED CV: BiLSTM WITH ATTENTION")
    print("=" * 65)
    
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=SEED)
    fold_f1_scores = []
    fold_acc_scores = []

    # Inverse frequency class weights for imbalance
    class_counts = df["label"].value_counts().sort_index().values
    weights = torch.tensor([len(df) / (len(class_counts) * c) for c in class_counts], dtype=torch.float32)
    print(f"Inverse Class Weights: {weights.tolist()}")

    for fold, (train_idx, val_idx) in enumerate(skf.split(df, df["label"]), 1):
        train_df = df.iloc[train_idx]
        val_df = df.iloc[val_idx]
        
        # Fit vocab on training fold only
        vocab = Vocabulary()
        vocab.fit(train_df["clean_text"].tolist())
        
        train_ds = TelecomReviewDataset(train_df["clean_text"].tolist(), train_df["label"].tolist(), vocab)
        val_ds = TelecomReviewDataset(val_df["clean_text"].tolist(), val_df["label"].tolist(), vocab)
        
        train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
        val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False)
        
        model = BiLSTMWithAttention(
            word_vocab_size=len(vocab.word2idx),
            char_vocab_size=len(vocab.char2idx),
        )
        optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
        criterion = nn.CrossEntropyLoss(weight=weights)
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode="max", factor=0.5, patience=2)

        best_val_f1 = 0.0
        best_val_acc = 0.0
        
        for epoch in range(1, epochs + 1):
            train_loss = train_epoch(model, train_loader, optimizer, criterion)
            val_f1, val_acc, _, _, _ = evaluate(model, val_loader)
            scheduler.step(val_f1)
            if val_f1 > best_val_f1:
                best_val_f1 = val_f1
                best_val_acc = val_acc
                
        print(f"Fold {fold}/{n_splits} -> Best Macro-F1: {best_val_f1:.4f} | Accuracy: {best_val_acc:.4f}")
        fold_f1_scores.append(best_val_f1)
        fold_acc_scores.append(best_val_acc)

    mean_f1 = np.mean(fold_f1_scores)
    std_f1 = np.std(fold_f1_scores)
    mean_acc = np.mean(fold_acc_scores)
    std_acc = np.std(fold_acc_scores)
    
    print("-" * 65)
    print(f"BiLSTM CV Macro-F1 : {mean_f1:.4f} (±{std_f1:.4f})")
    print(f"BiLSTM CV Accuracy : {mean_acc:.4f} (±{std_acc:.4f})")
    print("=" * 65)
    return {"mean_macro_f1": mean_f1, "std_macro_f1": std_f1, "mean_acc": mean_acc, "std_acc": std_acc}


def train_final_model(df: pd.DataFrame, epochs=10, batch_size=32):
    """Train BiLSTM model on full dataset and save artifact."""
    print("\nTraining final BiLSTM model on all 4,500 reviews...")
    vocab = Vocabulary()
    vocab.fit(df["clean_text"].tolist())
    
    dataset = TelecomReviewDataset(df["clean_text"].tolist(), df["label"].tolist(), vocab)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    
    class_counts = df["label"].value_counts().sort_index().values
    weights = torch.tensor([len(df) / (len(class_counts) * c) for c in class_counts], dtype=torch.float32)
    
    model = BiLSTMWithAttention(
        word_vocab_size=len(vocab.word2idx),
        char_vocab_size=len(vocab.char2idx),
    )
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
    criterion = nn.CrossEntropyLoss(weight=weights)
    
    for epoch in range(1, epochs + 1):
        loss = train_epoch(model, dataloader, optimizer, criterion)
        print(f"  Epoch {epoch:2d}/{epochs} - Loss: {loss:.4f}")
        
    # Save checkpoint + vocab
    checkpoint = {
        "model_state_dict": model.state_dict(),
        "vocab_word2idx": vocab.word2idx,
        "vocab_char2idx": vocab.char2idx,
        "label_map": LABEL_MAP,
    }
    model_path = MODELS_DIR / "bilstm_attention_model.pt"
    torch.save(checkpoint, model_path)
    print(f"BiLSTM model saved to: {model_path}")
    return model, vocab


if __name__ == "__main__":
    df = load_dataset()
    cv_res = run_cross_validation(df, epochs=8)
    final_model, vocab = train_final_model(df, epochs=8)
