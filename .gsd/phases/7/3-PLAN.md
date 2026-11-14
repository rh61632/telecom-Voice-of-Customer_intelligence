---
phase: 7
plan: 3
wave: 3
depends_on: ["2"]
files_modified:
  - scripts/search_repo.sh
  - scripts/setup_search.sh
  - scripts/validate-agents.sh
  - scripts/validate-all.sh
  - scripts/validate-encoding.sh
  - scripts/validate-skills.sh
  - scripts/validate-templates.sh
  - scripts/validate-workflows.sh
  - scripts/validate-encoding.ps1
  - scripts/validate-workflows.ps1
  - scripts/validate-skills.ps1
  - scripts/validate-agents.ps1
  - scripts/validate-templates.ps1
autonomous: true
gap_closure: false

must_haves:
  truths:
    - "All 8 scripts/*.sh have pure Unix LF (\n) line endings, zero \r (CR) characters, and no UTF-8 BOM"
    - "scripts/validate-encoding.ps1 and scripts/validate-encoding.sh verify both *.ps1 (UTF-8 BOM requirement when non-ASCII) and *.sh (pure LF, no BOM, shebang header)"
    - "scripts/validate-{workflows,skills,agents,templates,encoding}.ps1 and scripts/validate-{workflows,skills,agents,templates,encoding}.sh are fully anchored to repo root via $PSScriptRoot / dirname $0 and run successfully from any working directory"
    - "scripts/validate-workflows.ps1 and scripts/validate-skills.ps1 extract YAML frontmatter via anchored regex \\A---\\r?\\n([\\s\\S]*?)\\r?\\n--- preventing false positives from markdown body text"
    - "scripts/validate-agents.ps1 preserves all existing registered tool names (view_file, write_to_file, etc.) while registering native Antigravity tools (read_file, write_file, edit_file, manage_task), and anchors skill path verification at line 93"
    - "scripts/validate-all.ps1 passes cleanly (exit code 0) when executed from repository root and when executed from a nested working directory"
  artifacts:
    - "8 remediated scripts/*.sh files with pure LF line endings and anchored directory resolution"
    - "5 remediated scripts/validate-*.ps1 files with $PSScriptRoot anchoring and anchored frontmatter parsing"
---

# Plan 7.3: Shell Endings & GSD Harness Validators Remediation

## Objective
Convert all 8 shell scripts (`scripts/*.sh`) from Windows CRLF to Unix LF line endings without UTF-8 BOM, anchor their directory lookups against the script location, and extend `validate-encoding.ps1` and `validate-encoding.sh` to enforce LF endings and no BOM on all `.sh` scripts. Anchor PowerShell harness validators (`validate-workflows.ps1`, `validate-skills.ps1`, `validate-agents.ps1`, `validate-templates.ps1`) using `$PSScriptRoot`, anchor their YAML frontmatter extraction regexes, preserve the active tool registry while registering native Antigravity tools in `validate-agents.ps1`, and verify that `scripts/validate-all.ps1` passes cleanly both from the repo root and from nested directories.

## Context
Load these files for context:
- `.gsd/SPEC.md`
- `.gsd/REQUIREMENTS.md` (`REM-05`)
- `.gsd/DECISIONS.md` (`ADR-002`, `ADR-003`)
- `.gsd/phases/7/RESEARCH.md`
- `scripts/validate-all.ps1`
- `scripts/validate-encoding.ps1`
- `scripts/validate-workflows.ps1`
- `scripts/validate-skills.ps1`
- `scripts/validate-agents.ps1`
- `scripts/validate-templates.ps1`
- `scripts/validate-all.sh`
- `scripts/validate-encoding.sh`

## Tasks

<task type="auto">
  <name>Convert scripts/*.sh to LF endings, anchor bash scripts & extend validate-encoding</name>
  <files>
    scripts/search_repo.sh
    scripts/setup_search.sh
    scripts/validate-agents.sh
    scripts/validate-all.sh
    scripts/validate-encoding.sh
    scripts/validate-skills.sh
    scripts/validate-templates.sh
    scripts/validate-workflows.sh
    scripts/validate-encoding.ps1
  </files>
  <action>
    1. Line Ending Conversion across all 8 `scripts/*.sh`:
       - `scripts/search_repo.sh`
       - `scripts/setup_search.sh`
       - `scripts/validate-agents.sh`
       - `scripts/validate-all.sh`
       - `scripts/validate-encoding.sh`
       - `scripts/validate-skills.sh`
       - `scripts/validate-templates.sh`
       - `scripts/validate-workflows.sh`
       - Read each file in binary, replace all `\r\n` (and lone `\r`) with `\n`, strip any UTF-8 BOM if present (`EF BB BF`), and write back as pure UTF-8 without BOM.
    2. Anchor Directory Lookups in Child `.sh` Validators:
       - In `validate-workflows.sh`: compute `script_dir="$(cd "$(dirname "$0")" && pwd)"`, `repo_root="$(dirname "$script_dir")"`, target `"$repo_root/.agent/workflows"/*.md`, and anchor `description:` check inside frontmatter block.
       - In `validate-skills.sh`: compute `script_dir` and `repo_root`, target `"$repo_root/.agents/skills"/*`, check `SKILL.md`, and anchor `name:`/`description:` checks inside frontmatter block.
       - In `validate-agents.sh`: compute `script_dir` and `repo_root`, target `"$repo_root/.agents/agents"/*.md`, anchor skill path verification against `"$repo_root/.agents"`, and register both existing tools and native tools (`read_file`, `write_file`, `edit_file`, `manage_task`).
       - In `validate-templates.sh`: compute `script_dir` and `repo_root`, target `"$repo_root/.gsd/templates"/*.md`.
       - In `validate-all.sh`: compute `script_dir="$(cd "$(dirname "$0")" && pwd)"` so calling it from any directory runs the child validators properly.
    3. Extend `scripts/validate-encoding.ps1`:
       - Retain existing `*.ps1` validation (requiring UTF-8 BOM if non-ASCII characters are present, plus `[System.Management.Automation.Language.Parser]::ParseFile` AST syntax check). Note: if writing `validate-encoding.ps1` with PowerShell, preserve its UTF-8 BOM (`[System.Text.UTF8Encoding]::new($true)`).
       - Add verification for all `*.sh` files in `$PSScriptRoot`:
         - Read file bytes via `[System.IO.File]::ReadAllBytes($file.FullName)`.
         - Increment `$ScriptsChecked`.
         - Assert NO `\r` (byte `0x0D` / 13) exists: if byte 13 is found, report error `"CRLF line endings detected in shell script (must be LF)"`.
         - Assert NO UTF-8 BOM exists: if `bytes[0..2]` match `0xEF, 0xBB, 0xBF`, report error `"UTF-8 BOM detected in shell script (must be UTF-8 without BOM)"`.
         - Assert shebang exists: verify first two characters are `#!`.
    4. Extend `scripts/validate-encoding.sh`:
       - Retain existing `*.ps1` BOM checks for non-ASCII files.
       - Add scan for `*.sh` files: assert `grep -q $'\r'` returns non-zero (no CR), assert BOM is not present, and assert shebang starts with `#!`.
       - Ensure `validate-encoding.sh` itself is saved with pure LF and no BOM.

    AVOID: Leaving any `\r` character in any `.sh` file.
    AVOID: Stripping the UTF-8 BOM from `.ps1` files containing Unicode symbols.
    USE: Binary byte inspection to guarantee zero carriage returns in shell scripts.
  </action>
  <verify>
    powershell -ExecutionPolicy Bypass -Command "$shFiles = Get-ChildItem scripts -Filter '*.sh'; foreach ($f in $shFiles) { $bytes = [System.IO.File]::ReadAllBytes($f.FullName); if ($bytes -contains 13) { throw '$($f.Name) contains CR' }; if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) { throw '$($f.Name) has BOM' }; if ($bytes[0] -ne 0x23 -or $bytes[1] -ne 0x21) { throw '$($f.Name) missing shebang' } }; powershell -ExecutionPolicy Bypass -File scripts/validate-encoding.ps1; if ($LASTEXITCODE -ne 0) { throw 'validate-encoding failed' }; Write-Host '✓ Shell endings and validate-encoding verified!'"
  </verify>
  <done>
    All 8 scripts/*.sh have pure LF endings, no BOM, and valid shebangs; validate-encoding.ps1 and validate-encoding.sh verify both PowerShell and shell script encodings.
  </done>
</task>

<task type="auto">
  <name>Anchor scripts/validate-*.ps1 and verify validate-all.ps1 from root and nested paths</name>
  <files>
    scripts/validate-workflows.ps1
    scripts/validate-skills.ps1
    scripts/validate-agents.ps1
    scripts/validate-templates.ps1
  </files>
  <action>
    1. Update `scripts/validate-workflows.ps1`:
       - Anchor directory to repo root:
         `$repoRoot = Split-Path -Parent $PSScriptRoot`
         `$workflowsDir = Join-Path $repoRoot ".agent/workflows"`
         `if (-not (Test-Path $workflowsDir)) { Write-Host "❌ Missing $workflowsDir directory" -ForegroundColor Red; exit 1 }`
         `$workflows = Get-ChildItem $workflowsDir -Filter "*.md" -File`
       - Anchor frontmatter regex:
         `if ($content -match "\A---\r?\n([\s\S]*?)\r?\n---") {`
         `    $fm = $Matches[1]`
         `    if ($fm -notmatch "(?m)^description:\s*\S+") { ... }`
         `} else { ... missing frontmatter ... }`
       - Preserve UTF-8 BOM on write.
    2. Update `scripts/validate-skills.ps1`:
       - Anchor directory to repo root:
         `$repoRoot = Split-Path -Parent $PSScriptRoot`
         `$skillsDir = Join-Path $repoRoot ".agents/skills"`
         `if (-not (Test-Path $skillsDir)) { Write-Host "❌ Missing $skillsDir directory" -ForegroundColor Red; exit 1 }`
         `$skills = Get-ChildItem $skillsDir -Directory`
       - Anchor frontmatter regex checking `(?m)^name:\s*\S+` and `(?m)^description:\s*\S+` inside `$Matches[1]`.
       - Preserve UTF-8 BOM on write.
    3. Update `scripts/validate-agents.ps1`:
       - Anchor directory to repo root:
         `$repoRoot = Split-Path -Parent $PSScriptRoot`
         `$agentsDir = Join-Path $repoRoot ".agents/agents"`
         `if (-not (Test-Path $agentsDir)) { Write-Host "❌ Missing $agentsDir directory" -ForegroundColor Red; exit 1 }`
         `$agents = Get-ChildItem $agentsDir -Filter "*.md" -File`
       - Anchor frontmatter regex (`\A---\r?\n([\s\S]*?)\r?\n---`) before testing `name:`, `description:`, `subagent:`.
       - In `$knownTools`: retain all existing tools (`view_file`, `write_to_file`, `replace_file_content`, `multi_replace_file_content`, `list_dir`, `find_by_name`, `grep_search`, `search_web`, `read_url_content`, `run_command`, `manage_task`, `schedule`, `list_permissions`, `ask_permission`, `invoke_subagent`, `define_subagent`, `send_message`, `manage_subagents`, `ask_question`, `generate_image`) AND append native Antigravity tools: `"read_file"`, `"write_file"`, `"edit_file"`.
       - Anchor line 93 skill reference path:
         `$skillPath = Join-Path (Join-Path $repoRoot ".agents") (Join-Path $ref.Groups[1].Value "SKILL.md")`
       - Preserve UTF-8 BOM on write.
    4. Update `scripts/validate-templates.ps1`:
       - Anchor directory to repo root:
         `$repoRoot = Split-Path -Parent $PSScriptRoot`
         `$templatesDir = Join-Path $repoRoot ".gsd/templates"`
         `if (-not (Test-Path $templatesDir)) { Write-Host "❌ Missing $templatesDir directory" -ForegroundColor Red; exit 1 }`
         `$templates = Get-ChildItem $templatesDir -Filter "*.md" -File`
       - Preserve UTF-8 BOM on write.
    5. Empirically verify that `scripts/validate-all.ps1` runs and passes with exit code 0 when invoked:
       - From repo root: `powershell -ExecutionPolicy Bypass -File scripts/validate-all.ps1`
       - From `scripts/` directory: `powershell -ExecutionPolicy Bypass -Command "Set-Location scripts; .\validate-all.ps1"`

    AVOID: Deleting `view_file` or `write_to_file` from `$knownTools` in `validate-agents.ps1`.
    AVOID: Stripping UTF-8 BOM from `.ps1` files containing Unicode symbols.
    USE: `$repoRoot = Split-Path -Parent $PSScriptRoot` across all child validator scripts.
  </action>
  <verify>
    powershell -ExecutionPolicy Bypass -Command "$r1 = powershell -ExecutionPolicy Bypass -File scripts/validate-all.ps1; if ($LASTEXITCODE -ne 0) { throw 'Root validation failed' }; Set-Location scripts; $r2 = powershell -ExecutionPolicy Bypass -File ./validate-all.ps1; Set-Location ..; if ($LASTEXITCODE -ne 0) { throw 'Nested validation failed' }; Write-Host '✓ validate-all.ps1 passed from both repo root and nested directory!'"
  </verify>
  <done>
    scripts/validate-*.ps1 files are anchored to $PSScriptRoot with anchored frontmatter parsing; validate-agents.ps1 retains full tool registry; validate-all.ps1 passes cleanly from both root and nested paths.
  </done>
</task>

## Must-Haves
After all tasks complete, verify:
- [ ] All 8 `scripts/*.sh` have pure LF line endings, zero CR bytes, and no UTF-8 BOM
- [ ] `scripts/validate-encoding.ps1` checks both `.ps1` and `.sh` files and passes cleanly
- [ ] `scripts/validate-workflows.ps1`, `validate-skills.ps1`, `validate-agents.ps1`, and `validate-templates.ps1` use `$PSScriptRoot` anchoring and anchored frontmatter parsing
- [ ] `scripts/validate-agents.ps1` preserves existing tool names and registers native tools
- [ ] `scripts/validate-all.ps1` passes with 0 errors from repo root and from nested directory

## Success Criteria
- [ ] All tasks verified passing
- [ ] Must-haves confirmed
- [ ] No regressions in tests
