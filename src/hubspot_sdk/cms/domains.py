"""CMS Domains client."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class DomainsClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/cms/domains/{http.api_version}"

    async def list(self, **params: Any) -> dict[str, Any]:
        return await self._http.get(self._base, params=params or None)

    async def get(self, domain_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{domain_id}")
