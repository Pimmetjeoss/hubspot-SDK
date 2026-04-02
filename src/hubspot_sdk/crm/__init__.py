"""CRM domain module – contacts, companies, deals, tickets, and 40+ more object types."""

# Activity clients
from hubspot_sdk.crm.activities import (
    CallsClient,
    CommunicationsClient,
    EmailsClient,
    MeetingsClient,
    NotesClient,
    PostalMailClient,
    TasksClient,
)
from hubspot_sdk.crm.associations import AssociationsClient, AssociationsSchemaClient
from hubspot_sdk.crm.companies import CompaniesClient
from hubspot_sdk.crm.contacts import ContactsClient
from hubspot_sdk.crm.deals import DealsClient

# Extended CRM object clients
from hubspot_sdk.crm.extended_objects import (
    ContractsClient,
    CoursesClient,
    CrmUsersClient,
    FeedbackSubmissionsClient,
    GoalTargetsClient,
    LeadsClient,
    ListingsClient,
    PartnerClientsClient,
    PartnerServicesClient,
    ProjectsClient,
    ServicesClient,
    TaxRatesClient,
)
from hubspot_sdk.crm.extensions import (
    CallingExtensionsClient,
    CrmCardsClient,
    VideoConferencingClient,
)

# Specialized domain clients
from hubspot_sdk.crm.forecasts import ForecastsClient
from hubspot_sdk.crm.imports_exports import ExportsClient, ImportsClient
from hubspot_sdk.crm.limits import LimitsClient
from hubspot_sdk.crm.lists import ListsClient
from hubspot_sdk.crm.meetings_scheduler import MeetingsSchedulerClient
from hubspot_sdk.crm.object_library import ObjectLibraryClient
from hubspot_sdk.crm.objects import CrmObjectClient
from hubspot_sdk.crm.owners import OwnersClient
from hubspot_sdk.crm.pipelines import PipelinesClient
from hubspot_sdk.crm.properties import PropertiesClient
from hubspot_sdk.crm.property_validations import PropertyValidationsClient
from hubspot_sdk.crm.schemas import SchemasClient
from hubspot_sdk.crm.tickets import TicketsClient
from hubspot_sdk.crm.timeline import TimelineClient
from hubspot_sdk.crm.transcriptions import TranscriptionsClient

__all__ = [
    "CrmObjectClient",
    "ContactsClient",
    "CompaniesClient",
    "DealsClient",
    "TicketsClient",
    "AssociationsClient",
    "AssociationsSchemaClient",
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
    # Activities
    "CallsClient",
    "CommunicationsClient",
    "EmailsClient",
    "MeetingsClient",
    "NotesClient",
    "PostalMailClient",
    "TasksClient",
    # Extended objects
    "ContractsClient",
    "CoursesClient",
    "CrmUsersClient",
    "FeedbackSubmissionsClient",
    "GoalTargetsClient",
    "LeadsClient",
    "ListingsClient",
    "PartnerClientsClient",
    "PartnerServicesClient",
    "ProjectsClient",
    "ServicesClient",
    "TaxRatesClient",
    # Specialized
    "ForecastsClient",
    "LimitsClient",
    "MeetingsSchedulerClient",
    "ObjectLibraryClient",
    "PropertyValidationsClient",
    "TimelineClient",
    "TranscriptionsClient",
]
