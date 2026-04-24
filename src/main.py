import argparse
import shutil
import sys
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
        nargs="+",
        required=False,
        help="Optional path(s) to projects where KB cache should be copied"
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
    shared_kb_path = Path(output_path).expanduser().absolute()

    if shared_kb_path.exists():
        shutil.rmtree(shared_kb_path)
        print(f"[OK] Removed old shared KB: {shared_kb_path}")

    category_map = {}
    seen_page_ids = set()

    for category, urls in pages.items():
        print(f"\nCategory: {category}")
        category_map[category] = []

        if not urls:
            print(f"  ⚠ No URLs defined for category: {category}, skipping")
            continue

        for url in urls:
            try:
                page_id = extract_page_id(url)

                if page_id in seen_page_ids:
                    print(f"  ⚠ Skipping duplicate page ID {page_id}: {url}")
                    continue

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

                seen_page_ids.add(page_id)
                category_map[category].append(title)
                print(f"  ✔ Synced: {title} -> {file_path}")

            except Exception as e:
                print(f"  ✖ Failed for {url}")
                print(f"    Reason: {e}")

    write_indexes(output_path, category_map)
    print("\n[OK] Index files generated")

    if args.project_path:
        if not shared_kb_path.exists():
            print(f"[ERROR] Shared KB not found at {shared_kb_path}")
            print("\n=== Confluence KB Sync finished with errors ===")
            sys.exit(1)

        failed_paths = []

        for raw_path in args.project_path:
            project_kb_path = None
            try:
                project_path = Path(raw_path).expanduser().resolve()

                if not project_path.exists():
                    raise FileNotFoundError(f"Project path not found: {project_path}")

                if not project_path.is_dir():
                    raise NotADirectoryError(f"Project path is not a directory: {project_path}")

                project_kb_path = project_path / "kb"

                if project_kb_path.exists():
                    if project_kb_path.is_symlink():
                        raise NotADirectoryError(f"Expected a real directory at {project_kb_path}, but found a symlink")
                    if not project_kb_path.is_dir():
                        raise NotADirectoryError(f"Expected a directory at {project_kb_path}, but found a non-directory")
                    shutil.rmtree(project_kb_path)
                    print(f"[OK] Removed old project KB cache: {project_kb_path}")

                shutil.copytree(shared_kb_path, project_kb_path)
                print(f"[OK] Project KB cache created at: {project_kb_path}")

            except (OSError, shutil.Error) as e:
                print(f"  ✖ Failed for project path: {raw_path}")
                print(f"    Reason: {e}")
                if project_kb_path is not None and project_kb_path.exists():
                    try:
                        shutil.rmtree(project_kb_path)
                        print(f"  [cleanup] Removed partially copied KB: {project_kb_path}")
                    except OSError as cleanup_error:
                        print(f"  [cleanup] Failed to remove partially copied KB: {cleanup_error}")
                failed_paths.append(raw_path)

        if failed_paths:
            print(f"\n[WARNING] KB cache was not created for {len(failed_paths)} project(s):")
            for p in failed_paths:
                print(f"  - {p}")
            print("\n=== Confluence KB Sync finished with errors ===")
            sys.exit(1)

    print("\n=== Confluence KB Sync finished ===")


if __name__ == "__main__":
    main()
