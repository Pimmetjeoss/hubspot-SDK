"""Deals client – extends generic CRM object with merge + deal splits."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient
from hubspot_sdk.core.models import HubSpotObject
from hubspot_sdk.crm.objects import CrmObjectClient


class DealsClient(CrmObjectClient):
    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "0-3")
        self._splits_base = f"/deal-splits/{http.api_version}"

    async def merge(self, primary_id: str, object_id_to_merge: str) -> HubSpotObject:
        data = await self._http.post(
            f"{self._base}/merge",
            json={"primaryObjectId": primary_id, "objectIdToMerge": object_id_to_merge},
        )
        return HubSpotObject.model_validate(data)

    async def batch_read_splits(self, inputs: list[dict[str, Any]]) -> dict[str, Any]:
        return await self._http.post(f"{self._splits_base}/batch/read", json={"inputs": inputs})

    async def batch_upsert_splits(self, inputs: list[dict[str, Any]]) -> dict[str, Any]:
        return await self._http.post(f"{self._splits_base}/batch/upsert", json={"inputs": inputs})
