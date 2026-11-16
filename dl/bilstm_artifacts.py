"""
dl/bilstm_artifacts.py
Shared neural architectures and portable vocabulary loaders for the
Hybrid BiLSTM + Attention model suite. Eliminates __main__.Vocabulary
pickling fragility across production scripts.
"""

from __future__ import annotations

import json
import pickle
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import torch
import torch.nn as nn


class Vocabulary:
    """Portable vocabulary container with token transform methods."""

    def __init__(
        self,
        min_freq: int = 2,
        word2idx: Optional[Dict[str, int]] = None,
        idx2word: Optional[Dict[int, str]] = None,
        max_len: int = 40,
    ) -> None:
        self.min_freq = min_freq
        self.max_len = max_len
        if word2idx is not None:
            self.word2idx = dict(word2idx)
        else:
            self.word2idx = {"<pad>": 0, "<unk>": 1}

        if idx2word is not None:
            self.idx2word = {int(k): v for k, v in idx2word.items()}
        else:
            self.idx2word = {0: "<pad>", 1: "<unk>"}

    def transform(self, text: str, max_len: Optional[int] = None) -> List[int]:
        """Convert a text string into a fixed-length list of integer token IDs."""
        limit = max_len if max_len is not None else self.max_len
        words = str(text).lower().split()[:limit]
        seq = [self.word2idx.get(w, 1) for w in words]
        return seq + [0] * (limit - len(seq))

    def to_dict(self) -> dict:
        """Serialize vocabulary state to a clean JSON-serializable dictionary."""
        return {
            "min_freq": self.min_freq,
            "max_len": self.max_len,
            "word2idx": self.word2idx,
            "idx2word": {str(k): v for k, v in self.idx2word.items()},
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Vocabulary":
        """Instantiate Vocabulary from a dictionary."""
        return cls(
            min_freq=data.get("min_freq", 2),
            word2idx=data["word2idx"],
            idx2word={int(k): v for k, v in data["idx2word"].items()},
            max_len=data.get("max_len", 40),
        )

    @classmethod
    def from_json(cls, json_path: Union[str, Path]) -> "Vocabulary":
        """Load vocabulary from a JSON file."""
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)

    def __len__(self) -> int:
        return len(self.word2idx)


class BahdanauAttention(nn.Module):
    """Additive Bahdanau Attention mechanism for bidirectional recurrent hidden states."""

    def __init__(self, hidden_dim: int) -> None:
        super().__init__()
        self.w = nn.Linear(hidden_dim, hidden_dim)
        self.v = nn.Linear(hidden_dim, 1, bias=False)

    def forward(self, rnn_outputs: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        energy = torch.tanh(self.w(rnn_outputs))
        weights = torch.softmax(self.v(energy), dim=1)
        context = torch.sum(weights * rnn_outputs, dim=1)
        return context, weights


class HybridBiLSTMAttention(nn.Module):
    """Single-layer bidirectional LSTM with Bahdanau attention and dropout regularization."""

    def __init__(
        self,
        vocab_size: int,
        num_classes: int,
        embed_dim: int = 128,
        hidden_dim: int = 128,
    ) -> None:
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.bilstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True, bidirectional=True)
        self.attention = BahdanauAttention(hidden_dim * 2)
        self.fc = nn.Sequential(
            nn.Dropout(0.4),
            nn.Linear(hidden_dim * 2, 64),
            nn.ReLU(),
            nn.Linear(64, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        embedded = self.embedding(x)
        outputs, _ = self.bilstm(embedded)
        context, _ = self.attention(outputs)
        return self.fc(context)


def load_bilstm_vocab(dl_dir: Union[str, Path]) -> Vocabulary:
    """Load the BiLSTM vocabulary from JSON (preferred) or fallback to joblib."""
    dl_dir = Path(dl_dir)
    json_path = dl_dir / "bilstm_vocab.json"
    if json_path.exists():
        return Vocabulary.from_json(json_path)

    joblib_path = dl_dir / "bilstm_vocab.joblib"
    if not joblib_path.exists():
        raise FileNotFoundError(
            f"Neither bilstm_vocab.json nor bilstm_vocab.joblib found in {dl_dir}"
        )

    # Temporary shim for __main__.Vocabulary during joblib loading
    main_mod = sys.modules.get("__main__")
    prev_vocab = getattr(main_mod, "Vocabulary", None) if main_mod is not None else None
    try:
        import joblib
        if main_mod is not None:
            main_mod.Vocabulary = Vocabulary
        raw_vocab = joblib.load(joblib_path)
        if isinstance(raw_vocab, dict):
            word2idx = raw_vocab.get("word2idx", {})
            idx2word = raw_vocab.get("idx2word", {})
            min_freq = raw_vocab.get("min_freq", 2)
            max_len = raw_vocab.get("max_len", 40)
        else:
            word2idx = getattr(raw_vocab, "word2idx", {})
            idx2word = getattr(raw_vocab, "idx2word", {})
            min_freq = getattr(raw_vocab, "min_freq", 2)
            max_len = getattr(raw_vocab, "max_len", 40)
        return Vocabulary(min_freq=min_freq, word2idx=word2idx, idx2word=idx2word, max_len=max_len)
    finally:
        if main_mod is not None:
            if prev_vocab is not None:
                main_mod.Vocabulary = prev_vocab
            elif hasattr(main_mod, "Vocabulary"):
                delattr(main_mod, "Vocabulary")
