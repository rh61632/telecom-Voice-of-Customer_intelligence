import argparse
import sys
from pathlib import Path
import re
import numpy as np
import torch
import torch.nn.functional as F

DL_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DL_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(DL_DIR) not in sys.path:
    sys.path.insert(0, str(DL_DIR))

MODELS_DIR = DL_DIR / "models"
LABEL_MAP = {"Negative": 0, "Neutral": 1, "Positive": 2}
INV_LABEL_MAP = {v: k for k, v in LABEL_MAP.items()}


def clean_text(text: str) -> str:
    text = str(text).strip()
    text = re.sub(r"(.)\1{2,}", r"\1\1", text)
    text = re.sub(r"\s+", " ", text)
    return text.lower()


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


def predict_bilstm(text: str, model, vocab):
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
        "sentiment": INV_LABEL_MAP[pred_idx],
        "confidence": float(probs[pred_idx]),
        "probabilities": {INV_LABEL_MAP[i]: round(float(p), 4) for i, p in enumerate(probs)},
    }


def load_transformer():
    from transformers import AutoTokenizer, AutoModel
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


def predict_transformer(text: str, tokenizer, transformer, head):
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
        "sentiment": INV_LABEL_MAP[pred_idx],
        "confidence": float(probs[pred_idx]),
        "probabilities": {INV_LABEL_MAP[i]: round(float(p), 4) for i, p in enumerate(probs)},
    }


def main():
    parser = argparse.ArgumentParser(description="Deep Learning Sentiment Classifier Inference")
    parser.add_argument("--model", choices=["bilstm", "transformer"], default="bilstm", help="Model type to use")
    parser.add_argument("--text", "-t", type=str, help="Review text to classify")
    args = parser.parse_args()

    if args.model == "bilstm":
        model, vocab = load_bilstm()
        predict_fn = lambda t: predict_bilstm(t, model, vocab)
        model_name = "BiLSTM with Self-Attention"
    else:
        tokenizer, transformer, head = load_transformer()
        predict_fn = lambda t: predict_transformer(t, tokenizer, transformer, head)
        model_name = "Multilingual MiniLM Transformer"

    if args.text:
        res = predict_fn(args.text)
        print("\n" + "=" * 50)
        print(f"Model        : {model_name}")
        print(f"Input Review : {res['text']}")
        print(f"Sentiment    : {res['sentiment']}")
        print(f"Confidence   : {res['confidence'] * 100:.2f}%")
        print("Probabilities:")
        for s, p in res["probabilities"].items():
            print(f"  - {s:8s}: {p * 100:6.2f}%")
        print("=" * 50)
    else:
        print(f"Interactive {model_name} Sentiment Classifier (Bangla, Banglish, English)")
        print("Type 'exit' to quit.")
        while True:
            try:
                line = input("\nReview > ").strip()
                if not line or line.lower() in ("exit", "quit", "q"):
                    break
                res = predict_fn(line)
                print(f"-> {res['sentiment']} ({res['confidence'] * 100:.1f}%) | {res['probabilities']}")
            except (KeyboardInterrupt, EOFError):
                break


if __name__ == "__main__":
    main()
