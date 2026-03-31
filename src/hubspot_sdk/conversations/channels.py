"""Conversations Custom Channels client (13 endpoints)."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class CustomChannelsClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/conversations/custom-channels/{http.api_version}"

    async def list(self, **params: Any) -> dict[str, Any]:
        return await self._http.get(self._base, params=params or None)

    async def create(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(self._base, json=data)

    async def get(self, channel_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{channel_id}")

    async def update(self, channel_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.patch(f"{self._base}/{channel_id}", json=data)

    async def delete(self, channel_id: str) -> None:
        await self._http.delete(f"{self._base}/{channel_id}")

    # -- Messages -------------------------------------------------------------

    async def send_message(self, channel_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/{channel_id}/messages", json=data)

    async def get_message(self, channel_id: str, message_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{channel_id}/messages/{message_id}")

    async def update_message_status(self, channel_id: str, message_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.put(f"{self._base}/{channel_id}/messages/{message_id}/status", json=data)

    # -- Threads --------------------------------------------------------------

    async def create_thread(self, channel_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/{channel_id}/threads", json=data)

    async def get_thread(self, channel_id: str, thread_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{channel_id}/threads/{thread_id}")

    # -- Webhook callbacks ----------------------------------------------------

    async def create_token(self, channel_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/{channel_id}/token", json=data)
