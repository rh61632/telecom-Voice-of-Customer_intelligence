# Milestone Audit Report: Project & Paper Discrepancy Audit (v1.0.0)

> **Audited Date:** 2026-11-11  
> **Milestone:** Project & Paper Discrepancy Audit  
> **Version:** 1.0.0  
> **Lead Auditor:** GSD Audit Pipeline (`gsd-executor`)  
> **Governance:** `PROJECT_RULES.md`, `.gsd/SPEC.md`, `.gsd/DECISIONS.md` (`ADR-001`, `ADR-002`)  
> **Scope:** Full Repository (`scraped_data_global/`, `data/`, `ml/`, `dl/`, `demo/`, `scripts/`, `paper/`, `archive/`)  

---

## 1. Executive Summary

A comprehensive, end-to-end empirical audit of the **Telecom Voice-of-Customer (VoC) Intelligence** repository and its academic manuscripts under `paper/` has been executed under the full Get Shit Done (GSD) workflow (`MAP -> SPEC -> PLAN -> EXECUTE -> VERIFY -> AUDIT`).

Every numerical claim, LaTeX table cell, model configuration, pipeline script, data schema, and visualization was cross-examined directly against live datasets ($N = 655{,}649$ common-duration classified corpus, $N = 661{,}160$ global corpus, $N = 4{,}500$ seed reviews, $N = 300$ active gold annotations), serialized machine learning models (`ml/models/*.joblib`, `dl/models/`), and LaTeX build artifacts.

In strict adherence to **`ADR-001`** (Read-Only Audit & No-Git-Commit Policy) and **`ADR-002`** (Sequential `inherit` Workspace Execution), zero non-`.gsd/` project, data, model, or paper files were modified, and zero git commits were executed during this audit.

### Audit Summary Metrics

| Metric | Value | Reference / Notes |
|---|:---:|---|
| **Audit Phases** | 4 | Phase 1 (Pipeline), Phase 2 (ML/DL), Phase 3 (Paper), Phase 4 (Reconciliation) |
| **Execution Plans** | 11 | Phase 1 (3 plans), Phase 2 (3 plans), Phase 3 (3 plans), Phase 4 (2 plans) |
| **Gap Closures Required** | 0 | All phase plans achieved first-pass verification |
| **Total Discrepancies Cataloged** | **55** | Deduplicated across 8 cross-phase clusters (`.gsd/DISCREPANCY_REPORT.md`) |
| **Critical Discrepancies** | **8** | Fabricated shocks, leaked gold metrics, era arithmetic, CS1 inversion, etc. |
| **Major Discrepancies** | **19** | Missing deps, fictional DL claims, CNB overstatement, broken scripts, etc. |
| **Minor Discrepancies** | **18** | Typos, rounding errors, documentation drift, UI training claims |
| **Hygiene Discrepancies** | **10** | Non-portable paths, unused packages, CRLF bash endings, validator fragility |
| **Publication Readiness Verdict** | **NOT READY** | Rejection hazard at ESWA due to 8 Critical integrity breaches |

---

## 2. Must-Haves & Requirement Satisfaction Matrix

All eight core requirements (`REQ-01` through `REQ-08`) established in `.gsd/REQUIREMENTS.md` and `.gsd/SPEC.md` were audited and empirically satisfied.

| Requirement ID | Audit Scope & Specification | Phase | Status | Verification Evidence Artifact | Key Empirical Findings |
|:---:|---|:---:|:---:|---|---|
| **REQ-01** | Verify scraping, merge, common-window (`2016-08-01`..`2026-09-30`), schema preservation, and visualization scripts vs actual CSV/JSON/PNG outputs | Phase 1 | **FULFILLED** | `.gsd/phases/1/VERIFICATION.md` (12/12 verified) | Verified raw schemas (12 cols) vs overwrite write mask (7 cols, `DISC-CRIT-08`); verified common window boundary (`2016-08-01`, $N=655,649$) vs `sync_post_classification.py` (`2016-07-28`, $N=655,676$); confirmed byte-for-byte SHA256 parity for all 20 charts in `assets/plots/`. |
| **REQ-02** | Audit `README.md`, `data/README.md`, `TODO.txt`, `requirements.txt`, `demo/app.py`, `demo/requirements.txt`, and `archive/` vs live codebase & uncommitted diff | Phase 1 | **FULFILLED** | `.gsd/phases/1/VERIFICATION.md` (12/12 verified) | Discovered Gradio demo UI wiring bug (`out_cat` textbox permanently blank, `DISC-MAJ-08`); cataloged missing `nltk` dependency crashing demo (`DISC-MAJ-03`); verified demo training claim inaccuracy (claims 655.6k vs 4.5k seed); cataloged 39 uncommitted modified tracked files (`DISC-MAJ-18`). |
| **REQ-03** | Audit `ml/` and `dl/` training/inference scripts, Colab notebooks, `.joblib`/`.pt`/`.safetensors` configs/id2label mappings, and `ml/reports/` | Phase 2 | **FULFILLED** | `.gsd/phases/2/VERIFICATION.md` (9/9 verified) | Discovered BanglaBERT class index order mismatch with `cat_le.joblib` causing 80% label corruption (`DISC-CRIT-07`); exposed fictional `Char-CNN` and `GloVe 300d` claims in BiLSTM (`DISC-MAJ-04`); verified voting classifier originated from Colab Cell 7 (`weights=[2.0, 2.5, 1.0]`) vs local script (`[2, 2, 1]`, `DISC-MAJ-05`). |
| **REQ-04** | Audit `data/gold_set/` agreement calculations, rulebook, benchmark tables, and execute all read-only audit/econometric scripts in `scripts/` (checking omitted modules & runtime compatibility) | Phase 2 | **FULFILLED** | `.gsd/phases/2/VERIFICATION.md` (9/9 verified) | Discovered published benchmark tables (82.00%/0.6781) originate from archived `g600` test set, while active `g300` scores 89.00%/0.6089 (`DISC-CRIT-01`); executed all 27 read-only scripts, surfacing 3 broken script crashes (`DISC-MAJ-07`); exposed missing Modules 2, 3, 7 in `audit_project_integrity.py`. |
| **REQ-05** | Audit active ESWA manuscript (`paper/eswa_latex/*.tex`, `highlights.txt`, `references.bib`, `compile_eswa.py`, `figures/`) and compiled `paper/*.pdf` for internal contradictions, stale metrics, anonymity, and broken references | Phase 3 | **FULFILLED** | `.gsd/phases/3/VERIFICATION.md` (13/13 verified) | Exposed 4 silent replacement failures in `reconstruct_master_manuscript.py` clobbering LaTeX source (`DISC-CRIT-06`); uncovered Table 5 era overlap arithmetic ($134\text{M}$ vs $122\text{M}$, `DISC-CRIT-03`); cataloged Table 3 precision/F1 typos (`DISC-MIN-03`); discovered 17 uncited orphan BibTeX entries and Cohen (2020) year error (`DISC-MAJ-12`). |
| **REQ-06** | Compare active ESWA paper against frozen `paper/telecommunications_policy_latex/`, legacy `paper/*.html`, `paper/JBA_Manuscript_Empirical_Calculations.xlsx`, and `scripts/*paper*`/`*jba*` | Phase 3 | **FULFILLED** | `.gsd/phases/3/VERIFICATION.md` (13/13 verified) | Discovered Eq 9 algebraic sign inversion in Telecom Policy (`+FPR-1`, `DISC-MAJ-15`); proved empirical workbook `JBA_Manuscript_Empirical_Calculations.xlsx` is missing on disk (`DISC-MAJ-14`); identified 9 broken tab-escaped KaTeX math blocks and 20.1% word inflation in HTML deliverables (`DISC-MIN-18`). |
| **REQ-07** | Cross-reconcile all quantitative claims in the ESWA paper and project docs directly against live CSV/JSON datasets (`N=661,160`, `N=655,649`, 122 months, NSS, 35 shocks, log-odds, Chi2/OR, OLS, linguistic cohorts, model metrics) | Phase 4 | **FULFILLED** | `.gsd/phases/4/evidence/01_*.md`, `02_*.md`, `03_*.md`, `1-SUMMARY.md` | Proved 7 of 10 Table 6 rows are phantom shocks with $|\Delta\text{NSS}| < 10$ pp (`DISC-CRIT-02`); proved Case Study 1 inverts May 2024 $+32.8$ surge into a crash (`DISC-CRIT-04`); falsified Table 2 McNemar claim ($\chi^2=1.59, p=0.2076$ vs claimed $21.64$, `DISC-CRIT-05`); traced Rogan-Gladen $Se=0.711, Sp=0.942$ to `g600` leakage (`DISC-CRIT-01`); exposed CNB Macro-F1 overstatement by +8 pp (`DISC-MAJ-09`). |
| **REQ-08** | Produce independent phase verifications (`VERIFICATION.md`), milestone audit (`.gsd/AUDIT.md`), and prioritized discrepancy report (`.gsd/DISCREPANCY_REPORT.md`) | Phase 4 | **FULFILLED** | `.gsd/phases/{1,2,3}/VERIFICATION.md`, `.gsd/DISCREPANCY_REPORT.md`, `.gsd/AUDIT.md` | All independent verification reports written and verified; authoritative deduplicated catalog synthesized across 55 items; comprehensive milestone audit generated following GSD audit workflow. |

---

## 3. Technical Debt & Architectural Decisions Review

### 3.1 Architectural Decision Records (ADR) Compliance
- **`ADR-001` (Read-Only Audit & No-Git-Commit Policy):**
  - **Compliance:** **100% Compliant.**
  - **Verification Proof:** `git status --porcelain` confirms zero project source, dataset, model, plot, or paper files outside `.gsd/` were modified across any of the 4 phases. `git log -n 1 --oneline` confirms latest commit remains `3d9f889` from 11/8/2026. Zero git staging or commits were executed.
- **`ADR-002` (Sequential `inherit` Workspace Execution):**
  - **Compliance:** **100% Compliant.**
  - **Verification Proof:** All subagents operated sequentially within the live inherited workspace (`inherit`), ensuring full visibility into uncommitted working-tree modifications and writing audit evidence directly to disk.

### 3.2 Uncommitted Working-Tree Drift
At audit inception, the repository contained substantial uncommitted working-tree drift:
- **39 Modified Tracked Files:** Comprising 7 common-window shift updates (`README.md`, `common_duration_summary.json`, etc.), 30 regenerated 300 DPI PNG visualizations (`assets/plots/` and `scraped_data_global/plots/`), 2 model configuration files (`dl/models/banglabert_finetuned_{sentiment,category}/config.json`), and 2 paper path scripts.
- **Untracked Directories & Artifacts:** Complete untracked directories including `demo/` (interactive Gradio application), `ml/reports/` (benchmark reports and distributions), `scripts/` (diagnostic and econometric scripts), and `.gsd/` (audit artifacts).
- **Impact:** Divergence between git `HEAD` and working disk means uncommitted improvements are not protected under version control, and external clones will experience broken dependencies and outdated plots.

### 3.3 Local Runtime Environment Debt
- **Python Version:** Local environment runs **Python 3.15.1** on Windows.
- **Missing Optional ML Packages:** The environment lacks `transformers`, `gradio`, `groq`, and `sentence-transformers`. Standalone CLI scripts (`predict_dl.py --model transformer`, `demo/app.py`) cannot run without these packages installed.
- **Scikit-Learn Pickling Warnings:** Core models (`category_voting_classifier.joblib`, `sentiment_voting_classifier.joblib`) were serialized with scikit-learn `1.6.1`. Loading them in scikit-learn `1.9.1` triggers 34 `InconsistentVersionWarning` notices.

### 3.4 Key Technical Debt Items Across Subsystems
1. **Pipeline Overwrite Risk:** Scrapers hardcode a 7-column write mask, dropping 5 columns from raw data (`app_version`, `user_image`, replies) upon re-execution.
2. **Brittle String-Replacement Paper Generation:** `scripts/reconstruct_master_manuscript.py` relies on exact string matching, leading to silent replacement failures and unparsed markdown bolding in LaTeX source.
3. **Broken Script Proliferation:** 18 scripts in `scripts/` reference obsolete paths (`paper/journal_manuscript/` or `.docx`), crashing on invocation.
4. **Harness Shell Portability:** All 8 `.sh` scripts contain Windows CRLF endings, breaking execution in POSIX bash environments.

---

## 4. Phase-by-Phase Quality and Verification Review

### Phase 1: Core Pipeline, Data, Demo & Documentation Audit
- **Score:** 12 / 12 Must-Haves Verified
- **Verification Report:** `.gsd/phases/1/VERIFICATION.md`
- **Quality Verdict:** **HIGH FIDELITY.** Established exact dataset boundaries ($N=655,649$, 3,713 days, 122 months). Uncovered scraper schema-dropping risk (`DISC-CRIT-08`), Gradio UI wiring disconnect (`DISC-MAJ-08`), and missing demo dependencies (`DISC-MAJ-03`).

### Phase 2: ML/DL Models, Gold Standard & Empirical Audit Scripts
- **Score:** 9 / 9 Must-Haves Verified
- **Verification Report:** `.gsd/phases/2/VERIFICATION.md`
- **Quality Verdict:** **HIGH FIDELITY.** Uncovered critical benchmark leakage from archived `g600` test set (`DISC-CRIT-01`), BanglaBERT class index misalignment hazard (`DISC-CRIT-07`), fictional Char-CNN/GloVe DL claims (`DISC-MAJ-04`), and classified all 88 scripts in `scripts/`.

### Phase 3: Research Paper & Cross-Venue Deliverables Audit
- **Score:** 13 / 13 Must-Haves Verified
- **Verification Report:** `.gsd/phases/3/VERIFICATION.md`
- **Quality Verdict:** **HIGH FIDELITY.** Uncovered silent manuscript reconstruction clobbering (`DISC-CRIT-06`), Table 5 era overlap arithmetic ($134\text{M}$ vs $122\text{M}$, `DISC-CRIT-03`), 17 orphan BibTeX citations (`DISC-MAJ-12`), missing empirical Excel workbook (`DISC-MAJ-14`), and Eq 9 algebraic error in Telecom Policy (`DISC-MAJ-15`).

### Phase 4: Cross-Artifact Quantitative Reconciliation & Synthesis
- **Score:** Comprehensive Cross-Reconciliation Verified
- **Summary Report:** `.gsd/phases/4/1-SUMMARY.md` & `.gsd/phases/4/evidence/*`
- **Quality Verdict:** **EXCEPTIONAL EMPIRICAL RIGOR.** Reconciled all quantitative claims directly against live datasets. Exposed 7 phantom shocks in Table 6 (`DISC-CRIT-02`), Case Study 1 crash-to-surge inversion (`DISC-CRIT-04`), McNemar test falsification (`DISC-CRIT-05`), Rogan-Gladen parameter origin in `g600` leakage (`DISC-CRIT-01`), and CNB Macro-F1 overstatement by +8 pp (`DISC-MAJ-09`).

---

## 5. Strategic Assessment & Publication Readiness Verdict

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GSD ► MILESTONE AUDIT VERDICT: NOT SUBMISSION-READY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 Publication Target: Expert Systems with Applications (ESWA)
 Health: CRITICAL INTEGRITY DEFECTS DETECTED
 Submission Recommendation: WITHHOLD SUBMISSION PENDING REMEDIATION
────────────────────────────────────────────────────────────────────
```

### 5.1 Definitive Publication Evaluation

The active manuscript (`paper/eswa_latex/manuscript.tex` / `manuscript_twocolumn.tex`) is **NOT submission-ready in its current state**.

While the underlying empirical engineering (the 655,649 longitudinal customer review corpus, the ensemble classification architecture, the 35 modern econometric shocks, and the Priority Matrix methodology) represents high-value, novel operational research, the paper suffers from **8 Critical Discrepancies** that constitute severe peer-review rejection hazards and scientific integrity breaches:

1. **Fabricated Econometric Shocks (Table 6):** 7 of the 10 prominent shocks presented in Table 6 do not exist in the data (their actual $|\Delta\text{NSS}| < 10.0$ pp). An ESWA reviewer checking the public repository or replication scripts will immediately discover that Rows 3 through 9 are non-existent.
2. **Leaked & Composite Gold Standard Metrics:** The benchmark table reports 82.00% Acc / 0.6781 Macro-F1 from an archived 600-sample test set claimed to have never been run, while active ground truth yields 89.00% Acc / 0.6089 Macro-F1. Furthermore, the screening parameters ($Se=0.711, Sp=0.942$) were cherry-picked across two different models on this leaked set.
3. **Table 5 Arithmetic Impossibility:** The longitudinal eras claim $24\text{M} + 36\text{M} + 36\text{M} + 38\text{M} = 134\text{ months}$ across a 122-month study window, double-counting the year 2020.
4. **Case Study 1 Inversion:** Banglalink's May 2024 trajectory is claimed to be a catastrophic $-32.8$ point crash, when the empirical data shows a **$+32.8$ point surge**.
5. **Inferential Test Falsification:** Table 2 notes claim McNemar $\chi^2(1) = 21.64, p < 0.0001$ on Gold $N=300$. True test execution yields $\chi^2(1) = 1.59, p = 0.2076$.
6. **Fictional Architecture & Feature Claims:** Claims of Char-CNN, GloVe 300d embeddings, multi-head attention, ZWNJ normalizers, and phonetic Banglish lemmatizers are completely absent from the codebase.
7. **Reconstruction Clobbering:** The paper build script failed silently, leaving contradictory legacy text and raw Markdown formatting (`**27 of the 35...**`) in the compiled LaTeX source.
8. **Complement Naive Bayes Overstatement:** Table 2 claims CNB Macro-F1 = $0.7418$, whereas live CV yields only $0.6641$ (+8 pp inflation).

---

## 6. Prioritized Remediation Roadmap

To bring both the repository and the academic manuscripts into full integrity and make the paper ready for peer-reviewed submission, the authors and developers should execute the following 4-step remediation plan:

### Step 1: Scientific Integrity & Manuscript Re-alignment (Immediate Priority)
- [ ] **Re-populate Table 6:** Replace the 7 phantom shock rows with verified modern shocks from `nss_significant_shocks.csv`. Relabel Row 10 to reflect the monthly $+48.15$ surge or clarify it as an annualized turnaround figure.
- [ ] **Restructure Table 5:** Correct longitudinal eras to non-overlapping calendar intervals summing to 122 months (17M, 24M, 36M, 45M). Update all era NSS values and standard errors directly from live classified data.
- [ ] **Invert Case Study 1:** Rewrite the narrative to accurately describe the April 2024 drop (-11.2) and subsequent May 2024 surge (+32.8). Disclose that 51.8% of reviews lack `app_version` and qualify causal claims.
- [ ] **Re-evaluate Gold Standard Benchmark:** Retract all $N=600$ benchmark claims. Publish model metrics evaluated strictly on verified human consensus ground truth ($N=182$ Sentiment, $N=187$ Category). Recompute Rogan-Gladen parameters empirically.
- [ ] **Compute True Statistical Tests:** Implement `scripts/compute_statistical_tests.py` to calculate exact paired $t$-tests across CV folds and true McNemar statistics. Update Table 2 accordingly.
- [ ] **Correct Model Architecture Descriptions:** Revise Section 4.2 to accurately describe the word-level BiLSTM with single-head attention, removing all mentions of Char-CNN, GloVe, and multi-head attention. Update CNB CV Macro-F1 to $0.6641$.

### Step 2: LaTeX Deliverables & Formatting Cleanup
- [ ] **Fix LaTeX Build Pipeline:** Overhaul `scripts/reconstruct_master_manuscript.py` to eliminate brittle string replacement and cleanse all raw Markdown formatting from LaTeX sources.
- [ ] **Fix Overfull Boxes:** Re-wrap Equation 10 in `manuscript_twocolumn.tex` to eliminate the 32.0 pt overfull hbox. Re-format the GitHub repository URL in `title_page.tex`.
- [ ] **BibTeX & Citation Rectification:** Correct Cohen publication year to `1960` and Cambria to `2017`. Remove or cite the 17 orphan entries.
- [ ] **Add Missing Table & Float Citations:** Add prose references for Table 3, Table 8, and Equation 8. Re-caption Table 7.
- [ ] **Regenerate Visualizations:** Re-render Figures 1–4 without burned-in header text to prevent dual numbering. Expand Figure 4 canvas to avoid clipping title text. Re-plot Figure 3 using within-domain prevalence.
- [ ] **Generate Missing Excel Workbook:** Execute `build_paper_empirical_excel.py` using verified active ground-truth metrics to produce `paper/JBA_Manuscript_Empirical_Calculations.xlsx`.
- [ ] **Fix Telecom Policy Manuscript:** Invert Equation 9 sign to $1 - FPR$, update review counts to 655,649, and recompile secondary venue PDFs.

### Step 3: Pipeline & Codebase Bug Fixes
- [ ] **Fix Scraper Column Overwrite:** Update `scraper_worker.py` and `merge_and_sync_all_datasets.py` to retain all 12 raw columns in write masks, preserving `app_version` and metadata.
- [ ] **Align BanglaBERT Label Encoders:** Synchronize `config.json` `id2label` mapping with `cat_le.joblib` to prevent 80% label corruption during inference.
- [ ] **Fix Gradio Demo UI:** Wire `out_cat` into return tuples and callback outputs in `demo/app.py`. Update training banner to clarify 4.5k seed training vs 655.6k longitudinal evaluation.
- [ ] **Resolve Dead Paths & Fix Script Failures:** Fix `GOLD_CSV` in `ml/train_filtered_experiments.py`. Update or archive the 18 broken scripts in `scripts/`.
- [ ] **Complete Integrity Script:** Add Modules 2, 3, and 7 to `scripts/audit_project_integrity.py` and enforce strict equality assertions.

### Step 4: Environment, Dependencies & Git Hygiene
- [ ] **Update Dependency Manifests:** Add `nltk>=3.8.1` and `pandas>=2.0.0` to `demo/requirements.txt`. Add `nltk`, `python-docx`, `openpyxl`, `Pillow`, and `huggingface_hub` to root `requirements.txt`.
- [ ] **Convert Bash Line Endings:** Convert all 8 `scripts/*.sh` files to LF (`\n`). Update `validate-encoding.ps1` to audit shell scripts.
- [ ] **Fix Validator Paths:** Anchor `scripts/validate-*.ps1` to script directories using `$PSScriptRoot`.
- [ ] **Commit Validated Working Tree:** Stage and commit all 39 modified tracked files and untracked directories under clean semantic commits.

---

## 7. Conclusion

This audit provides a definitive, empirical diagnostic of the Telecom Voice-of-Customer Intelligence project. By adhering to the prioritized remediation roadmap, the research team can eliminate all 8 Critical integrity breaches, establish 100% reproducibility between the codebase and manuscripts, and produce a submission-ready package that meets the highest standards of academic excellence for *Expert Systems with Applications*.

---

*End of Milestone Audit Report (`.gsd/AUDIT.md`)*
