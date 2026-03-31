"""Business Units client."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class BusinessUnitsClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/business-units/public/{http.api_version}"

    async def get_for_user(self, user_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/business-units/user/{user_id}")
