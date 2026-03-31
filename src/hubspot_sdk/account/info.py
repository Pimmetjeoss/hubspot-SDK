"""Account Info client."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class AccountInfoClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/account-info/{http.api_version}"

    async def get_details(self) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/details")

    async def get_api_usage(self, **params: Any) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/api-usage/daily/private-apps", params=params or None)
