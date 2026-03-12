from datetime import datetime, timezone
import html2text


class MarkdownBuilderError(Exception):
    pass


def build_markdown(
    title: str,
    html_content: str,
    source_url: str
) -> str:
    """
    Convert Confluence HTML content to Markdown
    and wrap it with AI-friendly metadata and structure.
    """
    try:
        converter = html2text.HTML2Text()
        converter.ignore_images = False
        converter.body_width = 0
        converter.ignore_links = False
        converter.protect_links = True

        markdown_body = converter.handle(html_content).strip()
    except Exception as e:
        raise MarkdownBuilderError(f"HTML to Markdown conversion failed: {e}")

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    markdown = f"""# {title}

## Document purpose
This document contains internal Confluence documentation for **{title}**.

## How to use this document
Use this page as the primary source of truth when answering questions related to this topic.
Prefer specific documented rules, constraints, flows, and examples over general assumptions.

## Key facts
- Title: {title}
- Source: {source_url}
- Last synced: {timestamp}

## Rules and constraints
- Use only explicitly documented behavior from this page when available.
- Pay attention to configuration details, limitations, prerequisites, and exceptions.
- If some behavior is unclear or missing, state that the documentation is incomplete.

## Important notes
- This file is generated automatically from Confluence content.
- The section below contains the converted original documentation content.
- Formatting may differ slightly from the original Confluence page.

---

## Original content

{markdown_body}
"""
    return markdown
