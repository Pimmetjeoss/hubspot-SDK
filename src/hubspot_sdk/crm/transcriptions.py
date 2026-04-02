"""Calling transcriptions client."""
from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class TranscriptionsClient:
    """Manage call transcriptions and inbound calls.

    Endpoints:
        POST /crm/extensions/calling/{version}/inbound-call
        POST /crm/extensions/calling/{version}/transcripts
        GET  /crm/extensions/calling/{version}/transcripts/{transcriptId}
        DELETE /crm/extensions/calling/{version}/transcripts/{transcriptId}
    """
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/crm/extensions/calling/{http.api_version}"

    async def complete_inbound_call(self, call_data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/inbound-call", json=call_data)

    async def create_transcript(
        self, engagement_id: int, utterances: list[dict[str, Any]]
    ) -> dict[str, Any]:
        return await self._http.post(
            f"{self._base}/transcripts",
            json={"engagementId": engagement_id, "transcriptCreateUtterances": utterances},
        )

    async def get_transcript(self, transcript_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/transcripts/{transcript_id}")

    async def delete_transcript(self, transcript_id: str) -> None:
        await self._http.delete(f"{self._base}/transcripts/{transcript_id}")
