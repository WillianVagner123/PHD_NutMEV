.PHONY: test lint check

test:
	python -m pytest tests

lint:
	ruff check .

check: test
