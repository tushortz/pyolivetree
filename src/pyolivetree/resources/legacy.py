"""Generated legacy API resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyolivetree._operations import OPERATIONS

if TYPE_CHECKING:
    from pyolivetree.async_client import AsyncOliveTreeClient
    from pyolivetree.client import OliveTreeClient


class LegacyResource:
    """Resource methods for the Olive Tree API."""

    def __init__(self, client: OliveTreeClient | AsyncOliveTreeClient) -> None:
        self._client = client

    def daily_reading(self, type: int | str, template_ids: int | str, template_id: int | str, num_recommended: int | str, q: int | str, supportsDevotionalPlans: int | str, data: dict[str, Any] | None = None) -> Any:
        """Daily reading plans API (GET template_versions).

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["legacy_daily_reading"]
        path_params = {}
        query = {"type": type, "template_ids": template_ids, "template_id": template_id, "num_recommended": num_recommended, "q": q, "supportsDevotionalPlans": supportsDevotionalPlans}
        return self._client._api_request(spec, path_params=path_params, query=query, data=data)

    async def adaily_reading(self, type: int | str, template_ids: int | str, template_id: int | str, num_recommended: int | str, q: int | str, supportsDevotionalPlans: int | str, data: dict[str, Any] | None = None) -> Any:
        """Daily reading plans API (GET template_versions).

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["legacy_daily_reading"]
        path_params = {}
        query = {"type": type, "template_ids": template_ids, "template_id": template_id, "num_recommended": num_recommended, "q": q, "supportsDevotionalPlans": supportsDevotionalPlans}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=data)

    def daily_reading_post(self, type: int | str, template_ids: int | str, template_id: int | str, num_recommended: int | str, q: int | str, supportsDevotionalPlans: Any = None, data: dict[str, Any] | None = None) -> Any:
        """Daily reading plans API (POST template_details/search).

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["legacy_daily_reading_post"]
        path_params = {}
        query = {"type": type, "template_ids": template_ids, "template_id": template_id, "num_recommended": num_recommended, "q": q}
        payload: dict[str, Any] = {"supportsDevotionalPlans": supportsDevotionalPlans}
        payload = {k: v for k, v in payload.items() if v is not None}
        if data:
            payload.update(data)
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def adaily_reading_post(self, type: int | str, template_ids: int | str, template_id: int | str, num_recommended: int | str, q: int | str, supportsDevotionalPlans: Any = None, data: dict[str, Any] | None = None) -> Any:
        """Daily reading plans API (POST template_details/search).

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["legacy_daily_reading_post"]
        path_params = {}
        query = {"type": type, "template_ids": template_ids, "template_id": template_id, "num_recommended": num_recommended, "q": q}
        payload: dict[str, Any] = {"supportsDevotionalPlans": supportsDevotionalPlans}
        payload = {k: v for k, v in payload.items() if v is not None}
        if data:
            payload.update(data)
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def recommended(self, data: dict[str, Any] | None = None) -> Any:
        """Library recommendations.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["legacy_recommended"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def arecommended(self, data: dict[str, Any] | None = None) -> Any:
        """Library recommendations.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["legacy_recommended"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def appirater_config(self, data: dict[str, Any] | None = None) -> Any:
        """App rating configuration.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["legacy_appirater_config"]
        path_params = {}
        query = {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=data)

    async def aappirater_config(self, data: dict[str, Any] | None = None) -> Any:
        """App rating configuration.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["legacy_appirater_config"]
        path_params = {}
        query = {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=data)
