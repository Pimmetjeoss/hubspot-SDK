"""Account Audit Logs client."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class AuditLogsClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/account-info/{http.api_version}/activity"

    async def list_audit_logs(self, **params: Any) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/audit-logs", params=params or None)

    async def list_login_activity(self, **params: Any) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/login", params=params or None)

    async def list_security_activity(self, **params: Any) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/security", params=params or None)
