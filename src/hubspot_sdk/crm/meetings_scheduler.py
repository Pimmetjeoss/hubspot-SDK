"""Scheduler meetings client (not CRM meetings object - that's handled by CrmObjectClient)."""
from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class MeetingsSchedulerClient:
    """Meeting scheduling pages and booking.

    Endpoints:
        POST /scheduler/{version}/meetings/calendar
        GET  /scheduler/{version}/meetings/meeting-links
        POST /scheduler/{version}/meetings/meeting-links/book
        GET  /scheduler/{version}/meetings/meeting-links/book/availability-page/{slug}
        GET  /scheduler/{version}/meetings/meeting-links/book/{slug}
    """
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/scheduler/{http.api_version}/meetings"

    async def create_calendar_event(
        self, organizer_user_id: str, event_data: dict[str, Any]
    ) -> dict[str, Any]:
        return await self._http.post(
            f"{self._base}/calendar",
            json=event_data,
            params={"organizerUserId": organizer_user_id},
        )

    async def list_meeting_links(
        self,
        *,
        limit: int | None = None,
        after: str | None = None,
        name: str | None = None,
        organizer_user_id: str | None = None,
        link_type: str | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if limit:
            params["limit"] = limit
        if after:
            params["after"] = after
        if name:
            params["name"] = name
        if organizer_user_id:
            params["organizerUserId"] = organizer_user_id
        if link_type:
            params["type"] = link_type
        return await self._http.get(f"{self._base}/meeting-links", params=params)

    async def book_meeting(self, booking_data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/meeting-links/book", json=booking_data)

    async def get_availability(
        self, slug: str, timezone: str, *, month_offset: int | None = None
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"timezone": timezone}
        if month_offset is not None:
            params["monthOffset"] = month_offset
        return await self._http.get(
            f"{self._base}/meeting-links/book/availability-page/{slug}",
            params=params,
        )

    async def get_booking_info(self, slug: str, timezone: str) -> dict[str, Any]:
        return await self._http.get(
            f"{self._base}/meeting-links/book/{slug}",
            params={"timezone": timezone},
        )
