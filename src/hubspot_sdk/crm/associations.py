"""Associations client – manage relationships between CRM objects."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class AssociationsClient:
    """Covers /crm/associations/{version}/... endpoints."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/crm/associations/{http.api_version}"

    # -- Batch operations -----------------------------------------------------

    async def batch_associate_default(
        self, from_type: str, to_type: str, inputs: list[dict[str, Any]]
    ) -> dict[str, Any]:
        return await self._http.post(
            f"{self._base}/{from_type}/{to_type}/batch/associate/default",
            json={"inputs": inputs},
        )

    async def batch_create(
        self, from_type: str, to_type: str, inputs: list[dict[str, Any]]
    ) -> dict[str, Any]:
        return await self._http.post(
            f"{self._base}/{from_type}/{to_type}/batch/create",
            json={"inputs": inputs},
        )

    async def batch_read(
        self, from_type: str, to_type: str, inputs: list[dict[str, Any]]
    ) -> dict[str, Any]:
        return await self._http.post(
            f"{self._base}/{from_type}/{to_type}/batch/read",
            json={"inputs": inputs},
        )

    async def batch_archive(
        self, from_type: str, to_type: str, inputs: list[dict[str, Any]]
    ) -> None:
        await self._http.post(
            f"{self._base}/{from_type}/{to_type}/batch/archive",
            json={"inputs": inputs},
        )

    # -- Labels / report ------------------------------------------------------

    async def high_usage_report(self, user_id: str) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/usage/high-usage-report/{user_id}")


class AssociationsSchemaClient:
    """Covers /crm/associations/{version}/definitions/... endpoints."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/crm/associations/{http.api_version}/definitions"

    async def get_all_configurations(self) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/configurations/all")

    async def get_configurations(self, from_type: str, to_type: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/configurations/{from_type}/{to_type}")

    async def batch_create_configurations(
        self, from_type: str, to_type: str, inputs: list[dict[str, Any]]
    ) -> dict[str, Any]:
        return await self._http.post(
            f"{self._base}/configurations/{from_type}/{to_type}/batch/create",
            json={"inputs": inputs},
        )

    async def batch_update_configurations(
        self, from_type: str, to_type: str, inputs: list[dict[str, Any]]
    ) -> dict[str, Any]:
        return await self._http.post(
            f"{self._base}/configurations/{from_type}/{to_type}/batch/update",
            json={"inputs": inputs},
        )

    async def delete_configuration(
        self, from_type: str, to_type: str, association_type_id: int
    ) -> None:
        await self._http.delete(
            f"{self._base}/configurations/{from_type}/{to_type}/{association_type_id}"
        )

    async def get_types(self, from_type: str, to_type: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{from_type}/{to_type}")
