"""Settings Multicurrency client (15 endpoints)."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class CurrencyClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/settings/currencies/{http.api_version}"

    async def add_currency(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/central-fx-rates/add-currency", json=data)

    async def get_information(self) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/central-fx-rates/information")

    async def get_unsupported_currencies(self) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/central-fx-rates/unsupported-currencies")

    async def update_exchange_rate(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/central-fx-rates/update", json=data)

    async def list_currencies(self, **params: Any) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/currencies", params=params or None)

    async def create_currency(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/currencies", json=data)

    async def get_currency(self, currency_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/currencies/{currency_id}")

    async def update_currency(self, currency_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.patch(f"{self._base}/currencies/{currency_id}", json=data)

    async def delete_currency(self, currency_id: str) -> None:
        await self._http.delete(f"{self._base}/currencies/{currency_id}")

    async def batch_read_exchange_rates(self, inputs: list[dict[str, Any]]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/exchange-rates/batch/read", json={"inputs": inputs})

    async def set_company_currency(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/company-currency", json=data)
