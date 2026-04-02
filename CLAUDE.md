# HubSpot SDK

Async-first Python SDK + CLI for the complete HubSpot API.

## Project structure

```
src/hubspot_sdk/       # SDK package
  core/                # HTTP client, models, exceptions, pagination
  auth/                # OAuth2 + private app token auth
  crm/                 # CRM objects, associations, pipelines, properties, lists, etc.
    objects.py         # Generic CrmObjectClient (CRUD + batch + search)
    contacts.py        # Contacts (merge, GDPR delete)
    companies.py       # Companies (merge, GDPR delete)
    deals.py           # Deals (merge, deal splits)
    tickets.py         # Tickets (merge)
    activities.py      # Calls, Emails, Meetings, Notes, Tasks, Communications, PostalMail
    extended_objects.py # Leads, FeedbackSubmissions, Contracts, Projects, GoalTargets, Users, Services, Courses, Listings, Partners, TaxRates
    associations.py    # Association CRUD + schema
    pipelines.py       # Pipeline stages
    properties.py      # Property CRUD
    property_validations.py # Validation rules
    lists.py           # List/segment management
    imports_exports.py # Data import/export
    schemas.py         # Custom object schema definitions
    owners.py          # CRM owners
    extensions.py      # Calling, CRM cards, video conferencing
    timeline.py        # Integrator timeline events
    transcriptions.py  # Call transcriptions
    limits.py          # Account limits tracking
    forecasts.py       # Forecast type settings
    object_library.py  # Object enablement status
    meetings_scheduler.py # Scheduler meetings/booking (not CRM meetings)
  commerce/            # Commerce objects (products, line_items, quotes, invoices, orders, carts, payments, subscriptions, discounts, fees, taxes)
  cms/                 # Pages, blog, HubDB, domains, source code, redirects
  marketing/           # Campaigns, forms, marketing events, transactional email
  automation/          # Workflow actions, sequences
  conversations/       # Threads, messages, custom channels, visitor identification
  events/              # Event definitions, send, occurrences
  files/               # File upload/management
  settings/            # Multicurrency, user provisioning, feature flags, data sources
  webhooks/            # Webhook subscriptions
  account/             # Account info, audit logs, business units, subscriptions
  client.py            # Main HubSpotClient facade
cli/                   # Click + Rich CLI
specs/                 # OpenAPI 3.0.1 specs (.json + .txt summaries)
tests/                 # pytest + pytest-httpx + pytest-asyncio
```

## Key design decisions

- **Generic CRM object client**: `CrmObjectClient` handles ~40 object types with identical CRUD + batch + search patterns. Specialized clients (ContactsClient, DealsClient, etc.) extend it for extra endpoints like merge, GDPR delete, deal splits.
- **Async-first**: All methods are async using httpx. Use `asyncio.run()` or `async with` context manager.
- **Lazy sub-client instantiation**: `HubSpotClient` properties create sub-clients on first access.
- **Pydantic models**: `HubSpotObject`, `PaginatedResult`, `SearchResult`, `BatchResult` for typed responses.
- **Auto-pagination**: `paginate()` and `paginate_search()` async generators.
- **Rate limit + retry**: Automatic exponential backoff on 429/5xx with Retry-After support.

## Dev commands

```bash
pip install -e ".[dev]"
pytest
ruff check src/ cli/ tests/
mypy src/
```

## API version

All endpoints use version `2026-03` by default (configurable via `api_version` param).

## Specs

102 OpenAPI specs in `specs/`, covering 1128 endpoints across 10 categories.
3 specs have encoding issues: marketingEmails, marketingEmailsV3, mediaBridge.
