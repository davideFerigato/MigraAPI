# Tests for MigraAPI

This test suite validates that the migration rules defined in `migration-rules.json` correctly transform the `before` examples into the `after` examples.

## Run the test

```bash
python tests/test_migration.py
```

The test applies the same string substitution rules that the `rewriter` subagent would use. If the migrated content matches the expected `after` files, the test passes.

## What to do when test fails

- Check that `migration-rules.json` contains the correct old→new mappings.
- Verify that the `after` files represent the desired final state.
- Run the test after any change to rules or examples.

Note: This is a simulation test. In a real Claude Code environment, the `validator` subagent would perform similar checks.
