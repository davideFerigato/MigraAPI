#!/bin/bash
# MigraAPI - Demo Orchestrator Script
# Simulates the orchestration pattern: scan -> rewrite -> validate -> report
# Uses the scanner.py and mapping rules from the skill.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCANNER_SCRIPT="$SCRIPT_DIR/.claude/skills/api-migration/scripts/scanner.py"
MAPPING_FILE="$SCRIPT_DIR/.claude/skills/api-migration/migration-rules.json"
SOURCE_DIR="$SCRIPT_DIR/examples/before"
REPORT_FILE="$SCRIPT_DIR/migration_report.json"

echo "🚀 MigraAPI - Orchestration Demo"
echo "================================"
echo "Phase 1: Scanning files in $SOURCE_DIR"

# Check if scanner exists
if [ ! -f "$SCANNER_SCRIPT" ]; then
    echo "❌ Scanner script not found at $SCANNER_SCRIPT"
    exit 1
fi

# Run scanner on all files (simulated parallel via background jobs)
scan_results=()
for file in "$SOURCE_DIR"/*; do
    if [ -f "$file" ]; then
        echo "  Scanning $(basename "$file")..."
        # Run scanner in background (parallel)
        python3 "$SCANNER_SCRIPT" "$file" > "/tmp/scan_$(basename "$file").json" 2>/dev/null &
        scan_pids[$!]="$file"
    fi
done

# Wait for all scanners to finish
for pid in "${!scan_pids[@]}"; do
    wait "$pid"
    file="${scan_pids[$pid]}"
    result_file="/tmp/scan_$(basename "$file").json"
    if [ -s "$result_file" ]; then
        echo "  ✅ Scanned $(basename "$file")"
        scan_results+=("$result_file")
    else
        echo "  ⚠️ No occurrences or error in $(basename "$file")"
    fi
done

# Simulate rewriting (in real Claude Code, this would call rewriter subagent)
echo ""
echo "Phase 2: Rewriting files (simulated)"
for result_file in "${scan_results[@]}"; do
    # Extract filename from result file
    base=$(basename "$result_file" .json)
    # Here we would invoke the rewriter subagent with the occurrences
    # For demo, we just count occurrences
    occurrences=$(jq '.files[0].occurrences | length' "$result_file" 2>/dev/null || echo "0")
    echo "  ✏️ $base: $occurrences deprecated calls found (would rewrite)"
done

# Simulate validation
echo ""
echo "Phase 3: Validation (simulated)"
for file in "$SOURCE_DIR"/*; do
    if [ -f "$file" ]; then
        # In real scenario, call validator subagent
        echo "  🔍 Validating $(basename "$file")... syntax OK (simulated)"
    fi
done

# Generate final report
echo ""
echo "Phase 4: Generating final report"
cat > "$REPORT_FILE" << JSON_REPORT
{
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "source_directory": "$SOURCE_DIR",
  "files_scanned": $(find "$SOURCE_DIR" -type f | wc -l),
  "files_with_occurrences": ${#scan_results[@]},
  "status": "demo_success",
  "message": "This is a simulation. In real Claude Code execution, the orchestrator would call the scanner/rewriter/validator subagents using the Task tool."
}
JSON_REPORT

echo "✅ Report saved to $REPORT_FILE"
echo "================================"
echo "Demo completed. To see the real orchestration with Claude Code, run:"
echo "  claude"
echo "  then ask: 'Migrate the code in examples/before using the api-migration skill'"
