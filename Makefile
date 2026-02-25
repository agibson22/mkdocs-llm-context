.PHONY: install test lint build clean

install:
	pip install -e ".[dev]"

test:
	python -m pytest tests/ -v

lint:
	python -m ruff check .

build:
	pip install build --quiet
	python -m build

clean:
	rm -rf dist/ .pytest_cache/ src/*.egg-info
