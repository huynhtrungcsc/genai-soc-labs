.PHONY: install dev test lint seed smoke clean

install:
	python -m pip install -e ".[dev]"

dev:
	uvicorn app.main:app --app-dir backend --reload --host 0.0.0.0 --port 8003

test:
	pytest

lint:
	ruff check backend tests

seed:
	PYTHONPATH=backend python scripts/load_sample.py

smoke:
	PYTHONPATH=backend python scripts/smoke_test.py

clean:
	rm -rf .pytest_cache .ruff_cache data
