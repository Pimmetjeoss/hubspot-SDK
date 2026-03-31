"""Marketing Events client (36 endpoints)."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class MarketingEventsClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/marketing/marketing-events/{http.api_version}"

    async def list(self, **params: Any) -> dict[str, Any]:
        return await self._http.get(self._base, params=params or None)

    async def create(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(self._base, json=data)

    async def get(self, external_event_id: str, external_account_id: str) -> dict[str, Any]:
        return await self._http.get(
            f"{self._base}/{external_event_id}",
            params={"externalAccountId": external_account_id},
        )

    async def update(self, external_event_id: str, external_account_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.patch(
            f"{self._base}/{external_event_id}",
            json={**data, "externalAccountId": external_account_id},
        )

    async def delete(self, external_event_id: str, external_account_id: str) -> None:
        await self._http.delete(
            f"{self._base}/{external_event_id}",
            params={"externalAccountId": external_account_id},
        )

    async def upsert(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/upsert", json=data)

    async def batch_upsert(self, inputs: list[dict[str, Any]]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/batch/upsert", json={"inputs": inputs})

    async def search(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/search", json=data)

    # -- Participants ---------------------------------------------------------

    async def get_participants(self, external_event_id: str, external_account_id: str, **params: Any) -> dict[str, Any]:
        params["externalAccountId"] = external_account_id
        return await self._http.get(f"{self._base}/{external_event_id}/participants", params=params)

    async def upsert_participant(self, external_event_id: str, subscriber_state: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(
            f"{self._base}/{external_event_id}/{subscriber_state}", json=data
        )

    async def upsert_participant_by_email(self, external_event_id: str, subscriber_state: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(
            f"{self._base}/{external_event_id}/{subscriber_state}/email", json=data
        )

    async def batch_upsert_participants(self, external_event_id: str, subscriber_state: str, inputs: list[dict[str, Any]]) -> dict[str, Any]:
        return await self._http.post(
            f"{self._base}/{external_event_id}/{subscriber_state}/batch",
            json={"inputs": inputs},
        )

    # -- Associations ---------------------------------------------------------

    async def get_list_associations(self, external_account_id: str, external_event_id: str) -> dict[str, Any]:
        return await self._http.get(
            f"{self._base}/associations/{external_account_id}/{external_event_id}/lists"
        )

    async def associate_list(self, external_account_id: str, external_event_id: str, list_id: str) -> dict[str, Any]:
        return await self._http.put(
            f"{self._base}/associations/{external_account_id}/{external_event_id}/lists/{list_id}"
        )

    async def disassociate_list(self, external_account_id: str, external_event_id: str, list_id: str) -> None:
        await self._http.delete(
            f"{self._base}/associations/{external_account_id}/{external_event_id}/lists/{list_id}"
        )

    # -- Completion -----------------------------------------------------------

    async def complete(self, external_event_id: str, external_account_id: str) -> dict[str, Any]:
        return await self._http.post(
            f"{self._base}/{external_event_id}/complete",
            json={"externalAccountId": external_account_id},
        )

    async def cancel(self, external_event_id: str, external_account_id: str) -> dict[str, Any]:
        return await self._http.post(
            f"{self._base}/{external_event_id}/cancel",
            json={"externalAccountId": external_account_id},
        )
