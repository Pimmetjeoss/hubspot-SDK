"""Marketing Campaigns client (24 endpoints)."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class CampaignsClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/marketing/campaigns/{http.api_version}"

    async def list(self, **params: Any) -> dict[str, Any]:
        return await self._http.get(self._base, params=params or None)

    async def create(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(self._base, json=data)

    async def get(self, campaign_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{campaign_id}")

    async def update(self, campaign_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.patch(f"{self._base}/{campaign_id}", json=data)

    async def delete(self, campaign_id: str) -> None:
        await self._http.delete(f"{self._base}/{campaign_id}")

    async def batch_create(self, inputs: list[dict[str, Any]]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/batch/create", json={"inputs": inputs})

    async def batch_read(self, inputs: list[dict[str, Any]]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/batch/read", json={"inputs": inputs})

    async def batch_update(self, inputs: list[dict[str, Any]]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/batch/update", json={"inputs": inputs})

    async def batch_archive(self, inputs: list[dict[str, Any]]) -> None:
        await self._http.post(f"{self._base}/batch/archive", json={"inputs": inputs})

    async def search(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/search", json=data)

    # -- Revenue attribution --------------------------------------------------

    async def get_revenue_attribution(self, campaign_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{campaign_id}/revenue-attribution")

    async def batch_read_revenue_attribution(self, inputs: list[dict[str, Any]]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/revenue-attribution/batch/read", json={"inputs": inputs})

    # -- Assets ---------------------------------------------------------------

    async def get_assets(self, campaign_id: str, **params: Any) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{campaign_id}/assets", params=params or None)

    async def create_asset(self, campaign_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/{campaign_id}/assets", json=data)

    async def delete_asset(self, campaign_id: str, asset_id: str) -> None:
        await self._http.delete(f"{self._base}/{campaign_id}/assets/{asset_id}")

    async def batch_create_assets(self, campaign_id: str, inputs: list[dict[str, Any]]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/{campaign_id}/assets/batch/create", json={"inputs": inputs})

    async def batch_delete_assets(self, campaign_id: str, inputs: list[dict[str, Any]]) -> None:
        await self._http.post(f"{self._base}/{campaign_id}/assets/batch/archive", json={"inputs": inputs})
