"""Generated sync API resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyolivetree._operations import OPERATIONS

if TYPE_CHECKING:
    from pyolivetree.async_client import AsyncOliveTreeClient
    from pyolivetree.client import OliveTreeClient


class SyncResource:
    """Resource methods for the Olive Tree API."""

    def __init__(self, client: OliveTreeClient | AsyncOliveTreeClient) -> None:
        self._client = client

    def status(self, device_id: int | str, do_not_lock: int | str, managed_data_set: int | str, update_count: int | str, sync_client_protocol_version: int | str, reader_version: int | str, data: dict[str, Any] | None = None) -> Any:
        """Sync status and lock.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["sync_status"]
        path_params = {}
        query = {"device_id": device_id, "do_not_lock": do_not_lock, "managed_data_set": managed_data_set, "update_count": update_count, "sync_client_protocol_version": sync_client_protocol_version, "reader_version": reader_version}
        return self._client._api_request(spec, path_params=path_params, query=query, data=data)

    async def astatus(self, device_id: int | str, do_not_lock: int | str, managed_data_set: int | str, update_count: int | str, sync_client_protocol_version: int | str, reader_version: int | str, data: dict[str, Any] | None = None) -> Any:
        """Sync status and lock.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["sync_status"]
        path_params = {}
        query = {"device_id": device_id, "do_not_lock": do_not_lock, "managed_data_set": managed_data_set, "update_count": update_count, "sync_client_protocol_version": sync_client_protocol_version, "reader_version": reader_version}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=data)

    def release_lock(self, device_id: int | str, managed_data_set: int | str, sync_client_protocol_version: int | str, data: dict[str, Any] | None = None) -> Any:
        """Release sync lock.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["sync_release_lock"]
        path_params = {}
        query = {"device_id": device_id, "managed_data_set": managed_data_set, "sync_client_protocol_version": sync_client_protocol_version}
        return self._client._api_request(spec, path_params=path_params, query=query, data=data)

    async def arelease_lock(self, device_id: int | str, managed_data_set: int | str, sync_client_protocol_version: int | str, data: dict[str, Any] | None = None) -> Any:
        """Release sync lock.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["sync_release_lock"]
        path_params = {}
        query = {"device_id": device_id, "managed_data_set": managed_data_set, "sync_client_protocol_version": sync_client_protocol_version}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=data)

    def bad_annotation_data(self, data: dict[str, Any] | None = None) -> Any:
        """Get possibly bad annotation data.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["sync_bad_annotation_data"]
        path_params = {}
        query = {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=data)

    async def abad_annotation_data(self, data: dict[str, Any] | None = None) -> Any:
        """Get possibly bad annotation data.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["sync_bad_annotation_data"]
        path_params = {}
        query = {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=data)
