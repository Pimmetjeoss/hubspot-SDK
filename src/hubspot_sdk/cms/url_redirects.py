"""CMS URL Redirects client."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class UrlRedirectsClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/cms/url-redirects/{http.api_version}"

    async def list(self, **params: Any) -> dict[str, Any]:
        return await self._http.get(self._base, params=params or None)

    async def create(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(self._base, json=data)

    async def get(self, redirect_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{redirect_id}")

    async def update(self, redirect_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.patch(f"{self._base}/{redirect_id}", json=data)

    async def delete(self, redirect_id: str) -> None:
        await self._http.delete(f"{self._base}/{redirect_id}")
