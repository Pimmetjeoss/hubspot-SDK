"""Conversations Threads client."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class ThreadsClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        # Mix of v3 and versioned endpoints per spec
        self._base_v3 = "/conversations/conversations/v3/threads"
        self._base = "/conversations/v3/conversations"

    # -- Threads --------------------------------------------------------------

    async def list(self, **params: Any) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/threads", params=params or None)

    async def get(self, thread_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/threads/{thread_id}")

    async def update(self, thread_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.patch(f"{self._base}/threads/{thread_id}", json=data)

    async def set_assignee(self, thread_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.put(f"{self._base_v3}/{thread_id}/assignee", json=data)

    async def remove_assignee(self, thread_id: str) -> None:
        await self._http.delete(f"{self._base_v3}/{thread_id}/assignee")

    # -- Messages within threads ---------------------------------------------

    async def list_messages(self, thread_id: str, **params: Any) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/threads/{thread_id}/messages", params=params or None)

    async def get_message(self, thread_id: str, message_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/threads/{thread_id}/messages/{message_id}")

    async def send_message(self, thread_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/threads/{thread_id}/messages", json=data)

    # -- Actors ---------------------------------------------------------------

    async def batch_read_actors(self, inputs: list[dict[str, Any]]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/actors/batch/read", json={"inputs": inputs})

    async def get_actor(self, actor_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/actors/{actor_id}")

    # -- Inboxes --------------------------------------------------------------

    async def list_inboxes(self, **params: Any) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/inboxes", params=params or None)

    async def get_inbox(self, inbox_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/inboxes/{inbox_id}")

    # -- Channel accounts -----------------------------------------------------

    async def list_channel_accounts(self, **params: Any) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/channel-accounts", params=params or None)
