"""CMS Site Search client."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class SiteSearchClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/cms/site-search/{http.api_version}"

    async def search(self, *, q: str, **params: Any) -> dict[str, Any]:
        params["q"] = q
        return await self._http.get(f"{self._base}/search", params=params)

    async def get_indexed_data(self, content_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/indexed-data/{content_id}")
