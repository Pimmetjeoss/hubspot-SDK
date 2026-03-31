"""Communication Preferences Subscriptions client (10 endpoints)."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class SubscriptionsClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/communication-preferences/{http.api_version}"

    async def list_definitions(self) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/definitions")

    async def generate_link(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/links/generate", json=data)

    async def batch_read_statuses(self, inputs: list[dict[str, Any]]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/statuses/batch/read", json={"inputs": inputs})

    async def get_status(self, email: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/statuses/{email}")

    async def subscribe(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/subscribe", json=data)

    async def unsubscribe(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/unsubscribe", json=data)

    async def batch_subscribe(self, inputs: list[dict[str, Any]]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/batch/subscribe", json={"inputs": inputs})

    async def batch_unsubscribe(self, inputs: list[dict[str, Any]]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/batch/unsubscribe", json={"inputs": inputs})
