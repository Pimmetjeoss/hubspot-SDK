"""Marketing Forms client."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class FormsClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = "/marketing/v3/forms"

    async def list(self, **params: Any) -> dict[str, Any]:
        return await self._http.get(self._base, params=params or None)

    async def create(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(self._base, json=data)

    async def get(self, form_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{form_id}")

    async def update(self, form_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.patch(f"{self._base}/{form_id}", json=data)

    async def replace(self, form_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.put(f"{self._base}/{form_id}", json=data)

    async def delete(self, form_id: str) -> None:
        await self._http.delete(f"{self._base}/{form_id}")
