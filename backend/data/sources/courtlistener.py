"""CourtListener API client.

Covers case-law search and citation verification — the latter is our
direct hallucination guard (Tier 4 output guardrail): every citation an
agent produces gets checked against this before the lawyer sees it.

Docs: https://www.courtlistener.com/help/api/rest/
"""

from __future__ import annotations

import os

import httpx

BASE_URL = "https://www.courtlistener.com/api/rest/v4/"


class CourtListenerClient:
    def __init__(self, api_token: str | None = None, base_url: str = BASE_URL) -> None:
        self.api_token = api_token or os.environ.get("COURTLISTENER_API_TOKEN", "")
        self.base_url = base_url
        self._client = httpx.Client(
            base_url=self.base_url,
            headers={"Authorization": f"Token {self.api_token}"} if self.api_token else {},
            timeout=30.0,
        )

    def search_opinions(self, query: str, jurisdiction: str | None = None, limit: int = 10) -> dict:
        """Search case-law opinions.

        Args:
            query: free-text search query (case name, legal phrase, facts).
            jurisdiction: optional court/jurisdiction filter (e.g. "scotus", "ca9").
            limit: max number of results.
        """
        params = {"q": query, "order_by": "score desc"}
        if jurisdiction:
            params["court"] = jurisdiction

        response = self._client.get("search/", params=params)
        response.raise_for_status()
        data = response.json()
        return {
            "count": data.get("count", 0),
            "results": data.get("results", [])[:limit],
        }

    def verify_citation(self, citation_text: str) -> dict:
        """Look up a citation and confirm it resolves to a real case.

        Used as the citation-hallucination guard: if a citation an agent
        produced doesn't resolve here, it gets blocked before reaching
        the lawyer.
        """
        response = self._client.post("citation-lookup/", data={"text": citation_text})
        response.raise_for_status()
        data = response.json()
        citations = data if isinstance(data, list) else data.get("citations", [])
        found = any(c.get("status") == 200 for c in citations) if citations else False
        return {"verified": found, "raw": citations}

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "CourtListenerClient":
        return self

    def __exit__(self, *_exc) -> None:
        self.close()
