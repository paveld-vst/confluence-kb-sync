from datetime import datetime
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
    and wrap it with AI-friendly metadata.
    """
    try:
        converter = html2text.HTML2Text()
        converter.ignore_images = False
        converter.body_width = 0  # do not wrap lines

        markdown_body = converter.handle(html_content)
    except Exception as e:
        raise MarkdownBuilderError(f"HTML to Markdown conversion failed: {e}")

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    markdown = f"""# {title}

## AI Summary
This document describes **{title}** based on internal Confluence documentation.

## Source
Confluence URL: {source_url}  
Last synced: {timestamp}

---

## Original Content
{markdown_body}
"""

    return markdown
