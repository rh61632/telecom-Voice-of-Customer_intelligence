# 🗄️ Archived: Early Power BI Prototype Dashboard

> **Status: ARCHIVED / DISCARDED** (October 2026)  
> The interactive Power BI dashboard was built during the initial proof-of-concept phase and was subsequently discarded in favor of:
> 1. An automated, reproducible Python publication visualization suite ([`scraped_data_global_2020_2026/pipeline/generate_global_visualizations.py`](../../scraped_data_global_2020_2026/pipeline/generate_global_visualizations.py) generating 300 DPI figures in [`assets/plots/`](../../assets/plots/)).
> 2. Direct production batch scoring pipelines over the full 434k review corpus without proprietary BI tool dependencies.

---

## 📌 Archived Media

This folder preserves screen recordings of the original prototype Power BI interface (`Voice_of_Customer.pbix`):

1. **`page1_demo.gif`**:
   - **Page 1: Market Experience & Strategic Overview**
   - Showcased cross-operator sentiment benchmarking, category complaint breakdowns, and Net Sentiment Score (NSS) cards for Grameenphone, Robi, and Banglalink.
2. **`page2_demo.gif`**:
   - **Page 2: Voice-of-Customer Granular Inspector**
   - Showcased review filtering by operator, star rating, sentiment polarity, and upvotes (`thumbs_up`) along with English LLM summaries.

---

## 💡 Why Power BI Was Discarded

| Dimension | Initial Power BI Prototype | Current Python Production Pipeline |
| :--- | :--- | :--- |
| **Data Volume Capacity** | Slowed down on datasets >50k rows without import aggregation | Easily batch-scores and visualizes **434,803 records** (~18,000 rev/s) |
| **Model Integration** | Relied on static pre-exported CSV columns | Integrates directly with trained PyTorch DL models and Scikit-Learn Voting Ensembles |
| **Reproducibility** | Required manual UI clicks, proprietary Windows client, and manual dataset refreshes | Single-command reproduction (`python generate_global_visualizations.py`) |
| **Portability** | Requires Microsoft Power BI Desktop license / installation | Fully open-source, runs cross-platform (Linux/macOS/Windows/Colab) |
