#!/bin/bash
# GSD Skill Validation Script
# Validates all skill directories for required structure

error_count=0
skills_checked=0

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " GSD ► VALIDATING SKILLS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

script_dir="$(cd "$(dirname "$0")" && pwd)"
repo_root="$(dirname "$script_dir")"
skills_dir="$repo_root/.agents/skills"

if [ ! -d "$skills_dir" ]; then
    echo "❌ Missing $skills_dir directory"
    exit 1
fi

for skill_dir in "$skills_dir"/*/; do
    [ -d "$skill_dir" ] || continue
    ((skills_checked++))
    skill_name=$(basename "$skill_dir")
    skill_file="$skill_dir/SKILL.md"
    has_errors=false
    
    # Check SKILL.md exists
    if [ ! -f "$skill_file" ]; then
        echo "❌ $skill_name: Missing SKILL.md"
        ((error_count++))
        continue
    fi
    
    # Check for frontmatter
    if ! head -1 "$skill_file" | grep -q "^---"; then
        echo "❌ $skill_name: Missing frontmatter"
        ((error_count++))
        has_errors=true
    else
        fm=$(awk 'NR==1 && /^---$/ {found=1; next} found && /^---$/ {exit} found {print}' "$skill_file")
        if ! echo "$fm" | grep -q "^name:"; then
            echo "❌ $skill_name: Missing name in frontmatter"
            ((error_count++))
            has_errors=true
        fi
        if ! echo "$fm" | grep -q "^description:"; then
            echo "❌ $skill_name: Missing description in frontmatter"
            ((error_count++))
            has_errors=true
        fi
    fi
    
    if [ "$has_errors" = false ]; then
        echo "✅ $skill_name"
    fi
done

echo ""
echo "───────────────────────────────────────────────────────"
echo ""
echo "Skills checked: $skills_checked"
echo "Errors: $error_count"
echo ""

if [ $error_count -eq 0 ]; then
    echo "✅ All skills valid!"
    exit 0
else
    echo "❌ Validation failed"
    exit 1
fi
