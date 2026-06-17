# Contributing to MigraAPI

We welcome contributions that improve the project, extend language support, or fix issues.

## How to contribute

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-idea`).
3. Make your changes.
4. Run the test suite: `python tests/test_migration.py`.
5. Commit with a clear message (Conventional Commits preferred).
6. Push and open a Pull Request against `main`.

## Development setup

No external dependencies required. Just Python 3.9+ and optionally Node.js for JavaScript testing.

## Adding a new language

1. Extend `migration-rules.json` with rules for the new language.
2. Add regex patterns in `regex-patterns.md`.
3. Update `scanner.py` (add language to `EXTENSION_MAP` and `PATTERNS`).
4. Update the `rewriter` subagent prompt if needed.
5. Add example files in `examples/before/` and `examples/after/`.
6. Ensure `test_migration.py` passes.

## Code style

- Python: follow PEP 8 (use `ruff` if available).
- Markdown: wrap at 80 characters.
- JSON/YAML: 2 spaces indentation.

## Reporting issues

Use GitHub Issues. Provide steps to reproduce, expected vs actual behavior, and any logs.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
