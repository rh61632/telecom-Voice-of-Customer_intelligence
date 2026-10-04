import argparse
import sys
import warnings
from pathlib import Path
import numpy as np
import joblib

warnings.filterwarnings("ignore")

ML_DIR = Path(__file__).resolve().parent
MODELS_DIR = ML_DIR / "models"

MODEL_PATHS = {
    "ensemble": MODELS_DIR / "ensemble_voting_classifier.joblib",
    "logistic": MODELS_DIR / "primary_logistic_regression.joblib",
    "linearsvc": MODELS_DIR / "challenger_linearsvc.joblib",
}

CATEGORY_MODEL_PATH = MODELS_DIR / "category_voting_classifier.joblib"
FILTERED_SENTIMENT_PATH = MODELS_DIR / "sentiment_ensemble_filtered_min3words.joblib"
FILTERED_CATEGORY_PATH = MODELS_DIR / "category_ensemble_filtered_min3words.joblib"


def load_model(model_name: str = "ensemble", use_filtered: bool = False):
    if use_filtered and FILTERED_SENTIMENT_PATH.exists():
        return joblib.load(FILTERED_SENTIMENT_PATH), "ensemble (filtered >=3 words)"
    model_path = MODEL_PATHS.get(model_name)
    if not model_path or not model_path.exists():
        print(f"Model '{model_name}' not found at {model_path}. Falling back to available models...")
        for name, path in MODEL_PATHS.items():
            if path.exists():
                return joblib.load(path), name
        print("No trained models found. Run `python ml/train_sentiment.py` or `python ml/train_ensemble.py` first.")
        sys.exit(1)
    return joblib.load(model_path), model_name


def load_category_model(use_filtered: bool = False):
    if use_filtered and FILTERED_CATEGORY_PATH.exists():
        return joblib.load(FILTERED_CATEGORY_PATH)
    if CATEGORY_MODEL_PATH.exists():
        return joblib.load(CATEGORY_MODEL_PATH)
    return None


def predict_sentiment(text: str, model, model_name: str, cat_model=None):
    prediction = model.predict([text])[0]
    
    # Check if model supports predict_proba
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba([text])[0]
        prob_dict = {
            cls: round(float(prob), 4)
            for cls, prob in zip(model.classes_, probabilities)
        }
        confidence = prob_dict[prediction]
    else:
        prob_dict = {}
        confidence = 1.0

    cat_pred = None
    cat_conf = None
    if cat_model is not None:
        cat_pred = cat_model.predict([text])[0]
        if hasattr(cat_model, "predict_proba"):
            c_probs = cat_model.predict_proba([text])[0]
            cat_conf = round(float(np.max(c_probs)), 4)

    return {
        "text": text,
        "model": model_name,
        "sentiment": prediction,
        "confidence": confidence,
        "probabilities": prob_dict,
        "category": cat_pred,
        "category_confidence": cat_conf,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Predict telecom review sentiment using ML on device"
    )
    parser.add_argument(
        "--model", "-m",
        choices=["ensemble", "logistic", "linearsvc"],
        default="ensemble",
        help="Model architecture to use (default: ensemble)",
    )
    parser.add_argument(
        "--filtered", "-f",
        action="store_true",
        help="Use models trained on filtered substantive reviews (>= 3 words)",
    )
    parser.add_argument(
        "--text", "-t",
        type=str,
        help="Review text to classify",
    )
    args = parser.parse_args()

    model, actual_model_name = load_model(args.model, use_filtered=args.filtered)
    cat_model = load_category_model(use_filtered=args.filtered)

    if args.text:
        res = predict_sentiment(args.text, model, actual_model_name, cat_model)
        print("\n" + "=" * 60)
        print(f"Model Architecture  : {res['model'].upper()} ML")
        print(f"Input Review        : {res['text']}")
        print(f"Predicted Sentiment : {res['sentiment']} (Confidence: {res['confidence'] * 100:.2f}%)")
        if res["category"]:
            print(f"Predicted Comment Type: {res['category']} (Confidence: {res['category_confidence'] * 100:.2f}%)")
        if res["probabilities"]:
            print("\nSentiment Class Probabilities:")
            for s, prob in res["probabilities"].items():
                bar = "█" * int(prob * 25)
                print(f"  - {s:8s}: {prob * 100:6.2f}% {bar}")
        print("=" * 60)
    else:
        print(f"Interactive Telecom Review Analyzer [{actual_model_name.upper()}]")
        print("Enter review in Bangla, Banglish, or English (type 'exit' or 'q' to quit):")
        print("-" * 60)
        while True:
            try:
                line = input("\nReview > ").strip()
                if not line or line.lower() in ("exit", "quit", "q"):
                    break
                res = predict_sentiment(line, model, actual_model_name, cat_model)
                out_str = f"-> Sentiment: {res['sentiment']} ({res['confidence'] * 100:.1f}%)"
                if res["category"]:
                    out_str += f" | Type: {res['category']} ({res['category_confidence'] * 100:.1f}%)"
                print(out_str)
                if res["probabilities"]:
                    print(f"   Probabilities: {res['probabilities']}")
            except (KeyboardInterrupt, EOFError):
                break
        print("\nExited.")


if __name__ == "__main__":
    main()
