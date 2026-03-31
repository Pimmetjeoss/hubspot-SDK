"""Tests for the core HTTP client."""

from __future__ import annotations

import pytest
import httpx

from hubspot_sdk.core.http import HttpClient
from hubspot_sdk.core.exceptions import (
    HubSpotAuthError,
    HubSpotNotFoundError,
    HubSpotRateLimitError,
    HubSpotValidationError,
    HubSpotServerError,
)


@pytest.mark.asyncio
async def test_get_success(httpx_mock):
    httpx_mock.add_response(
        url="https://api.hubapi.com/test",
        json={"results": [{"id": "1"}]},
    )
    async with HttpClient("test-token", max_retries=0) as client:
        result = await client.get("/test")
    assert result["results"][0]["id"] == "1"


@pytest.mark.asyncio
async def test_auth_header(httpx_mock):
    httpx_mock.add_response(url="https://api.hubapi.com/test", json={})
    async with HttpClient("my-secret-token", max_retries=0) as client:
        await client.get("/test")
    request = httpx_mock.get_request()
    assert request.headers["Authorization"] == "Bearer my-secret-token"


@pytest.mark.asyncio
async def test_404_raises_not_found(httpx_mock):
    httpx_mock.add_response(
        url="https://api.hubapi.com/test/999",
        status_code=404,
        json={"message": "Not found", "correlationId": "abc"},
    )
    async with HttpClient("test-token", max_retries=0) as client:
        with pytest.raises(HubSpotNotFoundError) as exc_info:
            await client.get("/test/999")
    assert exc_info.value.status_code == 404
    assert exc_info.value.correlation_id == "abc"


@pytest.mark.asyncio
async def test_401_raises_auth_error(httpx_mock):
    httpx_mock.add_response(
        url="https://api.hubapi.com/test",
        status_code=401,
        json={"message": "Unauthorized"},
    )
    async with HttpClient("bad-token", max_retries=0) as client:
        with pytest.raises(HubSpotAuthError):
            await client.get("/test")


@pytest.mark.asyncio
async def test_400_raises_validation_error(httpx_mock):
    httpx_mock.add_response(
        url="https://api.hubapi.com/test",
        status_code=400,
        json={"message": "Bad request", "errors": [{"message": "missing field"}]},
    )
    async with HttpClient("test-token", max_retries=0) as client:
        with pytest.raises(HubSpotValidationError) as exc_info:
            await client.post("/test", json={})
    assert len(exc_info.value.errors) == 1


@pytest.mark.asyncio
async def test_204_returns_none(httpx_mock):
    httpx_mock.add_response(
        url="https://api.hubapi.com/test/1",
        status_code=204,
    )
    async with HttpClient("test-token", max_retries=0) as client:
        result = await client.delete("/test/1")
    assert result is None


@pytest.mark.asyncio
async def test_post_with_json(httpx_mock):
    httpx_mock.add_response(
        url="https://api.hubapi.com/test",
        json={"id": "123"},
        status_code=201,
    )
    async with HttpClient("test-token", max_retries=0) as client:
        result = await client.post("/test", json={"name": "Test"})
    assert result["id"] == "123"
    request = httpx_mock.get_request()
    assert request.headers["Content-Type"] == "application/json"
