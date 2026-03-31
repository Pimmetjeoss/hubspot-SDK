"""OAuth2 client for HubSpot app authentication."""

from __future__ import annotations

from typing import Any

import httpx

from hubspot_sdk.auth.token import TokenInfo
from hubspot_sdk.core.http import BASE_URL

AUTHORIZE_URL = "https://app.hubspot.com/oauth/authorize"
TOKEN_URL = f"{BASE_URL}/oauth/v1/token"


class OAuthClient:
    """Handles the HubSpot OAuth2 flow.

    Usage:
        oauth = OAuthClient(client_id="...", client_secret="...", redirect_uri="...")

        # Step 1: Get the authorization URL
        url = oauth.get_authorize_url(scopes=["crm.objects.contacts.read"])

        # Step 2: Exchange the code for tokens
        tokens = await oauth.exchange_code(code="...")

        # Step 3: Refresh when expired
        tokens = await oauth.refresh_token(refresh_token="...")
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
    ) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def get_authorize_url(
        self,
        scopes: list[str],
        state: str | None = None,
        optional_scopes: list[str] | None = None,
    ) -> str:
        """Build the OAuth authorization URL."""
        params: dict[str, str] = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": " ".join(scopes),
        }
        if state:
            params["state"] = state
        if optional_scopes:
            params["optional_scope"] = " ".join(optional_scopes)

        qs = "&".join(f"{k}={v}" for k, v in params.items())
        return f"{AUTHORIZE_URL}?{qs}"

    async def exchange_code(self, code: str) -> TokenInfo:
        """Exchange an authorization code for access + refresh tokens."""
        data = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "code": code,
        }
        return await self._token_request(data)

    async def refresh_token(self, refresh_token: str) -> TokenInfo:
        """Refresh an expired access token."""
        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token,
        }
        return await self._token_request(data)

    async def get_token_info(self, token: str) -> dict[str, Any]:
        """Introspect a token to get its metadata."""
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{BASE_URL}/oauth/v1/access-tokens/{token}",
            )
            resp.raise_for_status()
            return resp.json()

    async def revoke_token(self, token: str) -> None:
        """Revoke a refresh token."""
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{BASE_URL}/oauth/v1/refresh-tokens/{token}",
                headers={"Content-Type": "application/json"},
                json={"token": token},
            )
            resp.raise_for_status()

    async def _token_request(self, data: dict[str, str]) -> TokenInfo:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                TOKEN_URL,
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            resp.raise_for_status()
            body = resp.json()

        return TokenInfo(
            access_token=body["access_token"],
            token_type=body.get("token_type", "bearer"),
            expires_in=body.get("expires_in"),
            refresh_token=body.get("refresh_token"),
        )
