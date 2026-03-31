"""CRM Object Schemas client – manage custom object definitions."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class SchemasClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/crm-object-schemas/{http.api_version}/schemas"

    async def list(self) -> dict[str, Any]:
        return await self._http.get(self._base)

    async def create(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(self._base, json=data)

    async def batch_read(self, inputs: list[dict[str, Any]]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/batch/read", json={"inputs": inputs})

    async def get(self, object_type: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{object_type}")

    async def update(self, object_type: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.patch(f"{self._base}/{object_type}", json=data)

    async def delete(self, object_type: str) -> None:
        await self._http.delete(f"{self._base}/{object_type}")

    async def create_association(self, object_type: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/{object_type}/associations", json=data)

    async def delete_association(self, object_type: str, association_id: str) -> None:
        await self._http.delete(f"{self._base}/{object_type}/associations/{association_id}")
