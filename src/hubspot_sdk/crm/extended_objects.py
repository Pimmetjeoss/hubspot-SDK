"""Extended CRM object clients for remaining HubSpot object types.

Each class extends CrmObjectClient for the standard CRUD + batch + search
pattern.  Specialised merge() methods are added where the HubSpot API
supports the /merge endpoint for that object type.

TaxRatesClient is standalone (different base path: /tax-rates/{version}/).
"""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient
from hubspot_sdk.core.models import HubSpotObject, PaginatedResult
from hubspot_sdk.crm.objects import CrmObjectClient

# ---------------------------------------------------------------------------
# Leads
# ---------------------------------------------------------------------------


class LeadsClient(CrmObjectClient):
    """Client for HubSpot Leads (object type: leads)."""

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "leads")

    async def merge(self, primary_id: str, object_id_to_merge: str) -> HubSpotObject:
        """Merge two lead records, keeping *primary_id* as the surviving record."""
        data = await self._http.post(
            f"{self._base}/merge",
            json={"primaryObjectId": primary_id, "objectIdToMerge": object_id_to_merge},
        )
        return HubSpotObject.model_validate(data)


# ---------------------------------------------------------------------------
# Feedback Submissions
# ---------------------------------------------------------------------------


class FeedbackSubmissionsClient(CrmObjectClient):
    """Client for HubSpot Feedback Submissions (object type: feedback_submissions).

    In practice this object type is read-only through the CRM objects API –
    submissions are created via the Feedback Surveys product, not the API.
    The full CrmObjectClient interface is exposed but only read operations
    will succeed in production portals.
    """

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "feedback_submissions")


# ---------------------------------------------------------------------------
# Contracts
# ---------------------------------------------------------------------------


class ContractsClient(CrmObjectClient):
    """Client for HubSpot Contracts (object type: contracts)."""

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "contracts")


# ---------------------------------------------------------------------------
# Projects
# ---------------------------------------------------------------------------


class ProjectsClient(CrmObjectClient):
    """Client for HubSpot Projects (object type: projects)."""

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "projects")

    async def merge(self, primary_id: str, object_id_to_merge: str) -> HubSpotObject:
        """Merge two project records, keeping *primary_id* as the surviving record."""
        data = await self._http.post(
            f"{self._base}/merge",
            json={"primaryObjectId": primary_id, "objectIdToMerge": object_id_to_merge},
        )
        return HubSpotObject.model_validate(data)


# ---------------------------------------------------------------------------
# Goal Targets
# ---------------------------------------------------------------------------


class GoalTargetsClient(CrmObjectClient):
    """Client for HubSpot Goal Targets (object type: goal_targets)."""

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "goal_targets")


# ---------------------------------------------------------------------------
# CRM Users
# ---------------------------------------------------------------------------


class CrmUsersClient(CrmObjectClient):
    """Client for HubSpot Users via the CRM objects API (object type: users).

    Named *CrmUsersClient* to avoid collision with
    ``hubspot_sdk.settings.users.UserProvisioningClient``.
    """

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "users")


# ---------------------------------------------------------------------------
# Services  (numeric type ID)
# ---------------------------------------------------------------------------


class ServicesClient(CrmObjectClient):
    """Client for HubSpot Services (object type: 0-162)."""

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "0-162")


# ---------------------------------------------------------------------------
# Courses  (numeric type ID)
# ---------------------------------------------------------------------------


class CoursesClient(CrmObjectClient):
    """Client for HubSpot Courses (object type: 0-410)."""

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "0-410")


# ---------------------------------------------------------------------------
# Listings  (numeric type ID)
# ---------------------------------------------------------------------------


class ListingsClient(CrmObjectClient):
    """Client for HubSpot Listings (object type: 0-420)."""

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "0-420")


# ---------------------------------------------------------------------------
# Partner Clients  (limited CRUD – no single create or delete)
# ---------------------------------------------------------------------------


class PartnerClientsClient(CrmObjectClient):
    """Client for HubSpot Partner Clients (object type: partner_clients).

    This object type exposes a limited subset of the CRM objects API:
    single-object create and delete are not supported by HubSpot.
    The inherited ``create`` and ``delete`` methods are kept in the interface
    so callers receive the standard HubSpot API error rather than an
    AttributeError, making the limitation explicit at runtime.
    """

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "partner_clients")


# ---------------------------------------------------------------------------
# Partner Services  (limited CRUD)
# ---------------------------------------------------------------------------


class PartnerServicesClient(CrmObjectClient):
    """Client for HubSpot Partner Services (object type: partner_services).

    Like PartnerClientsClient, single-object create and delete are not
    supported by HubSpot for this type.
    """

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "partner_services")


# ---------------------------------------------------------------------------
# Tax Rates  (standalone – different base path)
# ---------------------------------------------------------------------------


class TaxRatesClient:
    """Client for the HubSpot Tax Rates API.

    Uses a dedicated base path that differs from the generic CRM objects
    pattern::

        GET /tax-rates/{version}/tax-rates
        GET /tax-rates/{version}/tax-rates/{taxRateId}

    This client does *not* extend CrmObjectClient.
    """

    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/tax-rates/{http.api_version}/tax-rates"

    async def list(
        self,
        *,
        limit: int = 10,
        after: str | None = None,
    ) -> PaginatedResult[HubSpotObject]:
        """List tax rates with optional cursor-based pagination."""
        params: dict[str, Any] = {"limit": limit}
        if after:
            params["after"] = after

        data = await self._http.get(self._base, params=params)
        return PaginatedResult[HubSpotObject].model_validate(data)

    async def get(self, tax_rate_id: str) -> HubSpotObject:
        """Retrieve a single tax rate by its ID."""
        data = await self._http.get(f"{self._base}/{tax_rate_id}")
        return HubSpotObject.model_validate(data)
