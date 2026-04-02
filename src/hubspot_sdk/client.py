"""Main HubSpotClient – single entry point composing all domain modules."""

from __future__ import annotations

from hubspot_sdk.account.audit_logs import AuditLogsClient
from hubspot_sdk.account.business_units import BusinessUnitsClient

# Account
from hubspot_sdk.account.info import AccountInfoClient
from hubspot_sdk.account.subscriptions import SubscriptionsClient

# Auth
from hubspot_sdk.auth.oauth import OAuthClient

# Automation
from hubspot_sdk.automation.actions import ActionsClient
from hubspot_sdk.automation.sequences import SequencesClient
from hubspot_sdk.cms.audit import CmsAuditClient
from hubspot_sdk.cms.blog import BlogAuthorsClient, BlogPostsClient, BlogSettingsClient, BlogTagsClient
from hubspot_sdk.cms.domains import DomainsClient
from hubspot_sdk.cms.hubdb import HubDbClient

# CMS
from hubspot_sdk.cms.pages import PagesClient
from hubspot_sdk.cms.site_search import SiteSearchClient
from hubspot_sdk.cms.source_code import SourceCodeClient
from hubspot_sdk.cms.url_redirects import UrlRedirectsClient

# Commerce
from hubspot_sdk.commerce.commerce import (
    CartsClient,
    CommerceSubscriptionsClient,
    DiscountsClient,
    FeesClient,
    InvoicesClient,
    LineItemsClient,
    OrdersClient,
    PaymentsClient,
    ProductsClient,
    QuotesClient,
    TaxesClient,
)
from hubspot_sdk.conversations.channels import CustomChannelsClient
from hubspot_sdk.conversations.messages import MessagesClient

# Conversations
from hubspot_sdk.conversations.threads import ThreadsClient
from hubspot_sdk.conversations.visitor_identification import VisitorIdentificationClient
from hubspot_sdk.core.http import API_VERSION, BASE_URL, HttpClient

# CRM – activities
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

# CRM – extended objects
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
from hubspot_sdk.crm.extensions import CallingExtensionsClient, CrmCardsClient, VideoConferencingClient

# CRM – specialized
from hubspot_sdk.crm.forecasts import ForecastsClient
from hubspot_sdk.crm.imports_exports import ExportsClient, ImportsClient
from hubspot_sdk.crm.limits import LimitsClient
from hubspot_sdk.crm.lists import ListsClient
from hubspot_sdk.crm.meetings_scheduler import MeetingsSchedulerClient
from hubspot_sdk.crm.object_library import ObjectLibraryClient

# CRM – core
from hubspot_sdk.crm.objects import CrmObjectClient
from hubspot_sdk.crm.owners import OwnersClient
from hubspot_sdk.crm.pipelines import PipelinesClient
from hubspot_sdk.crm.properties import PropertiesClient
from hubspot_sdk.crm.property_validations import PropertyValidationsClient
from hubspot_sdk.crm.schemas import SchemasClient
from hubspot_sdk.crm.tickets import TicketsClient
from hubspot_sdk.crm.timeline import TimelineClient
from hubspot_sdk.crm.transcriptions import TranscriptionsClient

# Events
from hubspot_sdk.events.definitions import EventDefinitionsClient
from hubspot_sdk.events.occurrences import EventOccurrencesClient
from hubspot_sdk.events.send import EventSendClient

# Files
from hubspot_sdk.files.files import FilesClient

# Marketing
from hubspot_sdk.marketing.campaigns import CampaignsClient
from hubspot_sdk.marketing.emails import SingleSendClient
from hubspot_sdk.marketing.events import MarketingEventsClient
from hubspot_sdk.marketing.forms import FormsClient
from hubspot_sdk.marketing.transactional import TransactionalEmailClient

# Settings
from hubspot_sdk.settings.currency import CurrencyClient
from hubspot_sdk.settings.data_sources import DataSourcesClient
from hubspot_sdk.settings.feature_flags import FeatureFlagsClient
from hubspot_sdk.settings.users import UserProvisioningClient

# Webhooks
from hubspot_sdk.webhooks.webhooks import WebhooksClient


class HubSpotClient:
    """Unified client for the entire HubSpot API.

    Usage::

        async with HubSpotClient(access_token="pat-xxx") as hs:
            contacts = await hs.contacts.list(limit=5)
            deal = await hs.deals.create({"dealname": "Big Deal", "pipeline": "default"})

    All sub-clients are lazily instantiated on first access.
    """

    def __init__(
        self,
        access_token: str,
        *,
        base_url: str = BASE_URL,
        api_version: str = API_VERSION,
        timeout: float = 30.0,
        max_retries: int = 4,
    ) -> None:
        self._http = HttpClient(
            access_token,
            base_url=base_url,
            api_version=api_version,
            timeout=timeout,
            max_retries=max_retries,
        )
        self._cache: dict[str, object] = {}

    def _get(self, key: str, factory: type) -> object:
        if key not in self._cache:
            self._cache[key] = factory(self._http)
        return self._cache[key]

    # -- Lifecycle ------------------------------------------------------------

    async def close(self) -> None:
        await self._http.close()

    async def __aenter__(self) -> HubSpotClient:
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self.close()

    # =========================================================================
    # CRM
    # =========================================================================

    @property
    def contacts(self) -> ContactsClient:
        return self._get("contacts", ContactsClient)  # type: ignore[return-value]

    @property
    def companies(self) -> CompaniesClient:
        return self._get("companies", CompaniesClient)  # type: ignore[return-value]

    @property
    def deals(self) -> DealsClient:
        return self._get("deals", DealsClient)  # type: ignore[return-value]

    @property
    def tickets(self) -> TicketsClient:
        return self._get("tickets", TicketsClient)  # type: ignore[return-value]

    @property
    def associations(self) -> AssociationsClient:
        return self._get("associations", AssociationsClient)  # type: ignore[return-value]

    @property
    def associations_schema(self) -> AssociationsSchemaClient:
        return self._get("associations_schema", AssociationsSchemaClient)  # type: ignore[return-value]

    @property
    def pipelines(self) -> PipelinesClient:
        return self._get("pipelines", PipelinesClient)  # type: ignore[return-value]

    @property
    def properties(self) -> PropertiesClient:
        return self._get("properties", PropertiesClient)  # type: ignore[return-value]

    @property
    def lists(self) -> ListsClient:
        return self._get("lists", ListsClient)  # type: ignore[return-value]

    @property
    def imports(self) -> ImportsClient:
        return self._get("imports", ImportsClient)  # type: ignore[return-value]

    @property
    def exports(self) -> ExportsClient:
        return self._get("exports", ExportsClient)  # type: ignore[return-value]

    @property
    def schemas(self) -> SchemasClient:
        return self._get("schemas", SchemasClient)  # type: ignore[return-value]

    @property
    def owners(self) -> OwnersClient:
        return self._get("owners", OwnersClient)  # type: ignore[return-value]

    @property
    def calling_extensions(self) -> CallingExtensionsClient:
        return self._get("calling_extensions", CallingExtensionsClient)  # type: ignore[return-value]

    @property
    def crm_cards(self) -> CrmCardsClient:
        return self._get("crm_cards", CrmCardsClient)  # type: ignore[return-value]

    @property
    def video_conferencing(self) -> VideoConferencingClient:
        return self._get("video_conferencing", VideoConferencingClient)  # type: ignore[return-value]

    def objects(self, object_type: str) -> CrmObjectClient:
        """Get a generic CRM object client for any object type.

        Useful for custom objects or less common types.
        """
        key = f"objects_{object_type}"
        if key not in self._cache:
            self._cache[key] = CrmObjectClient(self._http, object_type)
        return self._cache[key]  # type: ignore[return-value]

    # -- CRM Activities -------------------------------------------------------

    @property
    def calls(self) -> CallsClient:
        return self._get("calls", CallsClient)  # type: ignore[return-value]

    @property
    def emails(self) -> EmailsClient:
        return self._get("emails", EmailsClient)  # type: ignore[return-value]

    @property
    def meetings(self) -> MeetingsClient:
        return self._get("meetings", MeetingsClient)  # type: ignore[return-value]

    @property
    def notes(self) -> NotesClient:
        return self._get("notes", NotesClient)  # type: ignore[return-value]

    @property
    def tasks(self) -> TasksClient:
        return self._get("tasks", TasksClient)  # type: ignore[return-value]

    @property
    def communications(self) -> CommunicationsClient:
        return self._get("communications", CommunicationsClient)  # type: ignore[return-value]

    @property
    def postal_mail(self) -> PostalMailClient:
        return self._get("postal_mail", PostalMailClient)  # type: ignore[return-value]

    # -- CRM Extended Objects -------------------------------------------------

    @property
    def leads(self) -> LeadsClient:
        return self._get("leads", LeadsClient)  # type: ignore[return-value]

    @property
    def feedback_submissions(self) -> FeedbackSubmissionsClient:
        return self._get("feedback_submissions", FeedbackSubmissionsClient)  # type: ignore[return-value]

    @property
    def contracts(self) -> ContractsClient:
        return self._get("contracts", ContractsClient)  # type: ignore[return-value]

    @property
    def projects(self) -> ProjectsClient:
        return self._get("projects", ProjectsClient)  # type: ignore[return-value]

    @property
    def goal_targets(self) -> GoalTargetsClient:
        return self._get("goal_targets", GoalTargetsClient)  # type: ignore[return-value]

    @property
    def crm_users(self) -> CrmUsersClient:
        return self._get("crm_users", CrmUsersClient)  # type: ignore[return-value]

    @property
    def services(self) -> ServicesClient:
        return self._get("services", ServicesClient)  # type: ignore[return-value]

    @property
    def courses(self) -> CoursesClient:
        return self._get("courses", CoursesClient)  # type: ignore[return-value]

    @property
    def listings(self) -> ListingsClient:
        return self._get("listings", ListingsClient)  # type: ignore[return-value]

    @property
    def partner_clients(self) -> PartnerClientsClient:
        return self._get("partner_clients", PartnerClientsClient)  # type: ignore[return-value]

    @property
    def partner_services(self) -> PartnerServicesClient:
        return self._get("partner_services", PartnerServicesClient)  # type: ignore[return-value]

    @property
    def tax_rates(self) -> TaxRatesClient:
        return self._get("tax_rates", TaxRatesClient)  # type: ignore[return-value]

    # -- CRM Specialized ------------------------------------------------------

    @property
    def timeline(self) -> TimelineClient:
        return self._get("timeline", TimelineClient)  # type: ignore[return-value]

    @property
    def transcriptions(self) -> TranscriptionsClient:
        return self._get("transcriptions", TranscriptionsClient)  # type: ignore[return-value]

    @property
    def property_validations(self) -> PropertyValidationsClient:
        return self._get("property_validations", PropertyValidationsClient)  # type: ignore[return-value]

    @property
    def limits(self) -> LimitsClient:
        return self._get("limits", LimitsClient)  # type: ignore[return-value]

    @property
    def forecasts(self) -> ForecastsClient:
        return self._get("forecasts", ForecastsClient)  # type: ignore[return-value]

    @property
    def object_library(self) -> ObjectLibraryClient:
        return self._get("object_library", ObjectLibraryClient)  # type: ignore[return-value]

    @property
    def meetings_scheduler(self) -> MeetingsSchedulerClient:
        return self._get("meetings_scheduler", MeetingsSchedulerClient)  # type: ignore[return-value]

    # =========================================================================
    # Commerce
    # =========================================================================

    @property
    def products(self) -> ProductsClient:
        return self._get("products", ProductsClient)  # type: ignore[return-value]

    @property
    def line_items(self) -> LineItemsClient:
        return self._get("line_items", LineItemsClient)  # type: ignore[return-value]

    @property
    def quotes(self) -> QuotesClient:
        return self._get("quotes", QuotesClient)  # type: ignore[return-value]

    @property
    def invoices(self) -> InvoicesClient:
        return self._get("invoices", InvoicesClient)  # type: ignore[return-value]

    @property
    def orders(self) -> OrdersClient:
        return self._get("orders", OrdersClient)  # type: ignore[return-value]

    @property
    def carts(self) -> CartsClient:
        return self._get("carts", CartsClient)  # type: ignore[return-value]

    @property
    def payments(self) -> PaymentsClient:
        return self._get("payments", PaymentsClient)  # type: ignore[return-value]

    @property
    def commerce_subscriptions(self) -> CommerceSubscriptionsClient:
        return self._get("commerce_subscriptions", CommerceSubscriptionsClient)  # type: ignore[return-value]

    @property
    def discounts(self) -> DiscountsClient:
        return self._get("discounts", DiscountsClient)  # type: ignore[return-value]

    @property
    def fees(self) -> FeesClient:
        return self._get("fees", FeesClient)  # type: ignore[return-value]

    @property
    def taxes(self) -> TaxesClient:
        return self._get("taxes", TaxesClient)  # type: ignore[return-value]

    # =========================================================================
    # CMS
    # =========================================================================

    @property
    def pages(self) -> PagesClient:
        return self._get("pages", PagesClient)  # type: ignore[return-value]

    @property
    def blog_posts(self) -> BlogPostsClient:
        return self._get("blog_posts", BlogPostsClient)  # type: ignore[return-value]

    @property
    def blog_authors(self) -> BlogAuthorsClient:
        return self._get("blog_authors", BlogAuthorsClient)  # type: ignore[return-value]

    @property
    def blog_tags(self) -> BlogTagsClient:
        return self._get("blog_tags", BlogTagsClient)  # type: ignore[return-value]

    @property
    def blog_settings(self) -> BlogSettingsClient:
        return self._get("blog_settings", BlogSettingsClient)  # type: ignore[return-value]

    @property
    def hubdb(self) -> HubDbClient:
        return self._get("hubdb", HubDbClient)  # type: ignore[return-value]

    @property
    def domains(self) -> DomainsClient:
        return self._get("domains", DomainsClient)  # type: ignore[return-value]

    @property
    def source_code(self) -> SourceCodeClient:
        return self._get("source_code", SourceCodeClient)  # type: ignore[return-value]

    @property
    def url_redirects(self) -> UrlRedirectsClient:
        return self._get("url_redirects", UrlRedirectsClient)  # type: ignore[return-value]

    @property
    def site_search(self) -> SiteSearchClient:
        return self._get("site_search", SiteSearchClient)  # type: ignore[return-value]

    @property
    def cms_audit(self) -> CmsAuditClient:
        return self._get("cms_audit", CmsAuditClient)  # type: ignore[return-value]

    # =========================================================================
    # Marketing
    # =========================================================================

    @property
    def campaigns(self) -> CampaignsClient:
        return self._get("campaigns", CampaignsClient)  # type: ignore[return-value]

    @property
    def forms(self) -> FormsClient:
        return self._get("forms", FormsClient)  # type: ignore[return-value]

    @property
    def marketing_events(self) -> MarketingEventsClient:
        return self._get("marketing_events", MarketingEventsClient)  # type: ignore[return-value]

    @property
    def transactional_email(self) -> TransactionalEmailClient:
        return self._get("transactional_email", TransactionalEmailClient)  # type: ignore[return-value]

    @property
    def single_send(self) -> SingleSendClient:
        return self._get("single_send", SingleSendClient)  # type: ignore[return-value]

    # =========================================================================
    # Automation
    # =========================================================================

    @property
    def automation_actions(self) -> ActionsClient:
        return self._get("automation_actions", ActionsClient)  # type: ignore[return-value]

    @property
    def sequences(self) -> SequencesClient:
        return self._get("sequences", SequencesClient)  # type: ignore[return-value]

    # =========================================================================
    # Conversations
    # =========================================================================

    @property
    def threads(self) -> ThreadsClient:
        return self._get("threads", ThreadsClient)  # type: ignore[return-value]

    @property
    def messages(self) -> MessagesClient:
        return self._get("messages", MessagesClient)  # type: ignore[return-value]

    @property
    def custom_channels(self) -> CustomChannelsClient:
        return self._get("custom_channels", CustomChannelsClient)  # type: ignore[return-value]

    @property
    def visitor_identification(self) -> VisitorIdentificationClient:
        return self._get("visitor_identification", VisitorIdentificationClient)  # type: ignore[return-value]

    # =========================================================================
    # Events
    # =========================================================================

    @property
    def event_definitions(self) -> EventDefinitionsClient:
        return self._get("event_definitions", EventDefinitionsClient)  # type: ignore[return-value]

    @property
    def event_send(self) -> EventSendClient:
        return self._get("event_send", EventSendClient)  # type: ignore[return-value]

    @property
    def event_occurrences(self) -> EventOccurrencesClient:
        return self._get("event_occurrences", EventOccurrencesClient)  # type: ignore[return-value]

    # =========================================================================
    # Files
    # =========================================================================

    @property
    def files(self) -> FilesClient:
        return self._get("files", FilesClient)  # type: ignore[return-value]

    # =========================================================================
    # Settings
    # =========================================================================

    @property
    def currency(self) -> CurrencyClient:
        return self._get("currency", CurrencyClient)  # type: ignore[return-value]

    @property
    def user_provisioning(self) -> UserProvisioningClient:
        return self._get("user_provisioning", UserProvisioningClient)  # type: ignore[return-value]

    def feature_flags(self, app_id: str) -> FeatureFlagsClient:
        """Get a feature flags client for a specific app."""
        key = f"feature_flags_{app_id}"
        if key not in self._cache:
            self._cache[key] = FeatureFlagsClient(self._http, app_id)
        return self._cache[key]  # type: ignore[return-value]

    @property
    def data_sources(self) -> DataSourcesClient:
        return self._get("data_sources", DataSourcesClient)  # type: ignore[return-value]

    # =========================================================================
    # Webhooks
    # =========================================================================

    @property
    def webhooks(self) -> WebhooksClient:
        return self._get("webhooks", WebhooksClient)  # type: ignore[return-value]

    # =========================================================================
    # Account
    # =========================================================================

    @property
    def account_info(self) -> AccountInfoClient:
        return self._get("account_info", AccountInfoClient)  # type: ignore[return-value]

    @property
    def audit_logs(self) -> AuditLogsClient:
        return self._get("audit_logs", AuditLogsClient)  # type: ignore[return-value]

    @property
    def business_units(self) -> BusinessUnitsClient:
        return self._get("business_units", BusinessUnitsClient)  # type: ignore[return-value]

    @property
    def subscriptions(self) -> SubscriptionsClient:
        return self._get("subscriptions", SubscriptionsClient)  # type: ignore[return-value]

    # =========================================================================
    # Auth (static – no token needed)
    # =========================================================================

    @staticmethod
    def oauth(
        client_id: str,
        client_secret: str,
        redirect_uri: str,
    ) -> OAuthClient:
        """Get an OAuth client for authorization flows."""
        return OAuthClient(client_id, client_secret, redirect_uri)
