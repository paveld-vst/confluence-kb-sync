import argparse
import shutil
from pathlib import Path

from config_loader import load_yaml
from confluence_client import ConfluenceClient
from page_parser import extract_page_id
from markdown_builder import build_markdown
from file_writer import write_markdown
from index_builder import write_indexes


def parse_args():
    parser = argparse.ArgumentParser(description="Confluence KB Sync")
    parser.add_argument(
        "--project-path",
        type=str,
        required=False,
        help="Optional path to project where KB cache should be copied"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    print("=== Confluence KB Sync started ===")

    config = load_yaml("config/config.yaml")
    pages = load_yaml("config/pages.yaml")

    confluence_cfg = config["confluence"]
    output_cfg = config["output"]

    client = ConfluenceClient(
        base_url=confluence_cfg["base_url"],
        email=confluence_cfg["email"],
        api_token=confluence_cfg["api_token"],
    )

    output_path = output_cfg["path"]
    shared_kb_path = Path(output_path).expanduser()

    if shared_kb_path.exists():
        shutil.rmtree(shared_kb_path)
        print(f"[OK] Removed old shared KB: {shared_kb_path}")

    category_map = {}

    for category, urls in pages.items():
        print(f"\nCategory: {category}")
        category_map[category] = []

        for url in urls:
            try:
                page_id = extract_page_id(url)
                page = client.get_page(page_id)

                title = page["title"]
                html = page["body"]["storage"]["value"]

                markdown = build_markdown(
                    title=title,
                    html_content=html,
                    source_url=url,
                )

                file_path = write_markdown(
                    base_path=output_path,
                    category=category,
                    title=title,
                    content=markdown,
                )

                category_map[category].append(title)
                print(f"  ✔ Synced: {title} -> {file_path}")

            except Exception as e:
                print(f"  ✖ Failed for {url}")
                print(f"    Reason: {e}")

    write_indexes(output_path, category_map)
    print("\n[OK] Index files generated")
    print("\n=== Confluence KB Sync finished ===")

    if args.project_path:
        project_path = Path(args.project_path)
        project_kb_path = project_path / "kb"

        if not shared_kb_path.exists():
            raise FileNotFoundError(f"Shared KB not found at {shared_kb_path}")

        if project_kb_path.exists():
            shutil.rmtree(project_kb_path)
            print(f"[OK] Removed old project KB cache: {project_kb_path}")

        shutil.copytree(shared_kb_path, project_kb_path)

        print(f"\n[OK] Project KB cache created at: {project_kb_path}")


if __name__ == "__main__":
    main()
