#!/usr/bin/env python3
"""
scripts/upload_to_huggingface.py
Automated script to upload fine-tuned BUET BanglaBERT models to Hugging Face Model Hub:
1. telecom-voc-banglabert-sentiment (3-class Sentiment: Negative, Neutral, Positive)
2. telecom-voc-banglabert-category  (5-class Operational Category: App Login, Network, Billing, Offers, General)

Includes auto-generated Model Cards (README.md) with metadata, performance leaderboards,
and 2-line Python reproducibility snippets.
"""

import os
import sys
import argparse
from pathlib import Path

# Paths
REPO_ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = REPO_ROOT / "dl" / "models"
SENTIMENT_DIR = MODELS_DIR / "banglabert_finetuned_sentiment"
CATEGORY_DIR = MODELS_DIR / "banglabert_finetuned_category"

SENTIMENT_README = """---
language:
- bn
- en
license: mit
library_name: transformers
tags:
- text-classification
- sentiment-analysis
- bangla
- bengali
- banglish
- code-mixing
- telecommunications
- voice-of-customer
base_model: csebuetnlp/banglabert
pipeline_tag: text-classification
metrics:
- accuracy
- f1
model-index:
- name: telecom-voc-banglabert-sentiment
  results:
  - task:
      type: text-classification
      name: Sentiment Analysis
    dataset:
      type: telecom-voc-bd
      name: Telecom Voice-of-Customer Multi-Year Benchmark (Bangladesh)
    metrics:
    - type: accuracy
      value: 0.9160
    - type: f1
      value: 0.8598
---

# Telecom VoC BanglaBERT — Sentiment Analysis

Fine-tuned [BUET BanglaBERT (`csebuetnlp/banglabert`)](https://huggingface.co/csebuetnlp/banglabert) for **3-class Sentiment Analysis** (Positive, Neutral, Negative) across code-mixed Bengali, Romanized Banglish, and English telecommunications customer feedback.

This model is a primary verification anchor for the research paper:  
*“With Great Reviews Comes Great Responsibility: An Intelligent Decision Support System for Telecommunications Voice-of-the-Customer Diagnostics and Cross-Layer Subsystem Decoupling”* (Submitted to *Expert Systems with Applications*).

## Model Details
- **Base Architecture:** `csebuetnlp/banglabert` (110M Parameters, 12 layers, 768 hidden dimension)
- **Task:** 3-Class Sentiment Polarity (`Negative`, `Neutral`, `Positive`)
- **Dataset:** 4,500 annotated seed reviews across Grameenphone, Robi Axiata, and Banglalink, benchmarked over a 655,649 longitudinal review corpus (2016–2026).
- **Performance:** **91.60% Cross-Validation Accuracy** | **0.8598 Macro-F1** (Held-out Test Split $N=675$: **88.40% Accuracy** | **0.8173 Macro-F1**)

> [!NOTE]
> **Out-of-Domain Linguistic Limitation (DISC-MIN-08)**: BUET BanglaBERT is pretrained predominantly on formal Bengali script. While achieving state-of-the-art representations on native Bangla script, heavy Romanized Banglish (phonetic Bengali in Latin script) is out-of-domain for its tokenizer vocabulary. For high-volume Banglish streams, pairing with the Classical Soft-Voting Ensemble is recommended.

## Quickstart & Replication

```python
from transformers import pipeline

# Load pipeline directly from Hugging Face Hub
classifier = pipeline(
    "text-classification",
    model="{username}/telecom-voc-banglabert-sentiment"
)

# Test on Bengali / Banglish reviews
samples = [
    "নেট স্পিড একদম বাজে, সারাদিন বাফারিং করে",     # Negative
    "App login e problem hocche, OTP ashe na",       # Negative
    "Darun offer, valo service grameenphone er",      # Positive
]

for s in samples:
    print(s, "->", classifier(s))
```

Or with `AutoModelForSequenceClassification`:

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

model_id = "{username}/telecom-voc-banglabert-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSequenceClassification.from_pretrained(model_id)

inputs = tokenizer("App khule na bar bar crash kore", return_tensors="pt")
with torch.no_grad():
    logits = model(**inputs).logits
predicted_class = logits.argmax().item()
print("Sentiment:", model.config.id2label[predicted_class])
```

## Citation & Codebase
GitHub Repository: [telecom-Voice-of-Customer_intelligence](https://github.com/rh61632/telecom-Voice-of-Customer_intelligence)
"""

CATEGORY_README = """---
language:
- bn
- en
license: mit
library_name: transformers
tags:
- text-classification
- aspect-based-sentiment-analysis
- bangla
- bengali
- banglish
- telecommunications
- voice-of-customer
base_model: csebuetnlp/banglabert
pipeline_tag: text-classification
metrics:
- accuracy
- f1
model-index:
- name: telecom-voc-banglabert-category
  results:
  - task:
      type: text-classification
      name: Operational Category Classification
    dataset:
      type: telecom-voc-bd
      name: Telecom Voice-of-Customer Multi-Year Benchmark (Bangladesh)
    metrics:
    - type: accuracy
      value: 0.8527
    - type: f1
      value: 0.7624
---

# Telecom VoC BanglaBERT — Operational Category Classification

Fine-tuned [BUET BanglaBERT (`csebuetnlp/banglabert`)](https://huggingface.co/csebuetnlp/banglabert) for **5-class Operational Category Discrimination** across telecommunications customer feedback in Bangladesh.

Decouples customer complaints across 5 core operational domains:
1. `App Login & Technical Bugs` (Client-side frontend application defects)
2. `Network Speed & 4G Latency` (Physical RF access, BTS backhaul, throughput)
3. `Billing & Airtime Deductions` (VAS auto-renewals, recharge failures, balance deductions)
4. `Offers & Data Packs` (Commercial tariffs, package pricing, bundle validity)
5. `General Appreciation / Other` (Generic brand feedback, customer service compliments)

## Model Details
- **Base Architecture:** `csebuetnlp/banglabert` (110M Parameters)
- **Task:** 5-Class Operational Category Triage
- **Performance:** **85.27% Cross-Validation Accuracy** | **0.7624 Macro-F1** (Held-out Test Split $N=675$: **87.11% Accuracy** | **0.8023 Macro-F1**)

> [!NOTE]
> **Out-of-Domain Linguistic Limitation (DISC-MIN-08)**: BUET BanglaBERT is pretrained predominantly on formal Bengali script. While achieving state-of-the-art representation on native Bangla script and mixed domains, severe Romanized Banglish expressions (phonetic Bengali in Latin script) are out-of-domain for its subword vocabulary. In high-density Banglish production environments, pairing with the Dual-Gram TF-IDF Classical Ensemble is recommended.

## Quickstart & Replication

```python
from transformers import pipeline

classifier = pipeline(
    "text-classification",
    model="{username}/telecom-voc-banglabert-category"
)

review = "Taka kete niyeche kintu MB dey nai"
print(classifier(review))
# Output: [{'label': 'Billing & Airtime Deductions', 'score': 0.96}]
```

## Citation & Codebase
GitHub Repository: [telecom-Voice-of-Customer_intelligence](https://github.com/rh61632/telecom-Voice-of-Customer_intelligence)
"""


def main():
    parser = argparse.ArgumentParser(description="Upload Telecom VoC BanglaBERT models to Hugging Face")
    parser.add_argument("--token", type=str, default=os.getenv("HF_TOKEN"), help="Hugging Face User Access Token (Write permissions)")
    parser.add_argument("--username", type=str, default=None, help="Hugging Face username")
    parser.add_argument("--private", action="store_true", help="Make repositories private (default is public)")
    args = parser.parse_args()

    # Verify dependencies
    try:
        from huggingface_hub import HfApi, login
    except ImportError:
        print("\n[!] huggingface_hub is required. Installing now...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "huggingface_hub"])
        from huggingface_hub import HfApi, login

    token = args.token
    if not token:
        print("\n" + "=" * 70)
        print("HUGGING FACE AUTHENTICATION")
        print("=" * 70)
        print("Please obtain an Access Token with WRITE permissions from:")
        print("https://huggingface.co/settings/tokens")
        token = input("\nEnter your Hugging Face Access Token: ").strip()

    login(token=token)
    api = HfApi(token=token)

    user_info = api.whoami()
    username = args.username or user_info["name"]
    print(f"\n[✓] Authenticated successfully as: {username}")

    repos = [
        {
            "name": "telecom-voc-banglabert-sentiment",
            "dir": SENTIMENT_DIR,
            "readme": SENTIMENT_README.format(username=username),
            "label": "Sentiment Polarity (3 Classes)"
        },
        {
            "name": "telecom-voc-banglabert-category",
            "dir": CATEGORY_DIR,
            "readme": CATEGORY_README.format(username=username),
            "label": "Operational Category (5 Classes)"
        }
    ]

    for r in repos:
        repo_id = f"{username}/{r['name']}"
        local_dir = r["dir"]
        print("\n" + "=" * 70)
        print(f"UPLOADING: {r['label']} -> {repo_id}")
        print("=" * 70)

        if not local_dir.exists():
            print(f"[!] Error: Local model directory not found: {local_dir}")
            continue

        # Save generated README.md locally inside the folder before upload
        readme_path = local_dir / "README.md"
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(r["readme"])

        # Create repo if not exists
        print(f"Creating / verifying repository: {repo_id}...")
        api.create_repo(
            repo_id=repo_id,
            repo_type="model",
            private=args.private,
            exist_ok=True
        )

        # Upload folder
        print(f"Uploading files from {local_dir}...")
        api.upload_folder(
            folder_path=str(local_dir),
            repo_id=repo_id,
            repo_type="model",
            commit_message=f"feat: upload fine-tuned {r['name']} checkpoint and model card"
        )
        print(f"[✓] Successfully uploaded: https://huggingface.co/{repo_id}")

    print("\n" + "=" * 70)
    print("ALL MODELS SUCCESSFULLY SYNCHRONIZED TO HUGGING FACE!")
    print("=" * 70)
    print(f"\n1. Sentiment Model : https://huggingface.co/{username}/telecom-voc-banglabert-sentiment")
    print(f"2. Category Model  : https://huggingface.co/{username}/telecom-voc-banglabert-category")
    print("\nAnyone can now load your models with 1 line of Python:")
    print(f"  classifier = pipeline('text-classification', model='{username}/telecom-voc-banglabert-sentiment')")


if __name__ == "__main__":
    main()
