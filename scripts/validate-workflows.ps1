# GSD Workflow Validation Script
# Validates all workflow files for required structure

$ErrorCount = 0
$WarningCount = 0
$WorkflowsChecked = 0

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host " GSD ► VALIDATING WORKFLOWS" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

$repoRoot = Split-Path -Parent $PSScriptRoot
$workflowsDir = Join-Path $repoRoot ".agent/workflows"

if (-not (Test-Path $workflowsDir)) {
    Write-Host "❌ Missing $workflowsDir directory" -ForegroundColor Red
    exit 1
}

$workflows = Get-ChildItem $workflowsDir -Filter "*.md" -File

foreach ($file in $workflows) {
    $WorkflowsChecked++
    $content = Get-Content $file.FullName -Raw
    $hasErrors = $false

    # Check for anchored frontmatter
    if ($content -match "\A---\r?\n([\s\S]*?)\r?\n---") {
        $fm = $Matches[1]
        # Check for description
        if ($fm -notmatch "(?m)^description:\s*\S+") {
            Write-Host "❌ $($file.Name): Missing description in frontmatter" -ForegroundColor Red
            $ErrorCount++
            $hasErrors = $true
        }
    } else {
        Write-Host "❌ $($file.Name): Missing frontmatter" -ForegroundColor Red
        $ErrorCount++
        $hasErrors = $true
    }

    # Check for process tags (optional but recommended)
    if ($content -notmatch "<process>") {
        Write-Host "⚠️  $($file.Name): Missing <process> tag" -ForegroundColor Yellow
        $WarningCount++
    }

    if (-not $hasErrors) {
        Write-Host "✅ $($file.Name)" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "───────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host ""
Write-Host "Workflows checked: $WorkflowsChecked"
Write-Host "Errors: $ErrorCount" -ForegroundColor $(if ($ErrorCount -gt 0) { "Red" } else { "Green" })
Write-Host "Warnings: $WarningCount" -ForegroundColor $(if ($WarningCount -gt 0) { "Yellow" } else { "Green" })
Write-Host ""

if ($ErrorCount -eq 0) {
    Write-Host "✅ All workflows valid!" -ForegroundColor Green
    exit 0
} else {
    Write-Host "❌ Validation failed" -ForegroundColor Red
    exit 1
}
