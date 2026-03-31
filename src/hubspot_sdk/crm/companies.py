"""Companies client – extends generic CRM object with merge."""

from __future__ import annotations

from hubspot_sdk.core.http import HttpClient
from hubspot_sdk.core.models import HubSpotObject
from hubspot_sdk.crm.objects import CrmObjectClient


class CompaniesClient(CrmObjectClient):
    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "companies")

    async def merge(self, primary_id: str, object_id_to_merge: str) -> HubSpotObject:
        data = await self._http.post(
            f"{self._base}/merge",
            json={"primaryObjectId": primary_id, "objectIdToMerge": object_id_to_merge},
        )
        return HubSpotObject.model_validate(data)
