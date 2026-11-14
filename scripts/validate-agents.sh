#!/bin/bash
# GSD Subagent Validation Script
# Validates all subagent definitions in .agents/agents/

error_count=0
agents_checked=0

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " GSD ► VALIDATING SUBAGENTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

script_dir="$(cd "$(dirname "$0")" && pwd)"
repo_root="$(dirname "$script_dir")"
agents_dir="$repo_root/.agents/agents"

if [ ! -d "$agents_dir" ]; then
    echo "❌ Missing $agents_dir directory"
    exit 1
fi

for agent_file in "$agents_dir"/*.md; do
    [ -e "$agent_file" ] || continue
    ((agents_checked++))
    agent_name=$(basename "$agent_file" .md)
    has_errors=false

    # Check for frontmatter
    if ! head -1 "$agent_file" | grep -q "^---"; then
        echo "❌ $agent_name: Missing frontmatter"
        ((error_count++))
        has_errors=true
    else
        fm=$(awk 'NR==1 && /^---$/ {found=1; next} found && /^---$/ {exit} found {print}' "$agent_file")

        # Check required fields
        for field in "name" "description" "subagent"; do
            if ! echo "$fm" | grep -q "^$field:"; then
                echo "❌ $agent_name: Missing $field in frontmatter"
                ((error_count++))
                has_errors=true
            fi
        done

        # name must match filename (invoke_subagent targets the name field)
        declared_name=$(echo "$fm" | grep "^name:" | head -1 | sed 's/^name:[[:space:]]*//')
        if [ -n "$declared_name" ] && [ "$declared_name" != "$agent_name" ]; then
            echo "❌ $agent_name: name '$declared_name' does not match filename"
            ((error_count++))
            has_errors=true
        fi

        # subagent must be true
        if ! echo "$fm" | grep -q "^subagent:[[:space:]]*true"; then
            echo "❌ $agent_name: subagent must be true"
            ((error_count++))
            has_errors=true
        fi

        # Known Antigravity tool registry (antigravity.google/docs/hooks)
        # An unmapped or misspelled tool name makes the subagent hang, so this is an error.
        known_tools="view_file write_to_file replace_file_content multi_replace_file_content list_dir find_by_name grep_search search_web read_url_content run_command manage_task schedule list_permissions ask_permission invoke_subagent define_subagent send_message manage_subagents ask_question generate_image read_file write_file edit_file"

        # tools: must be declared — the field defaults to an empty list, it does NOT inherit
        tool_list=$(echo "$fm" | awk '/^tools:/{flag=1;next} /^[a-zA-Z]/{flag=0} flag && /^[[:space:]]*-/{gsub(/^[[:space:]]*-[[:space:]]*/,"");print}')

        if [ -z "$tool_list" ]; then
            echo "❌ $agent_name: No tools declared (tools: defaults to empty, it does not inherit)"
            ((error_count++))
            has_errors=true
        else
            for tool in $tool_list; do
                case " $known_tools " in
                    *" $tool "*) ;;
                    browser_*|*" browser_"*) ;;
                    *)
                        if [ "${tool#browser_}" = "$tool" ]; then
                            echo "❌ $agent_name: Unknown tool '$tool' (typos make subagents hang)"
                            ((error_count++))
                            has_errors=true
                        fi
                        ;;
                esac
            done
        fi

        # Referenced skills must exist
        while read -r skill_ref; do
            [ -n "$skill_ref" ] || continue
            skill_path="$repo_root/.agents/$skill_ref/SKILL.md"
            if [ ! -f "$skill_path" ]; then
                echo "❌ $agent_name: References missing skill '$skill_ref'"
                ((error_count++))
                has_errors=true
            fi
        done < <(echo "$fm" | grep -oE "^[[:space:]]+- skills/[a-z0-9-]+" | sed 's/^[[:space:]]*-[[:space:]]*//')
    fi

    # Return Contract keeps orchestrator context lean
    if ! grep -q "Return Contract" "$agent_file"; then
        echo "⚠️  $agent_name: Missing Return Contract section"
    fi

    if [ "$has_errors" = false ]; then
        echo "✅ $agent_name"
    fi
done

echo ""
echo "───────────────────────────────────────────────────────"
echo ""
echo "Subagents checked: $agents_checked"
echo "Errors: $error_count"
echo ""

if [ $error_count -eq 0 ]; then
    echo "✅ All subagents valid!"
    exit 0
else
    echo "❌ Validation failed"
    exit 1
fi
