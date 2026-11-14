# Plan 7.1 Summary: Canonical Statistical & Econometric Ground Truth Script

**Executed At:** `2026-11-11T17:28:00+06:00`  
**Phase:** 7 (Statistical Ground Truth, Integrity Tooling & Script Hygiene Remediation)  
**Plan:** 1 of 3 (`1-PLAN.md`)  
**Status:** Complete  
**Commits:** None (`ADR-003` policy: working-tree review without unsolicited git commits)  

---

## 1. Executive Summary

Plan 7.1 established the canonical, reproducible, single-source-of-truth empirical ground truth for the entire Telecom VoC Intelligence project and subsequent ESWA publication remediation. All metrics were computed directly from live datasets on disk (`scraped_data_global/classified/all_operators_common_duration_classified.csv` $N=655,649$, processed multi-operator seed $N=4,500$, active blind gold standard $N=300$ / $N=200$, and serialized production models in `ml/models/`).

The script `scripts/compute_statistical_tests.py` was implemented, executed end-to-end, and generated both:
1. `scraped_data_global/classified/paper_empirical_ground_truth.json` (99 KB UTF-8 structured data)
2. `scraped_data_global/classified/paper_empirical_ground_truth.md` (5.3 KB Markdown companion summary)

All 25 core mathematical, econometric, and machine-learning invariants were verified through empirical assertion tests.

---

## 2. Tasks Completed

| Task | Name | Files Touched | Verification |
|---|---|---|---|
| 1 | Implement `scripts/compute_statistical_tests.py` | `scripts/compute_statistical_tests.py` | AST parsed cleanly with zero syntax errors (`rc=0`) |
| 2 | Execute script and verify ground-truth JSON & companion MD | `scraped_data_global/classified/paper_empirical_ground_truth.json`, `scraped_data_global/classified/paper_empirical_ground_truth.md` | All 25 invariant assertions passed (`rc=0`) |

---

## 3. Empirical Results & Verified Invariants

### 3.1 Metadata & DL Benchmark Provenance
- **Metadata:** Recorded execution timestamp, host environment (`Python 3.15.1`, Windows platform), and relative dataset paths.
- **DL Benchmarks Recorded (`dl/reports/results.txt`, `dl/telecom_voc_banglabert_finetuning_colab.ipynb` cell 6):**
  - BanglaBERT Sentiment: Macro-F1 $0.8598 \pm 0.0102$, Accuracy $91.60\% \pm 0.74\%$
  - BanglaBERT Category: Macro-F1 $0.7624 \pm 0.0179$, Accuracy $85.27\% \pm 1.14\%$
  - BiLSTM+Char-CNN: Sentiment Macro-F1 $0.8229$, Category Macro-F1 $0.7259$
  - MiniLM: Sentiment Macro-F1 $0.7915$, Category Macro-F1 $0.7102$
  - Documented row concatenation order difference: classical ML (`[GP, BL, Robi]`) vs BanglaBERT (`[GP, Robi, BL]`).
- **Live CPU Inference Latency (Single-review):**
  - `category_voting_classifier.joblib`: $1.157\text{ ms/review}$ ($864.6\text{ reviews/sec}$)
  - `sentiment_voting_classifier.joblib`: $0.985\text{ ms/review}$ ($1,015.7\text{ reviews/sec}$)
  - `ensemble_voting_classifier.joblib`: $0.468\text{ ms/review}$ ($2,136.8\text{ reviews/sec}$)

### 3.2 Live 5-Fold Stratified Cross-Validation & Paired $t$-Tests ($N = 4,500$)
- **Operational Category:**
  - `Dummy (Most Frequent)`: Macro-F1 $0.1511 \pm 0.0001$, Accuracy $60.69\% \pm 0.04\%$
  - `ComplementNB`: Macro-F1 $0.6934 \pm 0.0191$, Accuracy $81.47\% \pm 1.37\%$
  - `Balanced Logistic Regression`: Macro-F1 $0.7845 \pm 0.0135$, Accuracy $87.16\% \pm 0.86\%$
  - `Calibrated LinearSVC`: Macro-F1 $0.7664 \pm 0.0160$, Accuracy $86.91\% \pm 0.74\%$
  - **Hero Soft-Voting Ensemble:** Fold macro-F1 scores $[0.7678, 0.7644, 0.7908, 0.8022, 0.7716]$, Mean Macro-F1 **$0.7794 \pm 0.0146$**, Weighted-F1 $0.8717$, Accuracy **$87.33\% \pm 0.81\%$** (replicates reference exactly).
  - Paired $t$-tests ($df=4$): Hero vs Dummy $t(4) = 85.67, p < 10^{-6}$; Hero vs CNB $t(4) = 12.25, p = 0.0003$; Hero vs LogReg $t(4) = -2.01, p = 0.1146$; Hero vs LinearSVC $t(4) = 1.81, p = 0.1445$; Hero vs BanglaBERT Colab folds $t(4) = 3.07, p = 0.0373$.
- **Sentiment Classification:**
  - `Dummy`: Macro-F1 $0.2542 \pm 0.0001$, Accuracy $61.64\% \pm 0.04\%$
  - `ComplementNB`: Macro-F1 $0.7055 \pm 0.0140$, Accuracy $84.22\% \pm 1.50\%$
  - `Balanced LogReg`: Macro-F1 $0.7779 \pm 0.0229$, Accuracy $85.87\% \pm 1.80\%$
  - `Balanced LinearSVC`: Macro-F1 $0.7798 \pm 0.0147$, Accuracy $87.64\% \pm 0.93\%$
  - **CLI Soft-Voting Ensemble:** Folds $[0.8001, 0.7646, 0.8114, 0.7798, 0.7542]$, Mean Macro-F1 **$0.7820 \pm 0.0213$**, Accuracy **$87.84\% \pm 1.13\%$**
  - **Global Prod Soft-Voting Ensemble:** Folds $[0.7674, 0.7547, 0.7990, 0.7774, 0.7457]$, Mean Macro-F1 **$0.7688 \pm 0.0186$**, Accuracy **$87.44\% \pm 1.31\%$**
  - Paired $t$-tests ($df=4$): CLI Ensemble vs CNB $t(4) = 6.64, p = 0.0027$; Prod Ensemble vs CNB $t(4) = 7.96, p = 0.0013$.

### 3.3 Active Gold Standard ($N = 300 / 200$), Consensus, IRR, McNemar & Rogan-Gladen
- **Inter-Rater Reliability:**
  - Sentiment ($N=200$): Raw agreement **$91.00\%$** (182/200), Cohen's $\kappa = 0.5762$, 3-class PABAK = **$0.8650$**; GP $89.55\%$ ($\kappa=0.6921$), BL $94.03\%$ ($\kappa=0.4846$), Robi $89.39\%$ ($\kappa=0.3400$).
  - Category ($N=196$ valid pairs): Raw agreement **$95.41\%$** (187/196), Cohen's $\kappa = 0.7694$, PABAK = $0.9427$.
- **Model Gold Standard Evaluation ($N=300$ & Consensus):**
  - Star heuristic: $N=300$ Acc $86.67\%$, Consensus $N=182$ Acc $92.86\%$.
  - `ensemble_voting_classifier.joblib` (CLI): $N=300$ Acc **$89.00\%$**, Consensus $N=182$ Acc **$91.21\%$** (166/182); McNemar vs heuristic ($b=22, c=15$): $\chi^2_c(1) = 0.9730, p = 0.3240$; Rogan-Gladen active parameters: $\mathrm{Se} = 0.5217, \mathrm{Sp} = 0.9747$.
  - `sentiment_voting_classifier.joblib` (Prod): $N=300$ Acc **$83.67\%$**, Consensus $N=182$ Acc **$87.91\%$** (160/182); McNemar vs heuristic ($b=21, c=30$): $\chi^2_c(1) = 1.2549, p = 0.2624$; Rogan-Gladen active parameters: $\mathrm{Se} = 0.4783, \mathrm{Sp} = 0.9711$.
  - `category_voting_classifier.joblib`: $N=300$ Acc **$91.33\%$**, Consensus $N=187$ Acc **$94.12\%$** (176/187).
  - Explicit retirement documentation of legacy unblinded `g600` parameters ($\mathrm{Se}=0.711, \mathrm{Sp}=0.942$).

### 3.4 Table 3 Full-Seed Confusion Matrix & Complexity ($V, d$) & Table 4 Linguistic Subcohorts
- `category_voting_classifier.joblib` full seed $N=4,500$: Accuracy $0.9900$, Macro Precision $0.9805$, Macro Recall $0.9965$, Macro-F1 $0.9883$.
- $5\times 5$ Confusion Matrix correctly mapped across all classes (`General 2,687/2,731`, `Offers 787/788`, `Login 400/400`, `Network 364/364`, `Billing 217/217`).
- Complexity parameters:
  - Category model: $V = 29,843$ (word 4,843 + char 25,000), $d_{\text{mean}} = 109.72$, $d_{\text{median}} = 59.0$, $d_{\min} = 0$, $d_{\max} = 1,199$.
  - CLI Ensemble model: $V = 18,027$, $d_{\text{mean}} = 110.86$, $d_{\text{median}} = 64.0$, $d_{\min} = 0$, $d_{\max} = 971$.
- Table 4 Linguistic Subcohorts ($N=4,500$):
  - English: $N=3,005$ ($66.8\%$), Cat Acc CV $90.18\%$, Sent Acc CV $90.82\%$
  - Bangla (Native): $N=1,091$ ($24.2\%$), Cat Acc CV $80.11\%$, Sent Acc CV $82.68\%$
  - Romanized Banglish: $N=390$ ($8.7\%$), Cat Acc CV $85.13\%$, Sent Acc CV $79.23\%$
  - Symbolic / Emoticons: $N=14$ ($0.3\%$), Cat Acc CV $100.00\%$, Sent Acc CV $92.86\%$

### 3.5 Table 1 Deployed %, 122M Non-Overlapping Partitions & Decade Scorecard
- **Table 1 Proportions ($N=655,649$):**
  - General Appreciation / Other: $567,468$ ($86.55\%$)
  - Offers & Data Packs: $33,077$ ($5.04\%$)
  - App Login & Technical Bugs: $32,701$ ($4.99\%$)
  - Network Speed & 4G Latency: $16,108$ ($2.46\%$)
  - Billing & Airtime Deductions: $6,295$ ($0.96\%$)
  - Sum of 2-decimal rounded percentages: **$100.00\%$** (resolves the $100.1\%$ manuscript rounding defect).
- **Decade Scorecard (2016–2026):**
  - Grameenphone: $320,140$ ($48.83\%$), NSS = $+64.85\%$ (95% CI: $[+64.61\%, +65.09\%]$)
  - Robi: $198,378$ ($30.26\%$), NSS = $+65.91\%$ (95% CI: $[+65.61\%, +66.21\%]$)
  - Banglalink: $137,131$ ($20.92\%$), NSS = $+53.04\%$ (95% CI: $[+52.63\%, +53.45\%]$)
  - Sector: $655,649$, NSS = $+62.70\%$
- **Non-Overlapping 122-Month Partitions:**
  - Partition A ($17\text{M} + 36\text{M} + 24\text{M} + 45\text{M} = 122\text{M}$): $4,780 + 93,348 + 197,864 + 359,657 = 655,649$ reviews.
  - Partition B ($17\text{M} + 24\text{M} + 36\text{M} + 45\text{M} = 122\text{M}$): $4,780 + 15,877 + 275,335 + 359,657 = 655,649$ reviews.
  - Partition C ($41\text{M} + 12\text{M} + 24\text{M} + 45\text{M} = 122\text{M}$): $20,657 + 77,471 + 197,864 + 359,657 = 655,649$ reviews.
  - All three partitions verified with zero month gaps, zero month overlaps, and exact row sums.
- **Annual Rogan-Gladen Prevalence:** Recorded for all 11 years (2016–2026) using active production parameters ($\mathrm{Se}=0.4783, \mathrm{Sp}=0.9711$).

### 3.6 All 35 Modern Shocks, Prominent Top-10 Lists, Contingency Tests & Priority Matrix
- **35 Modern Shocks ($2020\text{--}2026$, $|\Delta\text{NSS}| \ge 10.0$ pts):**
  - Distribution: GP 6, Robi 7, BL 22 (20 positive expansions, 15 negative drops).
  - Primary Operational Driver: **App Login & Technical Bugs: 27**, Network: 4, Offers: 4, Billing: 0.
- **Top-10 Lists:** Exported both `top10_by_abs_delta_nss` (magnitude-ranked) and `top10_curated_multi_operator` (balanced 4 GP, 3 Robi, 3 BL across 3 operational domains, matching `scripts/print_table6_rows.py`), plus `top_per_operator` (top 4 per operator).
- **Contingency Analysis (Proposition 2):**
  - Pooled $2\times 2$ (240 transitions): Shocks 27/35 ($77.14\%$) vs Non-shocks 91/205 ($44.39\%$) $\implies \chi^2(1) = 12.8317, p = 0.000341$, Yates $\chi^2(1) = 11.5547, p = 0.000676$, Fisher $\text{OR} = 4.2280, p = 0.000404$, Woolf 95% CI $[1.79, 9.98]$, Relative Risk $= 1.7378$.
  - Non-Surge $2\times 2$ ($|\text{vol\_pct}| < 50\%$, 208 transitions): Shocks 14/19 ($73.68\%$) vs Non-shocks 82/189 ($43.39\%$) $\implies \chi^2(1) = 6.38, p = 0.0116$, Fisher $\text{OR} = 3.65, p = 0.0150$.
  - Per-Operator BL Asymmetry: Shocks 20/22 vs Non-shocks 29/58 $\implies \text{OR} = 10.00, p = 0.0007$; non-surge $\text{OR} = 11.41, p = 0.0088$.
- **Proposition 1 Regression:** $\text{Gen/Other Diff} = 11.52 \cdot d_{\ln(\text{vol})} \implies R^2 = 0.5601, p = 2.35 \times 10^{-7}$.
- **RMSSD Volatility:**
  - Raw: GP 6.28, Robi 5.61, BL 13.61 (BL/Robi ratio: $2.43\times$).
  - Non-surge filtered: GP 5.14, Robi 4.53, BL 7.56 (BL/Robi ratio: $1.67\times$).
- **Priority Matrix ($N = 88,181$ in 4 functional domains):**
  - Omnibus test: $\chi^2(3) = 11,027.60, p < 0.0001$, Cramér's $V = 0.3536$.
  - Domain Negativity & Odds Ratios vs Offers ($54.56\%$, $N=33,077$):
    - Billing & Airtime Deductions: $91.93\%$ ($5,787/6,295$), $\text{OR} = 9.49$ $[8.64, 10.42]$
    - App Login & Technical Bugs: $88.54\%$ ($28,955/32,701$), $\text{OR} = 6.44$ $[6.18, 6.70]$
    - Network Speed & 4G Latency: $75.01\%$ ($12,083/16,108$), $\text{OR} = 2.50$ $[2.40, 2.61]$
    - Login vs Network: $\text{OR} = 2.57$ $[2.45, 2.70]$
  - Per-operator negativity bounds: Billing $[89.77\%, 92.89\%]$, Login $[87.10\%, 89.28\%]$, Network $[74.01\%, 76.37\%]$, Offers $[50.26\%, 56.62\%]$.

### 3.7 Case Studies 1 & 2 Telemetry & Decision Framework Tables 7 & 8
- **Case Study 1 (Banglalink Spring 2024):**
  - Apr 2024 Shock: $\Delta\text{NSS} = -11.18$ pts ($\Delta\text{Login} = -8.74$ pp, $N=1,315$, NSS $+31.63$)
  - May 2024 Rebound: $\Delta\text{NSS} = +32.78$ pts ($\Delta\text{Login} = +13.73$ pp, $\Delta\text{Gen} = +17.38$ pp, $N=2,265$, NSS $+64.42$)
  - Jun 2024 Continuation: $\Delta\text{NSS} = +15.13$ pts ($N=4,528$, NSS $+79.55$)
  - Telemetry: Build `v11.8.0` in Apr 2024 recorded NSS = **$-7.59$** ($N=158$); BL Version missingness rate = **$51.82\%$** ($71,068 / 137,131$).
  - Corpus reporting bias: reviews with version ($N=492,224$, NSS $+65.43\%$) vs without version ($N=163,425$, NSS $+54.47\%$), difference **$+10.96\text{ pp}$**.
- **Case Study 2 (Banglalink 2025 $\to$ 2026 Turnaround):**
  - Annual swing: **$+15.54$** NSS pts ($2.13\times$ volume growth: $10,238 \to 21,810$ reviews).
  - Decomposition: General = **$+10.33$** pts ($66.5\%$), Technical 4 Domains = **$+5.21$** pts ($33.5\%$: Login $+2.80$, Network $+1.07$, Offers $+0.98$, Billing $+0.36$).
  - Monthly transition ($2025\text{-}12 \to 2026\text{-}01$): $N=689$ (NSS $+37.01$) $\to N=4,644$ (NSS $+85.16$), $\Delta\text{NSS} = +48.15$ pts.
- **Decision Framework (Tables 7 & 8):**
  - Empirical baseline $p_{\text{base}} = P(\text{App Login \& Neg}) = 28,955 / 655,649 = 0.044162$ ($4.42\%$).
  - Per-operator baselines: GP $0.03454$ ($11,058 / 320,140$), Robi $0.04008$ ($7,951 / 198,378$), BL $0.07253$ ($9,946 / 137,131$).
  - Alert Level Counts across 240 modern transitions:
    - Level 1 (Routine: $|\Delta\text{NSS}| < 5.0$): **147** ($61.25\%$)
    - Level 2 (Warning: $5.0 \le |\Delta\text{NSS}| < 10.0$): **58** ($24.17\%$)
    - Level 3 (Incident: $\Delta\text{NSS} \le -10.0$): **15** ($6.25\%$)
    - Level 4 (Surge: $\text{vol\_pct} \ge 50\% \land \Delta\text{Gen} \ge 5.0\text{ pp}$): **13** ($5.42\%$)

---

## 4. Deviations & Remediation Notes

1. **PyArrow ChunkedArray Indexing Deviation:**
   - In Python 3.15 / pandas with Arrow string storage, indexing `y_cat.values` inside `CalibratedClassifierCV` raised `TypeError: only integer scalar arrays can be converted to a scalar index`.
   - Remediated by converting text/label series to pure object numpy arrays via `np.array(s.tolist(), dtype=object)` across all CV splits and evaluations.
2. **FeatureUnion Per-Fold Extraction Optimization:**
   - Instead of fitting `FeatureUnion` repeatedly across each model in each fold, feature extraction was fit/transformed once per fold, and models were fit on the pre-extracted sparse matrices. This reduced CV execution time from $>3\text{ minutes}$ to $\approx 50\text{ seconds}$ while preserving 100% exact numerical fidelity (Fold 0 Macro-F1: Category $0.7678$, CLI Sentiment $0.8001$, Prod Sentiment $0.7674$).
3. **JSON Serialization of NumPy Scalar Types:**
   - Added a `json_serializable` default handler to `json.dump` to serialize `np.bool_`, `np.integer`, and `np.floating` cleanly.

---

## 5. Artifacts Produced

- `scripts/compute_statistical_tests.py` (52 KB, executable Python 3 script)
- `scraped_data_global/classified/paper_empirical_ground_truth.json` (99 KB, complete canonical JSON ground truth)
- `scraped_data_global/classified/paper_empirical_ground_truth.md` (5.3 KB, human-readable Markdown summary)

---

## 6. Next Steps

Proceed directly to Plan 7.2 (`2-PLAN.md`):
- Complete all 8 audit modules in `scripts/audit_project_integrity.py` with tight tolerances, cross-referencing `paper_empirical_ground_truth.json`.
- Retire the 28 legacy/broken scripts to `archive/legacy_scripts/` with index `README.md`.
- Repair `verify_paper_complete.py` and `audit_paper_contradictions.py` in-place.
