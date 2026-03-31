"""Async pagination helpers for HubSpot cursor-based APIs."""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any, Callable, TypeVar

from hubspot_sdk.core.models import HubSpotObject, PaginatedResult

T = TypeVar("T")


async def paginate(
    fetch: Callable[..., Any],
    *,
    params: dict[str, Any] | None = None,
    limit: int = 100,
    max_items: int | None = None,
) -> AsyncIterator[HubSpotObject]:
    """Auto-paginate a HubSpot list endpoint.

    Args:
        fetch: An async callable that accepts (params=) and returns raw dict.
        params: Base query parameters.
        limit: Page size per request.
        max_items: Stop after yielding this many items (None = all).

    Yields:
        HubSpotObject instances.
    """
    params = dict(params or {})
    params["limit"] = limit
    yielded = 0

    while True:
        data = await fetch(params=params)
        page = PaginatedResult[HubSpotObject].model_validate(data)

        for item in page.results:
            yield item
            yielded += 1
            if max_items and yielded >= max_items:
                return

        if not page.has_next:
            break
        params["after"] = page.next_after


async def paginate_search(
    fetch: Callable[..., Any],
    *,
    json_body: dict[str, Any],
    max_items: int | None = None,
) -> AsyncIterator[HubSpotObject]:
    """Auto-paginate a HubSpot search endpoint.

    Args:
        fetch: An async callable that accepts (json=) and returns raw dict.
        json_body: The search request body.
        max_items: Stop after yielding this many items (None = all).

    Yields:
        HubSpotObject instances.
    """
    body = dict(json_body)
    yielded = 0

    while True:
        from hubspot_sdk.core.models import SearchResult

        data = await fetch(json=body)
        page = SearchResult[HubSpotObject].model_validate(data)

        for item in page.results:
            yield item
            yielded += 1
            if max_items and yielded >= max_items:
                return

        if not page.has_next:
            break
        body["after"] = page.next_after


async def collect(aiter: AsyncIterator[T]) -> list[T]:
    """Collect all items from an async iterator into a list."""
    return [item async for item in aiter]
