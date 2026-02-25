"""MkDocs plugin: bundle all pages into one JSON or TXT file for LLM context."""

import fnmatch
import json
import logging
from pathlib import Path
from typing import Any

from mkdocs.config import config_options as c
from mkdocs.config.base import Config as MkDocsConfig
from mkdocs.exceptions import PluginError
from mkdocs.plugins import BasePlugin
from mkdocs.structure.pages import Page

log = logging.getLogger("mkdocs.plugins.mkdocs_llm_context")


class LlmContextPluginConfig(MkDocsConfig):
    output = c.Optional(c.Type(str))
    format = c.Choice(("json", "txt"), default="json")
    exclude = c.Type(list, default=[])


class LlmContextPlugin(BasePlugin[LlmContextPluginConfig]):
    """Bundle the built MkDocs site into a single file (JSON or TXT) for LLM/agent context."""

    def __init__(self) -> None:
        super().__init__()
        self._pages: list[dict[str, str]] = []

    def on_pre_build(self, config: MkDocsConfig, **kwargs: Any) -> None:
        """Clear accumulator so mkdocs serve rebuilds don't duplicate."""
        self._pages = []

    def on_post_page(self, output: str, page: Page, config: MkDocsConfig, **kwargs: Any) -> None:
        """Accumulate page source markdown, skipping excluded pages."""
        if any(fnmatch.fnmatch(page.url, pattern) for pattern in self.config.exclude):
            log.debug("Skipping excluded page: %s", page.url)
            return
        self._pages.append({"url": page.url, "title": page.title, "content": page.markdown})

    def on_post_build(self, config: MkDocsConfig, **kwargs: Any) -> None:
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
