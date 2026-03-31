"""Events domain module."""

from hubspot_sdk.events.definitions import EventDefinitionsClient
from hubspot_sdk.events.send import EventSendClient
from hubspot_sdk.events.occurrences import EventOccurrencesClient

__all__ = ["EventDefinitionsClient", "EventSendClient", "EventOccurrencesClient"]
