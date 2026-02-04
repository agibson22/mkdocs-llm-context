"""Tests for mkdocs-llm-context plugin: run mkdocs build from fixture and assert output."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


def test_plugin_produces_json_output(tmp_path):
    """Run mkdocs build from fixture; default output is llm-context.json with expected structure."""
    result = subprocess.run(
        [sys.executable, "-m", "mkdocs", "build", "--site-dir", str(tmp_path / "site")],
        cwd=FIXTURES_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (result.stdout, result.stderr)

    out_file = tmp_path / "site" / "llm-context.json"
    assert out_file.exists(), f"Expected {out_file} to exist"

    with open(out_file, encoding="utf-8") as f:
        data = json.load(f)

    assert isinstance(data, list)
    assert len(data) == 2, "Fixture has two nav pages (index, other)"
    for item in data:
        assert "url" in item
        assert "title" in item
        assert "content" in item
        assert isinstance(item["content"], str)

    titles = {item["title"] for item in data}
    assert "Home" in titles  # nav title for index.md
    assert "Other" in titles

    contents = " ".join(item["content"] for item in data)
    assert "Some content" in contents
    assert "More content" in contents


def test_plugin_txt_format(tmp_path):
    """With format: txt, output is a single .txt file with section headers."""
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "mkdocs",
            "build",
            "--config-file",
            str(FIXTURES_DIR / "mkdocs_txt.yml"),
            "--site-dir",
            str(tmp_path / "site_txt"),
        ],
        cwd=FIXTURES_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (result.stdout, result.stderr)

    out_file = tmp_path / "site_txt" / "llm-context.txt"
    assert out_file.exists()
    text = out_file.read_text(encoding="utf-8")
    assert "## Test" in text or "## Other" in text
    assert "Some content" in text
    assert "More content" in text
