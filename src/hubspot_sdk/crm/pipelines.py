"""Pipelines client – manage CRM pipelines and stages."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class PipelinesClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/crm/pipelines/{http.api_version}"

    # -- Pipelines ------------------------------------------------------------

    async def list(self, object_type: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{object_type}")

    async def create(self, object_type: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/{object_type}", json=data)

    async def get(self, object_type: str, pipeline_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{object_type}/{pipeline_id}")

    async def update(self, object_type: str, pipeline_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.patch(f"{self._base}/{object_type}/{pipeline_id}", json=data)

    async def replace(self, object_type: str, pipeline_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.put(f"{self._base}/{object_type}/{pipeline_id}", json=data)

    async def delete(self, object_type: str, pipeline_id: str) -> None:
        await self._http.delete(f"{self._base}/{object_type}/{pipeline_id}")

    # -- Stages ---------------------------------------------------------------

    async def list_stages(self, object_type: str, pipeline_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{object_type}/{pipeline_id}/stages")

    async def create_stage(self, object_type: str, pipeline_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/{object_type}/{pipeline_id}/stages", json=data)

    async def get_stage(self, object_type: str, pipeline_id: str, stage_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{object_type}/{pipeline_id}/stages/{stage_id}")

    async def update_stage(self, object_type: str, pipeline_id: str, stage_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.patch(f"{self._base}/{object_type}/{pipeline_id}/stages/{stage_id}", json=data)

    async def replace_stage(self, object_type: str, pipeline_id: str, stage_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.put(f"{self._base}/{object_type}/{pipeline_id}/stages/{stage_id}", json=data)

    async def delete_stage(self, object_type: str, pipeline_id: str, stage_id: str) -> None:
        await self._http.delete(f"{self._base}/{object_type}/{pipeline_id}/stages/{stage_id}")

    # -- Audit ----------------------------------------------------------------

    async def get_audit(self, object_type: str, pipeline_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{object_type}/{pipeline_id}/audit")

    async def get_stage_audit(self, object_type: str, pipeline_id: str, stage_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{object_type}/{pipeline_id}/stages/{stage_id}/audit")
