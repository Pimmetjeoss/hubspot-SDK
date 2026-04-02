"""Public app feature flags client."""
from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class FeatureFlagsClient:
    """Manage feature flags for HubSpot public apps.

    Endpoints:
        GET    /feature-flags/{version}/{appId}/flags/all
        GET    /feature-flags/{version}/{appId}/flags/{flagName}
        PUT    /feature-flags/{version}/{appId}/flags/{flagName}
        DELETE /feature-flags/{version}/{appId}/flags/{flagName}
        GET    /feature-flags/{version}/{appId}/flags/{flagName}/portals
        POST   /feature-flags/{version}/{appId}/flags/{flagName}/portals/batch/delete
        POST   /feature-flags/{version}/{appId}/flags/{flagName}/portals/batch/upsert
    """
    def __init__(self, http: HttpClient, app_id: str) -> None:
        self._http = http
        self.app_id = app_id
        self._base = f"/feature-flags/{http.api_version}/{app_id}/flags"

    async def list_all(self) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/all")

    async def get(self, flag_name: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{flag_name}")

    async def set(self, flag_name: str, *, default_value: bool) -> dict[str, Any]:
        return await self._http.put(
            f"{self._base}/{flag_name}",
            json={"defaultValue": default_value},
        )

    async def delete(self, flag_name: str) -> None:
        await self._http.delete(f"{self._base}/{flag_name}")

    async def list_portals(
        self,
        flag_name: str,
        *,
        limit: int | None = None,
        start_portal_id: int | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if limit:
            params["limit"] = limit
        if start_portal_id:
            params["startPortalId"] = start_portal_id
        return await self._http.get(f"{self._base}/{flag_name}/portals", params=params)

    async def batch_upsert_portals(
        self, flag_name: str, inputs: list[dict[str, Any]]
    ) -> dict[str, Any]:
        return await self._http.post(
            f"{self._base}/{flag_name}/portals/batch/upsert",
            json={"inputs": inputs},
        )

    async def batch_delete_portals(
        self, flag_name: str, portal_ids: list[int]
    ) -> None:
        await self._http.post(
            f"{self._base}/{flag_name}/portals/batch/delete",
            json={"inputs": [{"portalId": pid} for pid in portal_ids]},
        )
