.PHONY: help test demo clean lint

help:
	@echo "Available targets:"
	@echo "  test   - Run migration tests (python tests/test_migration.py)"
	@echo "  demo   - Run orchestration demo script (./demo-script.sh)"
	@echo "  clean  - Remove temporary files (migration_report.json, .DS_Store, __pycache__)"
	@echo "  lint   - Run pre-commit hooks manually (if pre-commit installed)"

test:
	python tests/test_migration.py

demo:
	./demo-script.sh

clean:
	rm -f migration_report.json output.txt
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name ".DS_Store" -delete

lint:
	@echo "Install pre-commit first: pip install pre-commit && pre-commit install"
	pre-commit run --all-files || true
