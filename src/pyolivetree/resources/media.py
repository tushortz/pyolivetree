"""Generated media API resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyolivetree._operations import OPERATIONS

if TYPE_CHECKING:
    from pyolivetree.async_client import AsyncOliveTreeClient
    from pyolivetree.client import OliveTreeClient


class MediaResource:
    """Resource methods for the Olive Tree API."""

    def __init__(self, client: OliveTreeClient | AsyncOliveTreeClient) -> None:
        self._client = client

    def product_image(self, productId: int | str, data: dict[str, Any] | None = None) -> Any:
        """Legacy product image (40px).

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["media_product_image"]
        path_params = {"productId": productId}
        query = {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=data)

    async def aproduct_image(self, productId: int | str, data: dict[str, Any] | None = None) -> Any:
        """Legacy product image (40px).

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["media_product_image"]
        path_params = {"productId": productId}
        query = {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=data)
