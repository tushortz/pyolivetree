"""Authentication helpers."""

from __future__ import annotations

import base64
import hashlib
import hmac
from typing import TYPE_CHECKING, Any

from pyolivetree.exceptions import OliveTreeAuthError

if TYPE_CHECKING:
    from pyolivetree.config import ClientConfig


class AuthManager:
    """Manage bearer tokens, basic auth, and HMAC request signing."""

    def __init__(
        self,
        config: ClientConfig,
        *,
        access_token: str | None = None,
        refresh_token: str | None = None,
    ) -> None:
        """Initialize the auth manager.

        Args:
            config: Client configuration with credentials.
            access_token: Optional in-memory bearer token (e.g. after login).
            refresh_token: Optional in-memory refresh token (e.g. after login).

        Raises:
            None.
        """
        self._config = config
        self._access_token = access_token
        self._refresh_token = refresh_token

    @property
    def access_token(self) -> str | None:
        """Return the current bearer access token.

        Returns:
            Access token string, or None if not authenticated.
        """
        return self._access_token

    @property
    def refresh_token(self) -> str | None:
        """Return the current refresh token.

        Returns:
            Refresh token string, or None if unavailable.
        """
        return self._refresh_token

    @property
    def install_id(self) -> str:
        """Return the device install identifier.

        Returns:
            Install ID string.
        """
        return self._config.install_id or ""

    def set_tokens(self, access_token: str | None, refresh_token: str | None = None) -> None:
        """Store authentication tokens after login or refresh.

        Args:
            access_token: Bearer access token.
            refresh_token: Optional refresh token.

        Returns:
            None.

        Raises:
            None.
        """
        self._access_token = access_token
        if refresh_token is not None:
            self._refresh_token = refresh_token

    def update_from_response(self, data: dict[str, Any]) -> None:
        """Update tokens from an account auth response payload.

        Args:
            data: Parsed JSON auth response.

        Returns:
            None.

        Raises:
            OliveTreeAuthError: If authentication failed according to the response.
        """
        if data.get("authenticated") is False:
            raise OliveTreeAuthError("Authentication failed")
        token = data.get("authentication_token")
        if token:
            self._access_token = str(token)
        refresh = data.get("refresh_token")
        if refresh:
            self._refresh_token = str(refresh)

    def auth_headers(
        self, security: list[dict[str, list[str]]], *, server_url: str = ""
    ) -> dict[str, str]:
        """Build authentication headers for a request security requirement.

        Args:
            security: OpenAPI security list for the operation.
            server_url: Request server URL for auth scheme selection.

        Returns:
            Header mapping for the request.

        Raises:
            None.
        """
        if not security:
            return {}
        headers: dict[str, str] = {}
        schemes = {name for item in security for name in item}
        if (
            "OTBearerAuth" in schemes
            and self._access_token
            and not self._prefers_basic_auth(security, server_url)
        ):
            headers["OTAuthorization"] = f"Bearer {self._access_token}"
        return headers

    def basic_auth(
        self, security: list[dict[str, list[str]]], *, server_url: str = ""
    ) -> tuple[str, str] | None:
        """Return basic auth credentials when required and bearer is unavailable.

        Args:
            security: OpenAPI security list for the operation.
            server_url: Request server URL for auth scheme selection.

        Returns:
            Username/password tuple, or None if basic auth is not applicable.

        Raises:
            None.
        """
        if not security:
            return None
        schemes = {name for item in security for name in item}
        creds = self._config.username, self._config.password
        if "BasicAuth" in schemes and all(creds):
            if not self._access_token or self._prefers_basic_auth(security, server_url):
                return creds
        if "JenkinsBasicAuth" in schemes and all(creds):
            return creds
        return None

    @staticmethod
    def _prefers_basic_auth(security: list[dict[str, list[str]]], server_url: str) -> bool:
        """Return True when the Android app uses basic auth for this host.

        Sync endpoints accept bearer or basic in the spec, but the app sends
        olivetree.com credentials via HTTP basic auth.
        """
        if "sync.olivetree.com" not in server_url:
            return False
        schemes = {name for item in security for name in item}
        return "BasicAuth" in schemes

    def needs_bearer(self, security: list[dict[str, list[str]]]) -> bool:
        """Check whether an operation expects bearer authentication.

        Args:
            security: OpenAPI security list for the operation.

        Returns:
            True if OTBearerAuth is listed and no token is set yet.
        """
        if not security:
            return False
        schemes = {name for item in security for name in item}
        return "OTBearerAuth" in schemes and not self._access_token

    def needs_hmac(self, security: list[dict[str, list[str]]]) -> bool:
        """Check whether an operation requires HMAC signing.

        Args:
            security: OpenAPI security list for the operation.

        Returns:
            True if HMACSignature is required.
        """
        if not security:
            return False
        schemes = {name for item in security for name in item}
        return "HMACSignature" in schemes

    def sign_body(self, body: bytes, *, profile: str = "telemetry") -> str:
        """Compute the HMAC-SHA512 signature for a request body.

        Matches ``HMACVerification`` in the Olive Tree Android app: HmacSHA512
        with an uppercase hex digest in the ``signature`` header.

        Args:
            body: Raw request body bytes.
            profile: HMAC key profile for the endpoint.

        Returns:
            Uppercase hex digest for the signature header.

        Raises:
            OliveTreeAuthError: If the HMAC profile is unknown.
        """
        try:
            key = self._config.get_hmac_key(profile)
        except ValueError as exc:
            raise OliveTreeAuthError(str(exc)) from exc
        digest = hmac.new(key, body, hashlib.sha512).digest()
        return digest.hex().upper()

    @staticmethod
    def encode_basic(username: str, password: str) -> str:
        """Encode HTTP basic credentials.

        Args:
            username: Account username or email.
            password: Account password.

        Returns:
            Base64-encoded credentials string without the Basic prefix.
        """
        token = base64.b64encode(f"{username}:{password}".encode()).decode()
        return token
