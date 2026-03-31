"""Shared test fixtures."""

from __future__ import annotations

import pytest
import httpx

from hubspot_sdk.core.http import HttpClient
from hubspot_sdk import HubSpotClient


@pytest.fixture
def http_client(httpx_mock) -> HttpClient:
    """Provide an HttpClient backed by pytest-httpx."""
    return HttpClient("test-token-123", max_retries=0)


@pytest.fixture
def hs_client(httpx_mock) -> HubSpotClient:
    """Provide a full HubSpotClient backed by pytest-httpx."""
    return HubSpotClient("test-token-123")
