from config_loader import load_yaml
from confluence_client import ConfluenceClient
from page_parser import extract_page_id
from markdown_builder import build_markdown
from file_writer import write_markdown


def main():
    print("=== Confluence KB Sync started ===")

    # Load configs
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


    for category, urls in pages.items():
        print(f"\nCategory: {category}")

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

                print(f"  ✔ Synced: {title} -> {file_path}")

            except Exception as e:
                print(f"  ✖ Failed for {url}")
                print(f"    Reason: {e}")

    print("\n=== Confluence KB Sync finished ===")


if __name__ == "__main__":
    main()
