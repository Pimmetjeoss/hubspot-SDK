"""Custom exceptions for the HubSpot SDK."""

from __future__ import annotations

from typing import Any


class HubSpotError(Exception):
    """Base exception for all HubSpot SDK errors."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response_body: dict[str, Any] | None = None,
        correlation_id: str | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body or {}
        self.correlation_id = correlation_id

    def __str__(self) -> str:
        parts = [super().__str__()]
        if self.status_code:
            parts.append(f"status={self.status_code}")
        if self.correlation_id:
            parts.append(f"correlation_id={self.correlation_id}")
        return " | ".join(parts)


class HubSpotAuthError(HubSpotError):
    """Authentication or authorization failure (401/403)."""


class HubSpotNotFoundError(HubSpotError):
    """Resource not found (404)."""


class HubSpotRateLimitError(HubSpotError):
    """Rate limit exceeded (429)."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: float | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(message, **kwargs)
        self.retry_after = retry_after


class HubSpotValidationError(HubSpotError):
    """Request validation error (400)."""

    def __init__(
        self,
        message: str = "Validation error",
        errors: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(message, **kwargs)
        self.errors = errors or []


class HubSpotConflictError(HubSpotError):
    """Conflict error (409)."""


class HubSpotServerError(HubSpotError):
    """Server error (5xx)."""
