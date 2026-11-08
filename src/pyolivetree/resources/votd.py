"""Generated votd API resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyolivetree._operations import OPERATIONS

if TYPE_CHECKING:
    from pyolivetree.async_client import AsyncOliveTreeClient
    from pyolivetree.client import OliveTreeClient


class VotdResource:
    """Resource methods for the Olive Tree API."""

    def __init__(self, client: OliveTreeClient | AsyncOliveTreeClient) -> None:
        self._client = client

    def legacy_votd_index(self, date: int | str, version: int | str, data: dict[str, Any] | None = None) -> Any:
        """Verse of the day text.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["legacy_votd_index"]
        path_params = {}
        query = {"date": date, "version": version}
        return self._client._api_request(spec, path_params=path_params, query=query, data=data)

    async def alegacy_votd_index(self, date: int | str, version: int | str, data: dict[str, Any] | None = None) -> Any:
        """Verse of the day text.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["legacy_votd_index"]
        path_params = {}
        query = {"date": date, "version": version}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=data)

    def image(self, month: int | str, day: int | str, productId: int | str, data: dict[str, Any] | None = None) -> Any:
        """Verse of the day background image.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["votd_image"]
        path_params = {"month": month, "day": day, "productId": productId}
        query = {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=data)

    async def aimage(self, month: int | str, day: int | str, productId: int | str, data: dict[str, Any] | None = None) -> Any:
        """Verse of the day background image.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["votd_image"]
        path_params = {"month": month, "day": day, "productId": productId}
        query = {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=data)
