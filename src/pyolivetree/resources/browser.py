"""Generated browser API resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyolivetree._operations import OPERATIONS

if TYPE_CHECKING:
    from pyolivetree.async_client import AsyncOliveTreeClient
    from pyolivetree.client import OliveTreeClient


class BrowserResource:
    """Resource methods for the Olive Tree API."""

    def __init__(self, client: OliveTreeClient | AsyncOliveTreeClient) -> None:
        self._client = client

    def app_to_web_bridge(self, platform: int | str, ReaderVersion: int | str, OEM: int | str, clickId: int | str, productid: int | str, login_handoff_token: int | str, data: dict[str, Any] | None = None) -> Any:
        """Redirect to web store for purchase.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["browser_app_to_web_bridge"]
        path_params = {}
        query = {"platform": platform, "ReaderVersion": ReaderVersion, "OEM": OEM, "clickId": clickId, "productid": productid, "login_handoff_token": login_handoff_token}
        return self._client._api_request(spec, path_params=path_params, query=query, data=data)

    async def aapp_to_web_bridge(self, platform: int | str, ReaderVersion: int | str, OEM: int | str, clickId: int | str, productid: int | str, login_handoff_token: int | str, data: dict[str, Any] | None = None) -> Any:
        """Redirect to web store for purchase.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["browser_app_to_web_bridge"]
        path_params = {}
        query = {"platform": platform, "ReaderVersion": ReaderVersion, "OEM": OEM, "clickId": clickId, "productid": productid, "login_handoff_token": login_handoff_token}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=data)

    def manage_subscriptions(self, data: dict[str, Any] | None = None) -> Any:
        """Manage subscriptions web page.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["browser_manage_subscriptions"]
        path_params = {}
        query = {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=data)

    async def amanage_subscriptions(self, data: dict[str, Any] | None = None) -> Any:
        """Manage subscriptions web page.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["browser_manage_subscriptions"]
        path_params = {}
        query = {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=data)

    def bible_study_packs(self, data: dict[str, Any] | None = None) -> Any:
        """Bible study packs web page.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["browser_bible_study_packs"]
        path_params = {}
        query = {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=data)

    async def abible_study_packs(self, data: dict[str, Any] | None = None) -> Any:
        """Bible study packs web page.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["browser_bible_study_packs"]
        path_params = {}
        query = {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=data)

    def product_page(self, productid: int | str, data: dict[str, Any] | None = None) -> Any:
        """Web product page (shared links).

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["browser_product_page"]
        path_params = {}
        query = {"productid": productid}
        return self._client._api_request(spec, path_params=path_params, query=query, data=data)

    async def aproduct_page(self, productid: int | str, data: dict[str, Any] | None = None) -> Any:
        """Web product page (shared links).

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["browser_product_page"]
        path_params = {}
        query = {"productid": productid}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=data)

    def help_articles(self, data: dict[str, Any] | None = None) -> Any:
        """Help center Android articles.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["browser_help_articles"]
        path_params = {}
        query = {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=data)

    async def ahelp_articles(self, data: dict[str, Any] | None = None) -> Any:
        """Help center Android articles.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["browser_help_articles"]
        path_params = {}
        query = {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=data)

    def help_login(self, data: dict[str, Any] | None = None) -> Any:
        """Help article: Get Started Logging In.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["browser_help_login"]
        path_params = {}
        query = {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=data)

    async def ahelp_login(self, data: dict[str, Any] | None = None) -> Any:
        """Help article: Get Started Logging In.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["browser_help_login"]
        path_params = {}
        query = {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=data)

    def eula(self, data: dict[str, Any] | None = None) -> Any:
        """End user license agreement.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["browser_eula"]
        path_params = {}
        query = {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=data)

    async def aeula(self, data: dict[str, Any] | None = None) -> Any:
        """End user license agreement.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["browser_eula"]
        path_params = {}
        query = {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=data)

    def privacy_policy(self, data: dict[str, Any] | None = None) -> Any:
        """Privacy policy page.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["browser_privacy_policy"]
        path_params = {}
        query = {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=data)

    async def aprivacy_policy(self, data: dict[str, Any] | None = None) -> Any:
        """Privacy policy page.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["browser_privacy_policy"]
        path_params = {}
        query = {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=data)

    def press_privacy(self, data: dict[str, Any] | None = None) -> Any:
        """Press privacy and terms page.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["browser_press_privacy"]
        path_params = {}
        query = {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=data)

    async def apress_privacy(self, data: dict[str, Any] | None = None) -> Any:
        """Press privacy and terms page.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["browser_press_privacy"]
        path_params = {}
        query = {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=data)
