#!/usr/bin/env python3
"""
dl/predict_dl.py
Unified multi-architecture Deep Learning Inference CLI for Sentiment Analysis
and Operational Category Discrimination across Telecom Voice-of-Customer reviews.

Supported architectures:
- bilstm: Local Word + Char-CNN BiLSTM (dl/models/bilstm_attention_model.pt)
- transformer: Local Multilingual MiniLM Head (dl/models/minilm_transformer_head.pt)
- bilstm-colab-sentiment: Colab Word-only BiLSTM (dl/models/bilstm_sentiment_model.pt)
- bilstm-colab-category: Colab Word-only BiLSTM (dl/models/bilstm_category_model.pt)
- banglabert-sentiment: Fine-tuned BUET BanglaBERT (dl/models/banglabert_finetuned_sentiment)
- banglabert-category: Fine-tuned BUET BanglaBERT (dl/models/banglabert_finetuned_category)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import warnings
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np
import torch
import torch.nn.functional as F

warnings.filterwarnings("ignore", category=UserWarning)

DL_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DL_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(DL_DIR) not in sys.path:
    sys.path.insert(0, str(DL_DIR))

MODELS_DIR = DL_DIR / "models"

# Default Sentiment Map for local BiLSTM & MiniLM
SENTIMENT_LABEL_MAP = {"Negative": 0, "Neutral": 1, "Positive": 2}
INV_SENTIMENT_MAP = {v: k for k, v in SENTIMENT_LABEL_MAP.items()}


def clean_text(text: str) -> str:
    text = str(text).strip()
    text = re.sub(r"(.)\1{2,}", r"\1\1", text)
    text = re.sub(r"\s+", " ", text)
    return text.lower()


# ---------------------------------------------------------------------------
# 1. Local Word + Char-CNN BiLSTM (Sentiment)
# ---------------------------------------------------------------------------
def load_bilstm():
    from dl.train_bilstm import BiLSTMWithAttention, Vocabulary

    model_path = MODELS_DIR / "bilstm_attention_model.pt"
    if not model_path.exists():
        raise FileNotFoundError(f"Model checkpoint not found at {model_path}. Train it first.")

    ckpt = torch.load(model_path, map_location="cpu", weights_only=False)
    vocab = Vocabulary()
    vocab.word2idx = ckpt["vocab_word2idx"]
    vocab.char2idx = ckpt["vocab_char2idx"]

    model = BiLSTMWithAttention(
        word_vocab_size=len(vocab.word2idx),
        char_vocab_size=len(vocab.char2idx),
    )
    model.load_state_dict(ckpt["model_state_dict"])
    model.eval()
    return model, vocab


def predict_bilstm(text: str, model, vocab) -> Dict[str, Any]:
    cleaned = clean_text(text)
    w_ids, c_ids = vocab.encode(cleaned)
    w_tensor = torch.tensor([w_ids], dtype=torch.long)
    c_tensor = torch.tensor([c_ids], dtype=torch.long)

    with torch.no_grad():
        logits = model(w_tensor, c_tensor)
        probs = F.softmax(logits, dim=-1).squeeze(0).numpy()
        pred_idx = int(np.argmax(probs))

    return {
        "text": text,
        "task": "Sentiment Analysis",
        "prediction": INV_SENTIMENT_MAP[pred_idx],
        "confidence": float(probs[pred_idx]),
        "probabilities": {INV_SENTIMENT_MAP[i]: round(float(p), 4) for i, p in enumerate(probs)},
    }


# ---------------------------------------------------------------------------
# 2. Local Multilingual MiniLM Transformer Head (Sentiment)
# ---------------------------------------------------------------------------
def load_transformer():
    try:
        from transformers import AutoTokenizer, AutoModel
    except ImportError as e:
        raise ImportError(
            "The 'transformers' library is required to run the MiniLM model.\n"
            "Install it via 'pip install -r dl/requirements.txt' or choose a BiLSTM model "
            "like '--model bilstm', '--model bilstm-colab-sentiment', or '--model bilstm-colab-category'."
        ) from e

    from dl.train_transformer import MultilingualClassificationHead, MODEL_NAME

    ckpt_path = MODELS_DIR / "minilm_transformer_head.pt"
    if not ckpt_path.exists():
        raise FileNotFoundError(f"Transformer head checkpoint not found at {ckpt_path}. Train it first.")
    ckpt = torch.load(ckpt_path, map_location="cpu", weights_only=False)
    model_id = ckpt.get("model_name", MODEL_NAME)
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    transformer = AutoModel.from_pretrained(model_id)
    transformer.eval()
    head = MultilingualClassificationHead(in_features=384)
    head.load_state_dict(ckpt["head_state_dict"])
    head.eval()
    return tokenizer, transformer, head


def predict_transformer(text: str, tokenizer, transformer, head) -> Dict[str, Any]:
    from dl.train_transformer import mean_pooling

    with torch.no_grad():
        encoded = tokenizer([text], padding=True, truncation=True, max_length=96, return_tensors="pt")
        out = transformer(**encoded)
        pooled = mean_pooling(out, encoded["attention_mask"])
        normed = F.normalize(pooled, p=2, dim=1)
        logits = head(normed)
        probs = F.softmax(logits, dim=-1).squeeze(0).numpy()
        pred_idx = int(np.argmax(probs))
    return {
        "text": text,
        "task": "Sentiment Analysis",
        "prediction": INV_SENTIMENT_MAP[pred_idx],
        "confidence": float(probs[pred_idx]),
        "probabilities": {INV_SENTIMENT_MAP[i]: round(float(p), 4) for i, p in enumerate(probs)},
    }


# ---------------------------------------------------------------------------
# 3. Colab Word-Only Hybrid BiLSTM + Attention (Sentiment & Category)
# ---------------------------------------------------------------------------
def load_bilstm_colab(task: str):
    import joblib
    from dl.bilstm_artifacts import HybridBiLSTMAttention, load_bilstm_vocab

    vocab = load_bilstm_vocab(MODELS_DIR)
    if task == "sentiment":
        le = joblib.load(MODELS_DIR / "sent_le.joblib")
        ckpt_path = MODELS_DIR / "bilstm_sentiment_model.pt"
        task_name = "Sentiment Analysis"
    else:
        le = joblib.load(MODELS_DIR / "cat_le.joblib")
        ckpt_path = MODELS_DIR / "bilstm_category_model.pt"
        task_name = "Operational Category"

    if not ckpt_path.exists():
        raise FileNotFoundError(f"Colab checkpoint not found at {ckpt_path}")

    classes = list(le.classes_)
    model = HybridBiLSTMAttention(len(vocab.word2idx), len(classes))
    model.load_state_dict(torch.load(ckpt_path, map_location="cpu", weights_only=False))
    model.eval()
    return model, vocab, classes, task_name


def predict_bilstm_colab(text: str, model, vocab, classes: List[str], task_name: str) -> Dict[str, Any]:
    seq = vocab.transform(text)
    x = torch.tensor([seq], dtype=torch.long)
    with torch.no_grad():
        logits = model(x)
        probs = F.softmax(logits, dim=-1).squeeze(0).numpy()
        pred_idx = int(np.argmax(probs))
    return {
        "text": text,
        "task": task_name,
        "prediction": classes[pred_idx],
        "confidence": float(probs[pred_idx]),
        "probabilities": {classes[i]: round(float(p), 4) for i, p in enumerate(probs)},
    }


# ---------------------------------------------------------------------------
# 4. BUET BanglaBERT Fine-Tuned Models (Sentiment & Category)
# ---------------------------------------------------------------------------
def load_banglabert(task: str):
    try:
        from transformers import AutoModelForSequenceClassification, AutoTokenizer
    except ImportError as e:
        raise ImportError(
            f"The 'transformers' library is required to run BanglaBERT models.\n"
            f"Install it via 'pip install -r dl/requirements.txt' or select a non-transformer model "
            f"like '--model bilstm-colab-{task}' or '--model bilstm'."
        ) from e

    model_dir = MODELS_DIR / f"banglabert_finetuned_{task}"
    if not model_dir.exists():
        raise FileNotFoundError(f"BanglaBERT model directory not found at {model_dir}")

    config_path = model_dir / "config.json"
    if not config_path.exists():
        raise FileNotFoundError(f"config.json missing in {model_dir}")

    with open(config_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    id2label = {int(k): v for k, v in cfg.get("id2label", {}).items()}

    tokenizer = AutoTokenizer.from_pretrained(str(model_dir))
    model = AutoModelForSequenceClassification.from_pretrained(str(model_dir))
    model.eval()

    task_name = "Sentiment Analysis" if task == "sentiment" else "Operational Category"
    return tokenizer, model, id2label, task_name


def predict_banglabert(text: str, tokenizer, model, id2label: Dict[int, str], task_name: str) -> Dict[str, Any]:
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=96)
    with torch.no_grad():
        logits = model(**inputs).logits
        probs = F.softmax(logits, dim=-1).squeeze(0).numpy()
        pred_idx = int(np.argmax(probs))
    return {
        "text": text,
        "task": task_name,
        "prediction": id2label[pred_idx],
        "confidence": float(probs[pred_idx]),
        "probabilities": {id2label[i]: round(float(p), 4) for i in sorted(id2label.keys())},
    }


def main():
    parser = argparse.ArgumentParser(description="Deep Learning Multi-Architecture Inference CLI")
    parser.add_argument(
        "--model",
        choices=[
            "bilstm",
            "transformer",
            "bilstm-colab",
            "bilstm-colab-sentiment",
            "bilstm-colab-category",
            "banglabert",
            "banglabert-sentiment",
            "banglabert-category",
        ],
        default=None,
        help="Deep learning model architecture to use for prediction (default: bilstm-colab)",
    )
    parser.add_argument(
        "--task",
        choices=["sentiment", "category"],
        default=None,
        help="Target task: 'sentiment' (3 classes) or 'category' (5 operational classes)",
    )
    parser.add_argument("--text", "-t", type=str, help="Review text to classify")
    args = parser.parse_args()

    # Determine resolved task and model
    selected_model = args.model
    selected_task = args.task

    if selected_model is None:
        if selected_task == "sentiment":
            selected_model = "bilstm-colab-sentiment"
        elif selected_task == "category":
            selected_model = "bilstm-colab-category"
        else:
            selected_model = "bilstm-colab-category"
            selected_task = "category"
    elif selected_model == "bilstm-colab":
        if selected_task == "sentiment":
            selected_model = "bilstm-colab-sentiment"
        else:
            selected_model = "bilstm-colab-category"
            selected_task = "category"
    elif selected_model == "banglabert":
        if selected_task == "category":
            selected_model = "banglabert-category"
        else:
            selected_model = "banglabert-sentiment"
            selected_task = "sentiment"
    elif selected_model in ("bilstm", "transformer"):
        if selected_task == "category":
            print(f"Note: Local {selected_model} checkpoint is trained for Sentiment Analysis. Running Sentiment task.")
        selected_task = "sentiment"
    elif "-sentiment" in selected_model:
        selected_task = "sentiment"
    elif "-category" in selected_model:
        selected_task = "category"

    # Dispatch model loader
    if selected_model == "bilstm":
        model, vocab = load_bilstm()
        predict_fn = lambda t: predict_bilstm(t, model, vocab)
        model_display = "Local BiLSTM with Char-CNN (Sentiment)"
    elif selected_model == "transformer":
        tokenizer, transformer, head = load_transformer()
        predict_fn = lambda t: predict_transformer(t, tokenizer, transformer, head)
        model_display = "Local Multilingual MiniLM Transformer Head (Sentiment)"
    elif selected_model == "bilstm-colab-sentiment":
        model, vocab, classes, task_name = load_bilstm_colab("sentiment")
        predict_fn = lambda t: predict_bilstm_colab(t, model, vocab, classes, task_name)
        model_display = "Colab Word-Only Hybrid BiLSTM + Attention (Sentiment)"
    elif selected_model == "bilstm-colab-category":
        model, vocab, classes, task_name = load_bilstm_colab("category")
        predict_fn = lambda t: predict_bilstm_colab(t, model, vocab, classes, task_name)
        model_display = "Colab Word-Only Hybrid BiLSTM + Attention (Operational Category)"
    elif selected_model == "banglabert-sentiment":
        tokenizer, model, id2label, task_name = load_banglabert("sentiment")
        predict_fn = lambda t: predict_banglabert(t, tokenizer, model, id2label, task_name)
        model_display = "BUET BanglaBERT Fine-Tuned (Sentiment)"
    elif selected_model == "banglabert-category":
        tokenizer, model, id2label, task_name = load_banglabert("category")
        predict_fn = lambda t: predict_banglabert(t, tokenizer, model, id2label, task_name)
        model_display = "BUET BanglaBERT Fine-Tuned (Operational Category)"
    else:
        raise ValueError(f"Unknown model architecture: {selected_model}")

    if args.text:
        res = predict_fn(args.text)
        print("\n" + "=" * 65)
        print(f"Model Architecture : {model_display}")
        print(f"Target Task        : {res['task']}")
        print(f"Input Review       : {res['text']}")
        print(f"Predicted Class    : {res['prediction']}")
        print(f"Confidence         : {res['confidence'] * 100:.2f}%")
        print("Class Probabilities:")
        for label, prob in res["probabilities"].items():
            print(f"  - {label:32s}: {prob * 100:6.2f}%")
        print("=" * 65)
    else:
        print(f"\nInteractive {model_display}")
        print("Type 'exit' to quit.\n")
        while True:
            try:
                line = input("Review > ").strip()
                if not line or line.lower() in ("exit", "quit", "q"):
                    break
                res = predict_fn(line)
                print(f"-> {res['prediction']} ({res['confidence'] * 100:.1f}%) | {res['probabilities']}\n")
            except (KeyboardInterrupt, EOFError):
                break


if __name__ == "__main__":
    main()
