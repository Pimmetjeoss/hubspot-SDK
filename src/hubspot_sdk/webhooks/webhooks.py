"""Webhooks client – manage webhook subscriptions and settings (34 endpoints)."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class WebhooksClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._v = http.api_version

    # -- App-level settings ---------------------------------------------------

    async def get_settings(self, app_id: str) -> dict[str, Any]:
        return await self._http.get(f"/webhooks/{self._v}/{app_id}/settings")

    async def update_settings(self, app_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.put(f"/webhooks/{self._v}/{app_id}/settings", json=data)

    async def delete_settings(self, app_id: str) -> None:
        await self._http.delete(f"/webhooks/{self._v}/{app_id}/settings")

    # -- Subscriptions --------------------------------------------------------

    async def list_subscriptions(self, app_id: str) -> dict[str, Any]:
        return await self._http.get(f"/webhooks/{self._v}/{app_id}/subscriptions")

    async def create_subscription(self, app_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"/webhooks/{self._v}/{app_id}/subscriptions", json=data)

    async def get_subscription(self, app_id: str, subscription_id: str) -> dict[str, Any]:
        return await self._http.get(f"/webhooks/{self._v}/{app_id}/subscriptions/{subscription_id}")

    async def update_subscription(self, app_id: str, subscription_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.patch(f"/webhooks/{self._v}/{app_id}/subscriptions/{subscription_id}", json=data)

    async def delete_subscription(self, app_id: str, subscription_id: str) -> None:
        await self._http.delete(f"/webhooks/{self._v}/{app_id}/subscriptions/{subscription_id}")

    async def batch_update_subscriptions(self, app_id: str, inputs: list[dict[str, Any]]) -> dict[str, Any]:
        return await self._http.post(
            f"/webhooks/{self._v}/{app_id}/subscriptions/batch/update",
            json={"inputs": inputs},
        )
