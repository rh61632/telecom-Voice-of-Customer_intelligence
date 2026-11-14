# Phase 5 Research — Pipeline, Data Hygiene, Demo & Dependency Remediation

**Date:** 2026-11-11  
**Mode:** `research` (Level 2)  
**Target Requirements:** `REM-01`, `REM-02` (`.gsd/REQUIREMENTS.md:13-14`)  
**Scope Discrepancies:** `DISC-CRIT-08`, `DISC-MAJ-03`, `DISC-MAJ-08`, `DISC-MAJ-16`, `DISC-MIN-06`, `DISC-MIN-14..17`, `DISC-HYG-01..03`, `DISC-HYG-05`

---

## Question 1: Pipeline Scripts (`REM-01` — 12-Column Preservation, `2016-08-01` Boundary, JSON Schema & Safe Regeneration)

### 1.1 Empirical On-Disk Baseline & Hidden Deduplication Trap
- **Raw CSVs (`scraped_data_global/raw/`):**
  - `mygp_global.csv`: `321,374` rows, `12` columns (`null_id=0`, `dup_id=0`).
  - `myrobi_global.csv`: `200,652` rows, `12` columns (`null_id=1`, `dup_id=0`).
  - `mybl_global.csv`: `139,134` rows, `12` columns (`null_id=0`, `dup_id=0`).
  - **Exact 12-column header:** `['review_id', 'user_name', 'rating', 'review_date', 'review_text', 'thumbs_up', 'operator', 'app_version', 'user_image', 'developer_reply', 'developer_reply_date', 'is_enriched']`.
  - **Total raw / master classified (`all_operators_classified_global.csv`):** `661,160` rows (`24` columns = `12` raw + `10` model columns + `year`, `ym`).
- **Classified Common Window (`all_operators_common_duration_classified.csv`):**
  - `655,649` rows (`GP=320,140`, `Robi=198,378`, `BL=137,131`), date span `2016-08-01 22:52:08` to `2026-09-30 23:16:00`, enforced by `scripts/audit_project_integrity.py:36-48`.
- **CRITICAL TRAP — Why Running `merge_and_sync_all_datasets.py` As-Written Breaks `N=655,649` & `N=661,160`:**
  - The archive raw files (`archive/scraped_data_2020/raw/my{gp,robi,bl}_scraped_2020_to_sep2026.csv`) contain only `6` columns (`user_name`, `rating`, `review_date`, `review_text`, `thumbs_up`, `operator`).
  - On disk today, `mygp_global.csv`, `myrobi_global.csv`, and `mybl_global.csv` contain **`44,303` pairs (`88,606` rows)** that share the exact 4-tuple `("operator", "review_date", "review_text", "user_name")` while holding distinct `review_id`s (`_bd_` or `NaN` with `is_enriched=False` vs. Google Play UUID with `is_enriched=True`):
    - Grameenphone: `1` pair (`2` rows; `gr_bd_*` vs UUID)
    - Robi: `1` pair (`2` rows; `NaN` row index `72102` vs `831958fb-6eba-4362-bbb0-518ca11c50f0` row index `194430`)
    - Banglalink: `44,301` pairs (`88,602` rows; `ba_bd_*` vs UUID)
  - `scraped_data_global/pipeline/merge_and_sync_all_datasets.py:229` calls `combined.drop_duplicates(subset=["operator", "review_date", "review_text", "user_name"])`. If executed against disk CSVs, it drops **`44,303` rows** (`661,160 -> 616,857`), violating `SPEC.md:18` and `ADR-003` (`.gsd/DECISIONS.md:20`).
  - Worse, `merge_and_sync_all_datasets.py:243-247` joins `dedup` against `op_existing` (`all_operators_classified_global.csv`) on `["review_date", "review_text", "user_name"]`. Because `op_existing` contains BOTH rows for all `44,303` pairs, `dedup.merge(op_existing, ...)` causes a `1 -> 2` row expansion in `op_final` (`661,160`) while writing only `616,857` rows to `raw_out` (`merge_and_sync_all_datasets.py:272`), desynchronizing raw vs. classified CSVs!

### 1.2 Exact Line-by-Line Logic & Edits Needed

1. **`scraped_data_global/pipeline/scraper_worker.py` (`DISC-CRIT-08`, `DISC-HYG-05`):**
   - **Lines `49-57` (`FIELDNAMES`):** Expand from 7 fields to all 12 canonical raw fields:
     ```python
     FIELDNAMES = [
         "review_id", "user_name", "rating", "review_date", "review_text",
         "thumbs_up", "operator", "app_version", "user_image",
         "developer_reply", "developer_reply_date", "is_enriched",
     ]
     ```
   - **Lines `137-140` (Full mode header):** `csv.DictWriter(csv_file, fieldnames=FIELDNAMES)` automatically writes the 12-column header once `FIELDNAMES` is updated.
   - **Lines `163-170` & `264-275` (`lang="en"`, `country="us"` — `DISC-HYG-05`):** Parameterize `run_scraper(..., lang: str = "en", country: str = "us")` and add CLI flags `--lang` (default `"en"`) and `--country` (default `"us"`) to `argparse` (`lines 265-274`), passing `lang=lang, country=country` into `reviews(...)` at `lines 165-166`. Keeps `"en"` / `"us"` defaults for provenance parity.
   - **Lines `203-211` (Record dict mapping):** `google_play_scraper.constants.element.ElementSpecs.Review` exposes keys `['reviewId', 'userName', 'userImage', 'content', 'score', 'thumbsUpCount', 'reviewCreatedVersion', 'at', 'replyContent', 'repliedAt', 'appVersion']`. Populate all 12 fields and guard empty/null `reviewId`:
     ```python
     rev_id = str(r.get("reviewId") or "").strip()
     if not rev_id:
         continue  # prevent null review_id rows (DISC-HYG-05)
     replied_at = r.get("repliedAt")
     reply_text = r.get("replyContent")
     app_ver = r.get("appVersion") or r.get("reviewCreatedVersion")
     row = {
         "review_id": rev_id,
         "user_name": str(r.get("userName") or "A Google user"),
         "rating": int(r.get("score") or 0),
         "review_date": rev_dt.strftime("%Y-%m-%d %H:%M:%S"),
         "review_text": str(r.get("content") or "").strip(),
         "thumbs_up": int(r.get("thumbsUpCount") or 0),
         "operator": op_name,
         "app_version": str(app_ver).strip() if app_ver else None,
         "user_image": str(r.get("userImage")).strip() if r.get("userImage") else None,
         "developer_reply": str(reply_text).strip() if reply_text else None,
         "developer_reply_date": replied_at.strftime("%Y-%m-%d %H:%M:%S") if replied_at else None,
         "is_enriched": True,
     }
     ```
     *(Verified against `mygp_global.csv` row 0: `app_version` is null/empty when absent, `developer_reply_date` uses `%Y-%m-%d %H:%M:%S`, and `is_enriched` is boolean `True`.)*
   - **Lines `240-247` (Incremental append):** `new_df = pd.DataFrame(new_rows, columns=FIELDNAMES)` (`line 240`) writes all 12 columns. Before `new_df.to_csv(out_csv, mode="a", header=not out_csv.exists(), index=False)` (`line 247`), verify `existing_cols = pd.read_csv(out_csv, nrows=0).columns.tolist()` when `out_csv.exists()` and `reindex(columns=existing_cols)` if an older header exists so column alignment can never corrupt.

2. **`scraped_data_global/pipeline/run_parallel_scrapers.py` (`DISC-HYG-01`):**
   - **Lines `22-24` (`PYTHON_BIN`):** Hardcodes `PROJECT_ROOT / "dl" / ".venv" / "bin" / "python"` (POSIX-only; `dl/.venv` does not even exist on disk). Replace with cross-platform resolution:
     ```python
     venv_candidates = [
         PROJECT_ROOT / "dl" / ".venv" / ("Scripts" if os.name == "nt" else "bin") / ("python.exe" if os.name == "nt" else "python"),
         PROJECT_ROOT / "ml" / ".venv" / ("Scripts" if os.name == "nt" else "bin") / ("python.exe" if os.name == "nt" else "python"),
     ]
     PYTHON_BIN = next((str(p) for p in venv_candidates if p.exists()), sys.executable)
     ```
     (Or directly `PYTHON_BIN = sys.executable` per `.gsd/DISCREPANCY_REPORT.md:415`.)
   - **Lines `30-55` & `61-65`:** Optionally pass through `--lang` / `--country` flags to `WORKER_SCRIPT`, and check `p.returncode` after `while True` finishes so non-zero worker exits are reported rather than printing success unconditionally (`line 64`).

3. **`scraped_data_global/pipeline/merge_and_sync_all_datasets.py` (`DISC-CRIT-08`, `DISC-MAJ-16`, `DISC-MIN-06`):**
   - **Preserve 12 raw columns (`lines 217-224`, `272`):** Define `RAW_COLUMNS = ["review_id", "user_name", "rating", "review_date", "review_text", "thumbs_up", "operator", "app_version", "user_image", "developer_reply", "developer_reply_date", "is_enriched"]`. Ensure `df_bd` / `df_us` backfill any missing columns (`None` for string metadata, `False` for `is_enriched`) instead of slicing to 7 columns at `line 272`. Write `dedup[RAW_COLUMNS].to_csv(raw_out, index=False)`.
   - **Prevent `44,303`-row deletion & many-to-many join (`lines 225-261`):**
     - When `df_us` already carries the frozen historical corpus (`661,160` rows including `44,479` `_bd_` rows), deduplicating blindly on `["operator", "review_date", "review_text", "user_name"]` (`line 229`) drops `44,303` historical pairs. Instead:
       1. Keep `df_us` records intact if they already have distinct non-null `review_id`s (deduplicate `df_us` strictly by non-null `review_id`), and only append rows from `df_bd` whose `(operator, review_date, review_text, user_name)` is not already in `df_us` (or treat `review_id` as primary key when present).
       2. At `lines 236-247` (`dedup.merge(op_existing, ...)`), merge primarily on `review_id` (deduplicated) for non-null IDs, and deduplicate `op_existing` on `["review_date", "review_text", "user_name"]` before any fallback 4-tuple merge (`validate="many_to_one"`), preventing cartesian row multiplication.
   - **Enforce `2016-08-01` & fix `common_duration_days` (`lines 290`, `294`):**
     - `line 290` already has `start_common = pd.Timestamp("2016-08-01 00:00:00")` (uncommitted working-tree change).
     - **CRITICAL OFF-BY-ONE BUG at `line 294`:** `days = (end_common - start_common).days` evaluates to **`3712`** (`(2026-09-30 23:16:00 - 2016-08-01 00:00:00)` = `3712 days 23:16:00` -> `.days` truncates to `3712`), whereas the canonical inclusive calendar window (`Aug 1, 2016`–`Sep 30, 2026`) is **`3713` days** (`common_duration_summary.json:4`, `README.md:36`). Fix `line 294` to:
       ```python
       days = (end_common.normalize() - start_common.normalize()).days + 1
       ```
   - **Align `common_duration_summary.json` schema (`lines 317-324` — `DISC-MIN-06`):** Add `"positive_count": int(pos)`, `"neutral_count": int(neu)`, `"negative_count": int(neg)` to `summary["operators"][op]` matching `sync_post_classification.py:86-96`.

4. **`scraped_data_global/pipeline/sync_post_classification.py` (`DISC-MAJ-16`, `DISC-MIN-06` — Safe Canonical Regeneration Path):**
   - `sync_post_classification.py` reads ONLY `scraped_data_global/classified/my{bl,gp,robi}_classified_global.csv` (`139,134 + 321,374 + 200,652 = 661,160` rows, all `22` columns intact — `sync_post_classification.py:33-46`) and does NOT touch `raw/` or re-run `drop_duplicates`, making it 100% safe for regenerating derived files without breaking `N=661,160` or `N=655,649`!
   - **Line `58` (`start_common`):** Currently `start_common = max(df_sep[df_sep["operator"] == op]["review_date"].min() for op in OPERATOR_SERIAL)`, which resolves to `2016-07-28 22:36:00` (yielding `655,670` rows: `3` GP + `18` BL = `21` extra July 28–31 reviews, while excluding the `3` BL reviews earlier on July 28 before `22:36:00`). Replace line `58` with:
     ```python
     # Align to start of first complete calendar month (August 1, 2016)
     start_common = pd.Timestamp("2016-08-01 00:00:00")
     ```
   - **Line `62` (`days`):** Currently `days = (end_common - start_common).days`, which truncates to **`3712`** once `start_common` is `2016-08-01 00:00:00`! Fix line `62` to:
     ```python
     days = (end_common.normalize() - start_common.normalize()).days + 1
     ```
   - **Verified Simulation Result (executed against live classified CSVs):**
     - `all_operators_classified_global.csv`: `661,160` rows (`24` cols, all `12` raw cols preserved).
     - `all_operators_common_duration_classified.csv`: `655,649` rows (`GP=320,140`, `Robi=198,378`, `BL=137,131`), `2016-08-01 22:52:08` to `2026-09-30 23:16:00`, `days = 3713`.
     - `common_duration_summary.json`: `total_reviews: 655649`, `common_duration_days: 3713`, includes `positive_count`, `neutral_count`, `negative_count`.
     - `yearly_intelligence_trends.json`: currently sums to **`655,670`** (`2016` has `GP=441, Robi=126, BL=762` -> `21` stale July 2016 reviews!). Re-running `sync_post_classification.py` updates `2016` to **`GP=438` (`nss=2.51`, `pos=39.73%`, `neg=37.21%`), `Robi=126` (`nss=-57.94`, `pos=14.29%`, `neg=72.22%`), `BL=744` (`nss=45.30`, `pos=63.17%`, `neg=17.88%`)**, bringing total JSON sum to exact **`655,649`**.
     - `global_multi_year_intelligence_report.md`: currently has internal drift where Section 1 (`lines 17-20`) reports `655,649` (`GP=320,140`, `Robi=198,378`, `BL=137,131`) while Section 2 (`lines 32-34`) still reports stale `2016` totals (`441`, `126`, `762` summing to `655,670`). Re-running `sync_post_classification.py` makes Sections 1, 2, and 3 100% mutually consistent at `N=655,649` and `3,713` days.

---

## Question 2: Exact Null/Duplicate `review_id` Row in `myrobi_global.csv` vs. `all_operators_common_duration_classified.csv` (`DISC-HYG-05`)

### 2.1 Exact Row Identity & Provenance
- **In `scraped_data_global/raw/myrobi_global.csv` (`200,652` rows total):**
  - **Null `review_id` row:** DataFrame index **`72102`** (1-based data row `72,103`):
    - `review_id`: `NaN` (blank)
    - `user_name`: `'Shahidul Islam'`
    - `rating`: `5`
    - `review_date`: `'2024-09-17 08:15:53'`
    - `review_text`: `'nice'`
    - `thumbs_up`: `0`
    - `operator`: `'Robi'`
    - `app_version`: `NaN`, `user_image`: `NaN`, `developer_reply`: `NaN`, `developer_reply_date`: `NaN`, `is_enriched`: `False`
  - **Exact duplicate pair in `myrobi_global.csv`:** DataFrame index **`194430`**:
    - `review_id`: `'831958fb-6eba-4362-bbb0-518ca11c50f0'` (also found in `archive/robi_backfill/robi_backfilled_gap_2024_2025.csv` at index `37008`)
    - Identical `(operator, review_date, review_text, user_name, rating, thumbs_up)`, with full enriched metadata: `app_version='7.5.0'`, `user_image` populated, `developer_reply` populated, `developer_reply_date='2024-09-17 11:24:01'`, `is_enriched=True`.
  - **Unique `review_id` count:** `nunique(dropna=True) = 200,651`, `nunique(dropna=False) = 200,652`, `null_id = 1`, `non_null_dup_id = 0` (`mygp_global.csv` and `mybl_global.csv` both have `0` nulls and `0` duplicate `review_id`s).
- **In `scraped_data_global/classified/all_operators_common_duration_classified.csv` (`655,649` rows total):**
  - Null row appears at DataFrame index **`528897`** (`review_id=NaN`, `Shahidul Islam`, `5`, `2024-09-17 08:15:53`, `Robi`, `predicted_sentiment='Positive'`, `predicted_category='General Appreciation / Other'`).
  - Its enriched pair appears at DataFrame index **`649549`** (`review_id='831958fb-6eba-4362-bbb0-518ca11c50f0'`, identical `Positive` / `General Appreciation / Other`).
  - Also present in `myrobi_classified_global.csv` (`200,652` rows, `null_id=1`) and `all_operators_classified_global.csv` (`661,160` rows, `null_id=1`).

### 2.2 Safety Assessment: Can It Be Fixed Without Shifting `N=655,649` / `N=661,160`?
- **Deleting row `72102` / `528897` is NOT safe without shifting counts:**
  - Deletion reduces `myrobi_global.csv` & `myrobi_classified_global.csv` (`200,652 -> 200,651`), `all_operators_classified_global.csv` (`661,160 -> 661,159`), and `all_operators_common_duration_classified.csv` (`655,649 -> 655,648`; Robi `198,378 -> 198,377`, Robi Positive `154,477 -> 154,476`).
  - That breaks `SPEC.md:18` ("Non-Goals: ... mutating historical `N=655,649`"), `ADR-003` (`.gsd/DECISIONS.md:20`), `scripts/audit_project_integrity.py:36,41` (`assert total_rows == 655649` and `assert counts['Robi'] == 198378`), and invalidates Robi/Industry counts in `common_duration_summary.json`, `README.md`, and both manuscripts.
  - Moreover, `mybl_global.csv` already retains `44,301` non-null 4-tuple overlap pairs (`ba_bd_*` + UUID) and `mygp_global.csv` retains `1` (`gr_bd_*` + UUID) as part of the frozen `661,160`/`655,649` corpus.
- **Safe Non-Mutating / ID-Backfill Options (ZERO shift to `N=655,649` / `N=661,160`):**
  1. **Option A (Recommended — Assign synthetic deterministic `review_id` without deleting row):** Populate row `72102` in `myrobi_global.csv` and the corresponding row in `myrobi_classified_global.csv` with a non-colliding synthetic ID matching the repo's existing `_bd_` convention (verified existing IDs are `['ro_bd_23979', 'ro_bd_279', 'ro_bd_29670', 'ro_bd_29681', 'ro_bd_363', 'ro_bd_4370']`, so `ro_bd_missing_72102` or `ro_missing_72102` has zero collision), then regenerate `all_operators_*` via `sync_post_classification.py`. Result: `null_id = 0` and `100%` unique `review_id` across all `661,160` / `655,649` rows with **zero** shift to any count, NSS, shock, or audit assertion.
  2. **Option B (Leave row frozen & harden scraper/merge):** Keep `72102` untouched to avoid touching historical CSVs at all, and document why `review_id` has 1 null out of `661,160` while ensuring `scraper_worker.py:204` rejects null `reviewId` on future runs. *(Option A is cleaner if `audit_project_integrity.py` or downstream scripts assert `review_id.notna().all()`.)*

---

## Question 3: Exact Edits for `demo/`, Requirements, `README.md`, and `TODO.txt` (`REM-02`)

### 3.1 `demo/app.py` (`DISC-MAJ-08`, `DISC-MIN-14`)
- **UI wiring bug (`DISC-MAJ-08`):**
  - `demo/app.py:97` defines `out_cat = gr.Textbox(label="Operational Domain", interactive=False)` and `demo/app.py:38` computes `category_label = f"{res['category']} ({res['category_confidence'] * 100:.1f}%)"`, but both returns and the click listener omit it:
  - **Line `31`:** Change `return "N/A", "N/A", {}, {}, "Please enter a customer review."` -> `return "N/A", "N/A", "N/A", {}, {}, "Please enter a customer review."`
  - **Line `38` (defensive guard):** Change to `category_label = f"{res['category']} ({res['category_confidence'] * 100:.1f}%)" if res["category"] and res["category_confidence"] is not None else "N/A"` so missing `category_model` cannot crash with `TypeError`.
  - **Line `54`:** Change `return lang_badge, sentiment_label, res["probabilities"], cat_probs, diagnostic_summary` -> `return lang_badge, sentiment_label, category_label, res["probabilities"], cat_probs, diagnostic_summary`
  - **Line `108`:** Change `outputs=[out_lang, out_sent, out_sent_probs, out_cat_probs, out_diag]` -> `outputs=[out_lang, out_sent, out_cat, out_sent_probs, out_cat_probs, out_diag]`
- **Training volume claim (`DISC-MIN-14`):**
  - **Line `67`:** Change `*Trained on 655,649 longitudinal customer reviews across Grameenphone, Robi Axiata, and Banglalink (2016–2026).*` -> `*Demonstrating models trained on 4,500 expert/LLM-labeled seed reviews and evaluated across 655,649 longitudinal customer reviews from Grameenphone, Robi Axiata, and Banglalink (2016–2026).*`
- **Paper Title Verification (`demo/app.py:114`):**
  - `.gsd/phases/1/evidence/03_demo_application_audit.md:147-150` claimed `paper/eswa_latex/manuscript.tex` had dropped `"With Great Reviews Comes Great Responsibility:"`, **but direct inspection confirms** both `paper/eswa_latex/manuscript.tex:32` and `paper/eswa_latex/title_page.tex:14` use the exact full title `"With Great Reviews Comes Great Responsibility: An Intelligent Decision Support System for Telecommunications Voice-of-the-Customer Diagnostics and Cross-Layer Subsystem Decoupling"`, matching `demo/app.py:114` verbatim. (Only `paper/telecommunications_policy_latex/manuscript.tex:27` uses a different subtitle.) No title edit is needed on line `114`.

### 3.2 Dependency Manifests (`DISC-MAJ-03`, `DISC-HYG-02`, `DISC-HYG-03`)
*(Verified via AST scan across all active `.py` files in `ml/`, `dl/`, `demo/`, `scripts/`, `scraped_data_global/pipeline/`, `data/gold_set/`, plus live `sys.modules` trace of `demo/app.py` inference.)*

1. **`demo/requirements.txt` (`5` lines):**
   - **Line `2` (`DISC-HYG-03`):** Change `scikit-learn>=1.3.0` -> `scikit-learn>=1.4.0` (matches `requirements.txt:30`, `ml/requirements.txt:5`, `dl/requirements.txt:10`; `.joblib` models were pickled under `scikit-learn 1.6.1`).
   - **Add `nltk>=3.8.1` (`DISC-MAJ-03`):** Required at import time by `demo/app.py:13` -> `ml/predict.py:13` -> `ml/language_detector.py:18,28` (`from nltk.corpus import words`, `import nltk`). Currently crashes isolated installs with `ModuleNotFoundError: No module named 'nltk'`.
   - **Note on `pandas>=2.0.0`:** Live `sys.modules` trace of `ml.predict` + `ml.language_detector` + `.joblib` unpickling confirms `demo/app.py` does **not** directly import `pandas` at runtime (contrary to `03_demo_application_audit.md:177` which assumed a nonexistent `ml.feature_engineering` module). However, `.gsd/DISCREPANCY_REPORT.md:142` explicitly requests `nltk>=3.8.1` and `pandas>=2.0.0` in `demo/requirements.txt` (aligning with `ml/requirements.txt`), so including `pandas>=2.0.0` is safe and satisfies the discrepancy spec.

2. **`ml/requirements.txt` (`9` lines):**
   - **Add `nltk>=3.8.1` (`DISC-MAJ-03`):** `ml/predict.py:13` unconditionally imports `ml.language_detector`, which imports `nltk` (`ml/language_detector.py:18`). Without `nltk`, `python ml/predict.py` crashes in a clean `ml/` environment.

3. **`dl/requirements.txt` (`12` lines):**
   - **Remove lines `6-7` (`DISC-HYG-02`):** Delete `torchvision>=0.17.0` and `torchaudio>=2.2.0` (`0` imports in any `.py` file across the repository).
   - *(Note: `sentence-transformers>=2.7.0` on line `9` also has `0` imports in active `.py` files, used only in `archive/early_dl_experiments/`; retain with `# Optional / notebook MiniLM baseline` comment or leave until Phase 6.)*

4. **`requirements.txt` (`39` lines):**
   - **Remove lines `36-37` (`DISC-HYG-02`):** Delete `torchvision>=0.17.0` and `torchaudio>=2.2.0`.
   - **Add missing runtime packages (`DISC-MAJ-03`)** proven by AST scan of active `.py` files:
     - `nltk>=3.8.1` (`ml/language_detector.py:18,28`)
     - `gradio>=4.0.0` (`demo/app.py:5`)
     - `python-docx>=1.1.0` (`scripts/audit_docx.py:1`, `scripts/find_tables.py:1`, `scripts/convert_latex_to_docx.py:5`, `scripts/build_*_docx.py`, `scripts/build_jba_*.py` — `1.2.0` installed locally)
     - `openpyxl>=3.1.0` (`scripts/build_paper_empirical_excel.py:13` — `3.1.5` installed locally)
     - `Pillow>=10.0.0` (`scripts/check_crop.py:1`, `scripts/check_crop_wide.py:1`, `scripts/check_other_crops.py:1`, `scripts/test_figure1_offsets.py:6` — `13.0.0` installed locally)
     - `huggingface-hub>=0.23.0` (`scripts/upload_to_huggingface.py:195,200`)

### 3.3 `README.md` (`DISC-MIN-15`, `DISC-MIN-16` & Directly Observed Stale Drift)
- **Line `20` (`DISC-MIN-16`):** Currently displays only `Cohen's Kappa: κ = 0.77 (Substantial)` (Category $\kappa = 0.7694$), omitting Sentiment $\kappa = 0.5762$ (`Moderate`). Update badge or add a companion badge right alongside line `20` showing `Sentiment κ = 0.58 (Moderate)` and `Category κ = 0.77 (Substantial)`.
- **Line `416` (`DISC-MIN-15`):** Change `* **Common Period NSS:** \`+53.1%\` (137,131 reviews)` -> `* **Common Period NSS:** \`+53.0%\` (137,131 reviews)` (reconciles with `README.md:52`, `common_duration_summary.json:38` `53.04`, and `global_multi_year_intelligence_report.md:19`).
- **Additional directly observed `README.md` drift to also fix cleanly in Phase 5:**
  - **Line `120`:** Currently `| **2016** *(Jul–Dec)* | **+2.5%** (441) | **-57.9%** (126) | **+46.3%** (762) | ... 63.8% positive reviews. |` — still reflects the excluded July 28–31, 2016 reviews (`655,670` total)! Under canonical `Aug 1, 2016` (`N=655,649`), update to `*(Aug–Dec)*`, `**+2.5%** (438)`, `**-57.9%** (126)`, `**+45.3%** (744)`, and `63.2% positive reviews`. *(Also note lines `121-123, 130` inline negative/positive percentages—e.g. `67.8%` vs `68.4%` for Robi 2017, `47.9%` vs `50.4%` for GP 2018, `53.6%` vs `56.7%` for Robi 2018, `86.8%` vs `87.1%` for BL 2026, `16.2%` vs `17.4%` for GP 2026—differ slightly from `yearly_intelligence_trends.json`; verify whether to align those inline shares to `yearly_intelligence_trends.json` too.)*
  - **Lines `432-433`:** Directory comments `(123 Months)` and `(42 Months)` reflect pre-cutoff July 2016; update to `(122 Months)` and `(41 Months)` matching `README.md:97,107`.
  - **Lines `478-484` & tree:** `scraped_data_global/pipeline/` omits `sync_post_classification.py` (which `README.md:521` tells users to run!) and `evaluate_nss_stability_and_shocks.py`; `demo/` (`app.py`, `requirements.txt`) is also absent from the directory tree.
  - **Line `590`:** Says `interactive Streamlit web demos` (implemented demo in `demo/app.py` is **Gradio**, not Streamlit) and has malformed stray `$` math delimiters (`κ = 0.5762$` and `κ = 0.7694$`).

### 3.4 `TODO.txt` (`DISC-MIN-17`)
- **Lines `16` & `32`:** `banglabert_finetuned_models (1).zip` -> actual filename at repo root is `banglabert_finetuned_models.zip`.
- **Lines `49-50`:** `blind_annotation_300_ratul.csv` and `blind_annotation_200_friend.csv` -> actual anonymized filenames in `data/gold_set/` are `blind_annotation_300_annotator1.csv` and `blind_annotation_200_annotator2.csv` (also removes annotator identity leak).
- **Line `61`:** `Full-dataset model (N = 4,499)` -> true seed count is `N = 4,500` (`data/processed/{mygp,myrobi,mybl}_classified_reviews.csv` each have `1,500` rows).
- **Lines `63` & `69`:** Replace stale `398k production corpus` (`398k corpus`) with `655.6k common-window production corpus` (`661.2k master corpus`).
- **Lines `76-89` (Section 4 — Web Demo):** Mark local Gradio app implementation as `[COMPLETED LOCALLY]` (`demo/app.py` and `demo/requirements.txt` are built; only Hugging Face Spaces deployment remains pending), and remove `Streamlit` ambiguity or note Gradio implementation.

---

## Unknowns & Explicit Scope Boundaries
1. **Uninstalled Optional Cloud/DL Packages (`task-114`):** In the current host Python environment (`Python 3.15`), `gradio`, `transformers`, `sentence-transformers`, `groq`, `huggingface-hub`, `torchvision`, and `torchaudio` are not installed; syntax (`py_compile` / `ast.parse`) and `ml/` + `scraped_data_global/pipeline/` execution can be verified locally, while live Gradio UI rendering (`demo/app.py`) cannot be booted locally unless `gradio` is installed (per `SPEC.md:20`, installing cloud-only packages is not required).
2. **`data/README.md:23-25` Cross-File Spillover:** `data/README.md:23-24` still lists `blind_annotation_300_ratul.csv` and `blind_annotation_200_friend.csv` (with stray `$` at line `25`). Noted here for completeness; scheduled under `REM-04` / Phase 6 alongside `data/gold_set/`.
3. **NLTK `words` Corpus Download in Offline Environments:** `ml/language_detector.py:25-30` auto-downloads `nltk` `"words"` on `LookupError`. In air-gapped containers built from `demo/requirements.txt`, a pre-download step (`python -m nltk.downloader words`) in deployment instructions or README is helpful context though not a `requirements.txt` line edit.
