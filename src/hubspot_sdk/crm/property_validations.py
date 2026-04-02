"""CRM property validation rules client."""
from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class PropertyValidationsClient:
    """Read and update property validation rules.

    Endpoints:
        GET /crm/property-validations/{version}/{objectTypeId}
        GET /crm/property-validations/{version}/{objectTypeId}/{propertyName}
        GET /crm/property-validations/{version}/{objectTypeId}/{propertyName}/rule-type/{ruleType}
        PUT /crm/property-validations/{version}/{objectTypeId}/{propertyName}/rule-type/{ruleType}
    """
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/crm/property-validations/{http.api_version}"

    async def list_rules(self, object_type_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{object_type_id}")

    async def get_property_rules(self, object_type_id: str, property_name: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{object_type_id}/{property_name}")

    async def get_rule(self, object_type_id: str, property_name: str, rule_type: str) -> dict[str, Any]:
        return await self._http.get(
            f"{self._base}/{object_type_id}/{property_name}/rule-type/{rule_type}"
        )

    async def update_rule(
        self,
        object_type_id: str,
        property_name: str,
        rule_type: str,
        *,
        rule_arguments: list[dict[str, Any]],
        should_apply_normalization: bool = False,
    ) -> None:
        await self._http.put(
            f"{self._base}/{object_type_id}/{property_name}/rule-type/{rule_type}",
            json={
                "ruleArguments": rule_arguments,
                "shouldApplyNormalization": should_apply_normalization,
            },
        )
