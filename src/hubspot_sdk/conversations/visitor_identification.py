"""Visitor identification token generation."""
from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class VisitorIdentificationClient:
    """Generate identification tokens for website visitors.

    Endpoint:
        POST /visitor-identification/{version}/tokens/create
    """
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/visitor-identification/{http.api_version}/tokens"

    async def generate_token(
        self,
        email: str,
        *,
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"email": email}
        if first_name:
            body["firstName"] = first_name
        if last_name:
            body["lastName"] = last_name
        return await self._http.post(f"{self._base}/create", json=body)
