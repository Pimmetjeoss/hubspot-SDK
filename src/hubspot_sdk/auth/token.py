"""Token management for HubSpot private app and OAuth tokens."""

from __future__ import annotations

import time
from dataclasses import dataclass, field


@dataclass
class TokenInfo:
    """Holds token metadata."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int | None = None
    refresh_token: str | None = None
    _created_at: float = field(default_factory=time.time)

    @property
    def is_expired(self) -> bool:
        if self.expires_in is None:
            return False  # Private app tokens don't expire
        return time.time() > (self._created_at + self.expires_in - 60)


class TokenManager:
    """Manages access tokens with optional refresh support.

    For private app tokens, the token never expires.
    For OAuth tokens, auto-refresh is supported via OAuthClient.
    """

    def __init__(self, access_token: str) -> None:
        self._token = TokenInfo(access_token=access_token)
        self._refresh_callback: object | None = None

    @property
    def access_token(self) -> str:
        return self._token.access_token

    @property
    def is_expired(self) -> bool:
        return self._token.is_expired

    def update_token(self, token_info: TokenInfo) -> None:
        self._token = token_info
