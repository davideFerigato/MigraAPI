# Orchestration Example with the `Task` Tool (Claude Code)

When using MigraAPI with Claude Code, the orchestrator (main agent) executes a sequence similar to this:

## 1. Skill activation

User writes:
```
Migrate the code in examples/before from the old API to the new API.
```

Claude detects the `api-migration` skill (via `name`/`description`) and loads the full `SKILL.md`.

## 2. Orchestration with `Task`

Claude (orchestrator) generates commands like:

```
Task(subagent="scanner", prompt="Analyze examples/before/sample.py using patterns: old_api\.get_user, old_api\.fetch_posts. Return JSON.")
```

Receives JSON output:
```json
{
  "status": "success",
  "file": "examples/before/sample.py",
  "occurrences": [
    {"line": 2, "code": "from old_api import Client", "pattern": "import old_api"},
    {"line": 4, "code": "user = client.get_user(user_id=123)", "pattern": "old_api.get_user"}
  ]
}
```

## 3. Parallel execution

For multiple files, Claude can launch several `Task` calls concurrently:

```
Task(subagent="scanner", prompt="Analyze file1.py...")
Task(subagent="scanner", prompt="Analyze file2.py...")
```

It waits for all results.

## 4. Rewriting

For each scanner result, Claude invokes the rewriter:

```
Task(subagent="rewriter", prompt="Apply the following transformations to examples/before/sample.py: [mapping JSON]. Use the found occurrences: {...}")
```

## 5. Validation

After rewriting, Claude calls the validator on each modified file:

```
Task(subagent="validator", prompt="Validate examples/before/sample.py (Python language). Run syntax check.")
```

## 6. Final synthesis

Claude collects all JSON results and produces a summary report for the user.

---

**Note**: This flow is automatic when you use the skill. You don't need to write `Task` commands manually; Claude generates them based on the skill's instructions.
