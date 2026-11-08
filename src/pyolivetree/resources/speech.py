"""Generated speech API resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyolivetree._operations import OPERATIONS

if TYPE_CHECKING:
    from pyolivetree.async_client import AsyncOliveTreeClient
    from pyolivetree.client import OliveTreeClient


class SpeechResource:
    """Resource methods for the Olive Tree API."""

    def __init__(self, client: OliveTreeClient | AsyncOliveTreeClient) -> None:
        self._client = client

    def nowreading(self, locale: int | str, path: int | str, data: dict[str, Any] | None = None) -> Any:
        """TTS now-reading audio header.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["speech_nowreading"]
        path_params = {"locale": locale, "path": path}
        query = {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=data)

    async def anowreading(self, locale: int | str, path: int | str, data: dict[str, Any] | None = None) -> Any:
        """TTS now-reading audio header.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["speech_nowreading"]
        path_params = {"locale": locale, "path": path}
        query = {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=data)

    def completed_message(self, locale: int | str, data: dict[str, Any] | None = None) -> Any:
        """Reading plan completion audio.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["speech_completed_message"]
        path_params = {"locale": locale}
        query = {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=data)

    async def acompleted_message(self, locale: int | str, data: dict[str, Any] | None = None) -> Any:
        """Reading plan completion audio.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["speech_completed_message"]
        path_params = {"locale": locale}
        query = {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=data)
