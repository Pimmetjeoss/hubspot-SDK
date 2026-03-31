"""Automation Sequences client."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class SequencesClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/automation/sequences/{http.api_version}"

    async def list(self, **params: Any) -> dict[str, Any]:
        return await self._http.get(self._base, params=params or None)

    async def get(self, sequence_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{sequence_id}")

    async def enroll(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/enrollments", json=data)

    async def get_enrollments_for_contact(self, contact_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/enrollments/contact/{contact_id}")
