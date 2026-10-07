import json
import os
from pathlib import Path
import time
from groq import Groq
import pandas as pd

# Verify API key availability
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
  raise SystemExit("Error: GROQ_API_KEY is not set.")

client = Groq(api_key=api_key)

# Resolve paths relative to project root
BASE_DIR = Path(__file__).resolve().parent.parent
input_file = BASE_DIR / "data" / "raw" / "mybl_raw_reviews.csv"
output_file = BASE_DIR / "data" / "processed" / "mybl_classified_reviews.csv"
output_file.parent.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(input_file)
results = []
start_idx = 0

# Checkpoint resumption logic
if output_file.exists():
  cached_df = pd.read_csv(output_file)
  start_idx = len(cached_df)
  results = cached_df.to_dict(orient="records")
  print(f"Resuming MyBL classification from index {start_idx}...")

SYSTEM_PROMPT = """You are an expert telecom customer operations analyst for Banglalink's MyBL app.
The user review is in Banglish (Romanized Bengali), Bengali, or English.

Classify the feedback into EXACTLY ONE operational category:
- 'Billing & Airtime Deductions'
- 'Network Speed & 4G Latency'
- 'App Login & Technical Bugs'
- 'Offers & Data Packs'
- 'General Appreciation / Other'

Determine sentiment: 'Negative', 'Neutral', or 'Positive'.
Provide a concise 1-sentence English translation/summary.

Return valid JSON only:
{
    "category": "string",
    "sentiment": "string",
    "english_summary": "string"
}"""


def classify(text):
  try:
    completion = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Customer Review (output json): {text}",
            },
        ],
        response_format={"type": "json_object"},
        temperature=0.1,
    )
    return json.loads(completion.choices[0].message.content)
  except Exception as e:
    return {
        "category": "Unclassified",
        "sentiment": "Neutral",
        "english_summary": str(e),
    }


for i in range(start_idx, len(df)):
  row = df.iloc[i].to_dict()
  res = classify(row["review_text"])

  row["category"] = res.get("category", "Unclassified")
  row["sentiment"] = res.get("sentiment", "Neutral")
  row["english_summary"] = res.get("english_summary", "")
  results.append(row)

  print(
      f"[MyBL {i+1}/{len(df)}] Rating: {row['rating']} | Category:"
      f" {row['category']}"
  )

  # Checkpoint save every 25 rows
  if (i + 1) % 25 == 0 or (i + 1) == len(df):
    pd.DataFrame(results).to_csv(output_file, index=False)
    print(f">> Checkpoint saved to {output_file}")

  time.sleep(2.1)
