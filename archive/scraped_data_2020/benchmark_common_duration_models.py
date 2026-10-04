"""
Benchmark all ML and DL models on the common duration dataset (2025-08 to 2026-09)
with 5-Fold Stratified Cross-Validation and continuous fold-by-fold logging.
"""

import sys
import time
from pathlib import Path
import re
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.naive_bayes import ComplementNB
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import classification_report, f1_score, accuracy_score
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader

# Ensure project root is in python path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
COMMON_DIR = BASE_DIR / "scraped_data_2020" / "common_duration"
INPUT_CSV = COMMON_DIR / "all_operators_common_duration.csv"
REPORT_TXT = COMMON_DIR / "model_benchmark_results.txt"
CLASSIFIED_CSV = COMMON_DIR / "classified_all_operators_common_duration.csv"

LABEL_MAP = {"Negative": 0, "Neutral": 1, "Positive": 2}
INV_LABEL_MAP = {v: k for k, v in LABEL_MAP.items()}


def clean_text(text: str) -> str:
    text = str(text).strip()
    text = re.sub(r"(.)\1{2,}", r"\1\1", text)
    text = re.sub(r"\s+", " ", text)
    return text.lower()


def map_rating_to_sentiment(r: int) -> str:
    if r in [1, 2]:
        return "Negative"
    elif r == 3:
        return "Neutral"
    else:
        return "Positive"


# ---------------------------------------------------------------------------
# BiLSTM Architecture
# ---------------------------------------------------------------------------
class Vocabulary:
    def __init__(self, max_words=10000, max_chars=120):
        self.word2idx = {"<pad>": 0, "<unk>": 1}
        self.char2idx = {"<pad>": 0, "<unk>": 1}
        self.max_words = max_words
        self.max_chars = max_chars

    def build_vocab(self, texts):
        word_counts = {}
        char_counts = {}
        for t in texts:
            words = t.split()
            for w in words:
                word_counts[w] = word_counts.get(w, 0) + 1
            for c in t:
                char_counts[c] = char_counts.get(c, 0) + 1

        sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:self.max_words]
        for w, _ in sorted_words:
            if w not in self.word2idx:
                self.word2idx[w] = len(self.word2idx)

        sorted_chars = sorted(char_counts.items(), key=lambda x: x[1], reverse=True)[:self.max_chars]
        for c, _ in sorted_chars:
            if c not in self.char2idx:
                self.char2idx[c] = len(self.char2idx)

    def encode(self, text, max_len=64):
        words = text.split()[:max_len]
        w_ids = [self.word2idx.get(w, 1) for w in words]
        if len(w_ids) < max_len:
            w_ids += [0] * (max_len - len(w_ids))
        
        c_ids = [self.char2idx.get(c, 1) for c in text[:max_len * 5]]
        if len(c_ids) < max_len * 5:
            c_ids += [0] * (max_len * 5 - len(c_ids))
        return w_ids, c_ids


class TextDataset(Dataset):
    def __init__(self, texts, labels, vocab, max_len=64):
        self.samples = []
        for t, l in zip(texts, labels):
            w, c = vocab.encode(clean_text(t), max_len=max_len)
            self.samples.append((torch.tensor(w, dtype=torch.long), torch.tensor(c, dtype=torch.long), torch.tensor(l, dtype=torch.long)))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        return self.samples[idx]


class BiLSTMAttention(nn.Module):
    def __init__(self, word_vocab_size, char_vocab_size, embed_dim=100, char_dim=32, hidden_dim=64, num_classes=3):
        super().__init__()
        self.word_embed = nn.Embedding(word_vocab_size, embed_dim, padding_idx=0)
        self.char_embed = nn.Embedding(char_vocab_size, char_dim, padding_idx=0)
        self.char_conv = nn.Conv1d(char_dim, 32, kernel_size=3, padding=1)
        self.lstm = nn.LSTM(embed_dim + 32, hidden_dim, num_layers=1, bidirectional=True, batch_first=True)
        self.attn_dense = nn.Linear(hidden_dim * 2, hidden_dim)
        self.attn_v = nn.Linear(hidden_dim, 1, bias=False)
        self.classifier = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(hidden_dim * 2, 32),
            nn.ReLU(),
            nn.Linear(32, num_classes)
        )

    def forward(self, words, chars):
        w_emb = self.word_embed(words)  # [B, L, embed_dim]
        c_emb = self.char_embed(chars).transpose(1, 2)  # [B, char_dim, L*5]
        c_conv = F.relu(self.char_conv(c_emb))  # [B, 32, L*5]
        # Pool chars down to length L
        c_pooled = F.adaptive_avg_pool1d(c_conv, w_emb.shape[1]).transpose(1, 2)  # [B, L, 32]

        x = torch.cat([w_emb, c_pooled], dim=-1)  # [B, L, embed_dim + 32]
        lstm_out, _ = self.lstm(x)  # [B, L, hidden_dim*2]

        u = torch.tanh(self.attn_dense(lstm_out))
        attn_weights = F.softmax(self.attn_v(u), dim=1)
        ctx = torch.sum(lstm_out * attn_weights, dim=1)  # [B, hidden_dim*2]
        return self.classifier(ctx)


def train_eval_bilstm_fold(X_tr, y_tr, X_val, y_val, vocab, epochs=4, batch_size=64):
    train_ds = TextDataset(X_tr, y_tr, vocab)
    val_ds = TextDataset(X_val, y_val, vocab)
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False)

    model = BiLSTMAttention(len(vocab.word2idx), len(vocab.char2idx))
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
    criterion = nn.CrossEntropyLoss()

    model.train()
    for ep in range(epochs):
        for b_w, b_c, b_y in train_loader:
            optimizer.zero_grad()
            logits = model(b_w, b_c)
            loss = criterion(logits, b_y)
            loss.backward()
            optimizer.step()

    model.eval()
    all_preds = []
    with torch.no_grad():
        for b_w, b_c, _ in val_loader:
            logits = model(b_w, b_c)
            preds = torch.argmax(logits, dim=-1).cpu().numpy()
            all_preds.extend(preds)

    return np.array(all_preds)


# ---------------------------------------------------------------------------
# Main Benchmark Pipeline
# ---------------------------------------------------------------------------
def main():
    print("=" * 80, flush=True)
    print("TELECOM VOC INTELLIGENCE: 5-FOLD BENCHMARK ACROSS ALL ML & DL MODELS", flush=True)
    print("Dataset: Shared Common Duration (2025-08-24 to 2026-09-30)", flush=True)
    print("=" * 80, flush=True)

    if not INPUT_CSV.exists():
        print(f"Error: {INPUT_CSV} does not exist!", flush=True)
        sys.exit(1)

    print(f"Loading full dataset from: {INPUT_CSV.name}...", flush=True)
    full_df = pd.read_csv(INPUT_CSV)
    full_df["review_text"] = full_df["review_text"].fillna(" ").astype(str)
    full_df["sentiment"] = full_df["rating"].apply(map_rating_to_sentiment)
    full_df["label"] = full_df["sentiment"].map(LABEL_MAP)
    print(f"Total reviews in common window: {len(full_df):,d}", flush=True)
    print("Sentiment distribution across all operators:", flush=True)
    for sent, count in full_df["sentiment"].value_counts().items():
        print(f"  - {sent:8s}: {count:,d} ({count/len(full_df)*100:.1f}%)", flush=True)

    # Create balanced benchmark dataset across classes (3,000 samples: 1,000 per class)
    print("\nExtracting balanced stratified benchmark subset (3,000 samples)...", flush=True)
    sampled_dfs = []
    for s_name in ["Negative", "Neutral", "Positive"]:
        s_subset = full_df[full_df["sentiment"] == s_name]
        n_sample = min(1000, len(s_subset))
        sampled_dfs.append(s_subset.sample(n=n_sample, random_state=42))
    
    bench_df = pd.concat(sampled_dfs, ignore_index=True).sample(frac=1.0, random_state=42).reset_index(drop=True)
    X = bench_df["review_text"].astype(str).tolist()
    y = bench_df["label"].to_numpy()
    print(f"Benchmark subset prepared: {len(bench_df)} reviews balanced across classes.", flush=True)

    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    results_summary = []

    # -----------------------------------------------------------------------
    # MODEL 1: Balanced Logistic Regression
    # -----------------------------------------------------------------------
    print("\n" + "=" * 60, flush=True)
    print(">>> [MODEL 1/5] BALANCED LOGISTIC REGRESSION (TF-IDF Char N-Grams)", flush=True)
    print("=" * 60, flush=True)
    m1_f1_scores = []
    m1_acc_scores = []
    
    for fold, (train_idx, val_idx) in enumerate(skf.split(X, y), 1):
        print(f"  [LogReg] Starting Fold {fold}/5...", end="", flush=True)
        t_fold = time.time()
        X_tr = [X[i] for i in train_idx]
        y_tr = y[train_idx]
        X_va = [X[i] for i in val_idx]
        y_va = y[val_idx]

        vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), sublinear_tf=True, min_df=2)
        X_tr_vec = vec.fit_transform(X_tr)
        X_va_vec = vec.transform(X_va)

        clf = LogisticRegression(class_weight="balanced", max_iter=1000, C=1.5, random_state=42)
        clf.fit(X_tr_vec, y_tr)
        preds = clf.predict(X_va_vec)

        f1 = f1_score(y_va, preds, average="macro")
        acc = accuracy_score(y_va, preds)
        m1_f1_scores.append(f1)
        m1_acc_scores.append(acc)
        print(f" Done ({time.time()-t_fold:.1f}s) | Macro-F1: {f1:.4f} | Accuracy: {acc*100:.2f}%", flush=True)

    mean_f1_1 = np.mean(m1_f1_scores)
    std_f1_1 = np.std(m1_f1_scores)
    mean_acc_1 = np.mean(m1_acc_scores)
    print(f"  >> LogReg 5-Fold Mean Macro-F1: {mean_f1_1:.4f} ± {std_f1_1:.4f} | Mean Accuracy: {mean_acc_1*100:.2f}%", flush=True)
    results_summary.append(("Balanced Logistic Regression", mean_f1_1, std_f1_1, mean_acc_1))

    # -----------------------------------------------------------------------
    # MODEL 2: Calibrated LinearSVC
    # -----------------------------------------------------------------------
    print("\n" + "=" * 60, flush=True)
    print(">>> [MODEL 2/5] CALIBRATED LINEARSVC (TF-IDF Char N-Grams)", flush=True)
    print("=" * 60, flush=True)
    m2_f1_scores = []
    m2_acc_scores = []

    for fold, (train_idx, val_idx) in enumerate(skf.split(X, y), 1):
        print(f"  [LinearSVC] Starting Fold {fold}/5...", end="", flush=True)
        t_fold = time.time()
        X_tr = [X[i] for i in train_idx]
        y_tr = y[train_idx]
        X_va = [X[i] for i in val_idx]
        y_va = y[val_idx]

        vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), sublinear_tf=True, min_df=2)
        X_tr_vec = vec.fit_transform(X_tr)
        X_va_vec = vec.transform(X_va)

        base_svc = LinearSVC(class_weight="balanced", C=0.8, random_state=42)
        clf = CalibratedClassifierCV(estimator=base_svc, cv=3)
        clf.fit(X_tr_vec, y_tr)
        preds = clf.predict(X_va_vec)

        f1 = f1_score(y_va, preds, average="macro")
        acc = accuracy_score(y_va, preds)
        m2_f1_scores.append(f1)
        m2_acc_scores.append(acc)
        print(f" Done ({time.time()-t_fold:.1f}s) | Macro-F1: {f1:.4f} | Accuracy: {acc*100:.2f}%", flush=True)

    mean_f1_2 = np.mean(m2_f1_scores)
    std_f1_2 = np.std(m2_f1_scores)
    mean_acc_2 = np.mean(m2_acc_scores)
    print(f"  >> LinearSVC 5-Fold Mean Macro-F1: {mean_f1_2:.4f} ± {std_f1_2:.4f} | Mean Accuracy: {mean_acc_2*100:.2f}%", flush=True)
    results_summary.append(("Calibrated LinearSVC", mean_f1_2, std_f1_2, mean_acc_2))

    # -----------------------------------------------------------------------
    # MODEL 3: Soft-Voting Ensemble (LogReg + LinearSVC + ComplementNB)
    # -----------------------------------------------------------------------
    print("\n" + "=" * 60, flush=True)
    print(">>> [MODEL 3/5] SOFT-VOTING ENSEMBLE (LogReg + LinearSVC + ComplementNB)", flush=True)
    print("=" * 60, flush=True)
    m3_f1_scores = []
    m3_acc_scores = []

    for fold, (train_idx, val_idx) in enumerate(skf.split(X, y), 1):
        print(f"  [Ensemble] Starting Fold {fold}/5...", end="", flush=True)
        t_fold = time.time()
        X_tr = [X[i] for i in train_idx]
        y_tr = y[train_idx]
        X_va = [X[i] for i in val_idx]
        y_va = y[val_idx]

        vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), sublinear_tf=True, min_df=2)
        X_tr_vec = vec.fit_transform(X_tr)
        X_va_vec = vec.transform(X_va)

        clf_lr = LogisticRegression(class_weight="balanced", max_iter=1000, C=1.5, random_state=42)
        clf_svc = CalibratedClassifierCV(estimator=LinearSVC(class_weight="balanced", C=0.8, random_state=42), cv=3)
        clf_cnb = ComplementNB(alpha=0.5)

        ensemble = VotingClassifier(
            estimators=[("lr", clf_lr), ("svc", clf_svc), ("cnb", clf_cnb)],
            voting="soft",
            weights=[1.2, 1.2, 0.8]
        )
        ensemble.fit(X_tr_vec, y_tr)
        preds = ensemble.predict(X_va_vec)

        f1 = f1_score(y_va, preds, average="macro")
        acc = accuracy_score(y_va, preds)
        m3_f1_scores.append(f1)
        m3_acc_scores.append(acc)
        print(f" Done ({time.time()-t_fold:.1f}s) | Macro-F1: {f1:.4f} | Accuracy: {acc*100:.2f}%", flush=True)

    mean_f1_3 = np.mean(m3_f1_scores)
    std_f1_3 = np.std(m3_f1_scores)
    mean_acc_3 = np.mean(m3_acc_scores)
    print(f"  >> Ensemble 5-Fold Mean Macro-F1: {mean_f1_3:.4f} ± {std_f1_3:.4f} | Mean Accuracy: {mean_acc_3*100:.2f}%", flush=True)
    results_summary.append(("Soft-Voting Ensemble ML", mean_f1_3, std_f1_3, mean_acc_3))

    # -----------------------------------------------------------------------
    # MODEL 4: Hybrid BiLSTM + Attention (Deep Learning)
    # -----------------------------------------------------------------------
    print("\n" + "=" * 60, flush=True)
    print(">>> [MODEL 4/5] HYBRID BiLSTM + ATTENTION (Word + Char-CNN)", flush=True)
    print("=" * 60, flush=True)
    vocab = Vocabulary()
    vocab.build_vocab([clean_text(t) for t in X])
    print(f"  Vocabulary built: {len(vocab.word2idx)} words, {len(vocab.char2idx)} chars", flush=True)

    m4_f1_scores = []
    m4_acc_scores = []

    for fold, (train_idx, val_idx) in enumerate(skf.split(X, y), 1):
        print(f"  [BiLSTM] Starting Fold {fold}/5 (Epochs: 4)...", end="", flush=True)
        t_fold = time.time()
        X_tr = [X[i] for i in train_idx]
        y_tr = y[train_idx]
        X_va = [X[i] for i in val_idx]
        y_va = y[val_idx]

        preds = train_eval_bilstm_fold(X_tr, y_tr, X_va, y_va, vocab, epochs=4, batch_size=64)

        f1 = f1_score(y_va, preds, average="macro")
        acc = accuracy_score(y_va, preds)
        m4_f1_scores.append(f1)
        m4_acc_scores.append(acc)
        print(f" Done ({time.time()-t_fold:.1f}s) | Macro-F1: {f1:.4f} | Accuracy: {acc*100:.2f}%", flush=True)

    mean_f1_4 = np.mean(m4_f1_scores)
    std_f1_4 = np.std(m4_f1_scores)
    mean_acc_4 = np.mean(m4_acc_scores)
    print(f"  >> BiLSTM 5-Fold Mean Macro-F1: {mean_f1_4:.4f} ± {std_f1_4:.4f} | Mean Accuracy: {mean_acc_4*100:.2f}%", flush=True)
    results_summary.append(("Hybrid BiLSTM + Attention", mean_f1_4, std_f1_4, mean_acc_4))

    # -----------------------------------------------------------------------
    # MODEL 5: Multilingual MiniLM Transformer + Classification Head
    # -----------------------------------------------------------------------
    print("\n" + "=" * 60, flush=True)
    print(">>> [MODEL 5/5] PRETRAINED MULTILINGUAL MINILM TRANSFORMER", flush=True)
    print("=" * 60, flush=True)
    print("  Pre-extracting 384-dimensional dense sentence embeddings...", end="", flush=True)
    t_emb = time.time()
    from dl.predict_dl import load_transformer
    from dl.train_transformer import mean_pooling, MultilingualClassificationHead

    tokenizer, transformer, _ = load_transformer()
    transformer.eval()

    all_embeddings = []
    batch_size = 64
    for i in range(0, len(X), batch_size):
        b_texts = X[i : i + batch_size]
        encoded = tokenizer(b_texts, padding=True, truncation=True, max_length=64, return_tensors="pt")
        with torch.no_grad():
            out = transformer(**encoded)
            pooled = mean_pooling(out, encoded["attention_mask"])
            normed = F.normalize(pooled, p=2, dim=1)
            all_embeddings.append(normed.cpu())

    X_emb = torch.cat(all_embeddings, dim=0).numpy()
    print(f" Done ({time.time()-t_emb:.1f}s) Shape: {X_emb.shape}", flush=True)

    m5_f1_scores = []
    m5_acc_scores = []

    for fold, (train_idx, val_idx) in enumerate(skf.split(X, y), 1):
        print(f"  [MiniLM] Starting Fold {fold}/5...", end="", flush=True)
        t_fold = time.time()
        X_tr = torch.tensor(X_emb[train_idx], dtype=torch.float32)
        y_tr = torch.tensor(y[train_idx], dtype=torch.long)
        X_va = torch.tensor(X_emb[val_idx], dtype=torch.float32)
        y_va = torch.tensor(y[val_idx], dtype=torch.long)

        head = MultilingualClassificationHead(in_features=384, num_classes=3)
        optimizer = torch.optim.AdamW(head.parameters(), lr=2e-3, weight_decay=1e-3)
        criterion = nn.CrossEntropyLoss()

        head.train()
        for ep in range(15):
            optimizer.zero_grad()
            logits = head(X_tr)
            loss = criterion(logits, y_tr)
            loss.backward()
            optimizer.step()

        head.eval()
        with torch.no_grad():
            val_logits = head(X_va)
            preds = torch.argmax(val_logits, dim=-1).numpy()

        f1 = f1_score(y[val_idx], preds, average="macro")
        acc = accuracy_score(y[val_idx], preds)
        m5_f1_scores.append(f1)
        m5_acc_scores.append(acc)
        print(f" Done ({time.time()-t_fold:.1f}s) | Macro-F1: {f1:.4f} | Accuracy: {acc*100:.2f}%", flush=True)

    mean_f1_5 = np.mean(m5_f1_scores)
    std_f1_5 = np.std(m5_f1_scores)
    mean_acc_5 = np.mean(m5_acc_scores)
    print(f"  >> MiniLM 5-Fold Mean Macro-F1: {mean_f1_5:.4f} ± {std_f1_5:.4f} | Mean Accuracy: {mean_acc_5*100:.2f}%", flush=True)
    results_summary.append(("Pretrained MiniLM Transformer", mean_f1_5, std_f1_5, mean_acc_5))

    # -----------------------------------------------------------------------
    # FINAL BENCHMARK SUMMARY TABLE
    # -----------------------------------------------------------------------
    print("\n" + "=" * 80, flush=True)
    print("5-FOLD CROSS-VALIDATION BENCHMARK RESULTS (COMMON DURATION DATASET)", flush=True)
    print("=" * 80, flush=True)
    header = f"{'Model':<35} | {'Macro-F1 (Mean ± Std)':<22} | {'Accuracy':<10}"
    print(header, flush=True)
    print("-" * 80, flush=True)
    report_lines = [
        "================================================================================",
        "TELECOM VOC INTELLIGENCE: MODEL BENCHMARK ON COMMON DURATION REVIEWS",
        "Window: 2025-08-24 to 2026-09-30 (Shared across GP, Banglalink, Robi)",
        "================================================================================",
        header,
        "-" * 80,
    ]
    for name, f1, std, acc in results_summary:
        row = f"{name:<35} | {f1:.4f} ± {std:.4f}            | {acc*100:.2f}%"
        print(row, flush=True)
        report_lines.append(row)
    print("=" * 80, flush=True)

    # -----------------------------------------------------------------------
    # FULL DATASET INFERENCE (83,417 REVIEWS) VIA TOP ENSEMBLE MODEL
    # -----------------------------------------------------------------------
    print("\n" + "=" * 80, flush=True)
    print("RUNNING FULL-DATASET INFERENCE ON ALL 83,417 COMMON REVIEWS (Ensemble Model)...", flush=True)
    print("=" * 80, flush=True)

    # Train production ensemble on full benchmark set
    full_vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), sublinear_tf=True, min_df=2)
    X_train_vec = full_vec.fit_transform(X)
    prod_lr = LogisticRegression(class_weight="balanced", max_iter=1000, C=1.5, random_state=42)
    prod_svc = CalibratedClassifierCV(estimator=LinearSVC(class_weight="balanced", C=0.8, random_state=42), cv=3)
    prod_cnb = ComplementNB(alpha=0.5)
    prod_ensemble = VotingClassifier(
        estimators=[("lr", prod_lr), ("svc", prod_svc), ("cnb", prod_cnb)],
        voting="soft",
        weights=[1.2, 1.2, 0.8]
    )
    prod_ensemble.fit(X_train_vec, y)

    # Predict entire 83,417 dataset in batches
    t_inf = time.time()
    batch_size_inf = 10000
    all_preds_label = []
    all_probs_pos = []
    all_probs_neg = []

    for i in range(0, len(full_df), batch_size_inf):
        b_texts = [str(t) if pd.notna(t) and str(t).lower() != "nan" and len(str(t).strip()) > 0 else " " for t in full_df["review_text"].iloc[i : i + batch_size_inf]]
        b_vec = full_vec.transform(b_texts)
        b_preds = prod_ensemble.predict(b_vec)
        b_probs = prod_ensemble.predict_proba(b_vec)
        all_preds_label.extend([INV_LABEL_MAP[p] for p in b_preds])
        all_probs_pos.extend(b_probs[:, 2])
        all_probs_neg.extend(b_probs[:, 0])
        print(f"  Classified batch {i+len(b_texts):,d}/{len(full_df):,d} reviews...", flush=True)

    print(f"Full inference completed in {time.time()-t_inf:.2f}s ({len(full_df)/(time.time()-t_inf):.0f} reviews/sec)!", flush=True)

    full_df["predicted_sentiment"] = all_preds_label
    full_df["positive_probability"] = np.round(all_probs_pos, 4)
    full_df["negative_probability"] = np.round(all_probs_neg, 4)

    # Save classified full dataset
    cols_to_save = ["operator", "review_date", "rating", "review_text", "predicted_sentiment", "positive_probability", "negative_probability"]
    full_df[cols_to_save].to_csv(CLASSIFIED_CSV, index=False)
    print(f"Classified full dataset saved to: {CLASSIFIED_CSV.name}", flush=True)

    # Multi-Brand VoC Comparison Table
    print("\n" + "=" * 80, flush=True)
    print("VOICE-OF-CUSTOMER COMPARISON ACROSS OPERATORS IN COMMON DURATION", flush=True)
    print("=" * 80, flush=True)
    voc_report = []
    voc_report.append("\n================================================================================")
    voc_report.append("OPERATOR VOICE-OF-CUSTOMER SENTIMENT BENCHMARK (COMMON DURATION)")
    voc_report.append("================================================================================")
    voc_header = f"{'Operator':<15} | {'Total Reviews':<13} | {'Positive %':<11} | {'Neutral %':<10} | {'Negative %':<11} | {'Net Sentiment (NSS)':<18}"
    print(voc_header, flush=True)
    print("-" * 85, flush=True)
    voc_report.append(voc_header)
    voc_report.append("-" * 85)

    for op in ["Grameenphone", "Banglalink", "Robi"]:
        op_data = full_df[full_df["operator"] == op]
        total_op = len(op_data)
        pos = (op_data["predicted_sentiment"] == "Positive").sum()
        neu = (op_data["predicted_sentiment"] == "Neutral").sum()
        neg = (op_data["predicted_sentiment"] == "Negative").sum()
        pos_pct = (pos / total_op) * 100
        neu_pct = (neu / total_op) * 100
        neg_pct = (neg / total_op) * 100
        nss = pos_pct - neg_pct  # Net Sentiment Score
        row = f"{op:<15} | {total_op:<13,d} | {pos_pct:>9.1f}%  | {neu_pct:>8.1f}%  | {neg_pct:>9.1f}%  | {nss:>+16.1f}%"
        print(row, flush=True)
        voc_report.append(row)

    print("=" * 80, flush=True)
    report_lines.extend(voc_report)
    REPORT_TXT.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"\nComprehensive report written to: {REPORT_TXT.name}", flush=True)


if __name__ == "__main__":
    main()
