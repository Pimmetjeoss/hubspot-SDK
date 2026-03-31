"""Contacts client – extends generic CRM object with merge, GDPR delete."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient
from hubspot_sdk.core.models import HubSpotObject
from hubspot_sdk.crm.objects import CrmObjectClient


class ContactsClient(CrmObjectClient):
    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "contacts")

    async def merge(self, primary_id: str, object_id_to_merge: str) -> HubSpotObject:
        data = await self._http.post(
            f"{self._base}/merge",
            json={"primaryObjectId": primary_id, "objectIdToMerge": object_id_to_merge},
        )
        return HubSpotObject.model_validate(data)

    async def gdpr_delete(self, object_id: str, *, id_property: str | None = None) -> None:
        body: dict[str, Any] = {"objectId": object_id}
        if id_property:
            body["idProperty"] = id_property
        await self._http.post(f"{self._base}/gdpr-delete", json=body)
