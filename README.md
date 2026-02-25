# mkdocs-llm-context

[![CI](https://github.com/agibson22/mkdocs-llm-context/actions/workflows/ci.yml/badge.svg)](https://github.com/agibson22/mkdocs-llm-context/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/mkdocs-llm-context)](https://pypi.org/project/mkdocs-llm-context/)

Bundle your MkDocs site into a single file for LLM or agent context.

## Installation

```bash
pip install mkdocs-llm-context
```

## Usage

Add the plugin to your `mkdocs.yml`:

```yaml
plugins:
  - llm-context
```

### Configuration

```yaml
plugins:
  - llm-context:
      format: json        # "json" (default) or "txt"
      output: llm-context.json  # default derives from format
      exclude:
        - changelog/
        - api/reference/*
```

| Option | Default | Description |
|--------|---------|-------------|
| `format` | `json` | Output format: `json` (list of `{url, title, content}`) or `txt` (sections separated by `---`) |
| `output` | `llm-context.{format}` | Filename written to the site directory |
| `exclude` | `[]` | Glob patterns matched against `page.url` — matching pages are omitted |

After `mkdocs build`, the file appears in `site/` and can be used as context for an LLM or agent.

## Development

```bash
git clone https://github.com/agibson22/mkdocs-llm-context
cd mkdocs-llm-context
python -m venv .venv && source .venv/bin/activate
make install
```

```bash
make test   # run tests
make lint   # run ruff
make build  # build the wheel
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.
