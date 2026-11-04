# Archived Robi Historical Backfill Artifacts

This folder contains the historical, one-time backfill script and isolated raw slice created on October 8, 2026:
- `backfill_robi_gap.py`: Script originally written to target and fill an artificial 10-month historical gap (Sep 2024 to Aug 2025) caused by an interrupted file concatenation in an early scrape run.
- `robi_backfilled_gap_2024_2025.csv`: The isolated slice of ~37.1k reviews retrieved during that run.

### Status & Deprecation
These artifacts are preserved here solely for auditability and historical provenance. 
Empirical verification confirms that the production general scraper (`scraper_worker.py` / `run_parallel_scrapers.py`) traverses all years and months continuously without requiring any secondary backfill. All reviews in this slice are already permanently incorporated into the primary raw and classified datasets.

