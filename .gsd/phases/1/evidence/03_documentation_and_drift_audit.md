# Empirical Evidence: Documentation, Scorecard & Git Working-Tree Drift Audit

## 1. Executive Summary

This audit performs a strict read-only empirical evaluation of repository documentation (`README.md`, `data/README.md`, `TODO.txt`), reconciles all published metrics against the ground-truth common duration summary (`scraped_data_global/classified/common_duration_summary.json`), checks badge targets and URL integrity, verifies roadmap progress in `TODO.txt`, and exhaustively catalogs the 39 modified tracked files and untracked artifacts currently composing the uncommitted git working-tree drift.

---

## 2. Documentation Metric Reconciliation vs Ground Truth

### 2.1 Performance Scorecard Audit (`README.md` vs `common_duration_summary.json`)

`scraped_data_global/classified/common_duration_summary.json` serves as the single source of truth for the continuous common duration window ($N = 655,649$, August 1, 2016 – September 30, 2026, 3,713 Days).

| Metric Dimension | Entity | Ground Truth JSON | `README.md` Scorecard (L47-56) | Status / Discrepancy |
|---|---|:---:|:---:|:---:|
| **Total Reviews** | Grameenphone | 320,140 | 320,140 | Exact Match |
| | Robi | 198,378 | 198,378 | Exact Match |
| | Banglalink | 137,131 | 137,131 | Exact Match |
| | **Industry Total** | **655,649** | **655,649** | Exact Match |
| **Positive Share** | Grameenphone | 77.00% (246,500) | 77.0% | Exact Match |
| | Robi | 77.86% (154,477) | 77.9% | Exact Match (rounded) |
| | Banglalink | 70.38% (96,509) | 70.4% | Exact Match (rounded) |
| | **Industry Total** | **75.88% (497,486)** | **75.9%** | Exact Match (rounded) |
| **Neutral Share** | Grameenphone | 10.85% (34,746) | 10.9% | Exact Match (rounded) |
| | Robi | 10.20% (20,226) | 10.2% | Exact Match (rounded) |
| | Banglalink | 12.29% (16,851) | 12.3% | Exact Match (rounded) |
| | **Industry Total** | **10.95% (71,823)** | **10.9%** | Exact Match (rounded) |
| **Negative Share** | Grameenphone | 12.15% (38,894) | 12.1% | Exact Match (rounded) |
| | Robi | 11.95% (23,675) | 12.0% | Exact Match (rounded) |
| | Banglalink | 17.33% (23,771) | 17.3% | Exact Match (rounded) |
| | **Industry Total** | **13.17% (86,340)** | **13.2%** | Exact Match (rounded) |
| **Net Sentiment (NSS)** | Grameenphone | +64.85% | +64.9% | Exact Match (rounded) |
| | Robi | +65.91% | +65.9% | Exact Match (rounded) |
| | Banglalink | +53.04% | +53.0% | Exact Match (rounded) |
| | **Industry Total** | **+62.71%** | **+62.7%** | Exact Match (rounded) |
| **Temporal Span** | Window Dates | 2016-08-01 to 2026-09-30 | Aug 1, 2016 – Sep 30, 2026 | Exact Match |
| | Days Count | 3,713 Days | 3,713 Days | Exact Match |
| | Master Corpus | 661,160 reviews | 661,160 reviews | Exact Match |

### 2.2 Internal Inconsistency Identified in `README.md`

While the Section 1 Performance Scorecard (lines 47–56) accurately reports Banglalink NSS as **`+53.0%`** (matching ground-truth `53.04%`), a downstream section contains an uncorrected legacy value:

- **`README.md:416` (Section 6.3: Banglalink Roadmap):**
  `* **Common Period NSS:** +53.1% (137,131 reviews) | **2026 NSS:** +81.9%`
- **Reconciliation:** Under the legacy 3,716-day window ($N=137,149$), Banglalink NSS was $53.05\%$, which had been rounded to `+53.1%`. When review count was updated to `137,131` in the working tree, the text value `+53.1%` was not adjusted to `+53.0%`.
- **Finding:** Internal contradiction between Section 1 table (`+53.0%`) and Section 6 text (`+53.1%`).

### 2.3 Repository Badge Verification (`README.md:12-22`)

| Badge Name | Display Text | Target Path / URL | Audit Verdict |
|---|---|---|---|
| Python Version | `Python 3.10+` | `https://www.python.org/` | Valid |
| License | `License: MIT` | `https://opensource.org/licenses/MIT` | Valid |
| Data Last Scraped | `Data Last Scraped: Late Oct 2026` | `scraped_data_global/raw/` | Valid (Raw files date: Oct 2026) |
| Common Period Benchmark | `Active Benchmark: 655,649 Reviews` | `scraped_data_global/classified/common_duration_summary.json` | Valid & Synchronized |
| Master Corpus | `Master Corpus: 661,160 Reviews` | `scraped_data_global/classified/` | Valid |
| Common Window | `Common Window: Aug 2016--Sep 2026` | `scraped_data_global/classified/common_duration_summary.json` | Valid & Synchronized |
| Sentiment Model | `Sentiment Model: BanglaBERT (91.6% Acc)` | `dl/` | Valid (BanglaBERT 5-fold CV: 91.60%) |
| Category Model | `Category Model: Ensemble (87.4% Acc)` | `ml/` | Valid (Ensemble CV: 87.44%) |
| Inter-Annotator Reliability | `Cohen's Kappa: κ = 0.77 (Substantial)` | `data/gold_set/gold_standard_evaluation_report.md` | **Partial Discrepancy**: Displays Category Kappa (0.7694 $\approx$ 0.77) without noting Sentiment Kappa (0.5762, Moderate) |
| Roadmap | `Roadmap: TODO.txt` | `TODO.txt` | Valid |

### 2.4 Stale Window References Scan across Documentation & Scripts

A global regex scan (`655,670|655670|3,716|3716`) revealed that while core documentation (`README.md`, `data/README.md`) and primary publication manuscripts (`paper/eswa_latex/manuscript.tex`, `paper/telecommunications_policy_latex/manuscript_twocolumn.tex`) were updated to $N = 655,649$ / $3,713$ days, several peripheral builder scripts and archived drafts still embed the old `655,670` / `3,716` values:
- `scripts/build_jba_full_manuscript.py:228,312,377,394`
- `scripts/apply_reviewer_fixes_latex.py:13,40`
- `paper/eswa_latex/manuscript_base_1506.tex:28`
- `paper/journal_manuscript/` (prior journal submission branch artifacts)

---

## 3. `TODO.txt` Roadmap Items vs Live Repository State

| Item # | Title & Stated Goal | Status in `TODO.txt` | Live Codebase State | Verification Detail & Discrepancy |
|:---:|:---|:---:|:---|:---|
| **1** | Model Checkpoint Hosting (Hugging Face Model Hub) | Pending (High Priority) | **Script Prepared (`scripts/upload_to_huggingface.py`)**; Configs updated; Upload pending | `scripts/upload_to_huggingface.py` exists (278 lines) and model configs in `dl/models/` have human-readable labels; actual Hub repos pending token setup. |
| **2** | Human Gold Standard Expansion & Cohen's Kappa | `[COMPLETED]` | **Verified Complete on disk** | `data/gold_set/` contains dual annotations ($N=200$ pairs), `calculate_agreement.py` computes Sentiment $\kappa = 0.5762$ and Category $\kappa = 0.7694$. All metrics in `TODO.txt` match `gold_standard_evaluation_report.md` exactly. |
| **3** | Filtered vs Unfiltered Model Deployment Resolution | Open / Pending | **Artifacts Created (`ml/reports/short_text_filtering_ablation_study.md`)** | Filtered models exist in `ml/models/sentiment_ensemble_filtered_min3words.joblib`. **Discrepancy in `TODO.txt:63`**: Text states *"The 398k production corpus currently uses the full-dataset model"* — stale reference to early 398k corpus size prior to 655k/661k expansion. |
| **4** | Interactive Live Web Demo (Streamlit / Gradio) | Open / Pending | **Implemented in `demo/app.py`** | `demo/app.py` has already been built using Gradio (120 lines), but `TODO.txt` was not updated to mark Item 4 completed. |
| **5** | Model Confidence Calibration & Reliability Diagram | Open / Pending | **Pending** | `assets/plots/model_confidence_calibration.png` does not exist; no standalone calibration curve script executed. |
| **6** | Routine Data Refresh Cadence | Open (Operational SOP) | **Documented SOP** | Pipeline scripts exist in `scraped_data_global/pipeline/`. |

---

## 4. Comprehensive Catalog of Pre-Existing Git Working-Tree Drift

Executing `git status -s` reveals **39 modified tracked files** and **multiple untracked file groups**.

### 4.1 Categorization of the 39 Modified Tracked Files

The 39 modified files cluster into four distinct operational drivers:

#### Group A: Common Window Temporal Shift (2016-07-28 -> 2016-08-01 | 3,716 -> 3,713 Days | 655,670 -> 655,649 Reviews)
*Files modified to reflect the first-full-month alignment:*
1. `README.md` (Updated scorecard, badges, and narrative dates/counts)
2. `data/README.md` (Updated common window benchmark text)
3. `scraped_data_global/classified/common_duration_summary.json` (Updated start date, day count, operator and category totals)
4. `scraped_data_global/classified/global_multi_year_intelligence_report.md` (Updated markdown report table metrics)
5. `scraped_data_global/pipeline/merge_and_sync_all_datasets.py` (Hardcoded `start_common = pd.Timestamp("2016-08-01 00:00:00")`)
6. `scraped_data_global/pipeline/generate_global_visualizations.py` (Updated plot title dates, labels, and days count)
7. `scripts/audit_project_integrity.py` (Updated verification assertions to 655,649 rows and 2016-08-01 start date)

#### Group B: Regenerated Visualization Assets (30 Binary PNG Plots)
*All plots regenerated at 300 DPI reflecting the exact 3,713-day window:*
- **In `assets/plots/` (15 PNGs):**
  8. `assets/plots/category_sentiment_stacked_bars.png`
  9. `assets/plots/monthly_nss_trend_all_months.png`
  10. `assets/plots/monthly_nss_trend_early_era.png`
  11. `assets/plots/monthly_nss_trend_line.png`
  12. `assets/plots/monthly_nss_trend_modern_era.png`
  13. `assets/plots/monthly_nss_trend_pre2020.png`
  14. `assets/plots/monthly_sentiment_trend_line.png`
  15. `assets/plots/multi_year_sentiment_trend_line.png`
  16. `assets/plots/net_sentiment_score_comparison_bars.png`
  17. `assets/plots/operator_category_complaint_distribution_bars.png`
  18. `assets/plots/operator_sentiment_distribution_bars.png`
  19. `assets/plots/yearly_sentiment_trend_all_years.png`
  20. `assets/plots/yearly_sentiment_trend_early_era.png`
  21. `assets/plots/yearly_sentiment_trend_pre2020.png`
- **In `scraped_data_global/plots/` (15 Duplicate Synchronized PNGs):**
  22. `scraped_data_global/plots/category_sentiment_stacked_bars.png`
  23. `scraped_data_global/plots/monthly_nss_trend_all_months.png`
  24. `scraped_data_global/plots/monthly_nss_trend_early_era.png`
  25. `scraped_data_global/plots/monthly_nss_trend_line.png`
  26. `scraped_data_global/plots/monthly_nss_trend_modern_era.png`
  27. `scraped_data_global/plots/monthly_nss_trend_pre2020.png`
  28. `scraped_data_global/plots/monthly_sentiment_trend_line.png`
  29. `scraped_data_global/plots/multi_year_sentiment_trend_line.png`
  30. `scraped_data_global/plots/net_sentiment_score_comparison_bars.png`
  31. `scraped_data_global/plots/operator_category_complaint_distribution_bars.png`
  32. `scraped_data_global/plots/operator_sentiment_distribution_bars.png`
  33. `scraped_data_global/plots/yearly_sentiment_trend_all_years.png`
  34. `scraped_data_global/plots/yearly_sentiment_trend_early_era.png`
  35. `scraped_data_global/plots/yearly_sentiment_trend_pre2020.png`

#### Group C: Deep Learning Model Config Label Mappings (2 JSON Files)
*Replaced generic `LABEL_0...LABEL_4` with human-readable class names for Hugging Face Hub export:*
36. `dl/models/banglabert_finetuned_sentiment/config.json` (`Negative`, `Neutral`, `Positive`)
37. `dl/models/banglabert_finetuned_category/config.json` (`General Appreciation / Other`, `Offers & Data Packs`, `App Login & Technical Bugs`, `Network Speed & 4G Latency`, `Billing & Airtime Deductions`)

#### Group D: Path Restructuring to Decouple Manuscripts (2 Script Files)
*Updated paper directory paths from `paper/journal_manuscript/` to consolidated `paper/`:*
38. `scripts/build_paper_empirical_excel.py` (`PAPER_DIR = ROOT / "paper"`)
39. `scripts/generate_two_panel_figure.py` (`fig_path = 'paper/figures/monthly_nss_trend_modern_era.png'`)

---

### 4.2 Inventory of Untracked Artifacts

| Category | Untracked Paths | Purpose & Analysis |
|---|---|---|
| **Demo Application** | `demo/` (`app.py`, `requirements.txt`) | Interactive Gradio deployment module |
| **Linguistic Intelligence Reports** | `ml/reports/global_language_distribution.json`<br>`ml/reports/global_language_distribution.md`<br>`ml/reports/linguistic_subcohort_benchmark.csv`<br>`ml/reports/linguistic_subcohort_report.md` | Empirical language breakdown and model benchmark across Bengali, Banglish, and English cohorts |
| **Processed Language Data** | `data/processed/all_operators_classified_with_language.csv` | Master corpus enriched with linguistic classifier tags |
| **Statistical Telemetry** | `scraped_data_global/classified/shock_grievance_statistical_evidence.json` | 35 monthly sentiment shock attributions |
| **Model Hosting Utility** | `scripts/upload_to_huggingface.py` | Automated Hub pusher with model card generation |
| **Paper & Manuscript Scripts** | ~34 utility scripts in `scripts/` (`build_full_eswa_paper.py`, `build_concise_paper_docx.py`, `apply_eswa_enhancements.py`, etc.) | LaTeX, Word docx, and figure formatting pipelines |
| **GSD Methodology Suite** | `.agent/`, `.agents/`, `.gemini/`, `.gsd/`, `GSD-STYLE.md`, `PROJECT_RULES.md`, `VERSION`, `adapters/`, `model_capabilities.yaml` | GSD orchestration and state management suite |
| **Build Artifacts** | `texput.log` | LaTeX compilation output file |

---

## 5. Summary of Discrepancies & Audit Findings

1. **`README.md:416` Inconsistency:** Banglalink NSS is stated as `+53.1%` in Section 6.3, contradicting the Section 1 Scorecard (`+53.0%`) and ground-truth JSON (`53.04%`).
2. **`README.md:20` Badge Ambiguity:** Cohen's Kappa badge displays $\kappa = 0.77$ (Substantial Agreement) representing Operational Category, but omits Sentiment Kappa ($\kappa = 0.5762$, Moderate Agreement).
3. **`TODO.txt:63` Stale Corpus Size:** Refers to `"The 398k production corpus"`, which predates the 655k/661k multi-year scrape.
4. **`TODO.txt` Incomplete Status for Web Demo:** Item 4 remains unmarked despite `demo/app.py` being fully implemented.
5. **Git Working-Tree Cleanliness Risk:** 39 modified tracked files and multiple key project features (`demo/`, `scripts/upload_to_huggingface.py`, linguistic reports) exist uncommitted in the working tree, creating drift between git HEAD and local execution.
