# GSD Script Encoding Validation
# Parses every PowerShell script and checks shell script encoding to catch faults before users hit them.
#
# Windows PowerShell 5.1 reads .ps1 files as the system ANSI codepage unless a
# UTF-8 BOM is present. A script with non-ASCII characters and no BOM fails to
# parse entirely — the failure looks like a syntax error, not an encoding one.
#
# Unix shells fail or misbehave if .sh files contain CRLF line endings or a UTF-8 BOM.

$ErrorCount = 0
$ScriptsChecked = 0

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host " GSD ► VALIDATING SCRIPT ENCODING" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

$psScripts = Get-ChildItem $PSScriptRoot -Filter "*.ps1" -File | Sort-Object Name

foreach ($script in $psScripts) {
    $ScriptsChecked++
    $hasErrors = $false

    # Does the file carry a UTF-8 BOM?
    $bytes = [System.IO.File]::ReadAllBytes($script.FullName)
    $hasBom = $bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF

    # Does it contain non-ASCII characters?
    $hasNonAscii = $false
    foreach ($byte in $bytes) {
        if ($byte -gt 127) { $hasNonAscii = $true; break }
    }

    if ($hasNonAscii -and -not $hasBom) {
        Write-Host "❌ $($script.Name): non-ASCII characters without a UTF-8 BOM" -ForegroundColor Red
        $ErrorCount++
        $hasErrors = $true
    }

    # Parse it the way PowerShell would, without executing anything
    $parseErrors = $null
    [System.Management.Automation.Language.Parser]::ParseFile(
        $script.FullName, [ref]$null, [ref]$parseErrors) | Out-Null

    if ($parseErrors -and $parseErrors.Count -gt 0) {
        $first = $parseErrors[0]
        Write-Host "❌ $($script.Name): parse error at line $($first.Extent.StartLineNumber) — $($first.Message)" -ForegroundColor Red
        $ErrorCount++
        $hasErrors = $true
    }

    if (-not $hasErrors) {
        Write-Host "✅ $($script.Name)" -ForegroundColor Green
    }
}

$shScripts = Get-ChildItem $PSScriptRoot -Filter "*.sh" -File | Sort-Object Name

foreach ($script in $shScripts) {
    $ScriptsChecked++
    $hasErrors = $false

    $bytes = [System.IO.File]::ReadAllBytes($script.FullName)

    # Assert NO \r (byte 0x0D / 13) exists
    if ($bytes -contains 13) {
        Write-Host "❌ $($script.Name): CRLF line endings detected in shell script (must be LF)" -ForegroundColor Red
        $hasErrors = $true
    }

    # Assert NO UTF-8 BOM exists
    $hasBom = $bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF
    if ($hasBom) {
        Write-Host "❌ $($script.Name): UTF-8 BOM detected in shell script (must be UTF-8 without BOM)" -ForegroundColor Red
        $hasErrors = $true
    }

    # Assert shebang exists: first two characters are #!
    if ($bytes.Length -lt 2 -or $bytes[0] -ne 0x23 -or $bytes[1] -ne 0x21) {
        Write-Host "❌ $($script.Name): missing shebang header (must start with #!)" -ForegroundColor Red
        $hasErrors = $true
    }

    if ($hasErrors) {
        $ErrorCount++
    } else {
        Write-Host "✅ $($script.Name)" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "───────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host ""
Write-Host "Scripts checked: $ScriptsChecked"
Write-Host "Errors: $ErrorCount" -ForegroundColor $(if ($ErrorCount -gt 0) { "Red" } else { "Green" })
Write-Host ""

if ($ErrorCount -eq 0) {
    Write-Host "✅ All scripts parse cleanly and adhere to encoding standards!" -ForegroundColor Green
    exit 0
} else {
    Write-Host "❌ Validation failed" -ForegroundColor Red
    exit 1
}
