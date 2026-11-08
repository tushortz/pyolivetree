"""Generated messages API resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyolivetree._operations import OPERATIONS

if TYPE_CHECKING:
    from pyolivetree.async_client import AsyncOliveTreeClient
    from pyolivetree.client import OliveTreeClient


class MessagesResource:
    """Resource methods for the Olive Tree API."""

    def __init__(self, client: OliveTreeClient | AsyncOliveTreeClient) -> None:
        self._client = client

    def list(self, install_id: Any = None, data: dict[str, Any] | None = None) -> Any:
        """Messages API - messages.php.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["messages_list"]
        path_params = {}
        query = {}
        payload: dict[str, Any] = {"install_id": install_id}
        payload = {k: v for k, v in payload.items() if v is not None}
        if data:
            payload.update(data)
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def alist(self, install_id: Any = None, data: dict[str, Any] | None = None) -> Any:
        """Messages API - messages.php.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["messages_list"]
        path_params = {}
        query = {}
        payload: dict[str, Any] = {"install_id": install_id}
        payload = {k: v for k, v in payload.items() if v is not None}
        if data:
            payload.update(data)
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def devices(self, data: dict[str, Any] | None = None) -> Any:
        """Messages API - devices.php.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["messages_devices"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def adevices(self, data: dict[str, Any] | None = None) -> Any:
        """Messages API - devices.php.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["messages_devices"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def metrics(self, install_id: Any = None, message_id: Any = None, metrics: Any = None, data: dict[str, Any] | None = None) -> Any:
        """Messages API - metrics.php.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["messages_metrics"]
        path_params = {}
        query = {}
        payload: dict[str, Any] = {"install_id": install_id, "message_id": message_id, "metrics": metrics}
        payload = {k: v for k, v in payload.items() if v is not None}
        if data:
            payload.update(data)
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def ametrics(self, install_id: Any = None, message_id: Any = None, metrics: Any = None, data: dict[str, Any] | None = None) -> Any:
        """Messages API - metrics.php.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["messages_metrics"]
        path_params = {}
        query = {}
        payload: dict[str, Any] = {"install_id": install_id, "message_id": message_id, "metrics": metrics}
        payload = {k: v for k, v in payload.items() if v is not None}
        if data:
            payload.update(data)
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)
