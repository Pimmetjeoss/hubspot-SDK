"""CRM forecast types client."""
from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class ForecastsClient:
    """Read forecast type settings.

    Note: Uses v3 path, not the standard api_version.
    Endpoints:
        GET /forecast-settings/v3/forecast-types
        GET /forecast-settings/v3/forecast-types/{forecastTypeId}
    """
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = "/forecast-settings/v3/forecast-types"

    async def list(self) -> dict[str, Any]:
        return await self._http.get(self._base)

    async def get(self, forecast_type_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{forecast_type_id}")
