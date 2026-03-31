"""CMS Content Audit client."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class CmsAuditClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/cms/audit-logs/{http.api_version}"

    async def list(self, **params: Any) -> dict[str, Any]:
        return await self._http.get(self._base, params=params or None)

    async def export(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/export", json=data)
