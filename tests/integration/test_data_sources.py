"""Integration tests for external legal data sources.

These hit real APIs, so they need COURTLISTENER_API_TOKEN set in the
environment (via .env) and an internet connection. They are excluded
from CI (Step 8 runs unit tests only) and meant to be run locally:

    uv run pytest tests/integration/test_data_sources.py -v
"""

import os

import pytest

from backend.data.sources.courtlistener import CourtListenerClient
from backend.data.sources.ecfr import ECFRClient

COURTLISTENER_TOKEN = os.environ.get("COURTLISTENER_API_TOKEN", "")


@pytest.mark.skipif(not COURTLISTENER_TOKEN, reason="COURTLISTENER_API_TOKEN not set")
def test_courtlistener_search_returns_results():
    with CourtListenerClient() as client:
        result = client.search_opinions("civil litigation breach of contract")
        assert result["count"] > 0
        assert len(result["results"]) > 0


@pytest.mark.skipif(not COURTLISTENER_TOKEN, reason="COURTLISTENER_API_TOKEN not set")
def test_courtlistener_citation_lookup_known_case():
    # Marbury v. Madison — should always resolve.
    with CourtListenerClient() as client:
        result = client.verify_citation("5 U.S. 137")
        assert result["verified"] is True


def test_ecfr_search_returns_results():
    with ECFRClient() as client:
        result = client.search_regulations("civil procedure")
        assert result["count"] >= 0
        assert isinstance(result["results"], list)
