"""CRM Extensions – Calling, CRM Cards, Video Conferencing, Transcriptions."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class CallingExtensionsClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/crm/extensions/calling/{http.api_version}"

    async def create_inbound_call(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/inbound-call", json=data)

    async def mark_recording_ready(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/recordings/ready", json=data)

    async def get_settings(self, app_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{app_id}/settings")

    async def create_settings(self, app_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/{app_id}/settings", json=data)

    async def update_settings(self, app_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.patch(f"{self._base}/{app_id}/settings", json=data)

    async def delete_settings(self, app_id: str) -> None:
        await self._http.delete(f"{self._base}/{app_id}/settings")

    async def get_channel_connection_settings(self, app_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{app_id}/settings/channel-connection")

    async def create_channel_connection_settings(self, app_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/{app_id}/settings/channel-connection", json=data)

    async def update_channel_connection_settings(self, app_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.put(f"{self._base}/{app_id}/settings/channel-connection", json=data)

    async def delete_channel_connection_settings(self, app_id: str) -> None:
        await self._http.delete(f"{self._base}/{app_id}/settings/channel-connection")

    # -- Transcriptions -------------------------------------------------------

    async def create_transcript(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/transcripts", json=data)

    async def get_transcript(self, transcript_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/transcripts/{transcript_id}")

    async def delete_transcript(self, transcript_id: str) -> None:
        await self._http.delete(f"{self._base}/transcripts/{transcript_id}")


class CrmCardsClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/crm/extensions/cards-dev/{http.api_version}"

    async def get_sample_response(self) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/sample-response")

    async def list(self, app_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{app_id}")

    async def create(self, app_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/{app_id}", json=data)

    async def get(self, app_id: str, card_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{app_id}/{card_id}")

    async def update(self, app_id: str, card_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.patch(f"{self._base}/{app_id}/{card_id}", json=data)

    async def delete(self, app_id: str, card_id: str) -> None:
        await self._http.delete(f"{self._base}/{app_id}/{card_id}")


class VideoConferencingClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/crm/extensions/videoconferencing/{http.api_version}"

    async def get_settings(self, app_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/settings/{app_id}")

    async def update_settings(self, app_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.put(f"{self._base}/settings/{app_id}", json=data)

    async def delete_settings(self, app_id: str) -> None:
        await self._http.delete(f"{self._base}/settings/{app_id}")
