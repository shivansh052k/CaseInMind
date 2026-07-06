"""eCFR (Electronic Code of Federal Regulations) API client.

No API key required. Used during Investigation and Motion stages for
federal regulatory context.

Docs: https://www.ecfr.gov/developers/documentation/api/v1
"""

from __future__ import annotations

import httpx

BASE_URL = "https://www.ecfr.gov/api/search/v1/results"


class ECFRClient:
    def __init__(self, base_url: str = BASE_URL) -> None:
        self.base_url = base_url
        self._client = httpx.Client(timeout=30.0)

    def search_regulations(self, query: str, limit: int = 10) -> dict:
        """Search current federal regulation text.

        Args:
            query: free-text search query (e.g. "civil procedure").
            limit: max number of results.
        """
        response = self._client.get(self.base_url, params={"query": query, "per_page": limit})
        response.raise_for_status()
        data = response.json()
        return {
            "count": data.get("meta", {}).get("total_count", len(data.get("results", []))),
            "results": data.get("results", [])[:limit],
        }

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "ECFRClient":
        return self

    def __exit__(self, *_exc) -> None:
        self.close()
