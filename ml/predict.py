import argparse
import sys
from pathlib import Path
import joblib

ML_DIR = Path(__file__).resolve().parent
MODELS_DIR = ML_DIR / "models"

MODEL_PATHS = {
    "ensemble": MODELS_DIR / "ensemble_voting_classifier.joblib",
    "logistic": MODELS_DIR / "primary_logistic_regression.joblib",
    "linearsvc": MODELS_DIR / "challenger_linearsvc.joblib",
}


def load_model(model_name: str = "ensemble"):
    model_path = MODEL_PATHS.get(model_name)
    if not model_path or not model_path.exists():
        print(f"Model '{model_name}' not found at {model_path}. Falling back to available models...")
        for name, path in MODEL_PATHS.items():
            if path.exists():
                return joblib.load(path), name
        print("No trained models found. Run `python ml/train_sentiment.py` or `python ml/train_ensemble.py` first.")
        sys.exit(1)
    return joblib.load(model_path), model_name


def predict_sentiment(text: str, model, model_name: str):
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

    return {
        "text": text,
        "model": model_name,
        "sentiment": prediction,
        "confidence": confidence,
        "probabilities": prob_dict,
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
        "--text", "-t",
        type=str,
        help="Review text to classify",
    )
    args = parser.parse_args()

    model, actual_model_name = load_model(args.model)

    if args.text:
        res = predict_sentiment(args.text, model, actual_model_name)
        print("\n" + "=" * 55)
        print(f"Model Architecture : {res['model'].upper()} ML")
        print(f"Input Review       : {res['text']}")
        print(f"Predicted Sentiment: {res['sentiment']}")
        if res["probabilities"]:
            print(f"Confidence         : {res['confidence'] * 100:.2f}%")
            print("Class Probabilities:")
            for s, prob in res["probabilities"].items():
                bar = "█" * int(prob * 25)
                print(f"  - {s:8s}: {prob * 100:6.2f}% {bar}")
        print("=" * 55)
    else:
        print(f"Interactive Telecom Sentiment Classifier [{actual_model_name.upper()}]")
        print("Enter review in Bangla, Banglish, or English (type 'exit' or 'q' to quit):")
        print("-" * 55)
        while True:
            try:
                line = input("\nReview > ").strip()
                if not line or line.lower() in ("exit", "quit", "q"):
                    break
                res = predict_sentiment(line, model, actual_model_name)
                print(f"-> Sentiment: {res['sentiment']} (Confidence: {res['confidence'] * 100:.1f}%)")
                if res["probabilities"]:
                    print(f"   Probabilities: {res['probabilities']}")
            except (KeyboardInterrupt, EOFError):
                break
        print("\nExited.")


if __name__ == "__main__":
    main()
