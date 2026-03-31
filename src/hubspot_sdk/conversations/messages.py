"""Conversations Inbox Messages client (additional endpoints beyond threads)."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class MessagesClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = "/conversations/v3/conversations"

    async def get_message(self, message_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/messages/{message_id}")

    async def get_original_email(self, message_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/messages/{message_id}/original-email")
