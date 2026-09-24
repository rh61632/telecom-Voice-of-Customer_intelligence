import pandas as pd
from google_play_scraper import Sort, reviews

print("Connecting to Google Play Store (MyGP app)...")

# Fetch reviews from the Bangladesh store
raw_data, _ = reviews(
    'com.portonics.mygp',
    lang='en',  # Banglish is written using Latin/English characters
    country='bd',
    sort=Sort.NEWEST,
    count=10000,
)

df = pd.DataFrame(raw_data)

# Retain necessary fields and rename to snake_case
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

# Filter out blank, single-word, or emoji-only entries
df['review_text'] = df['review_text'].astype(str).str.strip()
df = df[df['review_text'].str.len() >= 12].reset_index(drop=True)

# Save initial scraped dataset
df.to_csv('mygp_raw_reviews.csv', index=False)
print(
    f"Saved {len(df)} filtered reviews to 'mygp_raw_reviews.csv' successfully."
)