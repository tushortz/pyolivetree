"""Generated account API resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyolivetree._operations import OPERATIONS

if TYPE_CHECKING:
    from pyolivetree.async_client import AsyncOliveTreeClient
    from pyolivetree.client import OliveTreeClient


class AccountResource:
    """Resource methods for the Olive Tree API."""

    def __init__(self, client: OliveTreeClient | AsyncOliveTreeClient) -> None:
        self._client = client

    def forgot_password(self, email: Any = None, data: dict[str, Any] | None = None) -> Any:
        """Forgot password.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["account_forgot_password"]
        path_params = {}
        query = {}
        payload: dict[str, Any] = {"email": email}
        payload = {k: v for k, v in payload.items() if v is not None}
        if data:
            payload.update(data)
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def aforgot_password(self, email: Any = None, data: dict[str, Any] | None = None) -> Any:
        """Forgot password.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["account_forgot_password"]
        path_params = {}
        query = {}
        payload: dict[str, Any] = {"email": email}
        payload = {k: v for k, v in payload.items() if v is not None}
        if data:
            payload.update(data)
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def signup(self, user: Any = None, password: Any = None, install_id: Any = None, supportsAccessToken: Any = None, subscribe_to_newsletter: Any = None, implicit_newsletter_consent: Any = None, first_name: Any = None, data: dict[str, Any] | None = None) -> Any:
        """Create account.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["account_signup"]
        path_params = {}
        query = {}
        payload: dict[str, Any] = {"user": user, "pass": password, "install_id": install_id, "supportsAccessToken": supportsAccessToken, "subscribe_to_newsletter": subscribe_to_newsletter, "implicit_newsletter_consent": implicit_newsletter_consent, "first_name": first_name}
        payload = {k: v for k, v in payload.items() if v is not None}
        if data:
            payload.update(data)
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def asignup(self, user: Any = None, password: Any = None, install_id: Any = None, supportsAccessToken: Any = None, subscribe_to_newsletter: Any = None, implicit_newsletter_consent: Any = None, first_name: Any = None, data: dict[str, Any] | None = None) -> Any:
        """Create account.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["account_signup"]
        path_params = {}
        query = {}
        payload: dict[str, Any] = {"user": user, "pass": password, "install_id": install_id, "supportsAccessToken": supportsAccessToken, "subscribe_to_newsletter": subscribe_to_newsletter, "implicit_newsletter_consent": implicit_newsletter_consent, "first_name": first_name}
        payload = {k: v for k, v in payload.items() if v is not None}
        if data:
            payload.update(data)
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def login(self, user: Any = None, password: Any = None, install_id: Any = None, supportsAccessToken: Any = None, subscribe_to_newsletter: Any = None, implicit_newsletter_consent: Any = None, first_name: Any = None, data: dict[str, Any] | None = None) -> Any:
        """Login with credentials.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["account_login"]
        path_params = {}
        query = {}
        payload: dict[str, Any] = {"user": user, "pass": password, "install_id": install_id, "supportsAccessToken": supportsAccessToken, "subscribe_to_newsletter": subscribe_to_newsletter, "implicit_newsletter_consent": implicit_newsletter_consent, "first_name": first_name}
        payload = {k: v for k, v in payload.items() if v is not None}
        if data:
            payload.update(data)
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def alogin(self, user: Any = None, password: Any = None, install_id: Any = None, supportsAccessToken: Any = None, subscribe_to_newsletter: Any = None, implicit_newsletter_consent: Any = None, first_name: Any = None, data: dict[str, Any] | None = None) -> Any:
        """Login with credentials.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["account_login"]
        path_params = {}
        query = {}
        payload: dict[str, Any] = {"user": user, "pass": password, "install_id": install_id, "supportsAccessToken": supportsAccessToken, "subscribe_to_newsletter": subscribe_to_newsletter, "implicit_newsletter_consent": implicit_newsletter_consent, "first_name": first_name}
        payload = {k: v for k, v in payload.items() if v is not None}
        if data:
            payload.update(data)
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def access_token(self, user: Any = None, password: Any = None, install_id: Any = None, supportsAccessToken: Any = None, subscribe_to_newsletter: Any = None, implicit_newsletter_consent: Any = None, first_name: Any = None, data: dict[str, Any] | None = None) -> Any:
        """Upgrade to access token.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["account_access_token"]
        path_params = {}
        query = {}
        payload: dict[str, Any] = {"user": user, "pass": password, "install_id": install_id, "supportsAccessToken": supportsAccessToken, "subscribe_to_newsletter": subscribe_to_newsletter, "implicit_newsletter_consent": implicit_newsletter_consent, "first_name": first_name}
        payload = {k: v for k, v in payload.items() if v is not None}
        if data:
            payload.update(data)
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def aaccess_token(self, user: Any = None, password: Any = None, install_id: Any = None, supportsAccessToken: Any = None, subscribe_to_newsletter: Any = None, implicit_newsletter_consent: Any = None, first_name: Any = None, data: dict[str, Any] | None = None) -> Any:
        """Upgrade to access token.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["account_access_token"]
        path_params = {}
        query = {}
        payload: dict[str, Any] = {"user": user, "pass": password, "install_id": install_id, "supportsAccessToken": supportsAccessToken, "subscribe_to_newsletter": subscribe_to_newsletter, "implicit_newsletter_consent": implicit_newsletter_consent, "first_name": first_name}
        payload = {k: v for k, v in payload.items() if v is not None}
        if data:
            payload.update(data)
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def refresh_token(self, data: dict[str, Any] | None = None) -> Any:
        """Refresh access token.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["account_refresh_token"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def arefresh_token(self, data: dict[str, Any] | None = None) -> Any:
        """Refresh access token.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["account_refresh_token"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def generate_web_handoff_token(self, data: dict[str, Any] | None = None) -> Any:
        """Generate web handoff token.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["account_generate_web_handoff_token"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def agenerate_web_handoff_token(self, data: dict[str, Any] | None = None) -> Any:
        """Generate web handoff token.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["account_generate_web_handoff_token"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def subscription(self, subscriptionId: int | str, data: dict[str, Any] | None = None) -> Any:
        """Account subscription action.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["account_subscription"]
        path_params = {"subscriptionId": subscriptionId}
        query = {}
        payload = data if data is not None else {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def asubscription(self, subscriptionId: int | str, data: dict[str, Any] | None = None) -> Any:
        """Account subscription action.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["account_subscription"]
        path_params = {"subscriptionId": subscriptionId}
        query = {}
        payload = data if data is not None else {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def add_variable_subscription_selections(self, selectionId: int | str, data: dict[str, Any] | None = None) -> Any:
        """Add variable subscription selections.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["account_add_variable_subscription_selections"]
        path_params = {"selectionId": selectionId}
        query = {}
        payload = data if data is not None else {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def aadd_variable_subscription_selections(self, selectionId: int | str, data: dict[str, Any] | None = None) -> Any:
        """Add variable subscription selections.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["account_add_variable_subscription_selections"]
        path_params = {"selectionId": selectionId}
        query = {}
        payload = data if data is not None else {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)
