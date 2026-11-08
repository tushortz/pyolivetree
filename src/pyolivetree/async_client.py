"""Asynchronous Olive Tree API client."""

from __future__ import annotations

from typing import Any

from pyolivetree._transport.async_ import AsyncTransport
from pyolivetree.auth import AuthManager
from pyolivetree.config import ClientConfig
from pyolivetree.resources import (
    AccountResource,
    AdminResource,
    AnalyticsResource,
    BrowserResource,
    CdnResource,
    FirebaseResource,
    LegacyResource,
    MediaResource,
    MessagesResource,
    PrivacyResource,
    SmartSearchResource,
    SpeechResource,
    StaticResource,
    StoreResource,
    StoreXmlResource,
    SyncResource,
    VotdResource,
)


class AsyncOliveTreeClient:
    """Asynchronous client for the Olive Tree Bible Reader API."""

    def __init__(
        self,
        *,
        username: str | None = None,
        password: str | None = None,
        install_id: str | None = None,
        access_token: str | None = None,
        refresh_token: str | None = None,
        hmac_key: str | bytes | None = None,
        timeout: float = 30.0,
        base_url: str = "https://www.olivetree.com",
        config: ClientConfig | None = None,
    ) -> None:
        """Initialize the asynchronous client.

        Args:
            username: Olive Tree account email.
            password: Olive Tree account password.
            install_id: Device install identifier.
            access_token: Optional bearer token to restore an in-memory session.
            refresh_token: Optional refresh token to restore an in-memory session.
            hmac_key: HMAC signing key for signed endpoints.
            timeout: Request timeout in seconds.
            base_url: Default API base URL.
            config: Pre-built configuration object. Overrides other args if set.

        Returns:
            None.

        Raises:
            ValueError: If hmac_key encoding is invalid.
        """
        self._config = config or ClientConfig.from_env(
            username=username,
            password=password,
            install_id=install_id,
            hmac_key=hmac_key,
            timeout=timeout,
            base_url=base_url,
        )
        self._auth = AuthManager(
            self._config,
            access_token=access_token,
            refresh_token=refresh_token,
        )
        self._transport = AsyncTransport(self._auth, timeout=self._config.timeout)
        self.store = StoreResource(self)
        self.account = AccountResource(self)
        self.store_xml = StoreXmlResource(self)
        self.legacy = LegacyResource(self)
        self.messages = MessagesResource(self)
        self.smart_search = SmartSearchResource(self)
        self.sync = SyncResource(self)
        self.analytics = AnalyticsResource(self)
        self.privacy = PrivacyResource(self)
        self.speech = SpeechResource(self)
        self.votd = VotdResource(self)
        self.cdn = CdnResource(self)
        self.media = MediaResource(self)
        self.static = StaticResource(self)
        self.admin = AdminResource(self)
        self.browser = BrowserResource(self)
        self.firebase = FirebaseResource(self)

    async def login(self, **kwargs: Any) -> dict[str, Any]:
        """Authenticate and cache bearer tokens.

        Args:
            **kwargs: Optional overrides for user, pass, install_id, and other login fields.

        Returns:
            Parsed account authentication response.

        Raises:
            OliveTreeAuthError: If login fails.
            OliveTreeAPIError: If the API returns an error status.
        """
        payload = {
            "user": kwargs.get("user", self._config.username),
            "pass": kwargs.get("pass", kwargs.get("password", self._config.password)),
            "install_id": kwargs.get("install_id", self._config.install_id),
            "supportsAccessToken": kwargs.get("supportsAccessToken", 1),
        }
        payload.update({k: v for k, v in kwargs.items() if k not in payload and v is not None})
        result = await self.account.alogin(
            user=payload.get("user"),
            password=payload.get("pass"),
            install_id=payload.get("install_id"),
            supportsAccessToken=payload.get("supportsAccessToken"),
            subscribe_to_newsletter=payload.get("subscribe_to_newsletter"),
            implicit_newsletter_consent=payload.get("implicit_newsletter_consent"),
            first_name=payload.get("first_name"),
        )
        if isinstance(result, dict):
            self._auth.update_from_response(result)
        return result

    async def refresh(self) -> dict[str, Any]:
        """Refresh bearer tokens via ``account_refresh_token``.

        Requires a current access token from :py:meth:`login`.

        Returns:
            Parsed account authentication response.

        Raises:
            OliveTreeAuthError: If refresh fails.
            OliveTreeAPIError: If the API returns an error status.
        """
        result = await self.account.arefresh_token()
        if isinstance(result, dict):
            self._auth.update_from_response(result)
        return result

    async def ensure_auth(self) -> None:
        """Login automatically when credentials are configured but no token is set.

        Returns:
            None.

        Raises:
            OliveTreeAuthError: If login fails.
        """
        if not self._auth.access_token and self._config.username and self._config.password:
            await self.login()

    async def _aapi_request(self, spec: Any, **kwargs: Any) -> Any:
        """Execute an async request with automatic authentication when required.

        Args:
            spec: Operation specification.
            **kwargs: Arguments forwarded to the transport layer.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAuthError: If automatic login fails.
            OliveTreeAPIError: If the API returns an error status.
        """
        if spec.security and self._auth.needs_bearer(spec.security):
            await self.ensure_auth()
        return await self._transport.request(spec, **kwargs)

    async def aclose(self) -> None:
        """Close the underlying HTTP client.

        Returns:
            None.
        """
        await self._transport.aclose()

    async def __aenter__(self) -> AsyncOliveTreeClient:
        """Enter async context manager.

        Returns:
            This client instance.
        """
        return self

    async def __aexit__(self, *args: object) -> None:
        """Exit async context manager and close connections.

        Returns:
            None.
        """
        await self.aclose()
