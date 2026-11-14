---
phase: 7
verified: 2026-11-11T18:17:00+06:00
status: passed
score: 36/36 must-haves verified
is_re_verification: false
---

# Phase 7 Verification Report: Statistical Ground Truth, Integrity Tooling & Script Hygiene Remediation

## Executive Summary

Phase 7 independent verification was executed against `.gsd/SPEC.md`, `.gsd/REQUIREMENTS.md` (`REM-05`), `.gsd/DECISIONS.md` (`ADR-002`, `ADR-003`), and `.gsd/phases/7/*-PLAN.md`. Every must-have across all three plans was empirically evaluated through live execution of Python test scripts, PowerShell validator harnesses, AST parsers, byte-level character scans, and git status tracking.

**Overall Verdict: PASS (36/36 must-haves verified).**

All statistical, econometric, and ML ground truth metrics were generated from live disk assets without fabrication. The 8-module master integrity audit executes in under 8 seconds passing 100% of empirical tests in default mode and correctly gating un-remediated Phase 8/9 paper defects via `--strict-paper`. 28 obsolete scripts were cleanly retired to `archive/legacy_scripts/` with an inventory `README.md`. All 8 shell scripts adhere to binary LF without BOM. All 5 PowerShell validators were anchored via `$PSScriptRoot`, and `validate-all.ps1` runs with exit code 0 from both repo root and nested paths. Exactly 0 git commits were made (`ADR-003`).

---

## 1. Empirical Verification of Must-Haves

### 1.1 Canonical Statistical & Econometric Ground Truth (Plan 7.1)

| Must-Have / Truth | Status | Empirical Evidence |
|---|---|---|
| `scripts/compute_statistical_tests.py` executes autonomously generating `paper_empirical_ground_truth.json` (99 KB) and `.md` (5.3 KB) | ✓ VERIFIED | Executed `python scripts/compute_statistical_tests.py` (Exit code 0). Generated `paper_empirical_ground_truth.json` (99,044 bytes) and companion Markdown `paper_empirical_ground_truth.md` (5,304 bytes). |
| Live 5-fold CV replicates exact reference Category Soft-Voting folds `[0.7678, 0.7644, 0.7908, 0.8022, 0.7716]` (macro-F1 $0.7794 \pm 0.0146$, Acc $87.33\% \pm 0.81\%$) | ✓ VERIFIED | Verified via live 5-fold stratified cross-validation on $N=4,500$ seed rows. Macro-F1 folds matched exactly to 4 decimals with paired $t$-tests ($df=4$). |
| Sentiment Soft-Voting 5-fold CV: CLI Macro-F1 $0.7820 \pm 0.0213$, Global Prod Macro-F1 $0.7688 \pm 0.0186$ (Acc $87.44\% \pm 1.31\%$) with paired $t$-tests | ✓ VERIFIED | Verified: CLI folds `[0.8001, 0.7646, 0.8114, 0.7798, 0.7542]` (mean 0.7820, std 0.0213); Global Prod folds `[0.7674, 0.7547, 0.7990, 0.7774, 0.7457]` (mean 0.7688, std 0.0186, Acc $87.44\% \pm 1.31\%$). |
| Active Gold $N=300$ McNemar tests and Rogan-Gladen parameters for Ensemble ($\mathrm{Se}=0.5217, \mathrm{Sp}=0.9747$, Acc $89.00\%$, Consensus $91.21\%$) and Sentiment Voting ($\mathrm{Se}=0.4783, \mathrm{Sp}=0.9711$, Acc $83.67\%$, Consensus $87.91\%$) | ✓ VERIFIED | Verified active blind gold evaluation with permanent retirement of unblinded `g600` ($\mathrm{Se}=0.711, \mathrm{Sp}=0.942$) documented in JSON and Markdown. |
| Table 3 full-seed confusion matrix ($N=4,500$, Acc $0.9900$, F1 $0.9883$) and complexity ($V=29,843, d_{\text{mean}}=109.72$) | ✓ VERIFIED | Evaluated `category_voting_classifier.joblib` on full seed $N=4,500$: Accuracy 0.9900, Macro-F1 0.9883. Feature dimension $V=29,843$ (word 4,843 + char 25,000), mean active features per review $d=109.72$. |
| Table 1 deployed percentages sum exactly to $100.00\%$ across $N=655,649$ (General 86.55%, Offers 5.04%, Login 4.99%, Network 2.46%, Billing 0.96%) | ✓ VERIFIED | Verified across all 655,649 classified rows. Categories sum to exactly 100.00%. |
| 122M non-overlapping era partitions A, B, and C all sum to 122 calendar months and 655,649 reviews | ✓ VERIFIED | Partition A ($17\text{M}+36\text{M}+24\text{M}+45\text{M}$), Partition B ($17\text{M}+24\text{M}+36\text{M}+45\text{M}$), and Partition C ($41\text{M}+12\text{M}+24\text{M}+45\text{M}$) all sum to 122 months and 655,649 reviews. |
| All 35 modern intra-era shocks decomposed; `top10_by_abs_delta_nss` and `top10_curated_multi_operator` exported | ✓ VERIFIED | Shocks: GP=6, Robi=7, BL=22 (total 35). Both magnitude-ranked and curated multi-operator lists contain 10 verified transitions. |
| Pooled $2\times 2$ ($\chi^2=12.83, \text{OR}=4.23$), non-surge $2\times 2$ ($\chi^2=6.38, \text{OR}=3.65$), BL asymmetry ($\text{OR}=10.00, p=0.0007$), Priority Matrix ($N=88,181, \chi^2=11,027.60, V=0.3536$, Billing $\text{OR}=9.49$, Login $\text{OR}=6.44$, Network $\text{OR}=2.50$) | ✓ VERIFIED | Verified: Contingency table `[[27, 8], [91, 114]]` ($\chi^2=12.83, p=0.0003, \text{OR}=4.23$), non-surge `[[14, 5], [82, 107]]` ($\chi^2=6.38, \text{OR}=3.65$). BL asymmetry Fisher OR = 10.00 ($p=0.0007$). Priority Matrix omnibus $\chi^2(3)=11,027.60$, Cramér's $V=0.3536$. |
| Case Studies 1 & 2: BL Spring 2024 transitions, missingness ($51.82\%$), `v11.8.0` ($N=158$, NSS $-7.59$), and 2025$\to$2026 turnaround ($+15.54$ NSS = $+10.33$ Gen + $+5.21$ Tech) | ✓ VERIFIED | Verified: 2024-03 (+42.82), 2024-04 (+31.63, $\Delta=-11.18$), 2024-05 (+64.42, $\Delta=+32.78$). BL `app_version` missingness = 51.82% (71,068 / 137,131). Turnaround swing = +15.54 points (+10.33 General, +5.21 Technical). |
| Table 7 & 8 Decision Framework: empirical $p_{\text{base}}=0.044162$ and 240-transition alert levels (Level 1: 147, Level 2: 58, Level 3: 15, Level 4: 13) | ✓ VERIFIED | Verified: $p_{\text{base}} = 28,955 / 655,649 = 0.044162$ (4.42%). Transition distribution across 240 modern monthly jumps: Level 1 (147, 61.25%), Level 2 (58, 24.17%), Level 3 (15, 6.25%), Level 4 (13, 5.42%). |

### 1.2 Master Integrity Audit & Legacy Script Retirement (Plan 7.2)

| Must-Have / Truth | Status | Empirical Evidence |
|---|---|---|
| 28 legacy scripts retired to `archive/legacy_scripts/` with inventory `README.md` | ✓ VERIFIED | Inspected `archive/legacy_scripts/`. Exactly 28 retired scripts plus `README.md` cataloging each category and replacement tool. Zero legacy scripts remain in `scripts/`. |
| `scripts/verify_paper_complete.py` reports 3,713 days (2016-08-01 to 2026-09-30), 20,657 early era reviews, and 88,181 functional reviews | ✓ VERIFIED | Executed `python scripts/verify_paper_complete.py` (Exit code 0). Output: `Total days: 3713`, `Early era reviews: 20,657`, `Total in 4 domains: 88,181`. |
| `scripts/audit_paper_contradictions.py` reports 88,181 functional reviews in 4 domains | ✓ VERIFIED | Executed `python scripts/audit_paper_contradictions.py` (Exit code 0). Output: `Total reviews in 4 domains: 88181`. |
| `scripts/audit_project_integrity.py` runs all 8 modules in under 10 seconds, passing cleanly (rc=0) with strict tolerances | ✓ VERIFIED | Executed `python scripts/audit_project_integrity.py` (Exit code 0). Runtime: **7.94s** (strictly under the 10.0s ceiling). 100% of empirical checks passed. |
| Module 1 validates common-duration $N=655,649$, global $N=661,160$, 0 dup/null review IDs, 51 null text rows allowed, telemetry JSONs | ✓ VERIFIED | Module 1 verified GP=320,140, Robi=198,378, BL=137,131, zero duplicate IDs, 51 text nulls, 2016 baseline = 438/126/744. |
| Module 2 validates Gold $N=300$ and $N=200$, zero seed overlap, IRR $\kappa$/PABAK, consensus subsets, and active McNemar bounds | ✓ VERIFIED | Module 2 verified: Sentiment agreement 91.00% ($\kappa=0.5762$, PABAK=0.8650), Category agreement 95.41% ($\kappa=0.7694$), zero seed overlap. |
| Module 3 validates all 7 core joblib models, `bilstm_vocab.json` (2,864 tokens), config parity, and live Hero model evaluation | ✓ VERIFIED | Module 3 verified: all 7 models deserialize cleanly, 2,864 vocab tokens, label mapping parity, live Hero model full-seed accuracy 99.00%. |
| Module 4 enforces strict `atol=0.01` on GP (+64.85), Robi (+65.91), BL (+53.04), Sector (+62.70), and additive decomposition ($10^{-6}$) | ✓ VERIFIED | Module 4 passed: max residual across all 121 sector transitions was $2.13\times 10^{-14} \le 10^{-6}$. |
| Module 5 enforces 122 consecutive months, `(curr - prev).n == 1`, CLT volume floor ($N \ge 294 \gg 30$), 240 transitions, 35 shocks, raw/filtered RMSSD & SSI | ✓ VERIFIED | Module 5 passed: GP 6.28 (filt 5.14), Robi 5.61 (filt 4.53), BL 13.61 (filt 7.56); SSI 93.72, 94.39, 86.39. |
| Module 6 verifies pooled $2\times 2$, non-surge $2\times 2$, BL asymmetry, Prop 1 regression ($R^2=0.5601$, slope=11.52), and Priority Matrix | ✓ VERIFIED | Module 6 passed: Fisher OR=4.23 ($p=4.04\times 10^{-4}$), non-surge OR=3.65, BL OR=10.00 ($p=0.0007$), Prop 1 $R^2=0.5601$ ($p=2.35\times 10^{-7}$). |
| Module 7 verifies BL Spring 2024 counterfactual telemetry, missingness 51.82%, `v11.8.0`, and Case Study 2 annual jump | ✓ VERIFIED | Module 7 passed: 2024-03 (+42.82), 2024-04 (+31.63, $\Delta=-11.18$), 2024-05 (+64.42, $\Delta=+32.78$), missingness 51.82%, turnaround $+15.54$ (+10.33 Gen, +5.21 Tech). |
| Module 8 double-blind anonymity (0 prohibited terms), structure, PDF existence, default mode warnings (rc=0), and `--strict-paper` mode (exit 1) | ✓ VERIFIED | Module 8 passed: 0 prohibited terms, default mode exited 0 with visible warnings on pending Phase 8/9 defects. Executed with `--strict-paper` and confirmed it explicitly exited 1 (`FAILED: --strict-paper mode enabled`). |

### 1.3 Shell Endings & GSD Harness Validators (Plan 7.3)

| Must-Have / Truth | Status | Empirical Evidence |
|---|---|---|
| All 8 `scripts/*.sh` have pure Unix LF (`\n`), zero `0x0D` (CR), and no UTF-8 BOM | ✓ VERIFIED | Byte inspection via `[System.IO.File]::ReadAllBytes`: All 8 scripts have `HasCR = False`, `HasBOM = False`, and `Shebang = #!/bin/bash`. |
| `scripts/validate-encoding.ps1` and `scripts/validate-encoding.sh` check both `*.ps1` and `*.sh` | ✓ VERIFIED | Executed `scripts/validate-encoding.ps1` (Exit code 0). 16 scripts checked (8 ps1 + 8 sh), 0 errors. |
| `scripts/validate-{workflows,skills,agents,templates,encoding}.ps1` anchored via `$PSScriptRoot` | ✓ VERIFIED | Verified code inspection of all 5 PS1 files: `$repoRoot = Split-Path -Parent $PSScriptRoot`. |
| Anchored YAML frontmatter regex `\A---\r?\n([\s\S]*?)\r?\n---` | ✓ VERIFIED | Verified in `validate-workflows.ps1`, `validate-skills.ps1`, and `validate-agents.ps1`. |
| `scripts/validate-agents.ps1` preserves all existing tool names while registering native Antigravity tools (`read_file`, `write_file`, `edit_file`) | ✓ VERIFIED | Inspected `$knownTools` in `validate-agents.ps1`: contains all 20 existing tool names + `read_file`, `write_file`, `edit_file`. Skill path lookup anchored via `$repoRoot`. |
| `scripts/validate-all.ps1` passes cleanly (`rc=0`) from BOTH repo root AND nested directories | ✓ VERIFIED | Ran from root: 27 workflows, 12 skills, 5 subagents, 24 templates, 16 scripts checked; 0 errors (Exit code 0). Ran from `scripts/` (Exit code 0). Ran from `data/gold_set/` (Exit code 0). |

### 1.4 Git Commits Policy (`ADR-003`)

| Must-Have / Truth | Status | Empirical Evidence |
|---|---|---|
| Zero unsolicited git commits made during Phase 7 | ✓ VERIFIED | Executed `git log -n 3 --oneline`. Latest commit remains `3d9f889` from earlier phase. All Phase 7 modifications are preserved in working tree for staged review. |

---

## 2. Artifact Verification (Three-Level Check)

| Artifact Path | Level 1: Exists | Level 2: Substantive | Level 3: Wired | Notes |
|---|:---:|:---:|:---:|---|
| `scripts/compute_statistical_tests.py` | ✓ | ✓ | ✓ | 1,761 lines of executable statistical, econometric, and ML routines. Deserializes models, runs 5-fold CV, computes paired tests, outputs canonical JSON & MD. |
| `scraped_data_global/classified/paper_empirical_ground_truth.json` | ✓ | ✓ | ✓ | 99,044 bytes, 8 top-level sections, valid UTF-8 JSON. Consumed directly by `audit_project_integrity.py` and downstream Phase 8/9 scripts. |
| `scraped_data_global/classified/paper_empirical_ground_truth.md` | ✓ | ✓ | ✓ | 5,304 bytes, 7 structured sections summarizing all paper numbers. |
| `archive/legacy_scripts/` (28 scripts + `README.md`) | ✓ | ✓ | ✓ | 28 legacy scripts archived; `README.md` documents catalog, rationales, and active replacements. |
| `scripts/verify_paper_complete.py` | ✓ | ✓ | ✓ | Repaired in-place: verified 3,713 days, 20,657 early era reviews, 88,181 functional reviews. Passes with rc=0. |
| `scripts/audit_paper_contradictions.py` | ✓ | ✓ | ✓ | Repaired in-place: verified 88,181 functional reviews, exact table matches, and transition metrics. Passes with rc=0. |
| `scripts/audit_project_integrity.py` | ✓ | ✓ | ✓ | Complete 8 modules, 7.94s execution time, passes rc=0 in default mode, exits 1 in `--strict-paper` mode. |
| `scripts/*.sh` (8 shell scripts) | ✓ | ✓ | ✓ | Pure LF, zero `0x0D`, zero BOM, valid shebangs, anchored directory resolution. |
| `scripts/validate-*.ps1` (5 PowerShell scripts) | ✓ | ✓ | ✓ | Anchored via `$PSScriptRoot`, anchored frontmatter regexes, tool registry preserved. |

---

## 3. Key Links & System Wiring

| From | To | Via | Status | Empirical Evidence |
|---|---|---|---|---|
| `scripts/compute_statistical_tests.py` | `ml/models/*.joblib` | `joblib.load` | ✓ WIRED | Deserializes and evaluates `category_voting_classifier.joblib` ($V=29,843, d=109.72$), `ensemble_voting_classifier.joblib`, `sentiment_voting_classifier.joblib`. |
| `scripts/compute_statistical_tests.py` | `scraped_data_global/classified/paper_empirical_ground_truth.json` | `json.dump` | ✓ WIRED | Generates 99 KB canonical ground-truth JSON with 25 verified mathematical invariants. |
| `scripts/audit_project_integrity.py` | `scraped_data_global/classified/paper_empirical_ground_truth.json` | `json.load` | ✓ WIRED | Module 3 loads ground-truth JSON to validate Hero model full-seed accuracy (99.00%), feature space ($V=29,843$), and gold accuracy bounds. |
| `scripts/validate-all.ps1` | `scripts/validate-*.ps1` | `& $PSScriptRoot\...` | ✓ WIRED | Invokes all child validators using relative script directory; runs cleanly from any working directory. |
| `scripts/validate-agents.ps1` | `.agents/agents/*.md` & `.agents/skills/*` | Regex & Path Anchoring | ✓ WIRED | Validates subagents against known tool list (preserving all 20 existing tools + native Antigravity tools) and resolves skill paths. |

---

## 4. Anti-Pattern & Hygiene Scan

- **Unsolicited Git Commits:** 0 commits created during Phase 7 (`git status` and `git diff` show clean staged working-tree state).
- **Hard-Coded Stubs / Placeholders:** AST inspection and module execution verified 0 stubbed functions or placeholder implementations across all modified files.
- **Line Ending Contamination:** Zero `\r` (CR) characters found across all 8 `scripts/*.sh` scripts.
- **Execution Performance:** Master integrity audit completes in **7.94 seconds** (strictly below the 10-second requirement).

---

## 5. Verdict

**Status: pass**  
**Must-Haves Verified: 36/36**  
**Blockers: None**  

Phase 7 has achieved all objectives set forth in `.gsd/ROADMAP.md` and `.gsd/REQUIREMENTS.md` (`REM-05`). The system is fully prepared to proceed to Phase 8 (`Publication Figures, Active ESWA Manuscript & Compiled PDFs Remediation`).
