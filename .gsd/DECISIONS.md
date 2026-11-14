# DECISIONS.md — Architecture & Audit/Remediation Decisions

## ADR-001: Read-Only Audit & No-Git-Commit Policy *(Superseded for v2.0.0 by ADR-003)*
- **Date:** 2026-11-11
- **Status:** Superseded by `ADR-003` (applied cleanly across Milestone v1.0.0 Phases 1–4)
- **Context:** Milestone v1.0.0 required a read-only diagnostic audit without modifying project or paper files.

## ADR-002: Sequential `inherit` Workspace Execution
- **Date:** 2026-11-11
- **Status:** Accepted (Active across v1.0.0 and v2.0.0)
- **Context:** `.gsd/` and uncommitted working-tree artifacts exist in the parent working tree and would be invisible in fresh `HEAD`-based git worktrees (`branch`/`share`).
- **Decision:** Run all GSD subagents sequentially with `workspace: inherit` (one active writer at a time) so every agent reads/writes directly against the live workspace.

## ADR-003: Milestone v2.0.0 Remediation Execution & Staged Review Policy
- **Date:** 2026-11-11
- **Status:** Accepted (Active for Milestone v2.0.0)
- **Context:** The user instructed `"fix them"` following the v1.0.0 discrepancy audit (`55` cataloged findings in `.gsd/DISCREPANCY_REPORT.md`).
- **Decision:**
  1. Authorize modifications to project code, configs, reports, plots, verification scripts, and `paper/` LaTeX/PDF/HTML/XLSX deliverables to resolve all 55 cataloged discrepancies empirically.
  2. **Empirical Truth Mandate:** Never invent, fabricate, or copy unverified numbers. Every statistic in code, reports, tables, figures, and manuscripts must come directly from executed scripts on live datasets (`N=661,160`, `N=655,649`, `N=4,500`, active Gold `N=300` / `N=200`). Any ungrounded external claim (`28% ARPU`, `3.5x–5.0x SAC`) without repo evidence must be removed or explicitly scoped/reframed without fabricated statistics.
  3. **Human Annotation & Weight Preservation:** Never fabricate or overwrite human ground-truth labels in `data/gold_set/blind_annotation_*.csv` or alter model `.safetensors` weights. Fix config/code mismatches to match true trained weights and true dataset rows.
  4. **No Unsolicited Git Commits:** Leave git commits to the user after completion so `git status` and `git diff` cleanly expose every remediation edit for review; `gsd-executor` verifies task persistence via empirical `<verify>` outputs, file checksums, and `.gsd/phases/{N}/SUMMARY.md`.
