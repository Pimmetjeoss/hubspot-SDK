"""Automation Actions V4 client (18 endpoints)."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class ActionsClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/automation/actions/{http.api_version}"

    async def list(self, app_id: str, **params: Any) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{app_id}", params=params or None)

    async def create(self, app_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/{app_id}", json=data)

    async def get(self, app_id: str, definition_id: str, **params: Any) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{app_id}/{definition_id}", params=params or None)

    async def update(self, app_id: str, definition_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.patch(f"{self._base}/{app_id}/{definition_id}", json=data)

    async def delete(self, app_id: str, definition_id: str) -> None:
        await self._http.delete(f"{self._base}/{app_id}/{definition_id}")

    # -- Functions ------------------------------------------------------------

    async def list_functions(self, app_id: str, definition_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{app_id}/{definition_id}/functions")

    async def get_function(self, app_id: str, definition_id: str, function_type: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{app_id}/{definition_id}/functions/{function_type}")

    async def create_or_replace_function(self, app_id: str, definition_id: str, function_type: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.put(f"{self._base}/{app_id}/{definition_id}/functions/{function_type}", json=data)

    async def delete_function(self, app_id: str, definition_id: str, function_type: str) -> None:
        await self._http.delete(f"{self._base}/{app_id}/{definition_id}/functions/{function_type}")

    async def get_function_by_id(self, app_id: str, definition_id: str, function_type: str, function_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{app_id}/{definition_id}/functions/{function_type}/{function_id}")

    async def create_or_replace_function_by_id(self, app_id: str, definition_id: str, function_type: str, function_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.put(f"{self._base}/{app_id}/{definition_id}/functions/{function_type}/{function_id}", json=data)

    async def delete_function_by_id(self, app_id: str, definition_id: str, function_type: str, function_id: str) -> None:
        await self._http.delete(f"{self._base}/{app_id}/{definition_id}/functions/{function_type}/{function_id}")

    # -- Revisions ------------------------------------------------------------

    async def list_revisions(self, app_id: str, definition_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{app_id}/{definition_id}/revisions")

    async def get_revision(self, app_id: str, definition_id: str, revision_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{app_id}/{definition_id}/revisions/{revision_id}")

    # -- Callbacks ------------------------------------------------------------

    async def complete_callback(self, callback_id: str, data: dict[str, Any]) -> None:
        await self._http.post(f"{self._base}/callbacks/{callback_id}/complete", json=data)

    async def batch_complete_callbacks(self, inputs: list[dict[str, Any]]) -> None:
        await self._http.post(f"{self._base}/callbacks/batch/complete", json={"inputs": inputs})
