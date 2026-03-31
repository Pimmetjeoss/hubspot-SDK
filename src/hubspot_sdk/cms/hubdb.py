"""HubDB client – manage HubDB tables and rows."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class HubDbClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/cms/hubdb/{http.api_version}/tables"

    # -- Tables ---------------------------------------------------------------

    async def list_tables(self, **params: Any) -> dict[str, Any]:
        return await self._http.get(self._base, params=params or None)

    async def create_table(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(self._base, json=data)

    async def get_table(self, table_id: str, *, draft: bool = False) -> dict[str, Any]:
        path = f"{self._base}/draft/{table_id}" if draft else f"{self._base}/{table_id}"
        return await self._http.get(path)

    async def update_table(self, table_id: str, data: dict[str, Any], *, draft: bool = False) -> dict[str, Any]:
        path = f"{self._base}/draft/{table_id}" if draft else f"{self._base}/{table_id}"
        return await self._http.patch(path, json=data)

    async def delete_table(self, table_id: str) -> None:
        await self._http.delete(f"{self._base}/{table_id}")

    async def clone_table(self, table_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/{table_id}/clone", json=data)

    async def export_table(self, table_id: str, *, draft: bool = False) -> Any:
        path = f"{self._base}/draft/{table_id}/export" if draft else f"{self._base}/{table_id}/export"
        return await self._http.get(path)

    async def import_table(self, table_id: str, *, files: Any = None, data: Any = None, draft: bool = False) -> dict[str, Any]:
        path = f"{self._base}/draft/{table_id}/import" if draft else f"{self._base}/{table_id}/import"
        return await self._http.post(path, files=files, data=data)

    async def publish_table(self, table_id: str) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/{table_id}/draft/publish")

    async def reset_draft_table(self, table_id: str) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/{table_id}/draft/reset")

    async def unpublish_table(self, table_id: str) -> None:
        await self._http.post(f"{self._base}/{table_id}/unpublish")

    async def list_draft_tables(self, **params: Any) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/draft", params=params or None)

    # -- Rows -----------------------------------------------------------------

    async def list_rows(self, table_id: str, *, draft: bool = False, **params: Any) -> dict[str, Any]:
        path = f"{self._base}/draft/{table_id}/rows" if draft else f"{self._base}/{table_id}/rows"
        return await self._http.get(path, params=params or None)

    async def create_row(self, table_id: str, data: dict[str, Any], *, draft: bool = False) -> dict[str, Any]:
        path = f"{self._base}/draft/{table_id}/rows" if draft else f"{self._base}/{table_id}/rows"
        return await self._http.post(path, json=data)

    async def get_row(self, table_id: str, row_id: str, *, draft: bool = False) -> dict[str, Any]:
        path = f"{self._base}/draft/{table_id}/rows/{row_id}" if draft else f"{self._base}/{table_id}/rows/{row_id}"
        return await self._http.get(path)

    async def update_row(self, table_id: str, row_id: str, data: dict[str, Any], *, draft: bool = False) -> dict[str, Any]:
        path = f"{self._base}/draft/{table_id}/rows/{row_id}" if draft else f"{self._base}/{table_id}/rows/{row_id}"
        return await self._http.patch(path, json=data)

    async def replace_row(self, table_id: str, row_id: str, data: dict[str, Any], *, draft: bool = False) -> dict[str, Any]:
        path = f"{self._base}/draft/{table_id}/rows/{row_id}" if draft else f"{self._base}/{table_id}/rows/{row_id}"
        return await self._http.put(path, json=data)

    async def delete_row(self, table_id: str, row_id: str, *, draft: bool = False) -> None:
        path = f"{self._base}/draft/{table_id}/rows/{row_id}" if draft else f"{self._base}/{table_id}/rows/{row_id}"
        await self._http.delete(path)

    # -- Batch rows -----------------------------------------------------------

    async def batch_create_rows(self, table_id: str, inputs: list[dict[str, Any]], *, draft: bool = False) -> dict[str, Any]:
        path = f"{self._base}/draft/{table_id}/rows/batch/create" if draft else f"{self._base}/{table_id}/rows/batch/create"
        return await self._http.post(path, json={"inputs": inputs})

    async def batch_read_rows(self, table_id: str, inputs: list[dict[str, Any]], *, draft: bool = False) -> dict[str, Any]:
        path = f"{self._base}/draft/{table_id}/rows/batch/read" if draft else f"{self._base}/{table_id}/rows/batch/read"
        return await self._http.post(path, json={"inputs": inputs})

    async def batch_replace_rows(self, table_id: str, inputs: list[dict[str, Any]], *, draft: bool = False) -> dict[str, Any]:
        path = f"{self._base}/draft/{table_id}/rows/batch/replace" if draft else f"{self._base}/{table_id}/rows/batch/replace"
        return await self._http.post(path, json={"inputs": inputs})

    async def batch_clone_rows(self, table_id: str, inputs: list[dict[str, Any]], *, draft: bool = False) -> dict[str, Any]:
        path = f"{self._base}/draft/{table_id}/rows/batch/clone" if draft else f"{self._base}/{table_id}/rows/batch/clone"
        return await self._http.post(path, json={"inputs": inputs})

    async def batch_purge_rows(self, table_id: str, inputs: list[dict[str, Any]], *, draft: bool = False) -> None:
        path = f"{self._base}/draft/{table_id}/rows/batch/purge" if draft else f"{self._base}/{table_id}/rows/batch/purge"
        await self._http.post(path, json={"inputs": inputs})
