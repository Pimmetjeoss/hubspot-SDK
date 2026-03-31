"""User Provisioning client (7 endpoints)."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class UserProvisioningClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/settings/users/{http.api_version}"

    async def list(self, **params: Any) -> dict[str, Any]:
        return await self._http.get(self._base, params=params or None)

    async def create(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(self._base, json=data)

    async def get(self, user_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{user_id}")

    async def update(self, user_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.put(f"{self._base}/{user_id}", json=data)

    async def delete(self, user_id: str) -> None:
        await self._http.delete(f"{self._base}/{user_id}")

    async def list_roles(self) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/roles")

    async def list_teams(self) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/teams")
