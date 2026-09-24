import json
import os
import time
from groq import Groq
import pandas as pd

api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
  raise SystemExit("Error: GROQ_API_KEY is not set in your environment.")

client = Groq(api_key=api_key)

# Load scraped reviews
df = pd.read_csv("mygp_raw_reviews.csv")
print(f"Loaded {len(df)} reviews to process.")

SYSTEM_PROMPT = """
You are an expert telecom customer operations analyst for Grameenphone's MyGP app.
The user review is in Banglish (Romanized Bengali), standard Bengali, or English.

Classify the feedback into EXACTLY ONE operational category:
- 'Billing & Airtime Deductions'
- 'Network Speed & 4G Latency'
- 'App Login & Technical Bugs'
- 'Offers & Data Packs'
- 'General Appreciation / Other'

Determine sentiment: 'Negative', 'Neutral', or 'Positive'.
Provide a concise 1-sentence English translation/summary.

Return ONLY a valid JSON object matching this schema:
{
    "category": string,
    "sentiment": string,
    "english_summary": string
}
"""


def process_review_text(text):
  try:
    chat_completion = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Customer Review: {text}"},
        ],
        response_format={"type": "json_object"},
        temperature=0.1,
    )
    return json.loads(chat_completion.choices[0].message.content)
  except Exception as err:
    return {
        "category": "Unclassified",
        "sentiment": "Neutral",
        "english_summary": f"Parse error: {str(err)}",
    }


output_file = "mygp_classified_reviews.csv"
results = []
start_index = 0

# Resume from checkpoint if interrupted
if os.path.exists(output_file):
  cached_df = pd.read_csv(output_file)
  start_index = len(cached_df)
  results = cached_df.to_dict(orient="records")
  print(f"Resuming pipeline from index {start_index}...")

for i in range(start_index, len(df)):
  row = df.iloc[i].to_dict()
  ai_data = process_review_text(row["review_text"])

  row["category"] = ai_data.get("category", "Unclassified")
  row["sentiment"] = ai_data.get("sentiment", "Neutral")
  row["english_summary"] = ai_data.get("english_summary", "")
  results.append(row)

  print(
      f"[{i+1}/{len(df)}] Rating: {row['rating']} | Category: {row['category']}"
  )

  # Save progress every 25 records
  if (i + 1) % 25 == 0 or (i + 1) == len(df):
    pd.DataFrame(results).to_csv(output_file, index=False)
    print(f">> Checkpoint saved to {output_file}")

  # Throttling to respect Groq free tier (30 requests/min max)
  time.sleep(2.1)

print(
    "Classification completed. Final dataset saved to"
    f" {output_file} successfully."
)