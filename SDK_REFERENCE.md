# HubSpot SDK – Complete Reference Guide

> **Version**: 0.1.0 | **API Version**: 2026-03 | **Python**: 3.12+ | **Async-first** via httpx

---

## Table of Contents

1. [Installation & Setup](#installation--setup)
2. [Authentication](#authentication)
3. [Quick Start](#quick-start)
4. [Architecture Overview](#architecture-overview)
5. [Error Handling](#error-handling)
6. [Pagination](#pagination)
7. [Data Models](#data-models)
8. [CRM – Core Objects](#crm--core-objects)
9. [CRM – Activities](#crm--activities)
10. [CRM – Commerce Objects](#crm--commerce-objects)
11. [CRM – Extended Objects](#crm--extended-objects)
12. [CRM – Associations](#crm--associations)
13. [CRM – Pipelines](#crm--pipelines)
14. [CRM – Properties](#crm--properties)
15. [CRM – Property Validations](#crm--property-validations)
16. [CRM – Lists (Segments)](#crm--lists-segments)
17. [CRM – Imports & Exports](#crm--imports--exports)
18. [CRM – Schemas (Custom Objects)](#crm--schemas-custom-objects)
19. [CRM – Owners](#crm--owners)
20. [CRM – Extensions](#crm--extensions)
21. [CRM – Timeline Events](#crm--timeline-events)
22. [CRM – Transcriptions](#crm--transcriptions)
23. [CRM – Limits Tracking](#crm--limits-tracking)
24. [CRM – Forecasts](#crm--forecasts)
25. [CRM – Object Library](#crm--object-library)
26. [CRM – Meetings Scheduler](#crm--meetings-scheduler)
27. [CMS – Pages](#cms--pages)
28. [CMS – Blog](#cms--blog)
29. [CMS – HubDB](#cms--hubdb)
30. [CMS – Domains](#cms--domains)
31. [CMS – Source Code](#cms--source-code)
32. [CMS – URL Redirects](#cms--url-redirects)
33. [CMS – Site Search](#cms--site-search)
34. [CMS – Audit Logs](#cms--audit-logs)
35. [Marketing – Campaigns](#marketing--campaigns)
36. [Marketing – Forms](#marketing--forms)
37. [Marketing – Events](#marketing--events)
38. [Marketing – Transactional Email](#marketing--transactional-email)
39. [Marketing – Single Send](#marketing--single-send)
40. [Automation – Workflow Actions](#automation--workflow-actions)
41. [Automation – Sequences](#automation--sequences)
42. [Conversations – Threads & Inbox](#conversations--threads--inbox)
43. [Conversations – Messages](#conversations--messages)
44. [Conversations – Custom Channels](#conversations--custom-channels)
45. [Conversations – Visitor Identification](#conversations--visitor-identification)
46. [Events – Definitions](#events--definitions)
47. [Events – Send](#events--send)
48. [Events – Occurrences](#events--occurrences)
49. [Files](#files)
50. [Settings – Currency](#settings--currency)
51. [Settings – User Provisioning](#settings--user-provisioning)
52. [Settings – Feature Flags](#settings--feature-flags)
53. [Settings – Data Sources](#settings--data-sources)
54. [Webhooks](#webhooks)
55. [Account – Info](#account--info)
56. [Account – Audit Logs](#account--audit-logs)
57. [Account – Business Units](#account--business-units)
58. [Account – Subscriptions](#account--subscriptions)
59. [OAuth](#oauth)

---

## Installation & Setup

```bash
# Install from source
git clone https://github.com/Pimmetjeoss/hubspot-SDK.git
cd hubspot-SDK
pip install -e ".[dev]"
```

### Dependencies

- `httpx` – Async HTTP client
- `pydantic` – Data validation and models
- `click` + `rich` – CLI interface (optional)
- `pytest` + `pytest-httpx` + `pytest-asyncio` – Testing (dev)

---

## Authentication

De SDK ondersteunt twee authenticatiemethoden:

### 1. Private App Token (aanbevolen voor server-side)

```python
from hubspot_sdk import HubSpotClient

# Direct met access token
async with HubSpotClient(access_token="pat-na1-xxxxx") as hs:
    contacts = await hs.contacts.list()
```

### 2. OAuth2 (voor apps die namens gebruikers handelen)

```python
from hubspot_sdk import HubSpotClient

# Stap 1: Genereer authorization URL
oauth = HubSpotClient.oauth(
    client_id="your-client-id",
    client_secret="your-client-secret",
    redirect_uri="https://yourapp.com/callback"
)
url = oauth.get_authorize_url(
    scopes=["crm.objects.contacts.read", "crm.objects.contacts.write"],
    state="random-state-value",
    optional_scopes=["crm.objects.deals.read"]  # optioneel
)

# Stap 2: Gebruiker stuurt authorization code terug
tokens = await oauth.exchange_code(code="auth-code-from-callback")
# tokens.access_token, tokens.refresh_token, tokens.expires_in

# Stap 3: Gebruik de access token
async with HubSpotClient(access_token=tokens.access_token) as hs:
    contacts = await hs.contacts.list()

# Stap 4: Refresh als token verlopen is
if tokens.is_expired:
    tokens = await oauth.refresh_token(refresh_token=tokens.refresh_token)

# Token introspection
info = await oauth.get_token_info(token=tokens.access_token)

# Token revocation
await oauth.revoke_token(token=tokens.refresh_token)
```

---

## Quick Start

```python
import asyncio
from hubspot_sdk import HubSpotClient

async def main():
    async with HubSpotClient(access_token="pat-na1-xxxxx") as hs:

        # --- Contacts ---
        # Lijst ophalen
        result = await hs.contacts.list(limit=10)
        for contact in result.results:
            print(f"{contact.id}: {contact.properties.get('email')}")

        # Contact aanmaken
        new_contact = await hs.contacts.create({
            "email": "jan@example.com",
            "firstname": "Jan",
            "lastname": "de Vries",
            "phone": "+31612345678"
        })
        print(f"Nieuw contact: {new_contact.id}")

        # Contact zoeken
        search = await hs.contacts.search(
            query="jan@example.com",
            properties=["email", "firstname", "lastname"]
        )
        print(f"Gevonden: {search.total} contacten")

        # --- Deals ---
        deal = await hs.deals.create({
            "dealname": "Grote Order Q2",
            "pipeline": "default",
            "dealstage": "appointmentscheduled",
            "amount": "15000"
        })

        # Deal koppelen aan contact
        await hs.deals.set_association(
            deal.id, "contacts", new_contact.id
        )

        # --- Alle contacten ophalen (auto-paginatie) ---
        async for contact in hs.contacts.list_all(
            properties=["email", "firstname"],
            max_items=500
        ):
            print(contact.properties.get("email"))

asyncio.run(main())
```

---

## Architecture Overview

```
HubSpotClient (facade)
├── HttpClient (core – retry, rate limiting, error mapping)
├── CRM
│   ├── CrmObjectClient (generic – CRUD + batch + search voor ~40 types)
│   ├── ContactsClient, CompaniesClient, DealsClient, TicketsClient
│   ├── CallsClient, EmailsClient, MeetingsClient, NotesClient, TasksClient
│   ├── CommunicationsClient, PostalMailClient
│   ├── LeadsClient, ProjectsClient, ContractsClient, ...
│   ├── AssociationsClient, AssociationsSchemaClient
│   ├── PipelinesClient, PropertiesClient, PropertyValidationsClient
│   ├── ListsClient, ImportsClient, ExportsClient
│   ├── SchemasClient, OwnersClient
│   ├── TimelineClient, TranscriptionsClient
│   ├── LimitsClient, ForecastsClient, ObjectLibraryClient
│   └── MeetingsSchedulerClient
├── Commerce
│   ├── ProductsClient, LineItemsClient, QuotesClient
│   ├── InvoicesClient, OrdersClient, CartsClient
│   ├── PaymentsClient, CommerceSubscriptionsClient
│   └── DiscountsClient, FeesClient, TaxesClient
├── CMS
│   ├── PagesClient (landing + site pages)
│   ├── BlogPostsClient, BlogAuthorsClient, BlogTagsClient, BlogSettingsClient
│   ├── HubDbClient, DomainsClient, SourceCodeClient
│   ├── UrlRedirectsClient, SiteSearchClient, CmsAuditClient
├── Marketing
│   ├── CampaignsClient, FormsClient, MarketingEventsClient
│   ├── TransactionalEmailClient, SingleSendClient
├── Automation
│   ├── ActionsClient, SequencesClient
├── Conversations
│   ├── ThreadsClient, MessagesClient, CustomChannelsClient
│   └── VisitorIdentificationClient
├── Events
│   ├── EventDefinitionsClient, EventSendClient, EventOccurrencesClient
├── Files
│   └── FilesClient
├── Settings
│   ├── CurrencyClient, UserProvisioningClient
│   ├── FeatureFlagsClient, DataSourcesClient
├── Webhooks
│   └── WebhooksClient
├── Account
│   ├── AccountInfoClient, AuditLogsClient
│   ├── BusinessUnitsClient, SubscriptionsClient
└── Auth
    └── OAuthClient
```

### Design Principles

- **Async-first**: Alle methoden zijn `async`. Gebruik `asyncio.run()` of `async with`.
- **Lazy instantiation**: Sub-clients worden pas aangemaakt bij eerste gebruik.
- **Generic CRM client**: `CrmObjectClient` dekt ~40 objecttypen met identieke CRUD + batch + search patronen. Specialized clients erven hiervan en voegen extra endpoints toe (merge, GDPR delete, etc.).
- **Typed responses**: Pydantic modellen (`HubSpotObject`, `PaginatedResult`, `SearchResult`, `BatchResult`).
- **Auto-retry**: Automatische exponential backoff bij 429 (rate limit) en 5xx (server errors). Respecteert `Retry-After` header. Standaard 4 retries.

---

## Error Handling

Alle SDK-fouten erven van `HubSpotError`:

```python
from hubspot_sdk.core.exceptions import (
    HubSpotError,              # Base – alle fouten
    HubSpotAuthError,          # 401/403 – Ongeldige/verlopen token
    HubSpotNotFoundError,      # 404 – Resource niet gevonden
    HubSpotRateLimitError,     # 429 – Rate limit bereikt (heeft .retry_after)
    HubSpotValidationError,    # 400/422 – Ongeldige request (heeft .errors list)
    HubSpotConflictError,      # 409 – Conflict (bijv. duplicate)
    HubSpotServerError,        # 5xx – HubSpot server probleem
)
```

### Voorbeeld foutafhandeling

```python
from hubspot_sdk.core.exceptions import (
    HubSpotNotFoundError,
    HubSpotValidationError,
    HubSpotRateLimitError,
)

try:
    contact = await hs.contacts.get("niet-bestaand-id")
except HubSpotNotFoundError as e:
    print(f"Contact niet gevonden: {e}")
    print(f"Correlation ID: {e.correlation_id}")  # voor HubSpot support
except HubSpotValidationError as e:
    print(f"Validatiefout: {e}")
    for error in e.errors:  # gedetailleerde fouten
        print(f"  - {error.get('message')}")
except HubSpotRateLimitError as e:
    print(f"Rate limited! Wacht {e.retry_after} seconden")
```

### Exception attributen

Elke exception heeft:
- `.status_code` – HTTP status code (int)
- `.response_body` – Volledige response body (dict)
- `.correlation_id` – HubSpot correlation ID voor support tickets

---

## Pagination

### Handmatige paginatie

```python
# Eerste pagina
page1 = await hs.contacts.list(limit=100)
print(f"Pagina 1: {len(page1.results)} resultaten")

# Volgende pagina
if page1.has_next:
    page2 = await hs.contacts.list(limit=100, after=page1.next_after)
```

### Auto-paginatie (aanbevolen)

```python
# Alle contacten ophalen (auto-paginate)
async for contact in hs.contacts.list_all(
    properties=["email", "firstname"],
    max_items=1000  # None = alles
):
    print(contact.properties.get("email"))

# Alle zoekresultaten ophalen
async for contact in hs.contacts.search_all(
    query="example.com",
    properties=["email"],
    max_items=500
):
    print(contact.id)
```

### Verzamel naar lijst

```python
from hubspot_sdk.core.pagination import collect

all_contacts = await collect(hs.contacts.list_all(properties=["email"]))
print(f"Totaal: {len(all_contacts)} contacten")
```

---

## Data Models

### HubSpotObject

Elk CRM-object (contact, deal, ticket, etc.) wordt geretourneerd als:

```python
class HubSpotObject:
    id: str                                    # HubSpot object ID
    properties: dict[str, Any]                 # Object properties
    properties_with_history: dict | None       # Waarden met historie
    associations: dict | None                  # Gekoppelde objecten
    created_at: datetime | None
    updated_at: datetime | None
    archived: bool
    archived_at: datetime | None
```

### PaginatedResult

```python
class PaginatedResult[T]:
    results: list[T]          # Lijst van objecten
    paging: Paging | None     # Paginatie-info

    has_next: bool            # Zijn er meer pagina's?
    next_after: str | None    # Cursor voor volgende pagina
```

### SearchResult

```python
class SearchResult[T]:
    total: int                # Totaal aantal matches
    results: list[T]          # Resultaten op deze pagina
    paging: Paging | None

    has_next: bool
    next_after: str | None
```

### BatchResult

```python
class BatchResult[T]:
    status: str               # "COMPLETE", "PENDING", etc.
    results: list[T]          # Succesvol verwerkte objecten
    errors: list[dict]        # Eventuele fouten
    num_errors: int
    started_at: datetime | None
    completed_at: datetime | None
```

### Overige modellen

| Model | Beschrijving |
|---|---|
| `Pipeline` | CRM pipeline met stages |
| `PipelineStage` | Stage binnen een pipeline |
| `Property` | Property definitie (naam, type, opties) |
| `PropertyOption` | Optie voor een enumeration property |
| `PropertyGroup` | Groep van properties |
| `Owner` | CRM eigenaar (gebruiker) |
| `FileObject` | Bestand in file manager |
| `Folder` | Map in file manager |
| `ImportResult` | Resultaat van een import |
| `WebhookSubscription` | Webhook abonnement |
| `TokenInfo` | OAuth token info (.access_token, .refresh_token, .is_expired) |
| `Filter` | Zoekfilter (propertyName, operator, value) |
| `FilterGroup` | Groep filters (AND-logica binnen groep, OR tussen groepen) |
| `AssociationSpec` | Associatie type specificatie |

---

## CRM – Core Objects

De volgende objecttypen hebben dedicated clients met volledige CRUD + batch + search + associations:

| Property | Client | Object Type | Extra methods |
|---|---|---|---|
| `hs.contacts` | `ContactsClient` | contacts | `merge()`, `gdpr_delete()` |
| `hs.companies` | `CompaniesClient` | companies | `merge()`, `gdpr_delete()` |
| `hs.deals` | `DealsClient` | 0-3 | `merge()`, `batch_read_splits()`, `batch_upsert_splits()` |
| `hs.tickets` | `TicketsClient` | tickets | `merge()` |

### Generic CRM Object Client

Voor elk objecttype dat geen dedicated client heeft, gebruik `hs.objects("type")`:

```python
# Elk CRM-objecttype werkt
custom = hs.objects("my_custom_object")
result = await custom.list(limit=10)
obj = await custom.create({"name": "Test"})
```

### Standaard methoden (alle CRM objects)

Elke CRM object client (inclusief activities, commerce, extended) heeft deze methoden:

#### CRUD

```python
# Lijst ophalen
result = await hs.contacts.list(
    limit=10,                              # max 100
    after="cursor-token",                  # paginatie cursor
    properties=["email", "firstname"],     # welke properties ophalen
    properties_with_history=["email"],     # met wijzigingshistorie
    associations=["deals", "companies"],   # gekoppelde objecten meeladen
    archived=False                         # ook gearchiveerde ophalen?
)

# Enkel object ophalen
contact = await hs.contacts.get(
    "123",
    properties=["email"],
    properties_with_history=["lifecycle_stage"],
    associations=["deals"],
    id_property="email",      # zoek op andere property dan ID
    archived=False
)

# Aanmaken
contact = await hs.contacts.create(
    properties={"email": "test@example.com", "firstname": "Test"},
    associations=[{
        "to": {"id": "456"},
        "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 1}]
    }]
)

# Bijwerken
contact = await hs.contacts.update(
    "123",
    properties={"firstname": "Nieuw"},
    id_property="email"  # update op basis van email i.p.v. ID
)

# Verwijderen (archiveren)
await hs.contacts.delete("123")
```

#### Batch operaties

```python
# Batch aanmaken
result = await hs.contacts.batch_create([
    {"properties": {"email": "a@example.com", "firstname": "Alice"}},
    {"properties": {"email": "b@example.com", "firstname": "Bob"}},
])

# Batch lezen
result = await hs.contacts.batch_read(
    ids=["123", "456", "789"],
    properties=["email", "firstname"],
    id_property="email"  # lees op basis van email
)
# OF met custom inputs:
result = await hs.contacts.batch_read(
    inputs=[{"id": "test@example.com"}],
    id_property="email"
)

# Batch bijwerken
result = await hs.contacts.batch_update([
    {"id": "123", "properties": {"firstname": "Updated"}},
    {"id": "456", "properties": {"firstname": "Also Updated"}},
])

# Batch upsert (aanmaken of bijwerken)
result = await hs.contacts.batch_upsert([
    {"id": "test@example.com", "idProperty": "email",
     "properties": {"firstname": "Upserted"}},
])

# Batch archiveren
await hs.contacts.batch_archive(["123", "456"])
```

#### Zoeken

```python
# Full-text zoeken
result = await hs.contacts.search(
    query="example.com",
    properties=["email", "firstname"],
    limit=20
)

# Filter zoeken
result = await hs.contacts.search(
    filter_groups=[{
        "filters": [
            {"propertyName": "email", "operator": "CONTAINS_TOKEN", "value": "example.com"},
            {"propertyName": "createdate", "operator": "GTE", "value": "2024-01-01"}
        ]
    }],
    sorts=[{"propertyName": "createdate", "direction": "DESCENDING"}],
    properties=["email", "firstname", "createdate"],
    limit=50
)

# Meerdere filtergroepen (OR logica tussen groepen, AND binnen groep)
result = await hs.contacts.search(
    filter_groups=[
        {"filters": [{"propertyName": "city", "operator": "EQ", "value": "Amsterdam"}]},
        {"filters": [{"propertyName": "city", "operator": "EQ", "value": "Rotterdam"}]},
    ]
)
```

**Zoekoperators**: `EQ`, `NEQ`, `LT`, `LTE`, `GT`, `GTE`, `BETWEEN`, `IN`, `NOT_IN`, `HAS_PROPERTY`, `NOT_HAS_PROPERTY`, `CONTAINS_TOKEN`, `NOT_CONTAINS_TOKEN`

#### Associaties (inline)

```python
# Koppeling maken (default type)
await hs.contacts.set_association("contact-123", "deals", "deal-456")

# Koppeling maken (met specifiek type)
await hs.contacts.set_association(
    "contact-123", "deals", "deal-456",
    association_specs=[{
        "associationCategory": "HUBSPOT_DEFINED",
        "associationTypeId": 3
    }]
)

# Koppeling verwijderen
await hs.contacts.remove_association("contact-123", "deals", "deal-456")
```

#### Merge (contacts, companies, deals, tickets, leads, projects, products, calls, emails, meetings, notes, tasks)

```python
# Twee objecten samenvoegen
merged = await hs.contacts.merge(
    primary_id="123",             # dit object blijft bestaan
    object_id_to_merge="456"      # dit object wordt samengevoegd
)
```

#### GDPR Delete (alleen contacts en companies)

```python
await hs.contacts.gdpr_delete("123")
await hs.contacts.gdpr_delete("test@example.com", id_property="email")
```

---

## CRM – Activities

Activity objects voor het tracken van interacties. Allemaal met CRUD + batch + search + associations.

| Property | Client | Object Type | Merge |
|---|---|---|---|
| `hs.calls` | `CallsClient` | calls | Ja |
| `hs.emails` | `EmailsClient` | emails | Ja |
| `hs.meetings` | `MeetingsClient` | meetings | Ja |
| `hs.notes` | `NotesClient` | notes | Ja |
| `hs.tasks` | `TasksClient` | tasks | Ja |
| `hs.communications` | `CommunicationsClient` | communications | Nee |
| `hs.postal_mail` | `PostalMailClient` | postal_mail | Nee |

### Voorbeeld: Call loggen

```python
call = await hs.calls.create({
    "hs_call_title": "Discovery call met klant",
    "hs_call_body": "Besproken: budget, timeline, requirements",
    "hs_call_status": "COMPLETED",
    "hs_call_duration": "1800000",  # 30 min in ms
    "hs_call_direction": "OUTBOUND",
    "hs_timestamp": "2024-03-15T10:00:00.000Z"
})
# Koppel aan contact
await hs.calls.set_association(call.id, "contacts", "contact-123")
```

### Voorbeeld: Taak aanmaken

```python
task = await hs.tasks.create({
    "hs_task_subject": "Follow-up offerte sturen",
    "hs_task_body": "Offerte opstellen en versturen",
    "hs_task_status": "NOT_STARTED",
    "hs_task_priority": "HIGH",
    "hs_timestamp": "2024-03-20T09:00:00.000Z",
    "hubspot_owner_id": "owner-123"
})
```

### Voorbeeld: Notitie toevoegen

```python
note = await hs.notes.create({
    "hs_note_body": "Klant is geïnteresseerd in Enterprise plan. Budget: €50k/jaar.",
    "hs_timestamp": "2024-03-15T14:30:00.000Z",
    "hubspot_owner_id": "owner-123"
})
await hs.notes.set_association(note.id, "deals", "deal-789")
```

---

## CRM – Commerce Objects

Commerce-gerelateerde objecten. Allemaal met CRUD + batch + search + associations.

| Property | Client | Object Type | Merge |
|---|---|---|---|
| `hs.products` | `ProductsClient` | products | Ja |
| `hs.line_items` | `LineItemsClient` | line_items | Nee |
| `hs.quotes` | `QuotesClient` | quotes | Nee |
| `hs.invoices` | `InvoicesClient` | invoices | Nee |
| `hs.orders` | `OrdersClient` | orders | Nee |
| `hs.carts` | `CartsClient` | carts | Nee |
| `hs.payments` | `PaymentsClient` | commerce_payments | Nee |
| `hs.commerce_subscriptions` | `CommerceSubscriptionsClient` | subscriptions | Nee |
| `hs.discounts` | `DiscountsClient` | discounts | Nee |
| `hs.fees` | `FeesClient` | fees | Nee |
| `hs.taxes` | `TaxesClient` | taxes | Nee |

### Voorbeeld: Product + Line Item + Quote flow

```python
# Product aanmaken
product = await hs.products.create({
    "name": "Enterprise Licentie",
    "price": "5000",
    "hs_recurring_billing_period": "P12M",  # 12 maanden
    "description": "Enterprise software licentie, jaarlijks"
})

# Line item van product voor een deal
line_item = await hs.line_items.create({
    "hs_product_id": product.id,
    "quantity": "3",
    "price": "5000"
})
await hs.line_items.set_association(line_item.id, "deals", "deal-123")

# Quote ophalen
quotes = await hs.quotes.search(
    filter_groups=[{
        "filters": [{"propertyName": "hs_status", "operator": "EQ", "value": "APPROVAL_NOT_NEEDED"}]
    }]
)

# Factuur zoeken
invoices = await hs.invoices.list(properties=["hs_invoice_status", "hs_amount_billed"])
```

---

## CRM – Extended Objects

Overige CRM-objecttypen. Allemaal met CRUD + batch + search + associations (tenzij anders vermeld).

| Property | Client | Object Type | Merge | Opmerking |
|---|---|---|---|---|
| `hs.leads` | `LeadsClient` | leads | Ja | Sales leads |
| `hs.feedback_submissions` | `FeedbackSubmissionsClient` | feedback_submissions | Nee | Read-heavy |
| `hs.contracts` | `ContractsClient` | contracts | Nee | |
| `hs.projects` | `ProjectsClient` | projects | Ja | |
| `hs.goal_targets` | `GoalTargetsClient` | goal_targets | Nee | |
| `hs.crm_users` | `CrmUsersClient` | users | Nee | CRM user records |
| `hs.services` | `ServicesClient` | 0-162 | Nee | Numeriek type ID |
| `hs.courses` | `CoursesClient` | 0-410 | Nee | Numeriek type ID |
| `hs.listings` | `ListingsClient` | 0-420 | Nee | Numeriek type ID |
| `hs.partner_clients` | `PartnerClientsClient` | partner_clients | Nee | Beperkte CRUD |
| `hs.partner_services` | `PartnerServicesClient` | partner_services | Nee | Beperkte CRUD |
| `hs.tax_rates` | `TaxRatesClient` | – | Nee | Eigen base path, read-only |

### TaxRatesClient (afwijkend patroon)

```python
# Tax rates hebben een eigen endpoint (NIET /crm/objects/)
rates = await hs.tax_rates.list()           # GET /tax-rates/{version}/tax-rates
rate = await hs.tax_rates.get("rate-123")   # GET /tax-rates/{version}/tax-rates/{id}
```

---

## CRM – Associations

Beheer koppelingen tussen objecttypen.

**Toegang**: `hs.associations` / `hs.associations_schema`

### AssociationsClient

```python
# Batch: standaard associaties leggen
await hs.associations.batch_associate_default(
    from_type="contacts",
    to_type="deals",
    inputs=[
        {"from": {"id": "contact-1"}, "to": {"id": "deal-1"}},
        {"from": {"id": "contact-2"}, "to": {"id": "deal-2"}},
    ]
)

# Batch: gelabelde associaties leggen
await hs.associations.batch_create(
    from_type="contacts",
    to_type="companies",
    inputs=[{
        "from": {"id": "contact-1"},
        "to": {"id": "company-1"},
        "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 1}]
    }]
)

# Batch: associaties lezen
result = await hs.associations.batch_read(
    from_type="contacts",
    to_type="deals",
    inputs=[{"id": "contact-123"}]
)

# Batch: associaties verwijderen
await hs.associations.batch_archive(
    from_type="contacts",
    to_type="deals",
    inputs=[{"from": {"id": "contact-1"}, "to": [{"id": "deal-1"}]}]
)

# High usage report
report = await hs.associations.high_usage_report(user_id="user-123")
```

### AssociationsSchemaClient

```python
# Alle configuraties ophalen
configs = await hs.associations_schema.get_all_configurations()

# Configuraties tussen twee objecttypen
configs = await hs.associations_schema.get_configurations("contacts", "deals")

# Associatietypes ophalen
types = await hs.associations_schema.get_types("contacts", "companies")

# Labels/configuraties aanmaken
await hs.associations_schema.batch_create_configurations(
    "contacts", "deals",
    inputs=[{"label": "Decision Maker", "name": "decision_maker"}]
)

# Labels updaten
await hs.associations_schema.batch_update_configurations(
    "contacts", "deals",
    inputs=[{"label": "Primary Decision Maker", "associationTypeId": 123}]
)

# Label verwijderen
await hs.associations_schema.delete_configuration("contacts", "deals", association_type_id=123)
```

---

## CRM – Pipelines

Beheer pipelines en stages voor deals, tickets, etc.

**Toegang**: `hs.pipelines`

```python
# Alle pipelines voor een objecttype
pipelines = await hs.pipelines.list("deals")

# Pipeline aanmaken
pipeline = await hs.pipelines.create("deals", {
    "label": "Enterprise Sales",
    "displayOrder": 1,
    "stages": [
        {"label": "Discovery", "displayOrder": 0, "metadata": {"probability": "0.1"}},
        {"label": "Proposal", "displayOrder": 1, "metadata": {"probability": "0.4"}},
        {"label": "Closed Won", "displayOrder": 2, "metadata": {"isClosed": "true", "probability": "1.0"}},
    ]
})

# Pipeline ophalen / bijwerken / vervangen / verwijderen
pipeline = await hs.pipelines.get("deals", "pipeline-id")
await hs.pipelines.update("deals", "pipeline-id", {"label": "Updated Name"})
await hs.pipelines.replace("deals", "pipeline-id", {... })  # volledige vervanging
await hs.pipelines.delete("deals", "pipeline-id")

# Stages beheren
stages = await hs.pipelines.list_stages("deals", "pipeline-id")
stage = await hs.pipelines.create_stage("deals", "pipeline-id", {
    "label": "Negotiation", "displayOrder": 2
})
stage = await hs.pipelines.get_stage("deals", "pipeline-id", "stage-id")
await hs.pipelines.update_stage("deals", "pipeline-id", "stage-id", {"label": "Updated"})
await hs.pipelines.replace_stage("deals", "pipeline-id", "stage-id", {... })
await hs.pipelines.delete_stage("deals", "pipeline-id", "stage-id")

# Audit trail
audit = await hs.pipelines.get_audit("deals", "pipeline-id")
stage_audit = await hs.pipelines.get_stage_audit("deals", "pipeline-id", "stage-id")
```

---

## CRM – Properties

Beheer property-definities voor CRM-objecttypen.

**Toegang**: `hs.properties`

```python
# Alle properties ophalen
props = await hs.properties.list("contacts")
props = await hs.properties.list("contacts", archived=True)  # inclusief gearchiveerde

# Property aanmaken
prop = await hs.properties.create("contacts", {
    "name": "favorite_color",
    "label": "Favoriete kleur",
    "type": "enumeration",
    "fieldType": "select",
    "groupName": "contactinformation",
    "options": [
        {"label": "Rood", "value": "red"},
        {"label": "Blauw", "value": "blue"},
        {"label": "Groen", "value": "green"},
    ]
})

# Property ophalen / bijwerken / verwijderen
prop = await hs.properties.get("contacts", "favorite_color")
await hs.properties.update("contacts", "favorite_color", {"label": "Lievelingskleur"})
await hs.properties.delete("contacts", "favorite_color")

# Batch operaties
await hs.properties.batch_create("contacts", [{"name": "a", ...}, {"name": "b", ...}])
result = await hs.properties.batch_read("contacts", [{"name": "email"}, {"name": "phone"}])
await hs.properties.batch_archive("contacts", [{"name": "old_property"}])

# Property groepen
groups = await hs.properties.list_groups("contacts")
group = await hs.properties.create_group("contacts", {
    "name": "custom_group", "label": "Onze Custom Velden"
})
group = await hs.properties.get_group("contacts", "custom_group")
await hs.properties.update_group("contacts", "custom_group", {"label": "Updated"})
await hs.properties.delete_group("contacts", "custom_group")
```

---

## CRM – Property Validations

Lees en beheer validatieregels voor properties.

**Toegang**: `hs.property_validations`

```python
# Alle validatieregels voor een objecttype
rules = await hs.property_validations.list_rules("0-1")  # contacts

# Regels voor een specifieke property
rules = await hs.property_validations.get_property_rules("0-1", "email")

# Specifieke regel ophalen
rule = await hs.property_validations.get_rule("0-1", "email", "FORMAT")

# Regel bijwerken
await hs.property_validations.update_rule(
    "0-1", "phone", "FORMAT",
    rule_arguments=[{"name": "format", "value": "E164"}],
    should_apply_normalization=True
)
```

---

## CRM – Lists (Segments)

Beheer contactlijsten en segmenten.

**Toegang**: `hs.lists`

```python
# Lijsten ophalen
lists = await hs.lists.list(count=50, offset=0)

# Lijst aanmaken
new_list = await hs.lists.create({
    "name": "Newsletter Subscribers",
    "objectTypeId": "0-1",  # contacts
    "processingType": "MANUAL"
})

# Lijst ophalen / bijwerken / verwijderen / herstellen
lst = await hs.lists.get("list-123", include_filters=True)
await hs.lists.update("list-123", {"name": "Updated Name"})
await hs.lists.delete("list-123")
await hs.lists.restore("list-123")

# Batch lezen
lists = await hs.lists.batch_read(["list-1", "list-2", "list-3"])

# Leden beheren
members = await hs.lists.get_memberships("list-123", limit=100, after="cursor")
await hs.lists.add_members("list-123", ["contact-1", "contact-2"])
await hs.lists.remove_members("list-123", ["contact-3"])
await hs.lists.add_and_remove_members(
    "list-123",
    add=["contact-4", "contact-5"],
    remove=["contact-6"]
)
await hs.lists.add_all_from_list("target-list", "source-list")
await hs.lists.get_memberships_join_order("list-123")

# Mappen
folders = await hs.lists.list_folders()
folder = await hs.lists.create_folder({"name": "Marketing Lists"})
await hs.lists.update_folder("folder-id", {"name": "Updated"})
await hs.lists.move_folder("folder-id", "new-parent-id")
await hs.lists.delete_folder("folder-id")

# Zoeken
results = await hs.lists.search(query="newsletter")
lst = await hs.lists.get_by_name("Newsletter Subscribers")
```

---

## CRM – Imports & Exports

### Imports

**Toegang**: `hs.imports`

```python
# Alle imports ophalen
imports = await hs.imports.list(limit=20)

# Import starten (met bestand)
result = await hs.imports.create(
    data={...},  # import configuratie
    files={"file": open("contacts.csv", "rb")}
)

# Import status controleren
status = await hs.imports.get("import-123")

# Import annuleren
await hs.imports.cancel("import-123")

# Import fouten bekijken
errors = await hs.imports.get_errors("import-123", limit=100)
```

### Exports

**Toegang**: `hs.exports`

```python
# Export starten
export = await hs.exports.create({
    "exportType": "LIST",
    "objectType": "CONTACT",
    "listId": "list-123"
})

# Status controleren
status = await hs.exports.get_status("task-123")

# Export ophalen
result = await hs.exports.get("export-123")
```

---

## CRM – Schemas (Custom Objects)

Definieer custom objecttypen.

**Toegang**: `hs.schemas`

```python
# Alle custom objectschema's
schemas = await hs.schemas.list()

# Schema aanmaken
schema = await hs.schemas.create({
    "name": "vehicle",
    "labels": {"singular": "Vehicle", "plural": "Vehicles"},
    "primaryDisplayProperty": "make",
    "requiredProperties": ["make", "model"],
    "properties": [
        {"name": "make", "label": "Make", "type": "string", "fieldType": "text"},
        {"name": "model", "label": "Model", "type": "string", "fieldType": "text"},
        {"name": "year", "label": "Year", "type": "number", "fieldType": "number"},
    ]
})

# Schema ophalen / bijwerken / verwijderen
schema = await hs.schemas.get("vehicle")
await hs.schemas.update("vehicle", {"labels": {"singular": "Voertuig"}})
await hs.schemas.delete("vehicle")

# Batch lezen
schemas = await hs.schemas.batch_read([{"objectType": "vehicle"}])

# Associaties voor custom objects
await hs.schemas.create_association("vehicle", {
    "fromObjectTypeId": "vehicle",
    "toObjectTypeId": "0-1",  # contacts
    "name": "vehicle_to_contact"
})
await hs.schemas.delete_association("vehicle", "association-id")
```

---

## CRM – Owners

**Toegang**: `hs.owners`

```python
# Alle owners ophalen
owners = await hs.owners.list(limit=100)
owners = await hs.owners.list(email="jan@company.com")
owners = await hs.owners.list(archived=True)

# Specifieke owner
owner = await hs.owners.get("owner-123")
owner = await hs.owners.get("jan@company.com", id_property="email")
```

---

## CRM – Extensions

### Calling Extensions

**Toegang**: `hs.calling_extensions`

```python
# Inbound call registreren
await hs.calling_extensions.create_inbound_call({...})

# Recording ready melden
await hs.calling_extensions.mark_recording_ready({...})

# App calling settings
settings = await hs.calling_extensions.get_settings("app-123")
await hs.calling_extensions.create_settings("app-123", {...})
await hs.calling_extensions.update_settings("app-123", {...})
await hs.calling_extensions.delete_settings("app-123")

# Channel connection settings
settings = await hs.calling_extensions.get_channel_connection_settings("app-123")
await hs.calling_extensions.create_channel_connection_settings("app-123", {...})
await hs.calling_extensions.update_channel_connection_settings("app-123", {...})
await hs.calling_extensions.delete_channel_connection_settings("app-123")

# Transcripts
transcript = await hs.calling_extensions.create_transcript({...})
transcript = await hs.calling_extensions.get_transcript("transcript-id")
await hs.calling_extensions.delete_transcript("transcript-id")
```

### CRM Cards

**Toegang**: `hs.crm_cards`

```python
sample = await hs.crm_cards.get_sample_response()
cards = await hs.crm_cards.list("app-123")
card = await hs.crm_cards.create("app-123", {...})
card = await hs.crm_cards.get("app-123", "card-id")
await hs.crm_cards.update("app-123", "card-id", {...})
await hs.crm_cards.delete("app-123", "card-id")
```

### Video Conferencing

**Toegang**: `hs.video_conferencing`

```python
settings = await hs.video_conferencing.get_settings("app-123")
await hs.video_conferencing.update_settings("app-123", {...})
await hs.video_conferencing.delete_settings("app-123")
```

---

## CRM – Timeline Events

Stuur custom timeline events vanuit integraties.

**Toegang**: `hs.timeline`

```python
# Enkel event versturen
await hs.timeline.send_event({
    "eventTypeName": "my_app_event",
    "objectId": "contact-123",
    "timestamp": "2024-03-15T10:00:00.000Z",
    "properties": {
        "action": "page_view",
        "page": "/pricing"
    }
})

# Batch events
await hs.timeline.send_events_batch([
    {"eventTypeName": "event1", "objectId": "123", ...},
    {"eventTypeName": "event2", "objectId": "456", ...},
])

# Event type resolven
result = await hs.timeline.resolve_event_type(
    developer_symbol="my_event",
    project_name="my_project"
)
```

---

## CRM – Transcriptions

Beheer call transcripties.

**Toegang**: `hs.transcriptions`

```python
# Inbound call voltooien
result = await hs.transcriptions.complete_inbound_call({
    "externalCallId": "ext-call-123",
    "fromNumber": {"e164Number": "+31612345678"},
    "toNumber": {"e164Number": "+31687654321"},
    "durationSeconds": 300,
    "finalCallStatus": "COMPLETED",
    "createEngagement": True
})

# Transcript aanmaken
transcript = await hs.transcriptions.create_transcript(
    engagement_id=12345,
    utterances=[
        {
            "text": "Hallo, waarmee kan ik u helpen?",
            "speaker": {"id": "agent-1", "name": "Agent"},
            "startTimeMillis": 0,
            "endTimeMillis": 3000,
            "languageCode": "nl"
        },
        {
            "text": "Ik heb een vraag over mijn factuur.",
            "speaker": {"id": "customer-1", "name": "Klant"},
            "startTimeMillis": 3500,
            "endTimeMillis": 6000,
            "languageCode": "nl"
        }
    ]
)

# Transcript ophalen / verwijderen
transcript = await hs.transcriptions.get_transcript("transcript-id")
await hs.transcriptions.delete_transcript("transcript-id")
```

---

## CRM – Limits Tracking

Controleer account limieten en gebruik.

**Toegang**: `hs.limits`

```python
# Record limieten
records = await hs.limits.records()

# Pipeline limieten
pipelines = await hs.limits.pipelines()

# Custom property limieten
props = await hs.limits.custom_properties()

# Custom object type limieten
objects = await hs.limits.custom_object_types()

# Berekende properties limieten
calc = await hs.limits.calculated_properties()

# Associatie label limieten
labels = await hs.limits.association_labels(
    from_object_type_id="0-1",
    to_object_type_id="0-3"
)

# Associatie record limieten
records = await hs.limits.association_records()
records = await hs.limits.association_records_from("0-1")
records = await hs.limits.association_records_between("0-1", "0-3")
```

---

## CRM – Forecasts

Lees forecast type instellingen.

**Toegang**: `hs.forecasts`

```python
# Alle forecast types
types = await hs.forecasts.list()

# Specifiek forecast type
forecast_type = await hs.forecasts.get("forecast-type-id")
```

---

## CRM – Object Library

Controleer of objecttypen ingeschakeld zijn.

**Toegang**: `hs.object_library`

```python
# Alle enablement statussen
all_status = await hs.object_library.list_enablement()

# Specifiek objecttype
status = await hs.object_library.get_enablement("0-1")  # contacts
```

---

## CRM – Meetings Scheduler

Beheer vergaderpagina's en boekingen (NIET het meetings CRM object - dat is `hs.meetings`).

**Toegang**: `hs.meetings_scheduler`

```python
# Meeting links ophalen
links = await hs.meetings_scheduler.list_meeting_links(
    limit=10,
    organizer_user_id="user-123",
    link_type="PERSONAL"
)

# Kalender event aanmaken
event = await hs.meetings_scheduler.create_calendar_event(
    organizer_user_id="user-123",
    event_data={
        "hs_meeting_title": "Demo Call",
        "hs_meeting_body": "Product demo",
        "hs_meeting_start_time": "2024-03-20T10:00:00.000Z",
        "hs_meeting_end_time": "2024-03-20T10:30:00.000Z"
    }
)

# Meeting boeken
booking = await hs.meetings_scheduler.book_meeting({
    "slug": "jan-de-vries/30min",
    "startTime": "2024-03-20T10:00:00.000Z",
    "formFields": [
        {"name": "email", "value": "klant@example.com"},
        {"name": "firstname", "value": "Klant"}
    ]
})

# Beschikbaarheid ophalen
availability = await hs.meetings_scheduler.get_availability(
    slug="jan-de-vries/30min",
    timezone="Europe/Amsterdam",
    month_offset=0
)

# Booking info
info = await hs.meetings_scheduler.get_booking_info(
    slug="jan-de-vries/30min",
    timezone="Europe/Amsterdam"
)
```

---

## CMS – Pages

Beheer landing pages en site pages.

**Toegang**: `hs.pages`

### Landing Pages

```python
# Lijst / CRUD
pages = await hs.pages.list_landing(limit=20)
page = await hs.pages.create_landing({"name": "Promo Page", ...})
page = await hs.pages.get_landing("page-id")
await hs.pages.update_landing("page-id", {"name": "Updated"})
await hs.pages.delete_landing("page-id")

# Draft / Live workflow
draft = await hs.pages.get_landing_draft("page-id")
await hs.pages.update_landing_draft("page-id", {"name": "Draft Update"})
await hs.pages.push_landing_live("page-id")

# Klonen
clone = await hs.pages.clone_landing("page-id")

# A/B testing
variation = await hs.pages.create_landing_ab_variation({...})
await hs.pages.end_landing_ab_test({...})

# Batch operaties
await hs.pages.batch_create_landing([...])
await hs.pages.batch_read_landing([...])
await hs.pages.batch_update_landing([...])
await hs.pages.batch_archive_landing([...])
```

### Site Pages (zelfde patroon)

```python
pages = await hs.pages.list_site(limit=20)
page = await hs.pages.create_site({...})
page = await hs.pages.get_site("page-id")
await hs.pages.update_site("page-id", {...})
await hs.pages.delete_site("page-id")
# + draft, live, clone, batch methoden...
```

---

## CMS – Blog

### Blog Posts

**Toegang**: `hs.blog_posts`

```python
# CRUD
posts = await hs.blog_posts.list(limit=20)
post = await hs.blog_posts.create({"name": "New Post", "contentGroupId": "blog-id", ...})
post = await hs.blog_posts.get("post-id")
await hs.blog_posts.update("post-id", {"name": "Updated"})
await hs.blog_posts.delete("post-id")

# Draft / Live
draft = await hs.blog_posts.get_draft("post-id")
await hs.blog_posts.update_draft("post-id", {...})
await hs.blog_posts.push_live("post-id")
await hs.blog_posts.reset_draft("post-id")

# Klonen / Plannen
clone = await hs.blog_posts.clone("post-id")
await hs.blog_posts.schedule({"id": "post-id", "publishDate": "2024-04-01T09:00:00Z"})

# Revisies
revisions = await hs.blog_posts.get_revisions("post-id")
revision = await hs.blog_posts.get_revision("post-id", "revision-id")
await hs.blog_posts.restore_revision("revision-id")

# Multi-language
await hs.blog_posts.attach_to_lang_group({...})
variation = await hs.blog_posts.create_lang_variation({...})
await hs.blog_posts.detach_from_lang_group({...})
await hs.blog_posts.set_new_lang_primary({...})
await hs.blog_posts.update_languages([...])

# Batch
await hs.blog_posts.batch_create([...])
await hs.blog_posts.batch_read([...])
await hs.blog_posts.batch_update([...])
await hs.blog_posts.batch_archive([...])
```

### Blog Authors / Tags / Settings

**Toegang**: `hs.blog_authors`, `hs.blog_tags`, `hs.blog_settings`

Zelfde CRUD + batch + multi-language patroon als blog posts. Blog settings heeft geen create/delete.

---

## CMS – HubDB

Database-achtige tabellen in HubSpot.

**Toegang**: `hs.hubdb`

```python
# Tabellen
tables = await hs.hubdb.list_tables()
table = await hs.hubdb.create_table({"name": "products", "label": "Products"})
table = await hs.hubdb.get_table("table-id", draft=True)
await hs.hubdb.update_table("table-id", {...}, draft=True)
await hs.hubdb.delete_table("table-id")
clone = await hs.hubdb.clone_table("table-id", {"newName": "clone"})

# Draft tabellen
drafts = await hs.hubdb.list_draft_tables()

# Publiceren / Reset / Unpublish
await hs.hubdb.publish_table("table-id")
await hs.hubdb.reset_draft_table("table-id")
await hs.hubdb.unpublish_table("table-id")

# Import / Export
await hs.hubdb.import_table("table-id", files={"file": ...}, draft=True)
data = await hs.hubdb.export_table("table-id", draft=False)

# Rijen
rows = await hs.hubdb.list_rows("table-id", draft=False)
row = await hs.hubdb.create_row("table-id", {"values": {"col1": "val1"}}, draft=True)
row = await hs.hubdb.get_row("table-id", "row-id")
await hs.hubdb.update_row("table-id", "row-id", {...})
await hs.hubdb.replace_row("table-id", "row-id", {...})
await hs.hubdb.delete_row("table-id", "row-id")

# Batch rij operaties
await hs.hubdb.batch_create_rows("table-id", [...], draft=True)
await hs.hubdb.batch_read_rows("table-id", [...])
await hs.hubdb.batch_replace_rows("table-id", [...])
await hs.hubdb.batch_clone_rows("table-id", [...])
await hs.hubdb.batch_purge_rows("table-id", [...])
```

---

## CMS – Domains

**Toegang**: `hs.domains`

```python
domains = await hs.domains.list()
domain = await hs.domains.get("domain-id")
```

---

## CMS – Source Code

Beheer CMS template bestanden.

**Toegang**: `hs.source_code`

```python
# Bestand ophalen / aanmaken / vervangen / verwijderen
content = await hs.source_code.get_content("developer", "templates/page.html")
await hs.source_code.create_or_update("developer", "templates/new.html", files=..., data=...)
await hs.source_code.replace("developer", "templates/page.html", files=..., data=...)
await hs.source_code.delete("developer", "templates/old.html")

# Metadata
meta = await hs.source_code.get_metadata("developer", "templates/page.html")

# Validatie
result = await hs.source_code.validate({...})

# Async extract
task = await hs.source_code.extract_async({...})
status = await hs.source_code.get_extract_status("task-id")
```

---

## CMS – URL Redirects

**Toegang**: `hs.url_redirects`

```python
redirects = await hs.url_redirects.list()
redirect = await hs.url_redirects.create({
    "routePrefix": "/old-page",
    "destination": "/new-page",
    "redirectStyle": 301
})
redirect = await hs.url_redirects.get("redirect-id")
await hs.url_redirects.update("redirect-id", {"destination": "/newer-page"})
await hs.url_redirects.delete("redirect-id")
```

---

## CMS – Site Search

**Toegang**: `hs.site_search`

```python
results = await hs.site_search.search(q="pricing", limit=10, offset=0)
indexed = await hs.site_search.get_indexed_data("content-id")
```

---

## CMS – Audit Logs

**Toegang**: `hs.cms_audit`

```python
logs = await hs.cms_audit.list(objectType="LANDING_PAGE", limit=50)
export = await hs.cms_audit.export({...})
```

---

## Marketing – Campaigns

**Toegang**: `hs.campaigns`

```python
# CRUD
campaigns = await hs.campaigns.list(limit=20)
campaign = await hs.campaigns.create({"name": "Q2 Campaign", ...})
campaign = await hs.campaigns.get("campaign-id")
await hs.campaigns.update("campaign-id", {"name": "Updated"})
await hs.campaigns.delete("campaign-id")

# Batch
await hs.campaigns.batch_create([...])
await hs.campaigns.batch_read([...])
await hs.campaigns.batch_update([...])
await hs.campaigns.batch_archive([...])

# Zoeken
results = await hs.campaigns.search({...})

# Revenue attribution
revenue = await hs.campaigns.get_revenue_attribution("campaign-id")
revenue = await hs.campaigns.batch_read_revenue_attribution([...])

# Assets
assets = await hs.campaigns.get_assets("campaign-id")
await hs.campaigns.create_asset("campaign-id", {...})
await hs.campaigns.delete_asset("campaign-id", "asset-id")
await hs.campaigns.batch_create_assets("campaign-id", [...])
await hs.campaigns.batch_delete_assets("campaign-id", [...])
```

---

## Marketing – Forms

**Toegang**: `hs.forms`

```python
forms = await hs.forms.list()
form = await hs.forms.create({...})
form = await hs.forms.get("form-id")
await hs.forms.update("form-id", {...})
await hs.forms.replace("form-id", {...})  # volledige vervanging
await hs.forms.delete("form-id")
```

---

## Marketing – Events

**Toegang**: `hs.marketing_events`

```python
# CRUD
events = await hs.marketing_events.list()
event = await hs.marketing_events.create({...})
event = await hs.marketing_events.get("ext-event-id", "ext-account-id")
await hs.marketing_events.update("ext-event-id", "ext-account-id", {...})
await hs.marketing_events.delete("ext-event-id", "ext-account-id")

# Upsert
await hs.marketing_events.upsert({...})
await hs.marketing_events.batch_upsert([...])

# Zoeken
results = await hs.marketing_events.search({...})

# Deelnemers
participants = await hs.marketing_events.get_participants("ext-event-id", "ext-account-id")
await hs.marketing_events.upsert_participant("ext-event-id", "REGISTERED", {...})
await hs.marketing_events.upsert_participant_by_email("ext-event-id", "ATTENDED", {...})
await hs.marketing_events.batch_upsert_participants("ext-event-id", "REGISTERED", [...])

# Lijstkoppeling
assocs = await hs.marketing_events.get_list_associations("ext-account-id", "ext-event-id")
await hs.marketing_events.associate_list("ext-account-id", "ext-event-id", "list-id")
await hs.marketing_events.disassociate_list("ext-account-id", "ext-event-id", "list-id")

# Status
await hs.marketing_events.complete("ext-event-id", "ext-account-id")
await hs.marketing_events.cancel("ext-event-id", "ext-account-id")
```

---

## Marketing – Transactional Email

**Toegang**: `hs.transactional_email`

```python
# Email versturen
result = await hs.transactional_email.send({
    "emailId": 12345,
    "message": {
        "to": "recipient@example.com",
        "from": "noreply@company.com",
        "sendId": "unique-send-id"
    },
    "contactProperties": {"firstname": "Jan"},
    "customProperties": {"order_number": "ORD-001"}
})

# SMTP tokens
tokens = await hs.transactional_email.list_smtp_tokens()
token = await hs.transactional_email.create_smtp_token({"campaignName": "Order Confirmations"})
token = await hs.transactional_email.get_smtp_token("token-id")
await hs.transactional_email.delete_smtp_token("token-id")
new_password = await hs.transactional_email.reset_smtp_token_password("token-id")
```

---

## Marketing – Single Send

**Toegang**: `hs.single_send`

```python
result = await hs.single_send.send({
    "emailId": 12345,
    "message": {
        "to": "recipient@example.com"
    },
    "customProperties": {"promo_code": "SPRING24"}
})
```

---

## Automation – Workflow Actions

**Toegang**: `hs.automation_actions`

```python
# Action definities
actions = await hs.automation_actions.list("app-123")
action = await hs.automation_actions.create("app-123", {...})
action = await hs.automation_actions.get("app-123", "definition-id")
await hs.automation_actions.update("app-123", "definition-id", {...})
await hs.automation_actions.delete("app-123", "definition-id")

# Functions (serverless code achter acties)
functions = await hs.automation_actions.list_functions("app-123", "definition-id")
func = await hs.automation_actions.get_function("app-123", "definition-id", "PRE_ACTION_EXECUTION")
await hs.automation_actions.create_or_replace_function("app-123", "definition-id", "PRE_ACTION_EXECUTION", {...})
await hs.automation_actions.delete_function("app-123", "definition-id", "PRE_ACTION_EXECUTION")

# Functions by ID
func = await hs.automation_actions.get_function_by_id("app-123", "def-id", "type", "func-id")
await hs.automation_actions.create_or_replace_function_by_id("app-123", "def-id", "type", "func-id", {...})
await hs.automation_actions.delete_function_by_id("app-123", "def-id", "type", "func-id")

# Revisies
revisions = await hs.automation_actions.list_revisions("app-123", "definition-id")
revision = await hs.automation_actions.get_revision("app-123", "definition-id", "revision-id")

# Callbacks
await hs.automation_actions.complete_callback("callback-id", {"outputFields": {...}})
await hs.automation_actions.batch_complete_callbacks([...])
```

---

## Automation – Sequences

**Toegang**: `hs.sequences`

```python
sequences = await hs.sequences.list()
sequence = await hs.sequences.get("sequence-id")

# Contact enrollen in sequence
enrollment = await hs.sequences.enroll({
    "sequenceId": "sequence-id",
    "contactId": "contact-123",
    "senderEmail": "sales@company.com"
})

# Enrollments voor een contact
enrollments = await hs.sequences.get_enrollments_for_contact("contact-123")
```

---

## Conversations – Threads & Inbox

**Toegang**: `hs.threads`

```python
# Threads
threads = await hs.threads.list(limit=20)
thread = await hs.threads.get("thread-id")
await hs.threads.update("thread-id", {"status": "CLOSED"})

# Toewijzing
await hs.threads.set_assignee("thread-id", {"actorId": "A-user-123"})
await hs.threads.remove_assignee("thread-id")

# Berichten in thread
messages = await hs.threads.list_messages("thread-id")
message = await hs.threads.get_message("thread-id", "message-id")
await hs.threads.send_message("thread-id", {
    "type": "MESSAGE",
    "text": "Bedankt voor uw bericht!",
    "senderActorId": "A-user-123"
})

# Actors
actors = await hs.threads.batch_read_actors([{"actorId": "A-user-123"}])
actor = await hs.threads.get_actor("A-user-123")

# Inboxen
inboxes = await hs.threads.list_inboxes()
inbox = await hs.threads.get_inbox("inbox-id")

# Channel accounts
channels = await hs.threads.list_channel_accounts()
```

---

## Conversations – Messages

**Toegang**: `hs.messages`

```python
message = await hs.messages.get_message("message-id")
original = await hs.messages.get_original_email("message-id")
```

---

## Conversations – Custom Channels

**Toegang**: `hs.custom_channels`

```python
# Kanalen
channels = await hs.custom_channels.list()
channel = await hs.custom_channels.create({...})
channel = await hs.custom_channels.get("channel-id")
await hs.custom_channels.update("channel-id", {...})
await hs.custom_channels.delete("channel-id")

# Berichten via kanaal
await hs.custom_channels.send_message("channel-id", {...})
message = await hs.custom_channels.get_message("channel-id", "message-id")
await hs.custom_channels.update_message_status("channel-id", "message-id", {...})

# Threads via kanaal
thread = await hs.custom_channels.create_thread("channel-id", {...})
thread = await hs.custom_channels.get_thread("channel-id", "thread-id")

# Token
token = await hs.custom_channels.create_token("channel-id", {...})
```

---

## Conversations – Visitor Identification

Genereer tokens om websitebezoekers te identificeren.

**Toegang**: `hs.visitor_identification`

```python
result = await hs.visitor_identification.generate_token(
    email="bezoeker@example.com",
    first_name="Jan",   # optioneel
    last_name="Jansen"  # optioneel
)
token = result["token"]
# Gebruik dit token in de HubSpot tracking code op je website
```

---

## Events – Definitions

Definieer custom behavioral events.

**Toegang**: `hs.event_definitions`

```python
# Event definities
events = await hs.event_definitions.list()
event = await hs.event_definitions.create({
    "name": "pe_product_viewed",
    "label": "Product Viewed",
    "primaryObject": "CONTACT"
})
event = await hs.event_definitions.get("pe_product_viewed")
await hs.event_definitions.update("pe_product_viewed", {"label": "Updated Label"})
await hs.event_definitions.delete("pe_product_viewed")

# Event properties
prop = await hs.event_definitions.create_property("pe_product_viewed", {
    "name": "product_name", "label": "Product Name", "type": "string"
})
prop = await hs.event_definitions.get_property("pe_product_viewed", "product_name")
await hs.event_definitions.update_property("pe_product_viewed", "product_name", {...})
await hs.event_definitions.delete_property("pe_product_viewed", "product_name")
```

---

## Events – Send

Verstuur behavioral events.

**Toegang**: `hs.event_send`

```python
# Enkel event
await hs.event_send.send({
    "eventName": "pe_product_viewed",
    "objectId": "contact-123",
    "properties": {
        "product_name": "Enterprise Plan",
        "product_price": "5000"
    },
    "occurredAt": "2024-03-15T10:00:00.000Z"
})

# Batch
await hs.event_send.send_batch([
    {"eventName": "pe_product_viewed", "objectId": "123", ...},
    {"eventName": "pe_product_viewed", "objectId": "456", ...},
])
```

---

## Events – Occurrences

Lees event voorkomens.

**Toegang**: `hs.event_occurrences`

```python
occurrences = await hs.event_occurrences.list(
    objectType="contact",
    objectId="123",
    after="cursor"
)

event_types = await hs.event_occurrences.list_event_types()
```

---

## Files

Beheer bestanden en mappen in de HubSpot file manager.

**Toegang**: `hs.files`

```python
# Upload
file = await hs.files.upload(
    files={"file": open("document.pdf", "rb")},
    data={"folderId": "folder-123", "options": '{"access": "PUBLIC_INDEXABLE"}'}
)

# Import van URL
task = await hs.files.import_from_url({
    "url": "https://example.com/image.png",
    "folderId": "folder-123"
})
status = await hs.files.get_import_status("task-id")

# CRUD
files = await hs.files.list(limit=50)
file = await hs.files.get("file-id")
await hs.files.update("file-id", {"name": "renamed.pdf"})
await hs.files.replace("file-id", files={"file": open("new.pdf", "rb")})
await hs.files.delete("file-id")

# URLs
signed = await hs.files.get_signed_url("file-id")
public = await hs.files.get_public_url_redirect("file-id")

# Mappen
folders = await hs.files.list_folders()
folder = await hs.files.create_folder({"name": "Documents"})
folder = await hs.files.get_folder("folder-id")
await hs.files.update_folder("folder-id", {"name": "Updated"})
await hs.files.delete_folder("folder-id")
status = await hs.files.check_folder_update_status("task-id")
```

---

## Settings – Currency

Beheer valuta-instellingen en wisselkoersen.

**Toegang**: `hs.currency`

```python
# Account valuta info
info = await hs.currency.get_information()
unsupported = await hs.currency.get_unsupported_currencies()

# Valuta's beheren
currencies = await hs.currency.list_currencies()
currency = await hs.currency.create_currency({"code": "EUR", ...})
currency = await hs.currency.get_currency("currency-id")
await hs.currency.update_currency("currency-id", {...})
await hs.currency.delete_currency("currency-id")

# Wisselkoersen
await hs.currency.update_exchange_rate({...})
rates = await hs.currency.batch_read_exchange_rates([...])

# Bedrijfsvaluta instellen
await hs.currency.set_company_currency({"currencyCode": "EUR"})
await hs.currency.add_currency({...})
```

---

## Settings – User Provisioning

Beheer gebruikers en hun rollen/teams.

**Toegang**: `hs.user_provisioning`

```python
users = await hs.user_provisioning.list()
user = await hs.user_provisioning.create({
    "email": "nieuwe.medewerker@company.com",
    "roleId": "role-123"
})
user = await hs.user_provisioning.get("user-id")
await hs.user_provisioning.update("user-id", {"roleId": "new-role"})
await hs.user_provisioning.delete("user-id")

roles = await hs.user_provisioning.list_roles()
teams = await hs.user_provisioning.list_teams()
```

---

## Settings – Feature Flags

Beheer feature flags voor HubSpot public apps.

**Toegang**: `hs.feature_flags("app-id")` (factory method, niet property)

```python
ff = hs.feature_flags("app-123")

# Alle flags
flags = await ff.list_all()

# Specifieke flag
flag = await ff.get("my_new_feature")

# Flag instellen
await ff.set("my_new_feature", default_value=True)

# Flag verwijderen
await ff.delete("my_new_feature")

# Portal-specifieke overrides
portals = await ff.list_portals("my_new_feature", limit=100)
await ff.batch_upsert_portals("my_new_feature", [
    {"portalId": 12345, "flagValue": True},
    {"portalId": 67890, "flagValue": False},
])
await ff.batch_delete_portals("my_new_feature", [12345, 67890])
```

---

## Settings – Data Sources

Beheer Data Studio data sources.

**Toegang**: `hs.data_sources`

```python
source = await hs.data_sources.create({...})
source = await hs.data_sources.get("datasource-id")
source = await hs.data_sources.update("datasource-id", {...})
await hs.data_sources.delete("datasource-id")
```

---

## Webhooks

Beheer webhook instellingen en abonnementen.

**Toegang**: `hs.webhooks`

```python
# App webhook settings
settings = await hs.webhooks.get_settings("app-123")
await hs.webhooks.update_settings("app-123", {
    "targetUrl": "https://yourapp.com/webhooks",
    "throttling": {"maxConcurrentRequests": 10, "period": "SECONDLY"}
})
await hs.webhooks.delete_settings("app-123")

# Subscriptions
subs = await hs.webhooks.list_subscriptions("app-123")
sub = await hs.webhooks.create_subscription("app-123", {
    "eventType": "contact.creation",
    "active": True
})
sub = await hs.webhooks.get_subscription("app-123", "sub-id")
await hs.webhooks.update_subscription("app-123", "sub-id", {"active": False})
await hs.webhooks.delete_subscription("app-123", "sub-id")
await hs.webhooks.batch_update_subscriptions("app-123", [...])
```

---

## Account – Info

**Toegang**: `hs.account_info`

```python
details = await hs.account_info.get_details()
usage = await hs.account_info.get_api_usage()
```

---

## Account – Audit Logs

**Toegang**: `hs.audit_logs`

```python
logs = await hs.audit_logs.list_audit_logs(limit=100)
login_activity = await hs.audit_logs.list_login_activity()
security = await hs.audit_logs.list_security_activity()
```

---

## Account – Business Units

**Toegang**: `hs.business_units`

```python
units = await hs.business_units.get_for_user("user-id")
```

---

## Account – Subscriptions

Beheer communicatie-voorkeuren.

**Toegang**: `hs.subscriptions`

```python
# Subscription definities
definitions = await hs.subscriptions.list_definitions()

# Preferences link genereren
link = await hs.subscriptions.generate_link({
    "portalId": 12345,
    "email": "user@example.com"
})

# Status controleren
status = await hs.subscriptions.get_status("user@example.com")
statuses = await hs.subscriptions.batch_read_statuses([
    {"email": "a@example.com"},
    {"email": "b@example.com"}
])

# Subscribe / Unsubscribe
await hs.subscriptions.subscribe({
    "emailAddress": "user@example.com",
    "subscriptionId": "sub-123",
    "legalBasis": "LEGITIMATE_INTEREST_CLIENT"
})
await hs.subscriptions.unsubscribe({
    "emailAddress": "user@example.com",
    "subscriptionId": "sub-123"
})

# Batch
await hs.subscriptions.batch_subscribe([...])
await hs.subscriptions.batch_unsubscribe([...])
```

---

## OAuth

Zie [Authentication](#authentication) voor volledige OAuth2 flow.

**Toegang**: `HubSpotClient.oauth(client_id, client_secret, redirect_uri)`

| Methode | Beschrijving |
|---|---|
| `get_authorize_url(scopes, state?, optional_scopes?)` | Bouw authorization URL |
| `exchange_code(code)` | Wissel auth code voor tokens |
| `refresh_token(refresh_token)` | Vernieuw verlopen access token |
| `get_token_info(token)` | Introspect token metadata |
| `revoke_token(token)` | Trek refresh token in |

---

## HubSpotClient Constructor

```python
HubSpotClient(
    access_token: str,          # Private app token of OAuth access token
    base_url: str = "https://api.hubapi.com",  # API base URL
    api_version: str = "2026-03",              # API versie
    timeout: float = 30.0,                      # Request timeout in seconden
    max_retries: int = 4,                       # Aantal retries bij 429/5xx
)
```

### Alle properties en methoden

```python
# CRM Core
hs.contacts             → ContactsClient
hs.companies            → CompaniesClient
hs.deals                → DealsClient
hs.tickets              → TicketsClient
hs.objects("type")      → CrmObjectClient (generic, voor elk type)
hs.associations         → AssociationsClient
hs.associations_schema  → AssociationsSchemaClient
hs.pipelines            → PipelinesClient
hs.properties           → PropertiesClient
hs.lists                → ListsClient
hs.imports              → ImportsClient
hs.exports              → ExportsClient
hs.schemas              → SchemasClient
hs.owners               → OwnersClient
hs.calling_extensions   → CallingExtensionsClient
hs.crm_cards            → CrmCardsClient
hs.video_conferencing   → VideoConferencingClient

# CRM Activities
hs.calls                → CallsClient
hs.emails               → EmailsClient
hs.meetings             → MeetingsClient
hs.notes                → NotesClient
hs.tasks                → TasksClient
hs.communications       → CommunicationsClient
hs.postal_mail          → PostalMailClient

# CRM Extended
hs.leads                → LeadsClient
hs.feedback_submissions → FeedbackSubmissionsClient
hs.contracts            → ContractsClient
hs.projects             → ProjectsClient
hs.goal_targets         → GoalTargetsClient
hs.crm_users            → CrmUsersClient
hs.services             → ServicesClient
hs.courses              → CoursesClient
hs.listings             → ListingsClient
hs.partner_clients      → PartnerClientsClient
hs.partner_services     → PartnerServicesClient
hs.tax_rates            → TaxRatesClient

# CRM Specialized
hs.timeline             → TimelineClient
hs.transcriptions       → TranscriptionsClient
hs.property_validations → PropertyValidationsClient
hs.limits               → LimitsClient
hs.forecasts            → ForecastsClient
hs.object_library       → ObjectLibraryClient
hs.meetings_scheduler   → MeetingsSchedulerClient

# Commerce
hs.products             → ProductsClient
hs.line_items           → LineItemsClient
hs.quotes               → QuotesClient
hs.invoices             → InvoicesClient
hs.orders               → OrdersClient
hs.carts                → CartsClient
hs.payments             → PaymentsClient
hs.commerce_subscriptions → CommerceSubscriptionsClient
hs.discounts            → DiscountsClient
hs.fees                 → FeesClient
hs.taxes                → TaxesClient

# CMS
hs.pages                → PagesClient
hs.blog_posts           → BlogPostsClient
hs.blog_authors         → BlogAuthorsClient
hs.blog_tags            → BlogTagsClient
hs.blog_settings        → BlogSettingsClient
hs.hubdb                → HubDbClient
hs.domains              → DomainsClient
hs.source_code          → SourceCodeClient
hs.url_redirects        → UrlRedirectsClient
hs.site_search          → SiteSearchClient
hs.cms_audit            → CmsAuditClient

# Marketing
hs.campaigns            → CampaignsClient
hs.forms                → FormsClient
hs.marketing_events     → MarketingEventsClient
hs.transactional_email  → TransactionalEmailClient
hs.single_send          → SingleSendClient

# Automation
hs.automation_actions   → ActionsClient
hs.sequences            → SequencesClient

# Conversations
hs.threads              → ThreadsClient
hs.messages             → MessagesClient
hs.custom_channels      → CustomChannelsClient
hs.visitor_identification → VisitorIdentificationClient

# Events
hs.event_definitions    → EventDefinitionsClient
hs.event_send           → EventSendClient
hs.event_occurrences    → EventOccurrencesClient

# Files
hs.files                → FilesClient

# Settings
hs.currency             → CurrencyClient
hs.user_provisioning    → UserProvisioningClient
hs.feature_flags("id")  → FeatureFlagsClient (factory method)
hs.data_sources         → DataSourcesClient

# Webhooks
hs.webhooks             → WebhooksClient

# Account
hs.account_info         → AccountInfoClient
hs.audit_logs           → AuditLogsClient
hs.business_units       → BusinessUnitsClient
hs.subscriptions        → SubscriptionsClient

# Auth (static)
HubSpotClient.oauth(client_id, client_secret, redirect_uri) → OAuthClient
```

---

*SDK Reference v0.1.0 – Gegenereerd op 2026-04-02*
