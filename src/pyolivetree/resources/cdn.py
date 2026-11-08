"""Generated cdn API resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyolivetree._operations import OPERATIONS

if TYPE_CHECKING:
    from pyolivetree.async_client import AsyncOliveTreeClient
    from pyolivetree.client import OliveTreeClient


class CdnResource:
    """Resource methods for the Olive Tree API."""

    def __init__(self, client: OliveTreeClient | AsyncOliveTreeClient) -> None:
        self._client = client

    def cover_jpg(self, productId: int | str, data: dict[str, Any] | None = None) -> Any:
        """Product cover image.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["cdn_cover_jpg"]
        path_params = {"productId": productId}
        query = {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=data)

    async def acover_jpg(self, productId: int | str, data: dict[str, Any] | None = None) -> Any:
        """Product cover image.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["cdn_cover_jpg"]
        path_params = {"productId": productId}
        query = {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=data)

    def cover_stack(self, productId: int | str, data: dict[str, Any] | None = None) -> Any:
        """Book set stack cover image.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["cdn_cover_stack"]
        path_params = {"productId": productId}
        query = {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=data)

    async def acover_stack(self, productId: int | str, data: dict[str, Any] | None = None) -> Any:
        """Book set stack cover image.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["cdn_cover_stack"]
        path_params = {"productId": productId}
        query = {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=data)

    def reading_plan_image(self, templateId: int | str, size: int | str, data: dict[str, Any] | None = None) -> Any:
        """Reading plan template image.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["cdn_reading_plan_image"]
        path_params = {"templateId": templateId, "size": size}
        query = {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=data)

    async def areading_plan_image(self, templateId: int | str, size: int | str, data: dict[str, Any] | None = None) -> Any:
        """Reading plan template image.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["cdn_reading_plan_image"]
        path_params = {"templateId": templateId, "size": size}
        query = {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=data)

    def www_reading_plan_list_image(self, templateId: int | str, data: dict[str, Any] | None = None) -> Any:
        """Reading plan list thumbnail on www.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["www_reading_plan_list_image"]
        path_params = {"templateId": templateId}
        query = {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=data)

    async def awww_reading_plan_list_image(self, templateId: int | str, data: dict[str, Any] | None = None) -> Any:
        """Reading plan list thumbnail on www.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["www_reading_plan_list_image"]
        path_params = {"templateId": templateId}
        query = {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=data)
