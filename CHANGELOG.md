# Changelog

All notable changes to this project will be documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project adheres to [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

### Added
- `exclude` config option: glob patterns matched against `page.url` to omit pages from the bundle
- Type hints on all plugin methods
- `ruff` linting in dev toolchain
- `Makefile` with `install`, `test`, `lint`, `build`, and `clean` targets

### Changed
- Plugin config migrated from deprecated `config_scheme` tuple to typed `Config` subclass (MkDocs 1.4+ pattern)
- Page content now uses `page.markdown` (source markdown) instead of rendering HTML and converting back with `markdownify` — output is cleaner and token-efficient
- `output` filename auto-derives from `format` when not explicitly set (`llm-context.json` or `llm-context.txt`)
- TXT format sections separated by `---` instead of blank lines

### Removed
- `markdownify` dependency (no longer needed)

---

## [0.1.0] - 2026-02-01

### Added
- Initial release
- `format` option: `json` (list of `{url, title, content}`) or `txt` (single file with `## Title` sections)
- `output` option: custom filename written to the MkDocs site directory
