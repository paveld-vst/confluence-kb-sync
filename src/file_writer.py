import os
import re
from pathlib import Path


class FileWriterError(Exception):
    pass


def sanitize_filename(name: str) -> str:
    """
    Convert page title to a safe filename.
    """
    name = name.strip()
    name = name.replace(" ", "_")
    name = re.sub(r"[^\w\-_.]", "", name)
    return name


def write_markdown(
    base_path: str,
    category: str,
    title: str,
    content: str
) -> Path:
    """
    Write markdown content to file.
    Creates category directory if it does not exist.
    Returns path to written file.
    """
    try:
        base_dir = Path(base_path).expanduser()
        category_dir = base_dir / category
        category_dir.mkdir(parents=True, exist_ok=True)

        safe_name = sanitize_filename(title)
        file_path = category_dir / f"{safe_name}.md"

        file_path.write_text(content, encoding="utf-8")
        return file_path

    except Exception as e:
        raise FileWriterError(f"Failed to write markdown file: {e}")
