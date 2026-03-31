"""Marketing Single-Send emails."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class SingleSendClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/marketing/email-campaigns/{http.api_version}"

    async def send(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/single-send", json=data)
