cat << 'EOF' > README.md
# Telecom Voice-of-Customer (VoC) Intelligence

An automated cross-operator competitive intelligence pipeline analyzing customer feedback across major Bangladesh telecom apps: Grameenphone (MyGP), Banglalink (MyBL), and Robi Axiata (My Robi).

## Pipeline Architecture
1. **Extraction**: Automated review scraping from Google Play Store using `google-play-scraper`.
2. **Filtering**: Pre-filtering noise, blank entries, and short reviews (<12 characters).
3. **NLP & Classification**: Sentiment analysis, operational issue tagging, and Banglish-to-English translation via LLMs (Groq / Qwen 2.5).
4. **Analytics**: Structured datasets ready for Power BI cross-brand benchmarking.

## Project Structure
```text
├── data/
│   ├── raw/            # Scraped raw customer feedback CSVs
│   └── processed/      # LLM-classified and structured CSVs
├── src/
│   ├── 01_scrape_*.py  # Data extraction scripts
│   └── 02_classify_*.py# LLM inference & tagging scripts
├── requirements.txt
└── README.md
