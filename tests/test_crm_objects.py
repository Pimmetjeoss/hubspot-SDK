"""Tests for the generic CRM object client."""

from __future__ import annotations

import re

import pytest

from hubspot_sdk import HubSpotClient


@pytest.mark.asyncio
async def test_contacts_list(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/contacts.*"),
        json={
            "results": [
                {"id": "1", "properties": {"email": "test@example.com", "firstname": "Test"}},
                {"id": "2", "properties": {"email": "user@example.com", "firstname": "User"}},
            ],
            "paging": None,
        },
    )
    client = HubSpotClient("test-token")
    result = await client.contacts.list(limit=2)
    assert len(result.results) == 2
    assert result.results[0].properties["email"] == "test@example.com"
    await client.close()


@pytest.mark.asyncio
async def test_contacts_get(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/contacts/123.*"),
        json={"id": "123", "properties": {"email": "test@example.com"}},
    )
    client = HubSpotClient("test-token")
    result = await client.contacts.get("123")
    assert result.id == "123"
    await client.close()


@pytest.mark.asyncio
async def test_contacts_create(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/contacts$"),
        json={"id": "999", "properties": {"email": "new@example.com"}},
        status_code=201,
    )
    client = HubSpotClient("test-token")
    result = await client.contacts.create({"email": "new@example.com"})
    assert result.id == "999"
    await client.close()


@pytest.mark.asyncio
async def test_contacts_search(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/contacts/search"),
        json={
            "total": 1,
            "results": [{"id": "1", "properties": {"email": "found@example.com"}}],
        },
    )
    client = HubSpotClient("test-token")
    result = await client.contacts.search(query="found@example.com")
    assert result.total == 1
    await client.close()


@pytest.mark.asyncio
async def test_contacts_batch_create(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/contacts/batch/create"),
        json={
            "status": "COMPLETE",
            "results": [
                {"id": "10", "properties": {"email": "a@b.com"}},
                {"id": "11", "properties": {"email": "c@d.com"}},
            ],
        },
    )
    client = HubSpotClient("test-token")
    result = await client.contacts.batch_create([
        {"properties": {"email": "a@b.com"}},
        {"properties": {"email": "c@d.com"}},
    ])
    assert len(result.results) == 2
    await client.close()


@pytest.mark.asyncio
async def test_contacts_delete(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/contacts/123"),
        status_code=204,
    )
    client = HubSpotClient("test-token")
    await client.contacts.delete("123")
    await client.close()


@pytest.mark.asyncio
async def test_generic_objects_client(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/line_items.*"),
        json={
            "results": [{"id": "1", "properties": {"name": "Widget"}}],
        },
    )
    client = HubSpotClient("test-token")
    result = await client.objects("line_items").list(limit=1)
    assert len(result.results) == 1
    await client.close()


@pytest.mark.asyncio
async def test_contacts_merge(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/contacts/merge"),
        json={"id": "1", "properties": {"email": "merged@example.com"}},
    )
    client = HubSpotClient("test-token")
    result = await client.contacts.merge("1", "2")
    assert result.id == "1"
    await client.close()
