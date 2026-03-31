"""CRM domain module – contacts, companies, deals, tickets, and 40+ more object types."""

from hubspot_sdk.crm.objects import CrmObjectClient
from hubspot_sdk.crm.contacts import ContactsClient
from hubspot_sdk.crm.companies import CompaniesClient
from hubspot_sdk.crm.deals import DealsClient
from hubspot_sdk.crm.tickets import TicketsClient
from hubspot_sdk.crm.associations import AssociationsClient
from hubspot_sdk.crm.pipelines import PipelinesClient
from hubspot_sdk.crm.properties import PropertiesClient
from hubspot_sdk.crm.lists import ListsClient
from hubspot_sdk.crm.imports_exports import ImportsClient, ExportsClient
from hubspot_sdk.crm.schemas import SchemasClient
from hubspot_sdk.crm.owners import OwnersClient
from hubspot_sdk.crm.extensions import (
    CallingExtensionsClient,
    CrmCardsClient,
    VideoConferencingClient,
)

__all__ = [
    "CrmObjectClient",
    "ContactsClient",
    "CompaniesClient",
    "DealsClient",
    "TicketsClient",
    "AssociationsClient",
    "PipelinesClient",
    "PropertiesClient",
    "ListsClient",
    "ImportsClient",
    "ExportsClient",
    "SchemasClient",
    "OwnersClient",
    "CallingExtensionsClient",
    "CrmCardsClient",
    "VideoConferencingClient",
]
