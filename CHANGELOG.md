# Changelog

All notable changes to this project will be documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project adheres to [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

---

## [0.1.0] - 2026-02-25

### Added
- `format` option: `json` (list of `{url, title, content}`) or `txt` (single file with `## Title` sections separated by `---`)
- `output` option: filename written to the MkDocs site directory; auto-derives from `format` when not set
- `exclude` option: glob patterns matched against `page.url` to omit pages from the bundle
- Type hints on all plugin methods
- `ruff` linting in dev toolchain
- `Makefile` with `install`, `test`, `lint`, `build`, and `clean` targets
- CI via GitHub Actions (Python 3.9 + 3.12 matrix)
- Dependabot for pip and GitHub Actions ecosystems

### Changed
- Plugin config uses typed `Config` subclass (MkDocs 1.4+ pattern) instead of deprecated `config_scheme` tuple
- Page content uses `page.markdown` (source markdown) instead of rendering HTML and converting back — output is cleaner and token-efficient
- Pages with no title fall back to `page.url` instead of producing `null`

### Removed
- `markdownify` dependency (no longer needed)
