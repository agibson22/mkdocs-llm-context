"""Tests for mkdocs-llm-context plugin: run mkdocs build from fixture and assert output."""

import json
import subprocess
import sys
from pathlib import Path

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


def _build(config_file: Path, site_dir: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "mkdocs",
            "build",
            "--config-file",
            str(config_file),
            "--site-dir",
            str(site_dir),
        ],
        cwd=FIXTURES_DIR,
        capture_output=True,
        text=True,
    )


def test_plugin_produces_json_output(tmp_path):
    """Default output is llm-context.json with expected structure."""
    result = _build(FIXTURES_DIR / "mkdocs.yml", tmp_path / "site")
    assert result.returncode == 0, (result.stdout, result.stderr)

    out_file = tmp_path / "site" / "llm-context.json"
    assert out_file.exists(), f"Expected {out_file} to exist"

    data = json.loads(out_file.read_text(encoding="utf-8"))
    assert isinstance(data, list)
    assert len(data) == 2, "Fixture has two nav pages"

    for item in data:
        assert {"url", "title", "content"} <= item.keys()
        assert isinstance(item["content"], str)

    titles = {item["title"] for item in data}
    assert "Home" in titles
    assert "Other" in titles

    contents = " ".join(item["content"] for item in data)
    assert "Some content" in contents
    assert "More content" in contents


def test_json_content_is_source_markdown(tmp_path):
    """Content field contains raw source markdown, not rendered HTML."""
    result = _build(FIXTURES_DIR / "mkdocs.yml", tmp_path / "site")
    assert result.returncode == 0, (result.stdout, result.stderr)

    data = json.loads((tmp_path / "site" / "llm-context.json").read_text(encoding="utf-8"))
    contents = " ".join(item["content"] for item in data)
    assert "<" not in contents, "Content should be source markdown, not HTML"


def test_plugin_txt_format_explicit_output(tmp_path):
    """With format: txt and explicit output name, file is written correctly."""
    result = _build(FIXTURES_DIR / "mkdocs_txt.yml", tmp_path / "site_txt")
    assert result.returncode == 0, (result.stdout, result.stderr)

    out_file = tmp_path / "site_txt" / "llm-context.txt"
    assert out_file.exists()
    text = out_file.read_text(encoding="utf-8")
    assert "## Home" in text
    assert "## Other" in text
    assert "Some content" in text
    assert "More content" in text
    assert "---" in text, "Sections should be separated by ---"


def test_plugin_txt_format_derives_output_name(tmp_path):
    """With format: txt and no output set, filename auto-derives to llm-context.txt."""
    result = _build(FIXTURES_DIR / "mkdocs_txt_auto.yml", tmp_path / "site_auto")
    assert result.returncode == 0, (result.stdout, result.stderr)

    assert (tmp_path / "site_auto" / "llm-context.txt").exists()
    assert not (tmp_path / "site_auto" / "llm-context.json").exists()
