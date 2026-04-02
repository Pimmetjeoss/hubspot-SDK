"""CRM object library enablement client."""
from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class ObjectLibraryClient:
    """Check object type enablement status.

    Endpoints:
        GET /crm/object-library/{version}/enablement
        GET /crm/object-library/{version}/enablement/{objectTypeId}
    """
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/crm/object-library/{http.api_version}/enablement"

    async def list_enablement(self) -> dict[str, Any]:
        return await self._http.get(self._base)

    async def get_enablement(self, object_type_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{object_type_id}")
