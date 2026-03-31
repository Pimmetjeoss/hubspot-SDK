"""Properties client – manage CRM object property definitions."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class PropertiesClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/crm/properties/{http.api_version}"

    # -- Properties -----------------------------------------------------------

    async def list(self, object_type: str, *, archived: bool = False) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{object_type}", params={"archived": archived})

    async def create(self, object_type: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/{object_type}", json=data)

    async def get(self, object_type: str, property_name: str, *, archived: bool = False) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{object_type}/{property_name}", params={"archived": archived})

    async def update(self, object_type: str, property_name: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.patch(f"{self._base}/{object_type}/{property_name}", json=data)

    async def delete(self, object_type: str, property_name: str) -> None:
        await self._http.delete(f"{self._base}/{object_type}/{property_name}")

    # -- Batch ----------------------------------------------------------------

    async def batch_create(self, object_type: str, inputs: list[dict[str, Any]]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/{object_type}/batch/create", json={"inputs": inputs})

    async def batch_read(self, object_type: str, inputs: list[dict[str, Any]]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/{object_type}/batch/read", json={"inputs": inputs})

    async def batch_archive(self, object_type: str, inputs: list[dict[str, Any]]) -> None:
        await self._http.post(f"{self._base}/{object_type}/batch/archive", json={"inputs": inputs})

    # -- Groups ---------------------------------------------------------------

    async def list_groups(self, object_type: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{object_type}/groups")

    async def create_group(self, object_type: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/{object_type}/groups", json=data)

    async def get_group(self, object_type: str, group_name: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{object_type}/groups/{group_name}")

    async def update_group(self, object_type: str, group_name: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.patch(f"{self._base}/{object_type}/groups/{group_name}", json=data)

    async def delete_group(self, object_type: str, group_name: str) -> None:
        await self._http.delete(f"{self._base}/{object_type}/groups/{group_name}")
