# mkdocs-llm-context

Bundle your MkDocs site into a single file for LLM or agent context.

## Installation

```bash
pip install mkdocs-llm-context
```

Until the plugin is on PyPI, install from a local path:

```bash
pip install -e /path/to/mkdocs-llm-context
```

## Usage

Add the plugin to your `mkdocs.yml`:

```yaml
plugins:
  - llm-context
```

Optional configuration:

```yaml
plugins:
  - llm-context:
      output: llm-context.json   # default
      format: json               # or "txt"
```

- **output**: Filename written to the site directory (default: `llm-context.json`).
- **format**: `json` — list of `{url, title, content}`; `txt` — single file with `## Title` and URL per section.

After `mkdocs build`, the file appears in `site/` and can be used as context for an LLM or agent.

## Development

### Running tests

From the repo root:

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

Tests run `mkdocs build` against a minimal fixture under `tests/fixtures/` and assert the output file exists with the expected structure.

### Using with another MkDocs site (e.g. Sema)

1. Install the plugin in editable mode: `pip install -e /path/to/mkdocs-llm-context`
2. Install that site’s docs dependencies (e.g. `pip install -e ".[docs]"` from the other repo).
3. In the site’s `mkdocs.yml`, add `llm-context` to the `plugins` list.
4. Run `mkdocs build`; the bundle is written to the site directory.

When the plugin is published to PyPI, you can add `mkdocs-llm-context` to your project’s docs dependencies instead of installing from path.
