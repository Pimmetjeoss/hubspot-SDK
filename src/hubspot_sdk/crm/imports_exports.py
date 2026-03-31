"""Imports and Exports clients for CRM data."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class ImportsClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/crm/imports/{http.api_version}"

    async def list(self, *, after: str | None = None, limit: int = 20) -> dict[str, Any]:
        params: dict[str, Any] = {"limit": limit}
        if after:
            params["after"] = after
        return await self._http.get(self._base, params=params)

    async def create(self, data: Any, *, files: Any = None) -> dict[str, Any]:
        return await self._http.post(self._base, data=data, files=files)

    async def get(self, import_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{import_id}")

    async def cancel(self, import_id: str) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/{import_id}/cancel")

    async def get_errors(self, import_id: str, *, after: str | None = None, limit: int = 20) -> dict[str, Any]:
        params: dict[str, Any] = {"limit": limit}
        if after:
            params["after"] = after
        return await self._http.get(f"{self._base}/{import_id}/errors", params=params)


class ExportsClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/crm/exports/{http.api_version}"

    async def create(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/export/async", json=data)

    async def get_status(self, task_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/export/async/tasks/{task_id}/status")

    async def get(self, export_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/export/{export_id}")
