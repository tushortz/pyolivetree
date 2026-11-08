"""Generated smart_search API resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyolivetree._operations import OPERATIONS

if TYPE_CHECKING:
    from pyolivetree.async_client import AsyncOliveTreeClient
    from pyolivetree.client import OliveTreeClient


class SmartSearchResource:
    """Resource methods for the Olive Tree API."""

    def __init__(self, client: OliveTreeClient | AsyncOliveTreeClient) -> None:
        self._client = client

    def models(self, data: dict[str, Any] | None = None) -> Any:
        """List AI models.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["ai_models"]
        path_params = {}
        query = {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=data)

    async def amodels(self, data: dict[str, Any] | None = None) -> Any:
        """List AI models.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["ai_models"]
        path_params = {}
        query = {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=data)

    def status(self, data: dict[str, Any] | None = None) -> Any:
        """AI usage status.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["ai_status"]
        path_params = {}
        query = {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=data)

    async def astatus(self, data: dict[str, Any] | None = None) -> Any:
        """AI usage status.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["ai_status"]
        path_params = {}
        query = {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=data)

    def query(self, query: Any = None, filters: Any = None, data: dict[str, Any] | None = None) -> Any:
        """Smart search query.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["ai_query"]
        path_params = {}
        query = {}
        payload: dict[str, Any] = {"query": query, "filters": filters}
        payload = {k: v for k, v in payload.items() if v is not None}
        if data:
            payload.update(data)
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def aquery(self, query: Any = None, filters: Any = None, data: dict[str, Any] | None = None) -> Any:
        """Smart search query.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["ai_query"]
        path_params = {}
        query = {}
        payload: dict[str, Any] = {"query": query, "filters": filters}
        payload = {k: v for k, v in payload.items() if v is not None}
        if data:
            payload.update(data)
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def set_usage(self, input_tokens: Any = None, output_tokens: Any = None, requests: Any = None, data: dict[str, Any] | None = None) -> Any:
        """Report AI token usage.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["ai_set_usage"]
        path_params = {}
        query = {}
        payload: dict[str, Any] = {"input_tokens": input_tokens, "output_tokens": output_tokens, "requests": requests}
        payload = {k: v for k, v in payload.items() if v is not None}
        if data:
            payload.update(data)
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def aset_usage(self, input_tokens: Any = None, output_tokens: Any = None, requests: Any = None, data: dict[str, Any] | None = None) -> Any:
        """Report AI token usage.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["ai_set_usage"]
        path_params = {}
        query = {}
        payload: dict[str, Any] = {"input_tokens": input_tokens, "output_tokens": output_tokens, "requests": requests}
        payload = {k: v for k, v in payload.items() if v is not None}
        if data:
            payload.update(data)
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)
