import os
import sys
from pathlib import Path
import numpy as np
import gradio as gr

# Ensure root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from ml.predict import load_model, load_category_model, predict_sentiment
from ml.language_detector import detector

# Preload production models
print("Loading VoC Intelligence models...")
sentiment_model, model_name = load_model("ensemble")
category_model = load_category_model()
print("Models loaded successfully!")

OPERATIONAL_DESCRIPTIONS = {
    "App Login & Technical Bugs": "Frontend Software Engineering (Authentication timeouts, biometric failure, crash on splash)",
    "Network Speed & 4G Latency": "Core Telecommunications RAN (RF propagation, 4G/3G drops, video buffering, fiber cut)",
    "Billing & Airtime Deductions": "Core Charging System (OCS) (Balance leakage, VAS auto-renewals, recharge failure)",
    "Offers & Data Packs": "Commercial / Marketing Strategy (Data package pricing, validity expiration, tariff restructuring)",
    "General Appreciation / Other": "Baseline User Experience (Generic 5-star praise, UI design compliments, customer care)"
}

def analyze_review(review_text: str):
    if not review_text or not review_text.strip():
        return "N/A", "N/A", "N/A", {}, {}, "Please enter a customer review."

    # Perform prediction
    res = predict_sentiment(review_text, sentiment_model, model_name, category_model)

    lang_badge = f"{res['language']} {'(Code-Mixed)' if res['is_code_mixed'] else ''}"
    sentiment_label = f"{res['sentiment']} ({res['confidence'] * 100:.1f}%)"
    category_label = (
        f"{res['category']} ({res['category_confidence'] * 100:.1f}%)"
        if res.get("category") and res.get("category_confidence") is not None
        else "N/A"
    )

    # Category probabilities
    cat_probs = {}
    if hasattr(category_model, "predict_proba"):
        probs = category_model.predict_proba([review_text])[0]
        cat_probs = {cls: float(p) for cls, p in zip(category_model.classes_, probs)}

    # Diagnostic triage attribution
    triage_note = OPERATIONAL_DESCRIPTIONS.get(res["category"], "")
    diagnostic_summary = (
        f"**Decoupled Subsystem:** {triage_note}\n\n"
        f"**Inference Hardware:** CPU (8.17 ms latency | 122.4 reviews/sec)\n"
        f"**Underlying Architecture:** Soft-Voting Ensemble (Calibrated LinearSVC + Balanced Logistic Regression + Complement Naive Bayes)"
    )

    return lang_badge, sentiment_label, category_label, res["probabilities"], cat_probs, diagnostic_summary

# Custom Gradio Interface
custom_css = """
.gradio-container { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
#title-box { text-align: center; margin-bottom: 1.5rem; }
"""

with gr.Blocks(title="Telecom VoC Intelligence", css=custom_css, theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 📱 Telecom Voice-of-Customer (VoC) Intelligence & Cross-Layer Diagnostics
        ### High-Throughput Multilingual Customer Intelligence for Telecommunications Self-Care Apps
        *Demonstrating models trained on 4,500 expert/LLM-labeled seed reviews and evaluated across 655,649 longitudinal customer reviews from Grameenphone, Robi Axiata, and Banglalink (2016–2026).*
        """
    )

    with gr.Row():
        with gr.Column(scale=1):
            input_text = gr.Textbox(
                label="Enter Customer Review (Bengali / Romanized Banglish / English)",
                placeholder="e.g., App khule na, bar bar crash kore login er shomoy...",
                lines=4
            )
            submit_btn = gr.Button("🔍 Classify & Decouple Subsystem", variant="primary")

            gr.Examples(
                examples=[
                    ["App khule na, bar bar crash kore login er shomoy"],
                    ["নেট স্পিড একদম স্লো, ফোরজি পেয়েও ভিডিও বাফারিং করে"],
                    ["Taka kete niyeche kintu MB dey nai, faltu service"],
                    ["Onek shundor offer ar kom dame bhalo internet pack"],
                    ["Very smooth app, recharge and balance check is super fast!"]
                ],
                inputs=[input_text],
                label="Benchmark Exemplar Grievances"
            )

        with gr.Column(scale=1):
            with gr.Row():
                out_lang = gr.Textbox(label="Detected Language / Modality", interactive=False)
                out_sent = gr.Textbox(label="Sentiment Polarity", interactive=False)
            
            out_cat = gr.Textbox(label="Operational Domain", interactive=False)
            
            with gr.Row():
                out_sent_probs = gr.Label(label="Sentiment Probabilities", num_top_classes=3)
                out_cat_probs = gr.Label(label="Category Probabilities", num_top_classes=5)
            
            out_diag = gr.Markdown(label="Diagnostic Subsystem Attribution")

    submit_btn.click(
        fn=analyze_review,
        inputs=[input_text],
        outputs=[out_lang, out_sent, out_cat, out_sent_probs, out_cat_probs, out_diag]
    )

    gr.Markdown(
        """
        ---
        **Research Paper:** *“An Intelligent Decision Support System for Telecommunications Voice-of-the-Customer Diagnostics and Cross-Layer Subsystem Decoupling”*  
        **Replication Codebase:** [GitHub Repository](https://github.com/rh61632/telecom-Voice-of-Customer_intelligence) | **Model Weights:** [Hugging Face Hub](https://huggingface.co/models?search=telecom-voc-banglabert)
        """
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
