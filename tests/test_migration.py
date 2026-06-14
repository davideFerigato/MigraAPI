#!/usr/bin/env python3
"""
Test migration rules against expected after files.
Usage: python tests/test_migration.py
"""

import json
import re
import sys
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
RULES_FILE = PROJECT_ROOT / ".claude/skills/api-migration/migration-rules.json"
BEFORE_DIR = PROJECT_ROOT / "examples/before"
AFTER_DIR = PROJECT_ROOT / "examples/after"

def load_rules():
    with open(RULES_FILE, "r") as f:
        data = json.load(f)
    return data["rules"]

def apply_migration(content, language, rules):
    """Apply migration rules to content for given language."""
    lang_rules = [r for r in rules if r["language"] == language]
    # Sort rules by length descending to avoid partial replacements
    lang_rules.sort(key=lambda x: -len(x["old"]))
    
    for rule in lang_rules:
        old = rule["old"]
        new = rule["new"]
        # Escape old string for regex (simple string replacement, but handle dots)
        # We use re.escape to be safe, but old patterns may have dots -> we want literal dot
        # Actually old can be e.g. "old_api.get_user" -> dot is literal
        pattern = re.escape(old)
        content = re.sub(pattern, new, content)
    return content

def test_file(before_path, after_path, rules):
    lang = "python" if before_path.suffix == ".py" else "javascript"
    with open(before_path, "r", encoding="utf-8") as f:
        before_content = f.read()
    migrated = apply_migration(before_content, lang, rules)
    
    with open(after_path, "r", encoding="utf-8") as f:
        expected = f.read()
    
    if migrated != expected:
        print(f"❌ Test failed for {before_path.name}")
        print("--- Migrated ---")
        print(migrated)
        print("--- Expected ---")
        print(expected)
        # Simple diff line by line
        migrated_lines = migrated.splitlines()
        expected_lines = expected.splitlines()
        for i, (ml, el) in enumerate(zip(migrated_lines, expected_lines)):
            if ml != el:
                print(f"First diff at line {i+1}:")
                print(f"  Migrated: {ml}")
                print(f"  Expected: {el}")
                break
        return False
    else:
        print(f"✅ {before_path.name} matches after migration")
        return True

def main():
    rules = load_rules()
    success = True
    for before_file in BEFORE_DIR.glob("*"):
        if before_file.is_file():
            after_file = AFTER_DIR / before_file.name
            if not after_file.exists():
                print(f"⚠️ No after file for {before_file.name}, skipping")
                continue
            if not test_file(before_file, after_file, rules):
                success = False
    if success:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
