"""Generic CRM object client covering the standard CRUD + batch + search pattern.

This single class handles ~40 object types that share identical endpoint
structures (contacts, companies, deals, tickets, line_items, products,
quotes, tasks, notes, emails, calls, meetings, communications, postal_mail,
feedback_submissions, invoices, orders, carts, subscriptions, commerce_payments,
taxes, fees, discounts, leads, contracts, goal_targets, users, projects,
services, courses, listings, partner_clients, partner_services, custom objects, etc.).
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any

from hubspot_sdk.core.http import HttpClient
from hubspot_sdk.core.models import (
    BatchResult,
    HubSpotObject,
    PaginatedResult,
    SearchResult,
)
from hubspot_sdk.core.pagination import paginate, paginate_search


class CrmObjectClient:
    """Client for a single CRM object type.

    Covers endpoints:
        GET    /crm/objects/{version}/{objectType}
        POST   /crm/objects/{version}/{objectType}
        GET    /crm/objects/{version}/{objectType}/{id}
        PATCH  /crm/objects/{version}/{objectType}/{id}
        DELETE /crm/objects/{version}/{objectType}/{id}
        POST   /crm/objects/{version}/{objectType}/batch/archive
        POST   /crm/objects/{version}/{objectType}/batch/create
        POST   /crm/objects/{version}/{objectType}/batch/read
        POST   /crm/objects/{version}/{objectType}/batch/update
        POST   /crm/objects/{version}/{objectType}/batch/upsert
        POST   /crm/objects/{version}/{objectType}/search
        PUT    /crm/objects/{version}/{fromType}/{fromId}/associations/default/{toType}/{toId}
        DELETE /crm/objects/{version}/{objectType}/{id}/associations/{toType}/{toId}
        PUT    /crm/objects/{version}/{objectType}/{id}/associations/{toType}/{toId}
    """

    def __init__(self, http: HttpClient, object_type: str) -> None:
        self._http = http
        self.object_type = object_type
        self._base = f"/crm/objects/{http.api_version}/{object_type}"

    # -- Single-object CRUD ---------------------------------------------------

    async def list(
        self,
        *,
        limit: int = 10,
        after: str | None = None,
        properties: list[str] | None = None,
        properties_with_history: list[str] | None = None,
        associations: list[str] | None = None,
        archived: bool = False,
    ) -> PaginatedResult[HubSpotObject]:
        """List objects with pagination."""
        params: dict[str, Any] = {
            "limit": limit,
            "archived": archived,
        }
        if after:
            params["after"] = after
        if properties:
            params["properties"] = ",".join(properties)
        if properties_with_history:
            params["propertiesWithHistory"] = ",".join(properties_with_history)
        if associations:
            params["associations"] = ",".join(associations)

        data = await self._http.get(self._base, params=params)
        return PaginatedResult[HubSpotObject].model_validate(data)

    async def list_all(
        self,
        *,
        properties: list[str] | None = None,
        associations: list[str] | None = None,
        archived: bool = False,
        max_items: int | None = None,
    ) -> AsyncIterator[HubSpotObject]:
        """Auto-paginate through all objects."""
        params: dict[str, Any] = {"archived": archived}
        if properties:
            params["properties"] = ",".join(properties)
        if associations:
            params["associations"] = ",".join(associations)

        async for obj in paginate(
            lambda **kw: self._http.get(self._base, **kw),
            params=params,
            limit=100,
            max_items=max_items,
        ):
            yield obj

    async def get(
        self,
        object_id: str,
        *,
        properties: list[str] | None = None,
        properties_with_history: list[str] | None = None,
        associations: list[str] | None = None,
        id_property: str | None = None,
        archived: bool = False,
    ) -> HubSpotObject:
        """Get a single object by ID."""
        params: dict[str, Any] = {"archived": archived}
        if properties:
            params["properties"] = ",".join(properties)
        if properties_with_history:
            params["propertiesWithHistory"] = ",".join(properties_with_history)
        if associations:
            params["associations"] = ",".join(associations)
        if id_property:
            params["idProperty"] = id_property

        data = await self._http.get(f"{self._base}/{object_id}", params=params)
        return HubSpotObject.model_validate(data)

    async def create(
        self,
        properties: dict[str, str],
        *,
        associations: list[dict[str, Any]] | None = None,
    ) -> HubSpotObject:
        """Create a new object."""
        body: dict[str, Any] = {"properties": properties}
        if associations:
            body["associations"] = associations
        data = await self._http.post(self._base, json=body)
        return HubSpotObject.model_validate(data)

    async def update(
        self,
        object_id: str,
        properties: dict[str, str],
        *,
        id_property: str | None = None,
    ) -> HubSpotObject:
        """Update an existing object."""
        params: dict[str, Any] = {}
        if id_property:
            params["idProperty"] = id_property
        data = await self._http.patch(
            f"{self._base}/{object_id}",
            json={"properties": properties},
        )
        return HubSpotObject.model_validate(data)

    async def delete(self, object_id: str) -> None:
        """Archive (soft-delete) an object."""
        await self._http.delete(f"{self._base}/{object_id}")

    # -- Batch operations -----------------------------------------------------

    async def batch_create(
        self,
        inputs: list[dict[str, Any]],
    ) -> BatchResult[HubSpotObject]:
        """Batch create objects."""
        data = await self._http.post(
            f"{self._base}/batch/create",
            json={"inputs": inputs},
        )
        return BatchResult[HubSpotObject].model_validate(data)

    async def batch_read(
        self,
        ids: list[str] | None = None,
        *,
        id_property: str | None = None,
        properties: list[str] | None = None,
        inputs: list[dict[str, Any]] | None = None,
        archived: bool = False,
    ) -> BatchResult[HubSpotObject]:
        """Batch read objects by ID."""
        body: dict[str, Any] = {}
        if inputs:
            body["inputs"] = inputs
        elif ids:
            body["inputs"] = [{"id": i} for i in ids]
        if properties:
            body["properties"] = properties
        if id_property:
            body["idProperty"] = id_property

        data = await self._http.post(
            f"{self._base}/batch/read",
            json=body,
            params={"archived": archived} if archived else None,
        )
        return BatchResult[HubSpotObject].model_validate(data)

    async def batch_update(
        self,
        inputs: list[dict[str, Any]],
    ) -> BatchResult[HubSpotObject]:
        """Batch update objects."""
        data = await self._http.post(
            f"{self._base}/batch/update",
            json={"inputs": inputs},
        )
        return BatchResult[HubSpotObject].model_validate(data)

    async def batch_upsert(
        self,
        inputs: list[dict[str, Any]],
    ) -> BatchResult[HubSpotObject]:
        """Batch upsert (create or update) objects."""
        data = await self._http.post(
            f"{self._base}/batch/upsert",
            json={"inputs": inputs},
        )
        return BatchResult[HubSpotObject].model_validate(data)

    async def batch_archive(self, ids: list[str]) -> None:
        """Batch archive objects."""
        await self._http.post(
            f"{self._base}/batch/archive",
            json={"inputs": [{"id": i} for i in ids]},
        )

    # -- Search ---------------------------------------------------------------

    async def search(
        self,
        *,
        filter_groups: list[dict[str, Any]] | None = None,
        query: str | None = None,
        sorts: list[dict[str, str]] | None = None,
        properties: list[str] | None = None,
        limit: int = 10,
        after: str | None = None,
    ) -> SearchResult[HubSpotObject]:
        """Search objects with filters and/or full-text query."""
        body: dict[str, Any] = {"limit": limit}
        if filter_groups:
            body["filterGroups"] = filter_groups
        if query:
            body["query"] = query
        if sorts:
            body["sorts"] = sorts
        if properties:
            body["properties"] = properties
        if after:
            body["after"] = after

        data = await self._http.post(f"{self._base}/search", json=body)
        return SearchResult[HubSpotObject].model_validate(data)

    async def search_all(
        self,
        *,
        filter_groups: list[dict[str, Any]] | None = None,
        query: str | None = None,
        sorts: list[dict[str, str]] | None = None,
        properties: list[str] | None = None,
        max_items: int | None = None,
    ) -> AsyncIterator[HubSpotObject]:
        """Auto-paginate through all search results."""
        body: dict[str, Any] = {"limit": 100}
        if filter_groups:
            body["filterGroups"] = filter_groups
        if query:
            body["query"] = query
        if sorts:
            body["sorts"] = sorts
        if properties:
            body["properties"] = properties

        async for obj in paginate_search(
            lambda **kw: self._http.post(f"{self._base}/search", **kw),
            json_body=body,
            max_items=max_items,
        ):
            yield obj

    # -- Associations (inline on the object) ----------------------------------

    async def set_association(
        self,
        object_id: str,
        to_object_type: str,
        to_object_id: str,
        *,
        association_specs: list[dict[str, Any]] | None = None,
    ) -> Any:
        """Create an association from this object to another."""
        base = f"/crm/objects/{self._http.api_version}"
        if association_specs:
            return await self._http.put(
                f"{base}/{self.object_type}/{object_id}/associations/{to_object_type}/{to_object_id}",
                json=association_specs,
            )
        return await self._http.put(
            f"{base}/{self.object_type}/{object_id}/associations/default/{to_object_type}/{to_object_id}",
        )

    async def remove_association(
        self,
        object_id: str,
        to_object_type: str,
        to_object_id: str,
    ) -> None:
        """Remove an association from this object to another."""
        base = f"/crm/objects/{self._http.api_version}"
        await self._http.delete(
            f"{base}/{self.object_type}/{object_id}/associations/{to_object_type}/{to_object_id}",
        )
