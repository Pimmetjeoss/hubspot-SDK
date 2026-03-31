# HubSpot SDK

Async-first Python SDK + CLI for the complete HubSpot API. Covers 1128 endpoints across 10 API categories.

## Install

```bash
pip install hubspot-sdk
```

## Quick Start

```python
import asyncio
from hubspot_sdk import HubSpotClient

async def main():
    async with HubSpotClient(access_token="pat-xxx") as hs:
        # List contacts
        contacts = await hs.contacts.list(limit=5, properties=["email", "firstname"])
        for c in contacts.results:
            print(c.id, c.properties.get("email"))

        # Create a deal
        deal = await hs.deals.create({"dealname": "Big Deal", "pipeline": "default"})
        print(f"Created deal: {deal.id}")

        # Search
        results = await hs.contacts.search(query="example.com")
        print(f"Found {results.total} contacts")

        # Any object type via generic client
        products = await hs.objects("products").list(limit=10)

asyncio.run(main())
```

## CLI

```bash
export HUBSPOT_ACCESS_TOKEN=pat-xxx

hubspot contacts list --limit 5 -p email -p firstname
hubspot contacts get 12345
hubspot contacts create -p email test@example.com -p firstname Test
hubspot contacts search -q "example.com"
hubspot deals list -p dealname -p amount
hubspot objects list line_items
hubspot files upload ./document.pdf
hubspot pipelines list deals
hubspot properties list contacts
hubspot account info
```

## API Coverage

| Category       | Specs | Endpoints |
|----------------|-------|-----------|
| CRM            | 53    | 628       |
| CMS            | 11    | 201       |
| Marketing      | 5     | 73        |
| Conversations  | 3     | 47        |
| Webhooks       | 1     | 34        |
| Settings       | 2     | 22        |
| Automation     | 2     | 22        |
| Files          | 1     | 20        |
| Events         | 3     | 13        |
| Auth           | 1     | 3         |
| Other          | 18    | 65        |
| **Total**      | **102** | **1128** |

## Requirements

- Python 3.10+
- httpx, pydantic, click, rich
