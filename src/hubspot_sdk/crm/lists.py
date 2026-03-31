"""CRM Lists client – manage contact lists and memberships."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class ListsClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/crm/lists/{http.api_version}"

    # -- Lists CRUD -----------------------------------------------------------

    async def list(self, *, count: int = 20, offset: int | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {"count": count}
        if offset is not None:
            params["offset"] = offset
        return await self._http.get(self._base, params=params)

    async def create(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(self._base, json=data)

    async def get(self, list_id: str, *, include_filters: bool = False) -> dict[str, Any]:
        return await self._http.get(
            f"{self._base}/{list_id}", params={"includeFilters": include_filters}
        )

    async def update(self, list_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.put(f"{self._base}/{list_id}", json=data)

    async def delete(self, list_id: str) -> None:
        await self._http.delete(f"{self._base}/{list_id}")

    async def restore(self, list_id: str) -> None:
        await self._http.put(f"{self._base}/{list_id}/restore")

    # -- Batch ----------------------------------------------------------------

    async def batch_read(self, list_ids: list[str]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/batch/read", json={"listIds": list_ids})

    # -- Memberships ----------------------------------------------------------

    async def get_memberships(self, list_id: str, *, after: str | None = None, limit: int = 100) -> dict[str, Any]:
        params: dict[str, Any] = {"limit": limit}
        if after:
            params["after"] = after
        return await self._http.get(f"{self._base}/{list_id}/memberships", params=params)

    async def add_members(self, list_id: str, record_ids: list[str]) -> dict[str, Any]:
        return await self._http.put(
            f"{self._base}/{list_id}/memberships/add", json={"recordIdsToAdd": record_ids}
        )

    async def remove_members(self, list_id: str, record_ids: list[str]) -> dict[str, Any]:
        return await self._http.put(
            f"{self._base}/{list_id}/memberships/remove", json={"recordIdsToRemove": record_ids}
        )

    async def add_and_remove_members(
        self, list_id: str, *, add: list[str] | None = None, remove: list[str] | None = None
    ) -> dict[str, Any]:
        body: dict[str, Any] = {}
        if add:
            body["recordIdsToAdd"] = add
        if remove:
            body["recordIdsToRemove"] = remove
        return await self._http.put(f"{self._base}/{list_id}/memberships/add-and-remove", json=body)

    async def add_all_from_list(self, list_id: str, source_list_id: str) -> None:
        await self._http.put(
            f"{self._base}/{list_id}/memberships/add-from/{source_list_id}"
        )

    # -- Folders --------------------------------------------------------------

    async def list_folders(self) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/folders")

    async def create_folder(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/folders", json=data)

    async def update_folder(self, folder_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.put(f"{self._base}/folders/{folder_id}", json=data)

    async def move_folder(self, folder_id: str, new_parent_folder_id: str) -> dict[str, Any]:
        return await self._http.put(
            f"{self._base}/folders/{folder_id}/move/{new_parent_folder_id}"
        )

    async def delete_folder(self, folder_id: str) -> None:
        await self._http.delete(f"{self._base}/folders/{folder_id}")

    # -- Search / mapping -----------------------------------------------------

    async def search(self, *, query: str | None = None, **params: Any) -> dict[str, Any]:
        p: dict[str, Any] = dict(params)
        if query:
            p["query"] = query
        return await self._http.get(f"{self._base}/search", params=p)

    async def get_by_name(self, list_name: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/object-type-id/name/{list_name}")

    async def get_memberships_join_order(self, list_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{list_id}/memberships/join-order")
