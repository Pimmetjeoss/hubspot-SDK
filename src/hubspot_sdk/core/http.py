"""Async HTTP client with retry, rate limiting, and error handling."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

import httpx

from hubspot_sdk.core.exceptions import (
    HubSpotAuthError,
    HubSpotConflictError,
    HubSpotError,
    HubSpotNotFoundError,
    HubSpotRateLimitError,
    HubSpotServerError,
    HubSpotValidationError,
)

logger = logging.getLogger("hubspot_sdk")

BASE_URL = "https://api.hubapi.com"
API_VERSION = "2026-03"

_RETRY_STATUS_CODES = {429, 500, 502, 503, 504}
_MAX_RETRIES = 4
_BASE_DELAY = 0.5  # seconds


class HttpClient:
    """Async HTTP client wrapping httpx with HubSpot-specific behaviour.

    Features:
    - Bearer token auth (private app) or OAuth2 access token
    - Automatic retry with exponential backoff on 429 / 5xx
    - Respects Retry-After header
    - Maps HTTP errors to typed exceptions
    """

    def __init__(
        self,
        access_token: str,
        *,
        base_url: str = BASE_URL,
        api_version: str = API_VERSION,
        timeout: float = 30.0,
        max_retries: int = _MAX_RETRIES,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.access_token = access_token
        self.base_url = base_url.rstrip("/")
        self.api_version = api_version
        self.max_retries = max_retries
        self._external_client = client is not None
        self._client = client or httpx.AsyncClient(
            base_url=self.base_url,
            timeout=timeout,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            follow_redirects=True,
        )

    # -- public helpers -------------------------------------------------------

    async def get(self, path: str, *, params: dict[str, Any] | None = None) -> Any:
        return await self._request("GET", path, params=params)

    async def post(
        self,
        path: str,
        *,
        json: Any | None = None,
        params: dict[str, Any] | None = None,
        data: Any | None = None,
        files: Any | None = None,
    ) -> Any:
        return await self._request("POST", path, json=json, params=params, data=data, files=files)

    async def put(self, path: str, *, json: Any | None = None) -> Any:
        return await self._request("PUT", path, json=json)

    async def patch(self, path: str, *, json: Any | None = None) -> Any:
        return await self._request("PATCH", path, json=json)

    async def delete(self, path: str, *, params: dict[str, Any] | None = None) -> Any:
        return await self._request("DELETE", path, params=params)

    # -- lifecycle ------------------------------------------------------------

    async def close(self) -> None:
        if not self._external_client:
            await self._client.aclose()

    async def __aenter__(self) -> HttpClient:
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self.close()

    # -- internal -------------------------------------------------------------

    async def _request(
        self,
        method: str,
        path: str,
        *,
        json: Any | None = None,
        params: dict[str, Any] | None = None,
        data: Any | None = None,
        files: Any | None = None,
    ) -> Any:
        # Strip None values from params
        if params:
            params = {k: v for k, v in params.items() if v is not None}

        kwargs: dict[str, Any] = {"params": params}
        if files:
            # Multipart upload: remove json content-type
            kwargs["files"] = files
            if data:
                kwargs["data"] = data
        elif json is not None:
            kwargs["json"] = json

        last_exc: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                response = await self._client.request(method, path, **kwargs)
                return self._handle_response(response)
            except HubSpotRateLimitError as exc:
                last_exc = exc
                delay = exc.retry_after or (_BASE_DELAY * 2**attempt)
                logger.warning("Rate limited (attempt %d/%d), retrying in %.1fs", attempt + 1, self.max_retries + 1, delay)
                await asyncio.sleep(delay)
            except HubSpotServerError as exc:
                last_exc = exc
                delay = _BASE_DELAY * 2**attempt
                logger.warning("Server error %s (attempt %d/%d), retrying in %.1fs", exc.status_code, attempt + 1, self.max_retries + 1, delay)
                await asyncio.sleep(delay)
            except httpx.TransportError as exc:
                last_exc = exc  # type: ignore[assignment]
                delay = _BASE_DELAY * 2**attempt
                logger.warning("Transport error (attempt %d/%d): %s", attempt + 1, self.max_retries + 1, exc)
                await asyncio.sleep(delay)

        raise last_exc  # type: ignore[misc]

    def _handle_response(self, response: httpx.Response) -> Any:
        if response.status_code == 204:
            return None

        body: dict[str, Any] = {}
        if response.content:
            try:
                body = response.json()
            except Exception:
                body = {"raw": response.text}

        if response.is_success:
            return body

        correlation_id = body.get("correlationId")
        message = body.get("message", response.reason_phrase or "Unknown error")
        common = dict(
            status_code=response.status_code,
            response_body=body,
            correlation_id=correlation_id,
        )

        if response.status_code == 401 or response.status_code == 403:
            raise HubSpotAuthError(message, **common)
        if response.status_code == 404:
            raise HubSpotNotFoundError(message, **common)
        if response.status_code == 429:
            retry_after_raw = response.headers.get("Retry-After")
            retry_after = float(retry_after_raw) if retry_after_raw else None
            raise HubSpotRateLimitError(message, retry_after=retry_after, **common)
        if response.status_code == 400 or response.status_code == 422:
            errors = body.get("errors", [])
            raise HubSpotValidationError(message, errors=errors, **common)
        if response.status_code == 409:
            raise HubSpotConflictError(message, **common)
        if response.status_code >= 500:
            raise HubSpotServerError(message, **common)

        raise HubSpotError(message, **common)
