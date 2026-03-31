"""Shared Pydantic models used across the SDK."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


# ---------------------------------------------------------------------------
# Common HubSpot response structures
# ---------------------------------------------------------------------------


class Paging(BaseModel):
    """Cursor-based paging info returned by HubSpot."""

    model_config = ConfigDict(extra="allow")

    class Next(BaseModel):
        after: str
        link: str | None = None

    next: Next | None = None


class HubSpotObject(BaseModel):
    """A single CRM / API object returned by HubSpot."""

    model_config = ConfigDict(extra="allow")

    id: str
    properties: dict[str, Any] = Field(default_factory=dict)
    properties_with_history: dict[str, list[dict[str, Any]]] | None = Field(
        default=None, alias="propertiesWithHistory"
    )
    associations: dict[str, Any] | None = None
    created_at: datetime | None = Field(default=None, alias="createdAt")
    updated_at: datetime | None = Field(default=None, alias="updatedAt")
    archived: bool = False
    archived_at: datetime | None = Field(default=None, alias="archivedAt")


class PaginatedResult(BaseModel, Generic[T]):
    """Paginated list response from HubSpot."""

    model_config = ConfigDict(extra="allow")

    results: list[T] = Field(default_factory=list)
    paging: Paging | None = None

    @property
    def has_next(self) -> bool:
        return self.paging is not None and self.paging.next is not None

    @property
    def next_after(self) -> str | None:
        if self.paging and self.paging.next:
            return self.paging.next.after
        return None


class SearchResult(BaseModel, Generic[T]):
    """Search response from HubSpot."""

    model_config = ConfigDict(extra="allow")

    total: int = 0
    results: list[T] = Field(default_factory=list)
    paging: Paging | None = None

    @property
    def has_next(self) -> bool:
        return self.paging is not None and self.paging.next is not None

    @property
    def next_after(self) -> str | None:
        if self.paging and self.paging.next:
            return self.paging.next.after
        return None


class BatchResult(BaseModel, Generic[T]):
    """Batch operation response from HubSpot."""

    model_config = ConfigDict(extra="allow")

    status: str = ""
    results: list[T] = Field(default_factory=list)
    errors: list[dict[str, Any]] = Field(default_factory=list)
    num_errors: int = Field(default=0, alias="numErrors")
    started_at: datetime | None = Field(default=None, alias="startedAt")
    completed_at: datetime | None = Field(default=None, alias="completedAt")


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------


class PropertyValue(BaseModel):
    """A single property name-value pair."""

    property: str  # noqa: A003
    value: str


class FilterGroup(BaseModel):
    """A group of filters for search requests."""

    filters: list[Filter]


class Filter(BaseModel):
    """A single filter in a search request."""

    property_name: str = Field(alias="propertyName")
    operator: str
    value: str | None = None
    values: list[str] | None = None
    high_value: str | None = Field(default=None, alias="highValue")


class SearchRequest(BaseModel):
    """Search request body sent to HubSpot."""

    model_config = ConfigDict(populate_by_name=True)

    filter_groups: list[FilterGroup] = Field(default_factory=list, alias="filterGroups")
    sorts: list[dict[str, str]] = Field(default_factory=list)
    query: str | None = None
    properties: list[str] = Field(default_factory=list)
    limit: int = 10
    after: str | None = None


class BatchInput(BaseModel):
    """Generic batch input."""

    inputs: list[dict[str, Any]]


# ---------------------------------------------------------------------------
# Association models
# ---------------------------------------------------------------------------


class AssociationSpec(BaseModel):
    """Specifies an association type."""

    association_category: str = Field(alias="associationCategory")
    association_type_id: int = Field(alias="associationTypeId")


class AssociationResult(BaseModel):
    """A single association between two objects."""

    model_config = ConfigDict(extra="allow")

    from_object_id: str = Field(alias="from")  # actually nested but simplified
    to_object_id: str = Field(alias="to")
    association_types: list[dict[str, Any]] = Field(default_factory=list, alias="associationTypes")


# ---------------------------------------------------------------------------
# Pipeline models
# ---------------------------------------------------------------------------


class Pipeline(BaseModel):
    """A CRM pipeline."""

    model_config = ConfigDict(extra="allow")

    id: str
    label: str
    display_order: int = Field(alias="displayOrder")
    stages: list[PipelineStage] = Field(default_factory=list)
    created_at: datetime | None = Field(default=None, alias="createdAt")
    updated_at: datetime | None = Field(default=None, alias="updatedAt")
    archived: bool = False


class PipelineStage(BaseModel):
    """A stage within a pipeline."""

    model_config = ConfigDict(extra="allow")

    id: str
    label: str
    display_order: int = Field(alias="displayOrder")
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime | None = Field(default=None, alias="createdAt")
    updated_at: datetime | None = Field(default=None, alias="updatedAt")
    archived: bool = False


# ---------------------------------------------------------------------------
# Property models
# ---------------------------------------------------------------------------


class Property(BaseModel):
    """A CRM object property definition."""

    model_config = ConfigDict(extra="allow")

    name: str
    label: str
    type: str  # noqa: A003
    field_type: str = Field(alias="fieldType")
    description: str = ""
    group_name: str = Field(default="", alias="groupName")
    options: list[PropertyOption] = Field(default_factory=list)
    display_order: int = Field(default=0, alias="displayOrder")
    has_unique_value: bool = Field(default=False, alias="hasUniqueValue")
    hidden: bool = False
    form_field: bool = Field(default=False, alias="formField")
    calculated: bool = False
    external_options: bool = Field(default=False, alias="externalOptions")
    archived: bool = False
    created_at: datetime | None = Field(default=None, alias="createdAt")
    updated_at: datetime | None = Field(default=None, alias="updatedAt")


class PropertyOption(BaseModel):
    """An option for an enumeration property."""

    label: str
    value: str
    display_order: int = Field(default=0, alias="displayOrder")
    hidden: bool = False


class PropertyGroup(BaseModel):
    """A group of properties."""

    model_config = ConfigDict(extra="allow")

    name: str
    label: str
    display_order: int = Field(default=0, alias="displayOrder")
    archived: bool = False


# ---------------------------------------------------------------------------
# Owner model
# ---------------------------------------------------------------------------


class Owner(BaseModel):
    """A CRM owner."""

    model_config = ConfigDict(extra="allow")

    id: str
    email: str = ""
    first_name: str = Field(default="", alias="firstName")
    last_name: str = Field(default="", alias="lastName")
    user_id: int | None = Field(default=None, alias="userId")
    teams: list[dict[str, Any]] = Field(default_factory=list)
    created_at: datetime | None = Field(default=None, alias="createdAt")
    updated_at: datetime | None = Field(default=None, alias="updatedAt")
    archived: bool = False


# ---------------------------------------------------------------------------
# File models
# ---------------------------------------------------------------------------


class FileObject(BaseModel):
    """A file in the HubSpot file manager."""

    model_config = ConfigDict(extra="allow")

    id: str
    name: str = ""
    path: str = ""
    size: int = 0
    type: str = ""  # noqa: A003
    url: str = ""
    created_at: datetime | None = Field(default=None, alias="createdAt")
    updated_at: datetime | None = Field(default=None, alias="updatedAt")
    archived: bool = False


class Folder(BaseModel):
    """A folder in the HubSpot file manager."""

    model_config = ConfigDict(extra="allow")

    id: str
    name: str = ""
    path: str = ""
    parent_folder_id: str | None = Field(default=None, alias="parentFolderId")
    created_at: datetime | None = Field(default=None, alias="createdAt")
    updated_at: datetime | None = Field(default=None, alias="updatedAt")
    archived: bool = False


# ---------------------------------------------------------------------------
# Import/Export models
# ---------------------------------------------------------------------------


class ImportResult(BaseModel):
    """Result of a CRM import operation."""

    model_config = ConfigDict(extra="allow")

    id: str
    state: str = ""
    opt_out_import: bool = Field(default=False, alias="optOutImport")
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime | None = Field(default=None, alias="createdAt")
    updated_at: datetime | None = Field(default=None, alias="updatedAt")


# ---------------------------------------------------------------------------
# Webhook models
# ---------------------------------------------------------------------------


class WebhookSubscription(BaseModel):
    """A webhook subscription."""

    model_config = ConfigDict(extra="allow")

    id: int | None = None
    event_type: str = Field(default="", alias="eventType")
    property_name: str | None = Field(default=None, alias="propertyName")
    active: bool = True
    created_at: datetime | None = Field(default=None, alias="createdAt")
    updated_at: datetime | None = Field(default=None, alias="updatedAt")


# Fix forward references
Pipeline.model_rebuild()
Property.model_rebuild()
