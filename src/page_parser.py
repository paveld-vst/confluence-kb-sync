import re


class PageParserError(Exception):
    pass


# Confluence Cloud URL pattern:
# https://<org>.atlassian.net/wiki/spaces/SPACE/pages/<PAGE_ID>/Page+Title
PAGE_ID_REGEX = re.compile(r"/pages/(\d+)(/|$)")


def extract_page_id(url: str) -> str:
    """
    Extract Confluence pageId from page URL.
    Raises PageParserError if pageId cannot be extracted.
    """
    match = PAGE_ID_REGEX.search(url)

    if not match:
        raise PageParserError(f"Cannot extract pageId from URL: {url}")

    return match.group(1)
