"""Timeline events client for integrator timeline events."""
from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class TimelineClient:
    """Manage timeline events for integrations.

    Endpoints:
        POST /integrators/timeline/{version}/events - send single event
        POST /integrators/timeline/{version}/events/batch - send batch events
        POST /integrators/timeline/{version}/types/projects - resolve event type
    """
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/integrators/timeline/{http.api_version}"

    async def send_event(self, event: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/events", json=event)

    async def send_events_batch(self, inputs: list[dict[str, Any]]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/events/batch", json={"inputs": inputs})

    async def resolve_event_type(self, developer_symbol: str, project_name: str) -> dict[str, Any]:
        return await self._http.post(
            f"{self._base}/types/projects",
            json={"developerSymbol": developer_symbol, "projectName": project_name},
        )
