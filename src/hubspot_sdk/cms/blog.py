"""CMS Blog clients – posts, authors, tags, settings."""

from __future__ import annotations

from typing import Any

from hubspot_sdk.core.http import HttpClient


class _BlogCrudBase:
    """Shared CRUD + batch + multi-language for blog resources."""

    def __init__(self, http: HttpClient, base_path: str) -> None:
        self._http = http
        self._base = base_path

    async def list(self, **params: Any) -> dict[str, Any]:
        return await self._http.get(self._base, params=params or None)

    async def create(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(self._base, json=data)

    async def get(self, resource_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{resource_id}")

    async def update(self, resource_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.patch(f"{self._base}/{resource_id}", json=data)

    async def delete(self, resource_id: str) -> None:
        await self._http.delete(f"{self._base}/{resource_id}")

    async def batch_create(self, inputs: list[dict[str, Any]]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/batch/create", json={"inputs": inputs})

    async def batch_read(self, inputs: list[dict[str, Any]]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/batch/read", json={"inputs": inputs})

    async def batch_update(self, inputs: list[dict[str, Any]]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/batch/update", json={"inputs": inputs})

    async def batch_archive(self, inputs: list[dict[str, Any]]) -> None:
        await self._http.post(f"{self._base}/batch/archive", json={"inputs": inputs})

    async def attach_to_lang_group(self, data: dict[str, Any]) -> None:
        await self._http.post(f"{self._base}/multi-language/attach-to-lang-group", json=data)

    async def create_lang_variation(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/multi-language/create-language-variation", json=data)

    async def detach_from_lang_group(self, data: dict[str, Any]) -> None:
        await self._http.post(f"{self._base}/multi-language/detach-from-lang-group", json=data)

    async def set_new_lang_primary(self, data: dict[str, Any]) -> None:
        await self._http.put(f"{self._base}/multi-language/set-new-lang-primary", json=data)

    async def update_languages(self, inputs: list[dict[str, Any]]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/multi-language/update-languages", json={"inputs": inputs})


class BlogPostsClient(_BlogCrudBase):
    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, f"/cms/blogs/{http.api_version}/posts")

    async def get_draft(self, post_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{post_id}/draft")

    async def update_draft(self, post_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.patch(f"{self._base}/{post_id}/draft", json=data)

    async def push_live(self, post_id: str) -> None:
        await self._http.post(f"{self._base}/{post_id}/draft/push-live")

    async def reset_draft(self, post_id: str) -> None:
        await self._http.post(f"{self._base}/{post_id}/draft/reset")

    async def clone(self, post_id: str) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/{post_id}/clone")

    async def get_revisions(self, post_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{post_id}/revisions")

    async def get_revision(self, post_id: str, revision_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{post_id}/revisions/{revision_id}")

    async def restore_revision(self, revision_id: str) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/revisions/{revision_id}/restore")

    async def schedule(self, data: dict[str, Any]) -> None:
        await self._http.post(f"{self._base}/schedule", json=data)


class BlogAuthorsClient(_BlogCrudBase):
    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, f"/cms/blogs/{http.api_version}/authors")


class BlogTagsClient(_BlogCrudBase):
    def __init__(self, http: HttpClient) -> None:
        super().__init__(http, f"/cms/blogs/{http.api_version}/tags")


class BlogSettingsClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self._base = f"/cms/blog-settings/{http.api_version}/settings"

    async def list(self, **params: Any) -> dict[str, Any]:
        return await self._http.get(self._base, params=params or None)

    async def get(self, setting_id: str) -> dict[str, Any]:
        return await self._http.get(f"{self._base}/{setting_id}")

    async def update(self, setting_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.put(f"{self._base}/{setting_id}", json=data)

    async def attach_to_lang_group(self, data: dict[str, Any]) -> None:
        await self._http.post(f"{self._base}/multi-language/attach-to-lang-group", json=data)

    async def create_lang_variation(self, data: dict[str, Any]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/multi-language/create-language-variation", json=data)

    async def detach_from_lang_group(self, data: dict[str, Any]) -> None:
        await self._http.post(f"{self._base}/multi-language/detach-from-lang-group", json=data)

    async def set_new_lang_primary(self, data: dict[str, Any]) -> None:
        await self._http.put(f"{self._base}/multi-language/set-new-lang-primary", json=data)

    async def update_languages(self, inputs: list[dict[str, Any]]) -> dict[str, Any]:
        return await self._http.post(f"{self._base}/multi-language/update-languages", json={"inputs": inputs})
