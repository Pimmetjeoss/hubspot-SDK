"""Core infrastructure for the HubSpot SDK."""

from hubspot_sdk.core.exceptions import (
    HubSpotAuthError,
    HubSpotError,
    HubSpotNotFoundError,
    HubSpotRateLimitError,
    HubSpotValidationError,
)
from hubspot_sdk.core.http import HttpClient
from hubspot_sdk.core.models import (
    BatchResult,
    HubSpotObject,
    PaginatedResult,
    SearchResult,
)

__all__ = [
    "HubSpotError",
    "HubSpotAuthError",
    "HubSpotNotFoundError",
    "HubSpotRateLimitError",
    "HubSpotValidationError",
    "HttpClient",
    "HubSpotObject",
    "BatchResult",
    "PaginatedResult",
    "SearchResult",
]
