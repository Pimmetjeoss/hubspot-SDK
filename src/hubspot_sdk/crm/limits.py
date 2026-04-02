"""CRM limits tracking client."""
from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class LimitsClient:
    """Read CRM account limits and usage.

    Endpoints:
        GET /crm/limits/{version}/associations/labels
        GET /crm/limits/{version}/associations/records/from
        GET /crm/limits/{version}/associations/records/{fromObjectTypeId}/to
        GET /crm/limits/{version}/associations/records/{fromObjectTypeId}/{toObjectTypeId}
        GET /crm/limits/{version}/calculated-properties
        GET /crm/limits/{version}/custom-object-types
        GET /crm/limits/{version}/custom-properties
        GET /crm/limits/{version}/pipelines
        GET /crm/limits/{version}/records
    """
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/crm/limits/{http.api_version}"

    async def association_labels(
        self,
        *,
        from_object_type_id: str | None = None,
        to_object_type_id: str | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if from_object_type_id:
            params["fromObjectTypeId"] = from_object_type_id
        if to_object_type_id:
            params["toObjectTypeId"] = to_object_type_id
        return await self._http.get(f"{self._base}/associations/labels", params=params)

    async def association_records(self) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/associations/records/from")

    async def association_records_from(self, from_object_type_id: str) -> dict[str, Any]:
        return await self._http.get(
            f"{self._base}/associations/records/{from_object_type_id}/to"
        )

    async def association_records_between(
        self, from_object_type_id: str, to_object_type_id: str
    ) -> dict[str, Any]:
        return await self._http.get(
            f"{self._base}/associations/records/{from_object_type_id}/{to_object_type_id}"
        )

    async def calculated_properties(self) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/calculated-properties")

    async def custom_object_types(self) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/custom-object-types")

    async def custom_properties(self) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/custom-properties")

    async def pipelines(self) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/pipelines")

    async def records(self) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/records")
