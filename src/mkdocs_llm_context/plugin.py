"""MkDocs plugin: bundle all pages into one JSON or TXT file for LLM context."""

import json
import logging
from pathlib import Path

from mkdocs.config import config_options as c
from mkdocs.config.base import Config as MkDocsConfig
from mkdocs.exceptions import PluginError
from mkdocs.plugins import BasePlugin

log = logging.getLogger("mkdocs.plugins.mkdocs_llm_context")


class LlmContextPluginConfig(MkDocsConfig):
    output = c.Optional(c.Type(str))
    format = c.Choice(("json", "txt"), default="json")


class LlmContextPlugin(BasePlugin[LlmContextPluginConfig]):
    """Bundle the built MkDocs site into a single file (JSON or TXT) for LLM/agent context."""

    def __init__(self):
        super().__init__()
        self._pages: list[dict] = []

    def on_pre_build(self, config, **kwargs):
        """Clear accumulator so mkdocs serve rebuilds don't duplicate."""
        self._pages = []

    def on_post_page(self, output, page, config, **kwargs):
        """Accumulate page source markdown."""
        self._pages.append({"url": page.url, "title": page.title, "content": page.markdown})

    def on_post_build(self, config, **kwargs):
        """Write accumulated pages to a single output file."""
        site_dir = Path(config["site_dir"])
        out_fmt = self.config.format
        output_name = self.config.output or f"llm-context.{out_fmt}"
        out_path = site_dir / output_name

        try:
            if out_fmt == "json":
                with open(out_path, "w", encoding="utf-8") as f:
                    json.dump(self._pages, f, indent=2, ensure_ascii=False)
            else:
                parts = [
                    f"## {r['title']}\nURL: {r['url']}\n\n{r['content']}"
                    for r in self._pages
                ]
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write("\n\n---\n\n".join(parts))
            log.info("Wrote %s (%d pages) to %s", output_name, len(self._pages), out_path)
        except OSError as e:
            raise PluginError(f"Failed to write {out_path}: {e}") from e
