"""Data Studio datasource ingestion client."""
from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class DataSourcesClient:
    """Manage Data Studio data sources.

    Endpoints:
        POST   /data-studio/{version}/data-source
        GET    /data-studio/{version}/data-source/{datasourceId}
        PUT    /data-studio/{version}/data-source/{datasourceId}
        DELETE /data-studio/{version}/data-source/{datasourceId}
    """
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/data-studio/{http.api_version}/data-source"

    async def create(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(self._base, json=data)

    async def get(self, datasource_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{datasource_id}")

    async def update(self, datasource_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.put(f"{self._base}/{datasource_id}", json=data)

    async def delete(self, datasource_id: str) -> None:
        await self._http.delete(f"{self._base}/{datasource_id}")
