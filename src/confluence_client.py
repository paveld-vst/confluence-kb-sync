import requests
from requests.auth import HTTPBasicAuth


class ConfluenceClientError(Exception):
    pass


class ConfluenceClient:
    def __init__(self, base_url: str, email: str, api_token: str):
        self.base_url = base_url.rstrip("/")
        self.auth = HTTPBasicAuth(email, api_token)

    def get_page(self, page_id: str) -> dict:
        """
        Fetch Confluence page by pageId.
        Returns parsed JSON response.
        """
        url = f"{self.base_url}/rest/api/content/{page_id}"
        params = {
            "expand": "body.storage,version"
        }

        response = requests.get(url, auth=self.auth, params=params)

        if response.status_code == 401:
            raise ConfluenceClientError("Unauthorized (check email or API token)")
        if response.status_code == 403:
            raise ConfluenceClientError("Forbidden (no access to this page)")
        if response.status_code != 200:
            raise ConfluenceClientError(
                f"Confluence API error {response.status_code}: {response.text}"
            )

        return response.json()
