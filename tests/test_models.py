"""Tests for Pydantic models."""

from __future__ import annotations

from hubspot_sdk.core.models import (
    HubSpotObject,
    PaginatedResult,
    SearchResult,
    BatchResult,
    Paging,
)


def test_hubspot_object_basic():
    obj = HubSpotObject(id="123", properties={"email": "test@example.com"})
    assert obj.id == "123"
    assert obj.properties["email"] == "test@example.com"
    assert obj.archived is False


def test_hubspot_object_from_api():
    data = {
        "id": "456",
        "properties": {"firstname": "John", "lastname": "Doe"},
        "createdAt": "2024-01-01T00:00:00Z",
        "updatedAt": "2024-06-15T12:00:00Z",
        "archived": False,
    }
    obj = HubSpotObject.model_validate(data)
    assert obj.id == "456"
    assert obj.created_at is not None


def test_paginated_result():
    data = {
        "results": [
            {"id": "1", "properties": {}},
            {"id": "2", "properties": {}},
        ],
        "paging": {"next": {"after": "2", "link": "https://api.hubapi.com/..."}},
    }
    page = PaginatedResult[HubSpotObject].model_validate(data)
    assert len(page.results) == 2
    assert page.has_next is True
    assert page.next_after == "2"


def test_paginated_result_no_next():
    data = {"results": [{"id": "1", "properties": {}}]}
    page = PaginatedResult[HubSpotObject].model_validate(data)
    assert page.has_next is False
    assert page.next_after is None


def test_search_result():
    data = {
        "total": 42,
        "results": [{"id": "1", "properties": {"email": "a@b.com"}}],
        "paging": {"next": {"after": "10"}},
    }
    result = SearchResult[HubSpotObject].model_validate(data)
    assert result.total == 42
    assert len(result.results) == 1
    assert result.has_next is True


def test_batch_result():
    data = {
        "status": "COMPLETE",
        "results": [{"id": "1", "properties": {}}],
        "errors": [],
        "numErrors": 0,
        "startedAt": "2024-01-01T00:00:00Z",
        "completedAt": "2024-01-01T00:00:01Z",
    }
    batch = BatchResult[HubSpotObject].model_validate(data)
    assert batch.status == "COMPLETE"
    assert len(batch.results) == 1
    assert batch.num_errors == 0
