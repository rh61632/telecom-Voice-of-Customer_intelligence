#!/bin/bash
# GSD Script Encoding Validation
# Checks that:
# 1. Every PowerShell script (.ps1) with non-ASCII characters carries a UTF-8 BOM.
# 2. Every shell script (.sh) has pure LF line endings, no UTF-8 BOM, and a shebang header.
#
# Windows PowerShell 5.1 reads .ps1 files as the system ANSI codepage unless a
# UTF-8 BOM is present. A script with non-ASCII characters and no BOM fails to
# parse entirely — the failure looks like a syntax error, not an encoding one.
#
# Unix shells fail or misbehave if .sh files contain CRLF line endings or a UTF-8 BOM.
#
# The PowerShell counterpart (validate-encoding.ps1) additionally parses each
# script. Run it on Windows for the stronger check.

error_count=0
scripts_checked=0

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " GSD ► VALIDATING SCRIPT ENCODING"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

script_dir="$(cd "$(dirname "$0")" && pwd)"

# 1. Check PowerShell scripts (.ps1)
for file in "$script_dir"/*.ps1; do
    [ -e "$file" ] || continue
    ((scripts_checked++))
    filename=$(basename "$file")

    # Count bytes outside the ASCII range
    non_ascii=$(LC_ALL=C tr -d '\000-\177' < "$file" | wc -c)

    # Detect a UTF-8 BOM (EF BB BF)
    bom=$(LC_ALL=C head -c 3 "$file" | od -An -tx1 | tr -d ' \n')

    if [ "$non_ascii" -gt 0 ] && [ "$bom" != "efbbbf" ]; then
        echo "❌ $filename: non-ASCII characters without a UTF-8 BOM"
        ((error_count++))
    else
        echo "✅ $filename"
    fi
done

# 2. Check Shell scripts (.sh)
for file in "$script_dir"/*.sh; do
    [ -e "$file" ] || continue
    ((scripts_checked++))
    filename=$(basename "$file")
    has_errors=false

    # Check for CRLF / carriage return
    if LC_ALL=C grep -q $'\r' "$file"; then
        echo "❌ $filename: CRLF line endings detected in shell script (must be LF)"
        has_errors=true
    fi

    # Check for UTF-8 BOM
    bom=$(LC_ALL=C head -c 3 "$file" | od -An -tx1 | tr -d ' \n')
    if [ "$bom" = "efbbbf" ]; then
        echo "❌ $filename: UTF-8 BOM detected in shell script (must be UTF-8 without BOM)"
        has_errors=true
    fi

    # Check for shebang header
    shebang=$(LC_ALL=C head -c 2 "$file")
    if [ "$shebang" != "#!" ]; then
        echo "❌ $filename: missing shebang header (must start with #!)"
        has_errors=true
    fi

    if [ "$has_errors" = true ]; then
        ((error_count++))
    else
        echo "✅ $filename"
    fi
done

echo ""
echo "───────────────────────────────────────────────────────"
echo ""
echo "Scripts checked: $scripts_checked"
echo "Errors: $error_count"
echo ""

if [ $error_count -eq 0 ]; then
    echo "✅ All scripts correctly encoded!"
    exit 0
else
    echo "❌ Validation failed"
    exit 1
fi
