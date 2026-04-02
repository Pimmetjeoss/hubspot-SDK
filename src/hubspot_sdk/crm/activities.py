"""CRM activity clients – extends generic CRM object for activity object types.

Each client maps to a specific HubSpot activity object type and adds merge()
where HubSpot's API supports it (calls, emails, meetings, notes, tasks).
CommunicationsClient and PostalMailClient do not expose merge.
"""

from __future__ import annotations

from hubspot_sdk.core.http import HttpClient
from hubspot_sdk.core.models import HubSpotObject
from hubspot_sdk.crm.objects import CrmObjectClient


class CallsClient(CrmObjectClient):
    """Client for HubSpot CRM calls (object_type='calls')."""

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "calls")

    async def merge(self, primary_id: str, object_id_to_merge: str) -> HubSpotObject:
        """Merge two call records into the primary record."""
        data = await self._http.post(
            f"{self._base}/merge",
            json={"primaryObjectId": primary_id, "objectIdToMerge": object_id_to_merge},
        )
        return HubSpotObject.model_validate(data)


class EmailsClient(CrmObjectClient):
    """Client for HubSpot CRM emails (object_type='emails')."""

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "emails")

    async def merge(self, primary_id: str, object_id_to_merge: str) -> HubSpotObject:
        """Merge two email records into the primary record."""
        data = await self._http.post(
            f"{self._base}/merge",
            json={"primaryObjectId": primary_id, "objectIdToMerge": object_id_to_merge},
        )
        return HubSpotObject.model_validate(data)


class MeetingsClient(CrmObjectClient):
    """Client for HubSpot CRM meetings (object_type='meetings')."""

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "meetings")

    async def merge(self, primary_id: str, object_id_to_merge: str) -> HubSpotObject:
        """Merge two meeting records into the primary record."""
        data = await self._http.post(
            f"{self._base}/merge",
            json={"primaryObjectId": primary_id, "objectIdToMerge": object_id_to_merge},
        )
        return HubSpotObject.model_validate(data)


class NotesClient(CrmObjectClient):
    """Client for HubSpot CRM notes (object_type='notes')."""

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "notes")

    async def merge(self, primary_id: str, object_id_to_merge: str) -> HubSpotObject:
        """Merge two note records into the primary record."""
        data = await self._http.post(
            f"{self._base}/merge",
            json={"primaryObjectId": primary_id, "objectIdToMerge": object_id_to_merge},
        )
        return HubSpotObject.model_validate(data)


class TasksClient(CrmObjectClient):
    """Client for HubSpot CRM tasks (object_type='tasks')."""

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "tasks")

    async def merge(self, primary_id: str, object_id_to_merge: str) -> HubSpotObject:
        """Merge two task records into the primary record."""
        data = await self._http.post(
            f"{self._base}/merge",
            json={"primaryObjectId": primary_id, "objectIdToMerge": object_id_to_merge},
        )
        return HubSpotObject.model_validate(data)


class CommunicationsClient(CrmObjectClient):
    """Client for HubSpot CRM communications (object_type='communications').

    HubSpot does not expose a merge endpoint for communications.
    """

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "communications")


class PostalMailClient(CrmObjectClient):
    """Client for HubSpot CRM postal mail (object_type='postal_mail').

    HubSpot does not expose a merge endpoint for postal mail.
    """

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "postal_mail")
