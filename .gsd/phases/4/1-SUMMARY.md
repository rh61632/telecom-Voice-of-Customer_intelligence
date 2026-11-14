---
phase: 4
plan: 1
wave: 1
status: complete
date: 2026-11-11
tasks_completed: 3
tasks_total: 3
files_modified:
  - .gsd/phases/4/evidence/01_corpus_eras_and_language_reconciliation.md
  - .gsd/phases/4/evidence/02_shocks_priority_matrix_and_cases_reconciliation.md
  - .gsd/phases/4/evidence/03_models_complexity_and_gold_reconciliation.md
  - .gsd/phases/4/1-SUMMARY.md
---

# Phase 4 Plan 1: Comprehensive Quantitative Cross-Reconciliation Summary

## 1. Executive Summary

Plan 4.1 executed a strictly read-only, end-to-end quantitative cross-reconciliation directly against live datasets (`all_operators_common_duration_classified.csv`, `all_operators_classified_global.csv`, `yearly_intelligence_trends.json`, `nss_stability_and_shocks_summary.json`, `all_operators_classified_with_language.csv`, `blind_annotation_*.csv`, and archived `gold_set_verified.csv`) and serialized models (`category_voting_classifier.joblib`, `sentiment_voting_classifier.joblib`).

All calculations were performed under strict adherence to `ADR-001` (zero modification outside `.gsd/`, zero git commits) and `ADR-002` (`workspace: inherit`).

### Core Quantitative Discoveries
1. **Corpus & Calendar Span:** $N = 655{,}649$ verified across Grameenphone (320,140 / 48.83%), Robi (198,378 / 30.26%), and Banglalink (137,131 / 20.92%). Calendar span is strictly 3,713 days (2016-08-01 to 2026-09-30) across 122 consecutive months with zero gaps.
2. **Table 1 Rounding Defect:** Deployed percentages sum to $100.1\%$ ($86.6 + 5.0 + 5.0 + 2.5 + 1.0$), while empirical unrounded values sum to exactly $100.0000\%$ ($86.55\%, 5.04\%, 4.99\%, 2.46\%, 0.96\%$).
3. **Table 5 Arithmetic Breakdown:** Table 5 lists 4 eras claiming $24\text{M} + 36\text{M} + 36\text{M} + 38\text{M} = 134\text{ months}$, whereas the calendar covers only 122 months. Table 5 double-counts 2020 in both Era 2 and Era 3, overstates Era 1 by 7 months (actual: 17M), and truncates Era 4 by 7 months (actual: 45M). Table 5 NSS values (e.g., GP $-18.42$) are mathematically irreconcilable with live data.
4. **2016 Review Count Mismatch (21 Reviews):** `yearly_intelligence_trends.json` reports 2016 review count as 1,329 (GP 441, Robi 126, BL 762), summing to $655,670$. The extra 21 reviews (3 GP, 18 BL) were scraped between July 28 and July 31, 2016 and erroneously retained in the yearly trends JSON.
5. **35 Modern Shocks & 7 Phantom Shocks in Table 6:**
   - Intra-era modern transitions (2020-01 to 2026-09) yield exactly 35 shocks: GP 6, Robi 7, BL 22.
   - Table 6 Rows 1 & 2 (BL `2024-04` $-11.2$ and `2024-05` $+32.8$) match live data.
   - Table 6 Row 10 (BL `2026-01` $+15.5$) conflated an annual/partial decomposition into a monthly transition whose actual $\Delta\text{NSS}$ was $+48.15$.
   - Table 6 Rows 3–9 are **7 phantom shocks**: their actual transitions had $|\Delta\text{NSS}| < 10.0$ pp (ranging from $-7.46$ to $+9.06$), proving their reported deltas were fabricated.
6. **Software Dominance Asymmetry:** While pooled contingency confirms App Login leads in 27/35 shocks (77.1%) vs 91/205 non-shocks (44.4%, $\chi^2 = 12.83, p = 0.0003, \text{OR} = 4.23$), disaggregation shows this is driven almost exclusively by Banglalink (20/22 shocks, $\text{OR} = 10.00, p = 0.0007$). For GP ($p = 0.6866$) and Robi ($p = 0.6949$), the software dominance hypothesis is statistically insignificant.
7. **Priority Matrix Sample Size ($N=88,181$):** Live functional reviews total 88,181, matching `manuscript.tex:488` exactly. Script references to 88,184 were hardcoded script errors. $\chi^2(3) = 11{,}027.60, V = 0.3536$, and all ORs are verified.
8. **Case Study 1 Inversion:** Banglalink's $-32.8$ plunge in May 2024 claimed in CS1 prose was actually a **$+32.8$ surge** in May 2024; the drop occurred in April 2024 and was only $-11.2$ points. Furthermore, 51.8% of BL reviews lack `app_version`, and `v11.8.0` appears in only 198 reviews.
9. **Complement Naive Bayes (CNB) Overstatement:** Table 2 claims CNB Macro-F1 = $0.7418$. In live 5-fold CV, CNB achieves only $0.6641$ (Config A) or $0.6481$ (Config B), overstated by $+7.8$ to $+9.4$ percentage points.
10. **Complexity Drift:** Fitted model vocabulary $V = 29,843$ features vs claimed $V \approx 50{,}000$; non-zero density $d = 109.72$ vs claimed $d \approx 20\text{--}45$.
11. **PABAK Mathematical Proof:** Inter-rater sentiment agreement on $N=200$ is $91.00\%$ ($\kappa = 0.5762$). 3-class PABAK from $91.00\%$ is $(3 \times 0.91 - 1)/2 = \mathbf{0.8650}$, matching `manuscript.tex:629` exactly, proving line 258's claimed $81.0\%$ was a typo.
12. **McNemar Chi-Square Falsification:** Active gold $N=300$ yields McNemar $\chi^2(1) = \mathbf{1.59}, p = \mathbf{0.2076}$ (the heuristic had fewer errors than the model). Table 2's claimed $\chi^2(1) = 21.64, p < 0.0001$ is completely falsified.
13. **Breakthrough Discovery on Rogan-Gladen Parameters ($Se=0.711, Sp=0.942$):** On the archived, deprecated $N=600$ gold set, `pred_ensemble` Negative Sensitivity is $54/76 = \mathbf{0.7105 \implies 0.711}$, and `pred_bilstm` Negative Specificity is $494/524 = \mathbf{0.9427 \implies 0.942}$. The paper's parameters are a hybrid composite cherry-picked across two different models from a leaked, retired test set!
14. **Commercial Claims:** BTRC market shares (GP 45.6%, Robi 30.9%, BL 19.9%, Teletalk 3.6%, private 96.4%) are mathematically sound. Claims of "28% higher ARPU" (`manuscript.tex:581`) and "3.5x-5.0x SAC ratio" (`manuscript.tex:242`) are completely unsubstantiated.

---

## 2. Task Execution Summary

| Task | Objective | Output Artifact | Verification Status |
|---|---|---|---|
| **Task 1** | Reconcile corpus counts, Table 1 deployed %, longitudinal NSS eras (Table 5 & prose), yearly_intelligence_trends.json mismatch, Rogan-Gladen simulation, and language distribution | `.gsd/phases/4/evidence/01_corpus_eras_and_language_reconciliation.md` | Verified passing (code 0) |
| **Task 2** | Reconcile econometric shocks (35 shocks & Table 6), contingency statistics, Priority Matrix (88,181 vs 88,184), Case Studies 1 & 2, and decision framework | `.gsd/phases/4/evidence/02_shocks_priority_matrix_and_cases_reconciliation.md` | Verified passing (code 0) |
| **Task 3** | Reconcile ML/DL model metrics (5-fold CV, CNB, Table 3, Table 4), complexity parameters ($V, d$), gold inter-rater reliability, McNemar, Rogan-Gladen $Se/Sp$ origin, PABAK, and commercial claims | `.gsd/phases/4/evidence/03_models_complexity_and_gold_reconciliation.md` | Verified passing (code 0) |

---

## 3. Deviations & Out-of-Scope Findings

None. All calculations were executed strictly as specified in `1-PLAN.md` using read-only Python scripts. Zero tracked files outside `.gsd/` were modified, and zero git commands were run (`commits: none (ADR-001)`).

---

## 4. Key Input to Plan 4.2

All evidence files generated in Plan 4.1 (`01_corpus_eras_and_language_reconciliation.md`, `02_shocks_priority_matrix_and_cases_reconciliation.md`, `03_models_complexity_and_gold_reconciliation.md`) provide the complete empirical foundation for Plan 4.2's deduplicated synthesis into `.gsd/DISCREPANCY_REPORT.md` and `.gsd/AUDIT.md`.
