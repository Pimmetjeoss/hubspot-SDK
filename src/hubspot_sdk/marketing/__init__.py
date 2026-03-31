"""Marketing domain module."""

from hubspot_sdk.marketing.campaigns import CampaignsClient
from hubspot_sdk.marketing.forms import FormsClient
from hubspot_sdk.marketing.events import MarketingEventsClient
from hubspot_sdk.marketing.transactional import TransactionalEmailClient
from hubspot_sdk.marketing.emails import SingleSendClient

__all__ = [
    "CampaignsClient",
    "FormsClient",
    "MarketingEventsClient",
    "TransactionalEmailClient",
    "SingleSendClient",
]
