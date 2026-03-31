"""Transactional Email & SMTP Tokens client."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class TransactionalEmailClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/marketing/transactional/{http.api_version}"

    async def send(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/single-email/send", json=data)

    # -- SMTP tokens ----------------------------------------------------------

    async def list_smtp_tokens(self, **params: Any) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/smtp-tokens", params=params or None)

    async def create_smtp_token(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/smtp-tokens", json=data)

    async def get_smtp_token(self, token_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/smtp-tokens/{token_id}")

    async def delete_smtp_token(self, token_id: str) -> None:
        await self._http.delete(f"{self._base}/smtp-tokens/{token_id}")

    async def reset_smtp_token_password(self, token_id: str) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/smtp-tokens/{token_id}/password-reset")
