"""Event Send client."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class EventSendClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/events/{http.api_version}/send"

    async def send(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(self._base, json=data)

    async def send_batch(self, inputs: list[dict[str, Any]]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/batch", json={"inputs": inputs})
