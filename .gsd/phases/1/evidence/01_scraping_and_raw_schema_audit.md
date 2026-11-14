# Evidence 01: Google Play Scraping Scripts, Raw CSV Schemas, and Pipeline Column Preservation Audit

**Milestone:** Project & Paper Discrepancy Audit (v1.0.0)  
**Phase:** 1 - Core Pipeline, Data, Demo & Documentation Audit  
**Plan:** `1-PLAN.md` (Task 1)  
**Date of Audit:** 2026-11-11  
**Execution Mode:** Strictly Read-Only Audit (`ADR-001`)

---

## 1. Executive Summary

This audit examined Google Play scraping workflows, raw dataset schemas, deduplication logic, and column preservation behavior across `scraped_data_global/raw/` and `scraped_data_global/pipeline/`.

### Key Findings
1. **Critical Overwrite / Schema-Dropping Hazard:** The raw CSV datasets on disk (`mygp_global.csv`, `myrobi_global.csv`, `mybl_global.csv`) each contain **12 columns** (including `app_version`, `user_image`, `developer_reply`, `developer_reply_date`, and `is_enriched`). However, both `scraper_worker.py` (lines 49-57, 137-140, 203-211) and `merge_and_sync_all_datasets.py` (line 272) hardcode a **7-column schema** (`review_id`, `user_name`, `rating`, `review_date`, `review_text`, `thumbs_up`, `operator`). Running either scraper in full mode or executing `merge_and_sync_all_datasets.py` will permanently slice away 5 columns and drop `app_version`.
2. **Downstream Pipeline Vulnerability:** Downstream script `scripts/check_version_bias.py` relies directly on `app_version` (`df['has_version'] = df['app_version'].notna()`). Overwriting the raw CSVs with the 7-column schema will crash downstream version bias evaluation with `KeyError: 'app_version'`.
3. **Platform Portability Defect:** `run_parallel_scrapers.py:22` hardcodes POSIX virtualenv binary path `PROJECT_ROOT / "dl" / ".venv" / "bin" / "python"`. On Windows hosts, the binary is located at `dl/.venv/Scripts/python.exe`. While a fallback to `sys.executable` exists, it bypasses the dedicated virtual environment if one is deployed on Windows.
4. **Scraping Boundary & Storefront Drift:** Scrapers are hardcoded with `country="us"` and `lang="en"` with batch pagination (`count=199`, `sort=Sort.NEWEST`). This queries the United States regional storefront for Bangladeshi telecommunications apps, and filters according to English language preferences.
5. **Progress JSON State Path Discrepancy:** Scrapers write progress files to `scraped_data_global/progress_{op}.json` (`TARGET_DIR / progress_{op}.json`), while plan references specify `scraped_data_global/raw/progress_{op}.json`. No progress files currently exist in either directory on disk because `scraped_data_global/progress_*.json` is gitignored.

---

## 2. Empirical Schema & Dataset Inspection

All three raw CSV files on disk were empirically inspected using non-destructive streaming analysis and parsed with RFC 4180 multiline handling.

### 2.1 File Characteristics & Parsed Records

| Operator | File Path | Parsed Rows | Physical Line Breaks | Raw Columns | Date Range (Min -> Max) |
|---|---|---|---|---|---|
| **Grameenphone** | `scraped_data_global/raw/mygp_global.csv` | **321,374** | 353,864 | 12 | `2016-07-28 22:36:00` -> `2026-10-31 15:57:34` |
| **Robi** | `scraped_data_global/raw/myrobi_global.csv` | **200,652** | 203,498 | 12 | `2015-02-03 12:01:31` -> `2026-10-31 16:46:54` |
| **Banglalink** | `scraped_data_global/raw/mybl_global.csv` | **139,134** | 173,597 | 12 | `2014-03-01 18:25:10` -> `2026-10-31 16:04:33` |
| **Total Raw** | — | **661,160** | 730,959 | — | `2014-03-01 18:25:10` -> `2026-10-31 16:46:54` |

> *Note on Line Count Divergence:* The raw text files contain 730,959 newline characters due to unescaped embedded newlines inside user review text and developer reply bodies. Correctly parsed RFC 4180 CSV records yield exactly **661,160** records.

### 2.2 Exact Column Names (12 Columns)
Both Grameenphone, Robi, and Banglalink share the identical 12 columns in their raw CSV headers:
1. `review_id` (str)
2. `user_name` (str)
3. `rating` (int64)
4. `review_date` (str, formatted `YYYY-MM-DD HH:MM:SS`)
5. `review_text` (str)
6. `thumbs_up` (int64)
7. `operator` (str)
8. `app_version` (str / null)
9. `user_image` (str / null)
10. `developer_reply` (str / null)
11. `developer_reply_date` (str / null)
12. `is_enriched` (bool: `True` / `False`)

### 2.3 Metadata & Enrichment Field Statistics

| Field / Metric | Grameenphone (`mygp_global.csv`) | Robi (`myrobi_global.csv`) | Banglalink (`mybl_global.csv`) |
|---|---|---|---|
| **Total Rows** | 321,374 | 200,652 | 139,134 |
| **Unique Review IDs** | 321,374 (100.0% unique) | 200,651 (1 duplicate ID: 1 null) | 139,134 (100.0% unique) |
| **Null Review Text** | 21 (0.007%) | 10 (0.005%) | 36 (0.026%) |
| **Null App Version** | 59,164 (**18.41%**) | 33,828 (**16.86%**) | 71,937 (**51.70%**) |
| **Populated App Version** | 262,210 (81.59%) | 166,824 (83.14%) | 67,197 (48.30%) |
| **Unique App Versions** | 210 | 165 | 170 |
| **Developer Reply Count** | 315,579 (**98.20%**) | 194,347 (**96.86%**) | 72,679 (**52.24%**) |
| **Enriched Flag = True** | 321,181 (99.94%) | 199,772 (99.56%) | 93,676 (67.33%) |
| **Enriched Flag = False** | 193 (0.06%) | 880 (0.44%) | 45,458 (32.67%) |

---

## 3. Detailed Code Analysis: Schema-Dropping Overwrite Risks

### 3.1 Hardcoded 7-Column Schema in `scraper_worker.py`
In `scraped_data_global/pipeline/scraper_worker.py`:
- **Lines 49–57:**
  ```python
  FIELDNAMES = [
      "review_id",
      "user_name",
      "rating",
      "review_date",
      "review_text",
      "thumbs_up",
      "operator",
  ]
  ```
- **Lines 137–140 (Full Scrape Mode):**
  ```python
  if not incremental:
      csv_file = open(out_csv, "w", encoding="utf-8", newline="")
      writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
      writer.writeheader()
  ```
- **Lines 203–211 (Record Construction):**
  ```python
  row = {
      "review_id": str(r.get("reviewId", "")),
      "user_name": str(r.get("userName", "A Google user")),
      "rating": int(r.get("score", 0)),
      "review_date": rev_dt.strftime("%Y-%m-%d %H:%M:%S"),
      "review_text": str(r.get("content", "")).strip(),
      "thumbs_up": int(r.get("thumbsUpCount", 0)),
      "operator": op_name,
  }
  ```
- **Lines 240, 247 (Incremental Scrape Mode):**
  ```python
  new_df = pd.DataFrame(new_rows, columns=FIELDNAMES)
  ...
  new_df.to_csv(out_csv, mode="a", header=not out_csv.exists(), index=False)
  ```

**Impact Assessment:**
- When running in default full mode, `scraper_worker.py` truncates the output file to the 7 fields in `FIELDNAMES`. Although the Google Play API payload `r` contains `r.get("appVersion")`, `r.get("userImage")`, `r.get("replyContent")`, and `r.get("repliedAt")`, none of these are mapped into `row`.
- When running in incremental mode (`--incremental`), newly appended rows have only 7 fields. Appending these 7-column rows to an existing 12-column file creates a schema mismatch where new rows lack the trailing 5 columns.

### 3.2 Overwrite Hazard in `merge_and_sync_all_datasets.py`
In `scraped_data_global/pipeline/merge_and_sync_all_datasets.py`:
- **Line 272:**
  ```python
  dedup[["review_id", "user_name", "rating", "review_date", "review_text", "thumbs_up", "operator"]].to_csv(raw_out, index=False)
  ```
- `raw_out` is defined at line 269 as:
  ```python
  file_key = "mygp" if op_name == "Grameenphone" else "myrobi" if op_name == "Robi" else "mybl"
  raw_out = raw_glob_dir / f"{file_key}_global.csv"
  ```

**Impact Assessment:**
- `raw_glob_dir / f"{file_key}_global.csv"` points directly to `scraped_data_global/raw/mygp_global.csv`, `myrobi_global.csv`, and `mybl_global.csv`.
- Line 272 explicitly filters `dedup` by selecting only 7 columns, and writes this DataFrame directly over `raw_out`.
- Executing `merge_and_sync_all_datasets.py` immediately overwrites the live raw files, permanently destroying `app_version`, `user_image`, `developer_reply`, `developer_reply_date`, and `is_enriched` on disk.

### 3.3 Downstream Dependency in `scripts/check_version_bias.py`
In `scripts/check_version_bias.py`:
- **Lines 5–6:**
  ```python
  df = pd.read_csv('scraped_data_global/classified/all_operators_common_duration_classified.csv')
  df['has_version'] = df['app_version'].notna()
  ```
- **Lines 37–40:**
  ```python
  bl_spring = df[(df['operator'] == 'Banglalink') & df['review_date'].str.contains('^2024-0[345]')].copy()
  bl_v = bl_spring[bl_spring['has_version']]
  bl_u = bl_spring[~bl_spring['has_version']]
  ```
If `merge_and_sync_all_datasets.py` overwrites the raw files, the classified files subsequently generated by `classify_global_dataset.py` or `merge_and_sync_all_datasets.py` lose `app_version`. `scripts/check_version_bias.py` then fails immediately with `KeyError: 'app_version'`.

---

## 4. Cross-Platform Interpreter Invocation Audit

In `scraped_data_global/pipeline/run_parallel_scrapers.py`:
- **Lines 21–25:**
  ```python
  PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
  PYTHON_BIN = PROJECT_ROOT / "dl" / ".venv" / "bin" / "python"
  if not PYTHON_BIN.exists():
      PYTHON_BIN = sys.executable
  ```

**Findings:**
1. On Windows environments, virtual environment executables reside in `Scripts\python.exe` rather than `bin/python`.
2. As a consequence, `(PROJECT_ROOT / "dl" / ".venv" / "bin" / "python").exists()` always evaluates to `False` on Windows hosts.
3. The fallback sets `PYTHON_BIN = sys.executable`. If dependencies like `google-play-scraper` are installed inside `dl/.venv` and the parent session runs a base Python interpreter, subprocess workers fail with `ModuleNotFoundError: No module named 'google_play_scraper'`.
4. Recommended cross-platform pattern:
   ```python
   def get_python_bin(project_root: Path) -> Path:
       venv_win = project_root / "dl" / ".venv" / "Scripts" / "python.exe"
       venv_posix = project_root / "dl" / ".venv" / "bin" / "python"
       if venv_win.exists():
           return venv_win
       if venv_posix.exists():
           return venv_posix
       return Path(sys.executable)
   ```

---

## 5. Scraping Query Parameters & Logic Audit

In `scraped_data_global/pipeline/scraper_worker.py`:
- **App IDs (Lines 28–47):**
  - Grameenphone: `com.portonics.mygp`
  - Banglalink: `com.arena.banglalinkmela.app`
  - Robi: `net.omobio.robisc`
- **Query Parameters (Lines 163–170):**
  - `country="us"`: Queries US Google Play storefront. Bangladeshi apps are listed globally, but regional storefront differences may influence localized reviews.
  - `lang="en"`: Explicit English language parameter. In practice, Google Play returns Latin-script English and Banglish, as well as Bengali Unicode text if submitted under the English UI language setting.
  - `sort=Sort.NEWEST`: Crawls from current time backwards towards `START_DATE = datetime(2014, 1, 1, 0, 0, 0)`.
  - `count=199`: Batch size per pagination request (maximum permitted by Google Play scraper API).
  - `continuation_token`: Pagination token. Loop breaks when `token is None` or cutoff date is reached.
- **Incremental Logic (Lines 198–201, 238–248):**
  - Inspects existing CSV, obtains `cutoff = df["review_date"].max()`.
  - Sets `effective_start = cutoff`.
  - Stops pagination when `rev_dt <= effective_start`.
  - Collects `new_rows`, deduplicates against `existing_ids`, and appends.

---

## 6. Progress Tracking & State Files

In `scraped_data_global/pipeline/scraper_worker.py`:
- **Lines 33, 39, 45:**
  - `progress_json` is mapped to `TARGET_DIR / "progress_{op}.json"`, pointing to `scraped_data_global/progress_{op}.json`.
- **Status on Disk:**
  - No `progress_*.json` files currently exist in `scraped_data_global/` or `scraped_data_global/raw/`.
  - The repository's `.gitignore` explicitly ignores `scraped_data_global/progress_*.json`:
    ```gitignore
    # Large progress/state files (scraper state)
    scraped_data_global/progress_*.json
    ```
  - This explains why progress files are absent in the working tree.

---

## 7. Audit Conclusion & Recommendations

1. **Keep Raw CSVs Read-Only:** Do not run `merge_and_sync_all_datasets.py` or `run_parallel_scrapers.py` without updating `FIELDNAMES` and output column projections to preserve all 12 columns.
2. **Harmonize Schema:** Update `FIELDNAMES` in `scraper_worker.py` to extract `appVersion`, `userImage`, `replyContent`, and `repliedAt`.
3. **Protect Line 272:** Replace `dedup[["review_id", ...]].to_csv(raw_out)` with full-column preservation (`dedup.to_csv(raw_out, index=False)`).
4. **Fix Path Resolution:** Adjust `run_parallel_scrapers.py` to check `Scripts/python.exe` on Windows.
