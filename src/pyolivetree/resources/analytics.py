"""Generated analytics API resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyolivetree._operations import OPERATIONS

if TYPE_CHECKING:
    from pyolivetree.async_client import AsyncOliveTreeClient
    from pyolivetree.client import OliveTreeClient


class AnalyticsResource:
    """Resource methods for the Olive Tree API."""

    def __init__(self, client: OliveTreeClient | AsyncOliveTreeClient) -> None:
        self._client = client

    def event_manifest(self, data: dict[str, Any] | None = None) -> Any:
        """Event manifest.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["analytics_event_manifest"]
        path_params = {}
        query = {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=data)

    async def aevent_manifest(self, data: dict[str, Any] | None = None) -> Any:
        """Event manifest.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["analytics_event_manifest"]
        path_params = {}
        query = {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=data)

    def event_manifest_range(self, fromDate: int | str, toDate: int | str, data: dict[str, Any] | None = None) -> Any:
        """Event manifest date range.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["analytics_event_manifest_range"]
        path_params = {"fromDate": fromDate, "toDate": toDate}
        query = {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=data)

    async def aevent_manifest_range(self, fromDate: int | str, toDate: int | str, data: dict[str, Any] | None = None) -> Any:
        """Event manifest date range.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["analytics_event_manifest_range"]
        path_params = {"fromDate": fromDate, "toDate": toDate}
        query = {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=data)

    def get_variant(self, experiment_id: int | str, install_id: int | str, customer_id: int | str, data: dict[str, Any] | None = None) -> Any:
        """Get A/B test variant.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["analytics_get_variant"]
        path_params = {}
        query = {"experiment_id": experiment_id, "install_id": install_id, "customer_id": customer_id}
        return self._client._api_request(spec, path_params=path_params, query=query, data=data)

    async def aget_variant(self, experiment_id: int | str, install_id: int | str, customer_id: int | str, data: dict[str, Any] | None = None) -> Any:
        """Get A/B test variant.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["analytics_get_variant"]
        path_params = {}
        query = {"experiment_id": experiment_id, "install_id": install_id, "customer_id": customer_id}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=data)

    def set_variant(self, data: dict[str, Any] | None = None) -> Any:
        """Set A/B test variant.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["analytics_set_variant"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def aset_variant(self, data: dict[str, Any] | None = None) -> Any:
        """Set A/B test variant.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["analytics_set_variant"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def events(self, data: dict[str, Any] | None = None) -> Any:
        """Batch report analytics events.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["analytics_events"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def aevents(self, data: dict[str, Any] | None = None) -> Any:
        """Batch report analytics events.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["analytics_events"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def ios_metrics(self, data: dict[str, Any] | None = None) -> Any:
        """iOS metrics and diagnostics manifest.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["analytics_ios_metrics"]
        path_params = {}
        query = {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=data)

    async def aios_metrics(self, data: dict[str, Any] | None = None) -> Any:
        """iOS metrics and diagnostics manifest.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["analytics_ios_metrics"]
        path_params = {}
        query = {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=data)
