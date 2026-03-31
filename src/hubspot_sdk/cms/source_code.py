"""CMS Source Code client – manage design files and themes."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class SourceCodeClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/cms/source-code/{http.api_version}"

    async def extract_async(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/extract/async", json=data)

    async def get_extract_status(self, task_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/extract/async/tasks/{task_id}/status")

    async def get_content(self, environment: str, path: str) -> Any:
        return await self._http.get(f"{self._base}/{environment}/content/{path}")

    async def create_or_update(self, environment: str, path: str, *, files: Any = None, data: Any = None) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/{environment}/content/{path}", files=files, data=data)

    async def replace(self, environment: str, path: str, *, files: Any = None, data: Any = None) -> dict[str, Any]:
        return await self._http.put(f"{self._base}/{environment}/content/{path}", json=data)

    async def delete(self, environment: str, path: str) -> None:
        await self._http.delete(f"{self._base}/{environment}/content/{path}")

    async def get_metadata(self, environment: str, path: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{environment}/metadata/{path}")

    async def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/validate", json=data)
