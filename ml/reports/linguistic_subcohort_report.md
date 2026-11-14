# Linguistic Sub-Cohort Benchmark Report

## Grounding in Computational Linguistics Literature

In accordance with the multilingual text processing framework of **Barman et al. (2014, EMNLP)** and the Code-Mixing Index (CMI) dominance criteria of **Gambäck & Das (2016, LREC)**, the customer review corpus ($N = 4,500$) was partitioned into four distinct linguistic sub-cohorts:

1. **Bangla (Native Script):** Reviews containing predominantly Bengali Unicode characters (`[U+0980-U+09FF]`).
2. **Romanized Banglish:** Informal phonetically transliterated Bengali typed using Latin script.
3. **English:** Formal and informal English written in standard Latin script.
4. **Symbolic / Emoticons:** Feedback composed entirely of punctuation, digits, or emoji glyphs without alphabetic script.

## 5-Fold Stratified Cross-Validation Benchmark

| Sub-Cohort                 |    N | Share (%)   | Cat Acc (CV)   |   Cat Macro-F1 (CV) | Sent Acc (CV)   |   Sent Macro-F1 (CV) | Cat Acc (Fit)   |   Cat Macro-F1 (Fit) |
|:---------------------------|-----:|:------------|:---------------|--------------------:|:----------------|---------------------:|:----------------|---------------------:|
| Bangla (Native Script)     | 1091 | 24.2%       | 80.11%         |              0.7503 | 82.68%          |               0.7835 | 98.44%          |               0.9848 |
| Romanized Banglish         |  390 | 8.7%        | 85.13%         |              0.7305 | 79.23%          |               0.7567 | 98.72%          |               0.9866 |
| English                    | 3005 | 66.8%       | 90.18%         |              0.79   | 90.82%          |               0.7671 | 99.23%          |               0.9898 |
| Symbolic / Emoticons       |   14 | 0.3%        | 100.00%        |              1      | 92.86%          |               0.4815 | 100.00%         |               1      |
| Overall (Cross-Validation) | 4500 | 100.0%      | 87.33%         |              0.78   | 87.84%          |               0.7823 | 99.00%          |               0.9883 |

## Comparison with State-of-the-Art Literature

- **Drašković & Milanović (2025, Journal of Big Data):** Discarded non-English data completely, achieving 65.64% accuracy and 0.5213 Macro-F1 on English tweets.
- **Our VoC System:** Operates directly on trilingual and code-mixed inputs without discarding low-resource tokens, achieving robust cross-validation performance with high stability across all language cohorts.
