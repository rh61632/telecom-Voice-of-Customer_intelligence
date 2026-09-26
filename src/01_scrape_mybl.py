from pathlib import Path
import pandas as pd
from google_play_scraper import Sort, reviews

print("Connecting to Google Play Store (MyBL app)...")

# Fetch reviews from the Bangladesh store
raw_data, _ = reviews(
    'com.arena.banglalinkmela.app',
    lang='en',  # Captures English and Romanized Bengali (Banglish)
    country='bd',
    sort=Sort.NEWEST,
    count=10000,
)

df = pd.DataFrame(raw_data)

# Retain required fields and rename to snake_case
df = df[['userName', 'score', 'at', 'content', 'thumbsUpCount']].copy()
df.rename(
    columns={
        'userName': 'user_name',
        'score': 'rating',
        'at': 'review_date',
        'content': 'review_text',
        'thumbsUpCount': 'thumbs_up',
    },
    inplace=True,
)

# Explicit operator label for multi-brand comparison
df['operator'] = 'Banglalink'

# Filter out empty or ultra-short reviews
df['review_text'] = df['review_text'].astype(str).str.strip()
df = df[df['review_text'].str.len() >= 12].reset_index(drop=True)

# Cap sample to match the 2,000 baseline across operators
df = df.head(2000)

# Resolve path relative to project root
BASE_DIR = Path(__file__).resolve().parent.parent
output_file = BASE_DIR / "data" / "raw" / "mybl_raw_reviews.csv"
output_file.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(output_file, index=False)
print(f"Saved {len(df)} filtered reviews to '{output_file}' successfully.")
