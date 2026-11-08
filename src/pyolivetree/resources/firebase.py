"""Generated firebase API resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyolivetree._operations import OPERATIONS

if TYPE_CHECKING:
    from pyolivetree.async_client import AsyncOliveTreeClient
    from pyolivetree.client import OliveTreeClient


class FirebaseResource:
    """Resource methods for the Olive Tree API."""

    def __init__(self, client: OliveTreeClient | AsyncOliveTreeClient) -> None:
        self._client = client

    def root(self, data: dict[str, Any] | None = None) -> Any:
        """Firebase Realtime Database root.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["firebase_root"]
        path_params = {}
        query = {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=data)

    async def aroot(self, data: dict[str, Any] | None = None) -> Any:
        """Firebase Realtime Database root.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["firebase_root"]
        path_params = {}
        query = {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=data)
