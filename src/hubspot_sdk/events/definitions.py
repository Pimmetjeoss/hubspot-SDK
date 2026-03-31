"""Event Definitions client (9 endpoints)."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class EventDefinitionsClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/events/{http.api_version}/event-definitions"

    async def list(self, **params: Any) -> dict[str, Any]:
        return await self._http.get(self._base, params=params or None)

    async def create(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(self._base, json=data)

    async def get(self, event_name: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{event_name}")

    async def update(self, event_name: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.patch(f"{self._base}/{event_name}", json=data)

    async def delete(self, event_name: str) -> None:
        await self._http.delete(f"{self._base}/{event_name}")

    async def create_property(self, event_name: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/{event_name}/properties", json=data)

    async def get_property(self, event_name: str, property_name: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{event_name}/properties/{property_name}")

    async def update_property(self, event_name: str, property_name: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.patch(f"{self._base}/{event_name}/properties/{property_name}", json=data)

    async def delete_property(self, event_name: str, property_name: str) -> None:
        await self._http.delete(f"{self._base}/{event_name}/properties/{property_name}")
