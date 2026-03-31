"""CRM Owners client."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class OwnersClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/crm/owners/{http.api_version}"

    async def list(self, *, after: str | None = None, limit: int = 100, email: str | None = None, archived: bool = False) -> dict[str, Any]:
        params: dict[str, Any] = {"limit": limit, "archived": archived}
        if after:
            params["after"] = after
        if email:
            params["email"] = email
        return await self._http.get(self._base, params=params)

    async def get(self, owner_id: str, *, id_property: str | None = None, archived: bool = False) -> dict[str, Any]:
        params: dict[str, Any] = {"archived": archived}
        if id_property:
            params["idProperty"] = id_property
        return await self._http.get(f"{self._base}/{owner_id}", params=params)
