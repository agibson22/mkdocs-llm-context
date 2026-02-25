# Contributing

Contributions are welcome — bug reports, feature requests, and pull requests.

## Setup

```bash
git clone https://github.com/agibson22/mkdocs-llm-context
cd mkdocs-llm-context
python -m venv .venv && source .venv/bin/activate
make install
```

## Development workflow

```bash
make test    # run tests
make lint    # run ruff
make build   # build the wheel
```

Tests run `mkdocs build` against a minimal fixture under `tests/fixtures/` and assert the output file structure and content. Add a fixture and test for any new config option.

## Submitting a pull request

1. Fork the repo and create a branch from `main`
2. Make your changes with tests
3. Ensure `make lint` and `make test` both pass
4. Open a pull request with a clear description of the change
