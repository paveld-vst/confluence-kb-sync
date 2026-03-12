from pathlib import Path
from typing import Dict, List


class IndexBuilderError(Exception):
    pass


def build_category_index(category: str, titles: List[str]) -> str:
    lines = [
        f"# {category} documentation index",
        "",
        "## Category overview",
        f"This category contains internal documentation related to **{category}**.",
        "",
        "## Documents in this category",
    ]

    if titles:
        for title in sorted(titles):
            lines.append(f"- {title}")
    else:
        lines.append("- No documents synced yet.")

    lines.extend([
        "",
        "## Usage guidance",
        "- Use these documents as the primary source of truth for this category.",
        "- Prefer documented rules, flows, constraints, and examples over assumptions.",
        "- If multiple documents are relevant, synthesize information across them.",
        "",
    ])

    return "\n".join(lines)


def build_root_index(category_map: Dict[str, List[str]]) -> str:
    lines = [
        "# Knowledge Base Index",
        "",
        "## Overview",
        "This index lists all synced internal documentation categories available in this project.",
        "",
        "## Categories",
    ]

    if category_map:
        for category in sorted(category_map.keys()):
            count = len(category_map[category])
            lines.append(f"- **{category}** ({count} documents)")
    else:
        lines.append("- No categories synced yet.")

    lines.extend([
        "",
        "## Category details",
    ])

    if category_map:
        for category in sorted(category_map.keys()):
            lines.append("")
            lines.append(f"### {category}")
            if category_map[category]:
                for title in sorted(category_map[category]):
                    lines.append(f"- {title}")
            else:
                lines.append("- No documents synced yet.")

    lines.extend([
        "",
        "## Usage guidance",
        "- Start with the relevant category, then inspect the most relevant document(s).",
        "- Prefer detailed documented behavior over general knowledge.",
        "- Include constraints, prerequisites, exceptions, and edge cases when documented.",
        "",
    ])

    return "\n".join(lines)


def write_indexes(base_path: str, category_map: Dict[str, List[str]]) -> None:
    try:
        base_dir = Path(base_path).expanduser()
        base_dir.mkdir(parents=True, exist_ok=True)

        root_index_path = base_dir / "_index.md"
        root_index_path.write_text(
            build_root_index(category_map),
            encoding="utf-8"
        )

        for category, titles in category_map.items():
            category_dir = base_dir / category
            category_dir.mkdir(parents=True, exist_ok=True)

            category_index_path = category_dir / "_index.md"
            category_index_path.write_text(
                build_category_index(category, titles),
                encoding="utf-8"
            )

    except Exception as e:
        raise IndexBuilderError(f"Failed to write index files: {e}")