"""CMS Pages client – landing pages and site pages (72 endpoints)."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class PagesClient:
    """Manage landing pages and site pages."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._v = http.api_version
        self._landing = f"/cms/pages/{self._v}/landing-pages"
        self._site = f"/cms/pages/{self._v}/site-pages"

    # -- Generic helper for both page types -----------------------------------

    async def _list(self, base: str, **params: Any) -> dict[str, Any]:
        return await self._http.get(base, params=params or None)

    async def _create(self, base: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(base, json=data)

    async def _get(self, base: str, page_id: str) -> dict[str, Any]:
        return await self._http.get(f"{base}/{page_id}")

    async def _update(self, base: str, page_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.patch(f"{base}/{page_id}", json=data)

    async def _delete(self, base: str, page_id: str) -> None:
        await self._http.delete(f"{base}/{page_id}")

    async def _draft(self, base: str, page_id: str) -> dict[str, Any]:
        return await self._http.get(f"{base}/{page_id}/draft")

    async def _update_draft(self, base: str, page_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.patch(f"{base}/{page_id}/draft", json=data)

    async def _push_live(self, base: str, page_id: str) -> None:
        await self._http.post(f"{base}/{page_id}/draft/push-live")

    async def _reset_draft(self, base: str, page_id: str) -> None:
        await self._http.post(f"{base}/{page_id}/draft/reset")

    async def _clone(self, base: str, page_id: str) -> dict[str, Any]:
        return await self._http.post(f"{base}/{page_id}/clone")

    async def _revisions(self, base: str, page_id: str, **params: Any) -> dict[str, Any]:
        return await self._http.get(f"{base}/{page_id}/revisions", params=params or None)

    async def _get_revision(self, base: str, page_id: str, revision_id: str) -> dict[str, Any]:
        return await self._http.get(f"{base}/{page_id}/revisions/{revision_id}")

    async def _restore_revision(self, base: str, revision_id: str) -> dict[str, Any]:
        return await self._http.post(f"{base}/revisions/{revision_id}/restore")

    # -- Batch operations -----------------------------------------------------

    async def _batch_create(self, base: str, inputs: list[dict[str, Any]]) -> dict[str, Any]:
        return await self._http.post(f"{base}/batch/create", json={"inputs": inputs})

    async def _batch_read(self, base: str, inputs: list[dict[str, Any]]) -> dict[str, Any]:
        return await self._http.post(f"{base}/batch/read", json={"inputs": inputs})

    async def _batch_update(self, base: str, inputs: list[dict[str, Any]]) -> dict[str, Any]:
        return await self._http.post(f"{base}/batch/update", json={"inputs": inputs})

    async def _batch_archive(self, base: str, inputs: list[dict[str, Any]]) -> None:
        await self._http.post(f"{base}/batch/archive", json={"inputs": inputs})

    # -- A/B testing ----------------------------------------------------------

    async def _create_ab_variation(self, base: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{base}/ab-test/create-variation", json=data)

    async def _end_ab_test(self, base: str, data: dict[str, Any]) -> None:
        await self._http.post(f"{base}/ab-test/end", json=data)

    # -- Multi-language -------------------------------------------------------

    async def _attach_to_lang_group(self, base: str, data: dict[str, Any]) -> None:
        await self._http.post(f"{base}/multi-language/attach-to-lang-group", json=data)

    async def _create_lang_variation(self, base: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{base}/multi-language/create-language-variation", json=data)

    async def _detach_from_lang_group(self, base: str, data: dict[str, Any]) -> None:
        await self._http.post(f"{base}/multi-language/detach-from-lang-group", json=data)

    async def _set_new_lang_primary(self, base: str, data: dict[str, Any]) -> None:
        await self._http.put(f"{base}/multi-language/set-new-lang-primary", json=data)

    async def _update_langs(self, base: str, inputs: list[dict[str, Any]]) -> dict[str, Any]:
        return await self._http.post(f"{base}/multi-language/update-languages", json={"inputs": inputs})

    # -- Schedule -------------------------------------------------------------

    async def _schedule(self, base: str, data: dict[str, Any]) -> None:
        await self._http.post(f"{base}/schedule", json=data)

    # =========================================================================
    # Landing Pages
    # =========================================================================

    async def list_landing(self, **params: Any) -> dict[str, Any]:
        return await self._list(self._landing, **params)

    async def create_landing(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._create(self._landing, data)

    async def get_landing(self, page_id: str) -> dict[str, Any]:
        return await self._get(self._landing, page_id)

    async def update_landing(self, page_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._update(self._landing, page_id, data)

    async def delete_landing(self, page_id: str) -> None:
        await self._delete(self._landing, page_id)

    async def get_landing_draft(self, page_id: str) -> dict[str, Any]:
        return await self._draft(self._landing, page_id)

    async def update_landing_draft(self, page_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._update_draft(self._landing, page_id, data)

    async def push_landing_live(self, page_id: str) -> None:
        await self._push_live(self._landing, page_id)

    async def clone_landing(self, page_id: str) -> dict[str, Any]:
        return await self._clone(self._landing, page_id)

    async def batch_create_landing(self, inputs: list[dict[str, Any]]) -> dict[str, Any]:
        return await self._batch_create(self._landing, inputs)

    async def batch_read_landing(self, inputs: list[dict[str, Any]]) -> dict[str, Any]:
        return await self._batch_read(self._landing, inputs)

    async def batch_update_landing(self, inputs: list[dict[str, Any]]) -> dict[str, Any]:
        return await self._batch_update(self._landing, inputs)

    async def batch_archive_landing(self, inputs: list[dict[str, Any]]) -> None:
        await self._batch_archive(self._landing, inputs)

    async def create_landing_ab_variation(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._create_ab_variation(self._landing, data)

    async def end_landing_ab_test(self, data: dict[str, Any]) -> None:
        await self._end_ab_test(self._landing, data)

    # =========================================================================
    # Site Pages
    # =========================================================================

    async def list_site(self, **params: Any) -> dict[str, Any]:
        return await self._list(self._site, **params)

    async def create_site(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._create(self._site, data)

    async def get_site(self, page_id: str) -> dict[str, Any]:
        return await self._get(self._site, page_id)

    async def update_site(self, page_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._update(self._site, page_id, data)

    async def delete_site(self, page_id: str) -> None:
        await self._delete(self._site, page_id)

    async def get_site_draft(self, page_id: str) -> dict[str, Any]:
        return await self._draft(self._site, page_id)

    async def update_site_draft(self, page_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._update_draft(self._site, page_id, data)

    async def push_site_live(self, page_id: str) -> None:
        await self._push_live(self._site, page_id)

    async def clone_site(self, page_id: str) -> dict[str, Any]:
        return await self._clone(self._site, page_id)

    async def batch_create_site(self, inputs: list[dict[str, Any]]) -> dict[str, Any]:
        return await self._batch_create(self._site, inputs)

    async def batch_read_site(self, inputs: list[dict[str, Any]]) -> dict[str, Any]:
        return await self._batch_read(self._site, inputs)

    async def batch_update_site(self, inputs: list[dict[str, Any]]) -> dict[str, Any]:
        return await self._batch_update(self._site, inputs)

    async def batch_archive_site(self, inputs: list[dict[str, Any]]) -> None:
        await self._batch_archive(self._site, inputs)
