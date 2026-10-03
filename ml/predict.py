import argparse
import sys
from pathlib import Path
import joblib

ML_DIR = Path(__file__).resolve().parent
MODEL_PATH = ML_DIR / "models" / "primary_logistic_regression.joblib"


def load_model():
    if not MODEL_PATH.exists():
        print(f"Error: Model artifact not found at {MODEL_PATH}")
        print("Please run `python ml/train_sentiment.py` first.")
        sys.exit(1)
    return joblib.load(MODEL_PATH)


def predict_sentiment(text: str, model=None):
    if model is None:
        model = load_model()

    prediction = model.predict([text])[0]
    probabilities = model.predict_proba([text])[0]
    prob_dict = {
        cls: round(float(prob), 4)
        for cls, prob in zip(model.classes_, probabilities)
    }

    return {
        "text": text,
        "sentiment": prediction,
        "confidence": prob_dict[prediction],
        "probabilities": prob_dict,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Predict telecom review sentiment (Bangla, Banglish, English)"
    )
    parser.add_argument(
        "--text", "-t",
        type=str,
        help="Review text to classify",
    )
    args = parser.parse_args()

    model = load_model()

    if args.text:
        res = predict_sentiment(args.text, model)
        print("\n" + "=" * 50)
        print(f"Input Review : {res['text']}")
        print(f"Sentiment    : {res['sentiment']}")
        print(f"Confidence   : {res['confidence'] * 100:.2f}%")
        print("Probability Breakdown:")
        for sentiment, prob in res["probabilities"].items():
            print(f"  - {sentiment:8s}: {prob * 100:6.2f}%")
        print("=" * 50)
    else:
        print("Interactive Telecom Sentiment Classifier")
        print("Enter review text in Bangla, Banglish, or English (type 'exit' or 'q' to quit):")
        print("-" * 50)
        while True:
            try:
                line = input("\nReview > ").strip()
                if not line:
                    continue
                if line.lower() in ("exit", "quit", "q"):
                    break
                res = predict_sentiment(line, model)
                print(f"-> Sentiment: {res['sentiment']} (Confidence: {res['confidence'] * 100:.1f}%)")
                print(f"   Probabilities: {res['probabilities']}")
            except (KeyboardInterrupt, EOFError):
                break
        print("\nGoodbye!")


if __name__ == "__main__":
    main()
