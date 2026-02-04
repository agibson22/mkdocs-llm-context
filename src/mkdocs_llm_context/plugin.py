"""MkDocs plugin: bundle all pages into one JSON or TXT file for LLM context."""

import json
import logging
from pathlib import Path

import mkdocs.config.config_options as c
from markdownify import markdownify
from mkdocs.plugins import BasePlugin
from mkdocs.exceptions import PluginError

log = logging.getLogger("mkdocs.plugins.mkdocs_llm_context")


class LlmContextPlugin(BasePlugin):
    """Bundle the built MkDocs site into a single file (JSON or TXT) for LLM/agent context."""

    config_scheme = (
        ("output", c.Type(str, default="llm-context.json")),
        ("format", c.Choice(("json", "txt"), default="json")),
    )

    def __init__(self):
        super().__init__()
        self._pages = []

    def on_pre_build(self, config, **kwargs):
        """Clear accumulator so mkdocs serve rebuilds don't duplicate."""
        self._pages = []

    def on_post_page(self, output, page, config, **kwargs):
        """Accumulate (url, title, html) for each page."""
        self._pages.append((page.url, page.title, output))
        return None

    def on_post_build(self, config, **kwargs):
        """Convert accumulated HTML to Markdown and write one output file."""
        site_dir = Path(config["site_dir"])
        output_name = self.config["output"]
        out_fmt = self.config["format"]

        records = []
        for url, title, html in self._pages:
            try:
                content = markdownify(html, strip=["script", "style"])
            except Exception as e:
                raise PluginError(f"markdownify failed for {url!r}: {e}") from e
            records.append({"url": url, "title": title, "content": content})

        out_path = site_dir / output_name
        try:
            if out_fmt == "json":
                with open(out_path, "w", encoding="utf-8") as f:
                    json.dump(records, f, indent=2, ensure_ascii=False)
            else:
                parts = []
                for r in records:
                    parts.append(f"\n\n## {r['title']}\nURL: {r['url']}\n\n{r['content']}\n\n")
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(parts).strip() or "")
            log.info("Wrote %s (%d pages) to %s", output_name, len(records), out_path)
        except OSError as e:
            raise PluginError(f"Failed to write {out_path}: {e}") from e
