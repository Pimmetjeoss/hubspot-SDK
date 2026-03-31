"""Files client – upload, manage, and organize files (20 endpoints)."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class FilesClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/files/{http.api_version}/files"
        self._folders = f"/files/{http.api_version}/folders"

    # -- Files ----------------------------------------------------------------

    async def upload(self, *, files: Any, data: Any = None) -> dict[str, Any]:
        return await self._http.post(self._base, files=files, data=data)

    async def import_from_url(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/import-from-url/async", json=data)

    async def get_import_status(self, task_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/import-from-url/async/tasks/{task_id}/status")

    async def list(self, **params: Any) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/search", params=params or None)

    async def get(self, file_id: str, **params: Any) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{file_id}", params=params or None)

    async def update(self, file_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.patch(f"{self._base}/{file_id}", json=data)

    async def replace(self, file_id: str, *, files: Any, data: Any = None) -> dict[str, Any]:
        return await self._http.put(f"{self._base}/{file_id}", json=data)

    async def delete(self, file_id: str) -> None:
        await self._http.delete(f"{self._base}/{file_id}")

    async def get_signed_url(self, file_id: str, **params: Any) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{file_id}/signed-url", params=params or None)

    async def get_public_url_redirect(self, file_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{file_id}/public-url-redirect")

    # -- Folders --------------------------------------------------------------

    async def list_folders(self, **params: Any) -> dict[str, Any]:
        return await self._http.get(f"{self._folders}/search", params=params or None)

    async def create_folder(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(self._folders, json=data)

    async def get_folder(self, folder_id: str, **params: Any) -> dict[str, Any]:
        return await self._http.get(f"{self._folders}/{folder_id}", params=params or None)

    async def update_folder(self, folder_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.patch(f"{self._folders}/{folder_id}", json=data)

    async def delete_folder(self, folder_id: str) -> None:
        await self._http.delete(f"{self._folders}/{folder_id}")

    async def check_folder_update_status(self, task_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._folders}/async/tasks/{task_id}/status")
