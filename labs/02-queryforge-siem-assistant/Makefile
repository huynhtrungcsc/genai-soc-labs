.PHONY: install dev test lint seed clean

install:
	python -m pip install -e ".[dev]"

dev:
	uvicorn app.main:app --app-dir backend --reload --host 0.0.0.0 --port 8002

test:
	pytest

lint:
	ruff check backend tests

seed:
	PYTHONPATH=backend python scripts/load_sample.py

clean:
	rm -rf .pytest_cache .ruff_cache data
