# Telecom Voice-of-Customer (VoC) Intelligence

An end-to-end automated competitive intelligence and customer operations analytics pipeline. This project scrapes, cleans, classifies, and translates customer feedback from Google Play Store across the top three telecommunication self-service applications in Bangladesh: **Grameenphone (MyGP)**, **Banglalink (MyBL)**, and **Robi Axiata (My Robi)**.

---

## What This Project Does

Customer reviews on app stores are filled with unstructured complaints, bug reports, and service requests written in a mix of English, Bengali script, and Romanized Bengali (Banglish). 

This pipeline automates the transformation of that unstructured feedback into structured business intelligence:
* **Targeted Extraction**: Fetches genuine user reviews directly from Google Play Store for each telecom provider.
* **Text Normalization**: Strips low-signal noise, such as one-word responses, pure emojis, and blank feedback, focusing on actionable reviews ($\ge 12$ characters).
* **Multi-Lingual LLM Classification**: Uses LLM inference (`qwen/qwen-2.5-32b` via Groq) to parse complex Banglish and Bengali text into standardized categories:
  * *Billing & Airtime Deductions*
  * *Network Speed & 4G Latency*
  * *App Login & Technical Bugs*
  * *Offers & Data Packs*
  * *General Appreciation / Other*
* **Sentiment & Translation Engine**: Assigns sentiment (`Positive`, `Neutral`, `Negative`) and generates an accurate one-sentence English summary for every non-English review.
* **Checkpoint & Fault Tolerance**: Includes automated checkpointing so interrupted batch jobs resume from the exact row where they stopped without duplicating API calls.
* **Business Analytics Ready**: Produces standardized CSV exports ready for direct visualization in Power BI to track cross-operator Net Sentiment, issue distribution, and version stability.

---

## Pipeline Workflow
