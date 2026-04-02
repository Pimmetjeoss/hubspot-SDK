"""Commerce CRM object clients.

Each class targets a specific commerce object type and extends CrmObjectClient,
which already provides the full CRUD + batch + search + association surface.
ProductsClient adds merge() because the HubSpot products API supports it;
the remaining commerce objects do not expose a merge endpoint.
"""

from __future__ import annotations

from hubspot_sdk.core.http import HttpClient
from hubspot_sdk.core.models import HubSpotObject
from hubspot_sdk.crm.objects import CrmObjectClient


class ProductsClient(CrmObjectClient):
    """Client for the 'products' object type.

    Inherits full CRUD + batch + search + association methods from
    CrmObjectClient and adds merge() for deduplication.
    """

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "products")

    async def merge(self, primary_id: str, object_id_to_merge: str) -> HubSpotObject:
        """Merge two product records, keeping ``primary_id`` as the winner."""
        data = await self._http.post(
            f"{self._base}/merge",
            json={"primaryObjectId": primary_id, "objectIdToMerge": object_id_to_merge},
        )
        return HubSpotObject.model_validate(data)


class LineItemsClient(CrmObjectClient):
    """Client for the 'line_items' object type.

    Line items are child objects of quotes, orders, and invoices.
    Full CRUD + batch + search + association methods are inherited.
    """

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "line_items")


class QuotesClient(CrmObjectClient):
    """Client for the 'quotes' object type.

    Quotes are primarily read-heavy; they are created through the
    HubSpot UI or via associations from deals.  Full CRUD + batch +
    search + association methods are still inherited for completeness.
    """

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "quotes")


class InvoicesClient(CrmObjectClient):
    """Client for the 'invoices' object type.

    Full CRUD + batch + search + association methods are inherited.
    """

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "invoices")


class OrdersClient(CrmObjectClient):
    """Client for the 'orders' object type.

    Full CRUD + batch + search + association methods are inherited.
    """

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "orders")


class CartsClient(CrmObjectClient):
    """Client for the 'carts' object type.

    Full CRUD + batch + search + association methods are inherited.
    """

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "carts")


class PaymentsClient(CrmObjectClient):
    """Client for the 'commerce_payments' object type.

    Full CRUD + batch + search + association methods are inherited.
    """

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "commerce_payments")


class CommerceSubscriptionsClient(CrmObjectClient):
    """Client for the 'subscriptions' object type.

    Represents recurring billing subscriptions in HubSpot Commerce.
    Full CRUD + batch + search + association methods are inherited.
    """

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "subscriptions")


class DiscountsClient(CrmObjectClient):
    """Client for the 'discounts' object type.

    Full CRUD + batch + search + association methods are inherited.
    """

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "discounts")


class FeesClient(CrmObjectClient):
    """Client for the 'fees' object type.

    Full CRUD + batch + search + association methods are inherited.
    """

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "fees")


class TaxesClient(CrmObjectClient):
    """Client for the 'taxes' object type.

    Full CRUD + batch + search + association methods are inherited.
    """

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, "taxes")
