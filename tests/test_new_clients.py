"""Tests for all new HubSpot SDK clients.

Covers:
    - Group 1: CRM activity clients (calls, emails, meetings, notes, tasks,
      communications, postal_mail)
    - Group 2: Commerce clients (products, line_items, quotes, invoices, orders,
      carts, payments, commerce_subscriptions, discounts, fees, taxes)
    - Group 3: Extended CRM object clients (leads, feedback_submissions,
      contracts, projects, goal_targets, crm_users, services, courses, listings,
      partner_clients, partner_services, tax_rates)
    - Group 4: Specialised domain clients (timeline, transcriptions,
      property_validations, limits, forecasts, object_library,
      meetings_scheduler, visitor_identification, data_sources, feature_flags)
"""

from __future__ import annotations

import re

import pytest

from hubspot_sdk import HubSpotClient

# ---------------------------------------------------------------------------
# Shared response helpers
# ---------------------------------------------------------------------------

_LIST_RESPONSE = {
    "results": [{"id": "1", "properties": {"name": "Test"}}],
    "paging": None,
}

_MERGE_RESPONSE = {"id": "1", "properties": {"name": "Merged"}}


# ===========================================================================
# Group 1 – CRM Activity Clients
# ===========================================================================


@pytest.mark.asyncio
async def test_calls_list(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/calls.*"),
        json=_LIST_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.calls.list(limit=1)
    assert len(result.results) == 1
    assert result.results[0].id == "1"
    await client.close()


@pytest.mark.asyncio
async def test_calls_merge(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/calls/merge"),
        json=_MERGE_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.calls.merge("1", "2")
    assert result.id == "1"
    await client.close()


@pytest.mark.asyncio
async def test_emails_list(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/emails.*"),
        json=_LIST_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.emails.list(limit=1)
    assert len(result.results) == 1
    await client.close()


@pytest.mark.asyncio
async def test_emails_merge(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/emails/merge"),
        json=_MERGE_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.emails.merge("1", "2")
    assert result.id == "1"
    await client.close()


@pytest.mark.asyncio
async def test_meetings_list(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/meetings.*"),
        json=_LIST_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.meetings.list(limit=1)
    assert len(result.results) == 1
    await client.close()


@pytest.mark.asyncio
async def test_meetings_merge(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/meetings/merge"),
        json=_MERGE_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.meetings.merge("1", "2")
    assert result.id == "1"
    await client.close()


@pytest.mark.asyncio
async def test_notes_list(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/notes.*"),
        json=_LIST_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.notes.list(limit=1)
    assert len(result.results) == 1
    await client.close()


@pytest.mark.asyncio
async def test_notes_merge(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/notes/merge"),
        json=_MERGE_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.notes.merge("1", "2")
    assert result.id == "1"
    await client.close()


@pytest.mark.asyncio
async def test_tasks_list(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/tasks.*"),
        json=_LIST_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.tasks.list(limit=1)
    assert len(result.results) == 1
    await client.close()


@pytest.mark.asyncio
async def test_tasks_merge(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/tasks/merge"),
        json=_MERGE_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.tasks.merge("1", "2")
    assert result.id == "1"
    await client.close()


@pytest.mark.asyncio
async def test_communications_list(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/communications.*"),
        json=_LIST_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.communications.list(limit=1)
    assert len(result.results) == 1
    await client.close()


@pytest.mark.asyncio
async def test_postal_mail_list(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/postal_mail.*"),
        json=_LIST_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.postal_mail.list(limit=1)
    assert len(result.results) == 1
    await client.close()


# ===========================================================================
# Group 2 – Commerce Clients
# ===========================================================================


@pytest.mark.asyncio
async def test_products_list(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/products.*"),
        json=_LIST_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.products.list(limit=1)
    assert len(result.results) == 1
    await client.close()


@pytest.mark.asyncio
async def test_products_merge(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/products/merge"),
        json=_MERGE_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.products.merge("1", "2")
    assert result.id == "1"
    await client.close()


@pytest.mark.asyncio
async def test_line_items_list(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/line_items.*"),
        json=_LIST_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.line_items.list(limit=1)
    assert len(result.results) == 1
    await client.close()


@pytest.mark.asyncio
async def test_quotes_list(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/quotes.*"),
        json=_LIST_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.quotes.list(limit=1)
    assert len(result.results) == 1
    await client.close()


@pytest.mark.asyncio
async def test_invoices_list(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/invoices.*"),
        json=_LIST_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.invoices.list(limit=1)
    assert len(result.results) == 1
    await client.close()


@pytest.mark.asyncio
async def test_orders_list(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/orders.*"),
        json=_LIST_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.orders.list(limit=1)
    assert len(result.results) == 1
    await client.close()


@pytest.mark.asyncio
async def test_carts_list(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/carts.*"),
        json=_LIST_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.carts.list(limit=1)
    assert len(result.results) == 1
    await client.close()


@pytest.mark.asyncio
async def test_payments_list(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/commerce_payments.*"),
        json=_LIST_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.payments.list(limit=1)
    assert len(result.results) == 1
    await client.close()


@pytest.mark.asyncio
async def test_commerce_subscriptions_list(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/subscriptions.*"),
        json=_LIST_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.commerce_subscriptions.list(limit=1)
    assert len(result.results) == 1
    await client.close()


@pytest.mark.asyncio
async def test_discounts_list(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/discounts.*"),
        json=_LIST_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.discounts.list(limit=1)
    assert len(result.results) == 1
    await client.close()


@pytest.mark.asyncio
async def test_fees_list(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/fees.*"),
        json=_LIST_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.fees.list(limit=1)
    assert len(result.results) == 1
    await client.close()


@pytest.mark.asyncio
async def test_taxes_list(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/taxes.*"),
        json=_LIST_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.taxes.list(limit=1)
    assert len(result.results) == 1
    await client.close()


# ===========================================================================
# Group 3 – Extended CRM Object Clients
# ===========================================================================


@pytest.mark.asyncio
async def test_leads_list(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/leads.*"),
        json=_LIST_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.leads.list(limit=1)
    assert len(result.results) == 1
    await client.close()


@pytest.mark.asyncio
async def test_leads_merge(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/leads/merge"),
        json=_MERGE_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.leads.merge("1", "2")
    assert result.id == "1"
    await client.close()


@pytest.mark.asyncio
async def test_feedback_submissions_list(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/feedback_submissions.*"),
        json=_LIST_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.feedback_submissions.list(limit=1)
    assert len(result.results) == 1
    await client.close()


@pytest.mark.asyncio
async def test_contracts_list(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/contracts.*"),
        json=_LIST_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.contracts.list(limit=1)
    assert len(result.results) == 1
    await client.close()


@pytest.mark.asyncio
async def test_projects_list(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/projects.*"),
        json=_LIST_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.projects.list(limit=1)
    assert len(result.results) == 1
    await client.close()


@pytest.mark.asyncio
async def test_projects_merge(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/projects/merge"),
        json=_MERGE_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.projects.merge("1", "2")
    assert result.id == "1"
    await client.close()


@pytest.mark.asyncio
async def test_goal_targets_list(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/goal_targets.*"),
        json=_LIST_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.goal_targets.list(limit=1)
    assert len(result.results) == 1
    await client.close()


@pytest.mark.asyncio
async def test_crm_users_list(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/users.*"),
        json=_LIST_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.crm_users.list(limit=1)
    assert len(result.results) == 1
    await client.close()


@pytest.mark.asyncio
async def test_services_list(httpx_mock):
    # ServicesClient uses numeric object type 0-162
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/0-162.*"),
        json=_LIST_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.services.list(limit=1)
    assert len(result.results) == 1
    await client.close()


@pytest.mark.asyncio
async def test_courses_list(httpx_mock):
    # CoursesClient uses numeric object type 0-410
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/0-410.*"),
        json=_LIST_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.courses.list(limit=1)
    assert len(result.results) == 1
    await client.close()


@pytest.mark.asyncio
async def test_listings_list(httpx_mock):
    # ListingsClient uses numeric object type 0-420
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/0-420.*"),
        json=_LIST_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.listings.list(limit=1)
    assert len(result.results) == 1
    await client.close()


@pytest.mark.asyncio
async def test_partner_clients_list(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/partner_clients.*"),
        json=_LIST_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.partner_clients.list(limit=1)
    assert len(result.results) == 1
    await client.close()


@pytest.mark.asyncio
async def test_partner_services_list(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/objects/.*/partner_services.*"),
        json=_LIST_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.partner_services.list(limit=1)
    assert len(result.results) == 1
    await client.close()


@pytest.mark.asyncio
async def test_tax_rates_list(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/tax-rates/.*/tax-rates.*"),
        json=_LIST_RESPONSE,
    )
    client = HubSpotClient("test-token")
    result = await client.tax_rates.list(limit=1)
    assert len(result.results) == 1
    await client.close()


@pytest.mark.asyncio
async def test_tax_rates_get(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/tax-rates/.*/tax-rates/123.*"),
        json={"id": "123", "properties": {"name": "Standard VAT"}},
    )
    client = HubSpotClient("test-token")
    result = await client.tax_rates.get("123")
    assert result.id == "123"
    await client.close()


# ===========================================================================
# Group 4 – Specialised Domain Clients
# ===========================================================================

# -- Timeline ----------------------------------------------------------------


@pytest.mark.asyncio
async def test_timeline_send_event(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/integrators/timeline/.*/events$"),
        json={"status": "PENDING"},
        status_code=200,
    )
    client = HubSpotClient("test-token")
    result = await client.timeline.send_event(
        {"eventTemplateId": "tpl-1", "objectId": "42"}
    )
    assert result["status"] == "PENDING"
    await client.close()


@pytest.mark.asyncio
async def test_timeline_send_events_batch(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/integrators/timeline/.*/events/batch"),
        json={"status": "COMPLETE", "results": []},
    )
    client = HubSpotClient("test-token")
    result = await client.timeline.send_events_batch(
        [{"eventTemplateId": "tpl-1", "objectId": "42"}]
    )
    assert result["status"] == "COMPLETE"
    await client.close()


@pytest.mark.asyncio
async def test_timeline_resolve_event_type(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/integrators/timeline/.*/types/projects"),
        json={"eventTemplateId": "tpl-99"},
    )
    client = HubSpotClient("test-token")
    result = await client.timeline.resolve_event_type("DEAL_SIGNED", "my-project")
    assert "eventTemplateId" in result
    await client.close()


# -- Transcriptions ----------------------------------------------------------


@pytest.mark.asyncio
async def test_transcriptions_complete_inbound_call(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/extensions/calling/.*/inbound-call"),
        json={"engagementId": 101},
        status_code=200,
    )
    client = HubSpotClient("test-token")
    result = await client.transcriptions.complete_inbound_call(
        {"fromNumber": "+1555000001", "toNumber": "+1555000002"}
    )
    assert result["engagementId"] == 101
    await client.close()


@pytest.mark.asyncio
async def test_transcriptions_create_transcript(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/extensions/calling/.*/transcripts$"),
        json={"id": "txn-1"},
        status_code=200,
    )
    client = HubSpotClient("test-token")
    result = await client.transcriptions.create_transcript(
        engagement_id=101,
        utterances=[{"speaker": "agent", "text": "Hello!"}],
    )
    assert result["id"] == "txn-1"
    await client.close()


@pytest.mark.asyncio
async def test_transcriptions_get_transcript(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/extensions/calling/.*/transcripts/txn-1"),
        json={"id": "txn-1", "utterances": []},
    )
    client = HubSpotClient("test-token")
    result = await client.transcriptions.get_transcript("txn-1")
    assert result["id"] == "txn-1"
    await client.close()


@pytest.mark.asyncio
async def test_transcriptions_delete_transcript(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/extensions/calling/.*/transcripts/txn-1"),
        status_code=204,
    )
    client = HubSpotClient("test-token")
    await client.transcriptions.delete_transcript("txn-1")
    await client.close()


# -- Property Validations ----------------------------------------------------


@pytest.mark.asyncio
async def test_property_validations_list_rules(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/property-validations/.*/0-1$"),
        json={"objectTypeId": "0-1", "rules": []},
    )
    client = HubSpotClient("test-token")
    result = await client.property_validations.list_rules("0-1")
    assert result["objectTypeId"] == "0-1"
    await client.close()


@pytest.mark.asyncio
async def test_property_validations_get_property_rules(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/property-validations/.*/0-1/email$"),
        json={"propertyName": "email", "rules": []},
    )
    client = HubSpotClient("test-token")
    result = await client.property_validations.get_property_rules("0-1", "email")
    assert result["propertyName"] == "email"
    await client.close()


@pytest.mark.asyncio
async def test_property_validations_get_rule(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/property-validations/.*/0-1/email/rule-type/REGEX"),
        json={"ruleType": "REGEX", "ruleArguments": []},
    )
    client = HubSpotClient("test-token")
    result = await client.property_validations.get_rule("0-1", "email", "REGEX")
    assert result["ruleType"] == "REGEX"
    await client.close()


@pytest.mark.asyncio
async def test_property_validations_update_rule(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/property-validations/.*/0-1/email/rule-type/REGEX"),
        status_code=204,
    )
    client = HubSpotClient("test-token")
    await client.property_validations.update_rule(
        "0-1",
        "email",
        "REGEX",
        rule_arguments=[{"value": r".*@example\.com"}],
    )
    await client.close()


# -- Limits ------------------------------------------------------------------


@pytest.mark.asyncio
async def test_limits_records(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/limits/.*/records$"),
        json={"limit": 1000000, "used": 5000},
    )
    client = HubSpotClient("test-token")
    result = await client.limits.records()
    assert "limit" in result
    await client.close()


@pytest.mark.asyncio
async def test_limits_pipelines(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/limits/.*/pipelines$"),
        json={"limit": 50, "used": 3},
    )
    client = HubSpotClient("test-token")
    result = await client.limits.pipelines()
    assert "limit" in result
    await client.close()


@pytest.mark.asyncio
async def test_limits_custom_properties(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/limits/.*/custom-properties$"),
        json={"limit": 1000, "used": 42},
    )
    client = HubSpotClient("test-token")
    result = await client.limits.custom_properties()
    assert "limit" in result
    await client.close()


# -- Forecasts ---------------------------------------------------------------


@pytest.mark.asyncio
async def test_forecasts_list(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/forecast-settings/v3/forecast-types$"),
        json={"results": [{"id": "ft-1", "name": "Commit"}]},
    )
    client = HubSpotClient("test-token")
    result = await client.forecasts.list()
    assert result["results"][0]["id"] == "ft-1"
    await client.close()


@pytest.mark.asyncio
async def test_forecasts_get(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/forecast-settings/v3/forecast-types/ft-1"),
        json={"id": "ft-1", "name": "Commit"},
    )
    client = HubSpotClient("test-token")
    result = await client.forecasts.get("ft-1")
    assert result["id"] == "ft-1"
    await client.close()


# -- Object Library ----------------------------------------------------------


@pytest.mark.asyncio
async def test_object_library_list_enablement(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/object-library/.*/enablement$"),
        json={"results": [{"objectTypeId": "0-1", "enabled": True}]},
    )
    client = HubSpotClient("test-token")
    result = await client.object_library.list_enablement()
    assert "results" in result
    await client.close()


@pytest.mark.asyncio
async def test_object_library_get_enablement(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/crm/object-library/.*/enablement/0-1"),
        json={"objectTypeId": "0-1", "enabled": True},
    )
    client = HubSpotClient("test-token")
    result = await client.object_library.get_enablement("0-1")
    assert result["objectTypeId"] == "0-1"
    await client.close()


# -- Meetings Scheduler ------------------------------------------------------


@pytest.mark.asyncio
async def test_meetings_scheduler_list_meeting_links(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/scheduler/.*/meetings/meeting-links(\?.*)?$"),
        json={"results": [{"slug": "my-meeting", "name": "Intro Call"}]},
    )
    client = HubSpotClient("test-token")
    result = await client.meetings_scheduler.list_meeting_links(limit=10)
    assert result["results"][0]["slug"] == "my-meeting"
    await client.close()


@pytest.mark.asyncio
async def test_meetings_scheduler_book_meeting(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/scheduler/.*/meetings/meeting-links/book$"),
        json={"id": "booking-99", "slug": "my-meeting"},
        status_code=200,
    )
    client = HubSpotClient("test-token")
    result = await client.meetings_scheduler.book_meeting(
        {"slug": "my-meeting", "startTime": "2026-04-10T10:00:00Z"}
    )
    assert result["id"] == "booking-99"
    await client.close()


@pytest.mark.asyncio
async def test_meetings_scheduler_get_availability(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/scheduler/.*/meetings/meeting-links/book/availability-page/my-meeting"),
        json={"slots": []},
    )
    client = HubSpotClient("test-token")
    result = await client.meetings_scheduler.get_availability(
        "my-meeting", "Europe/Amsterdam"
    )
    assert "slots" in result
    await client.close()


# -- Visitor Identification --------------------------------------------------


@pytest.mark.asyncio
async def test_visitor_identification_generate_token(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/visitor-identification/.*/tokens/create"),
        json={"token": "vis-tok-abc123"},
    )
    client = HubSpotClient("test-token")
    result = await client.visitor_identification.generate_token(
        "visitor@example.com",
        first_name="Alice",
        last_name="Smith",
    )
    assert result["token"] == "vis-tok-abc123"
    await client.close()


# -- Data Sources ------------------------------------------------------------


@pytest.mark.asyncio
async def test_data_sources_create(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/data-studio/.*/data-source$"),
        json={"id": "ds-1", "name": "My Source"},
        status_code=200,
    )
    client = HubSpotClient("test-token")
    result = await client.data_sources.create({"name": "My Source"})
    assert result["id"] == "ds-1"
    await client.close()


@pytest.mark.asyncio
async def test_data_sources_get(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/data-studio/.*/data-source/ds-1"),
        json={"id": "ds-1", "name": "My Source"},
    )
    client = HubSpotClient("test-token")
    result = await client.data_sources.get("ds-1")
    assert result["id"] == "ds-1"
    await client.close()


@pytest.mark.asyncio
async def test_data_sources_update(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/data-studio/.*/data-source/ds-1"),
        json={"id": "ds-1", "name": "Renamed Source"},
    )
    client = HubSpotClient("test-token")
    result = await client.data_sources.update("ds-1", {"name": "Renamed Source"})
    assert result["name"] == "Renamed Source"
    await client.close()


@pytest.mark.asyncio
async def test_data_sources_delete(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/data-studio/.*/data-source/ds-1"),
        status_code=204,
    )
    client = HubSpotClient("test-token")
    await client.data_sources.delete("ds-1")
    await client.close()


# -- Feature Flags -----------------------------------------------------------


@pytest.mark.asyncio
async def test_feature_flags_list_all(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/feature-flags/.*/app123/flags/all"),
        json={"flags": [{"name": "beta-ui", "defaultValue": False}]},
    )
    client = HubSpotClient("test-token")
    result = await client.feature_flags("app123").list_all()
    assert result["flags"][0]["name"] == "beta-ui"
    await client.close()


@pytest.mark.asyncio
async def test_feature_flags_get(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/feature-flags/.*/app123/flags/beta-ui$"),
        json={"name": "beta-ui", "defaultValue": False},
    )
    client = HubSpotClient("test-token")
    result = await client.feature_flags("app123").get("beta-ui")
    assert result["name"] == "beta-ui"
    await client.close()


@pytest.mark.asyncio
async def test_feature_flags_set(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/feature-flags/.*/app123/flags/beta-ui$"),
        json={"name": "beta-ui", "defaultValue": True},
    )
    client = HubSpotClient("test-token")
    result = await client.feature_flags("app123").set("beta-ui", default_value=True)
    assert result["defaultValue"] is True
    await client.close()


@pytest.mark.asyncio
async def test_feature_flags_delete(httpx_mock):
    httpx_mock.add_response(
        url=re.compile(r".*/feature-flags/.*/app123/flags/beta-ui$"),
        status_code=204,
    )
    client = HubSpotClient("test-token")
    await client.feature_flags("app123").delete("beta-ui")
    await client.close()
