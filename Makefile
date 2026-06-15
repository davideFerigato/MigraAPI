.PHONY: test demo clean

test:
	python tests/test_migration.py

demo:
	./demo-script.sh

clean:
	rm -f migration_report.json output.txt
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name ".DS_Store" -delete
