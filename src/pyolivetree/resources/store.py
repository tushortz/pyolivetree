"""Generated store API resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyolivetree._operations import OPERATIONS

if TYPE_CHECKING:
    from pyolivetree.async_client import AsyncOliveTreeClient
    from pyolivetree.client import OliveTreeClient


class StoreResource:
    """Resource methods for the Olive Tree API."""

    def __init__(self, client: OliveTreeClient | AsyncOliveTreeClient) -> None:
        self._client = client

    def home(self, data: dict[str, Any] | None = None) -> Any:
        """Store home feed.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_home"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def ahome(self, data: dict[str, Any] | None = None) -> Any:
        """Store home feed.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_home"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def banner(self, data: dict[str, Any] | None = None) -> Any:
        """Sale banners.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_banner"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def abanner(self, data: dict[str, Any] | None = None) -> Any:
        """Sale banners.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_banner"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def featured_categories(self, data: dict[str, Any] | None = None) -> Any:
        """Featured categories.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_featured_categories"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def afeatured_categories(self, data: dict[str, Any] | None = None) -> Any:
        """Featured categories.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_featured_categories"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def library(self, data: dict[str, Any] | None = None) -> Any:
        """Library sync metadata.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_library"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def alibrary(self, data: dict[str, Any] | None = None) -> Any:
        """Library sync metadata.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_library"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def purchased(self, data: dict[str, Any] | None = None) -> Any:
        """Purchased products.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_purchased"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def apurchased(self, data: dict[str, Any] | None = None) -> Any:
        """Purchased products.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_purchased"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def user_wishlists(self, data: dict[str, Any] | None = None) -> Any:
        """User wishlists.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_user_wishlists"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def auser_wishlists(self, data: dict[str, Any] | None = None) -> Any:
        """User wishlists.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_user_wishlists"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def subscriptions_available(self, data: dict[str, Any] | None = None) -> Any:
        """Available subscriptions.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_subscriptions_available"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def asubscriptions_available(self, data: dict[str, Any] | None = None) -> Any:
        """Available subscriptions.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_subscriptions_available"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def first_run_subscriptions(self, data: dict[str, Any] | None = None) -> Any:
        """First-run subscription offers.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_first_run_subscriptions"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def afirst_run_subscriptions(self, data: dict[str, Any] | None = None) -> Any:
        """First-run subscription offers.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_first_run_subscriptions"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def first_run_interests(self, data: dict[str, Any] | None = None) -> Any:
        """First-run interests.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_first_run_interests"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def afirst_run_interests(self, data: dict[str, Any] | None = None) -> Any:
        """First-run interests.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_first_run_interests"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def first_run_bible_list(self, data: dict[str, Any] | None = None) -> Any:
        """First-run bible list.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_first_run_bible_list"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def afirst_run_bible_list(self, data: dict[str, Any] | None = None) -> Any:
        """First-run bible list.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_first_run_bible_list"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def need_interests(self, data: dict[str, Any] | None = None) -> Any:
        """Check if interests needed.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_need_interests"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def aneed_interests(self, data: dict[str, Any] | None = None) -> Any:
        """Check if interests needed.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_need_interests"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def paid_features(self, data: dict[str, Any] | None = None) -> Any:
        """Paid features list.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_paid_features"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def apaid_features(self, data: dict[str, Any] | None = None) -> Any:
        """Paid features list.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_paid_features"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def paid_features_marketing(self, data: dict[str, Any] | None = None) -> Any:
        """Paid features marketing.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_paid_features_marketing"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def apaid_features_marketing(self, data: dict[str, Any] | None = None) -> Any:
        """Paid features marketing.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_paid_features_marketing"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def ads(self, data: dict[str, Any] | None = None) -> Any:
        """Fullscreen ads.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_ads"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def aads(self, data: dict[str, Any] | None = None) -> Any:
        """Fullscreen ads.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_ads"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def product_manifest(self, data: dict[str, Any] | None = None) -> Any:
        """Product manifest.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_product_manifest"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def aproduct_manifest(self, data: dict[str, Any] | None = None) -> Any:
        """Product manifest.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_product_manifest"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def support_delete_account(self, data: dict[str, Any] | None = None) -> Any:
        """Request account deletion.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_support_delete_account"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def asupport_delete_account(self, data: dict[str, Any] | None = None) -> Any:
        """Request account deletion.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_support_delete_account"]
        path_params = {}
        query = {}
        payload = data if data is not None else {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def register_subscription(self, signupSource: Any = None, receiptData: Any = None, subscriptionProductId: Any = None, platformToken: Any = None, packageName: Any = None, data: dict[str, Any] | None = None) -> Any:
        """Register Google Play subscription.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_register_subscription"]
        path_params = {}
        query = {}
        payload: dict[str, Any] = {"signupSource": signupSource, "receiptData": receiptData, "subscriptionProductId": subscriptionProductId, "platformToken": platformToken, "packageName": packageName}
        payload = {k: v for k, v in payload.items() if v is not None}
        if data:
            payload.update(data)
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def aregister_subscription(self, signupSource: Any = None, receiptData: Any = None, subscriptionProductId: Any = None, platformToken: Any = None, packageName: Any = None, data: dict[str, Any] | None = None) -> Any:
        """Register Google Play subscription.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_register_subscription"]
        path_params = {}
        query = {}
        payload: dict[str, Any] = {"signupSource": signupSource, "receiptData": receiptData, "subscriptionProductId": subscriptionProductId, "platformToken": platformToken, "packageName": packageName}
        payload = {k: v for k, v in payload.items() if v is not None}
        if data:
            payload.update(data)
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def product_detail(self, productId: int | str, data: dict[str, Any] | None = None) -> Any:
        """Product detail.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_product_detail"]
        path_params = {"productId": productId}
        query = {}
        payload = data if data is not None else {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def aproduct_detail(self, productId: int | str, data: dict[str, Any] | None = None) -> Any:
        """Product detail.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_product_detail"]
        path_params = {"productId": productId}
        query = {}
        payload = data if data is not None else {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def product_set(self, productIds: int | str, data: dict[str, Any] | None = None) -> Any:
        """Multiple products by comma-separated IDs.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_product_set"]
        path_params = {"productIds": productIds}
        query = {}
        payload = data if data is not None else {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def aproduct_set(self, productIds: int | str, data: dict[str, Any] | None = None) -> Any:
        """Multiple products by comma-separated IDs.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_product_set"]
        path_params = {"productIds": productIds}
        query = {}
        payload = data if data is not None else {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def category(self, categoryId: int | str, data: dict[str, Any] | None = None) -> Any:
        """Category product listing.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_category"]
        path_params = {"categoryId": categoryId}
        query = {}
        payload = data if data is not None else {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def acategory(self, categoryId: int | str, data: dict[str, Any] | None = None) -> Any:
        """Category product listing.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_category"]
        path_params = {"categoryId": categoryId}
        query = {}
        payload = data if data is not None else {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def search(self, q: int | str, data: dict[str, Any] | None = None) -> Any:
        """Store/library search.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_search"]
        path_params = {}
        query = {"q": q}
        payload = data if data is not None else {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def asearch(self, q: int | str, data: dict[str, Any] | None = None) -> Any:
        """Store/library search.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_search"]
        path_params = {}
        query = {"q": q}
        payload = data if data is not None else {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def library_details(self, productIds: int | str, data: dict[str, Any] | None = None) -> Any:
        """Library details for product IDs.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_library_details"]
        path_params = {"productIds": productIds}
        query = {}
        payload = data if data is not None else {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def alibrary_details(self, productIds: int | str, data: dict[str, Any] | None = None) -> Any:
        """Library details for product IDs.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_library_details"]
        path_params = {"productIds": productIds}
        query = {}
        payload = data if data is not None else {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def giveaway(self, code: int | str, data: dict[str, Any] | None = None) -> Any:
        """Redeem giveaway code.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_giveaway"]
        path_params = {"code": code}
        query = {}
        payload = data if data is not None else {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def agiveaway(self, code: int | str, data: dict[str, Any] | None = None) -> Any:
        """Redeem giveaway code.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_giveaway"]
        path_params = {"code": code}
        query = {}
        payload = data if data is not None else {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def allow_subscription_purchase(self, basePlanId: int | str, data: dict[str, Any] | None = None) -> Any:
        """Check subscription purchase allowed.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_allow_subscription_purchase"]
        path_params = {"basePlanId": basePlanId}
        query = {}
        payload = data if data is not None else {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def aallow_subscription_purchase(self, basePlanId: int | str, data: dict[str, Any] | None = None) -> Any:
        """Check subscription purchase allowed.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_allow_subscription_purchase"]
        path_params = {"basePlanId": basePlanId}
        query = {}
        payload = data if data is not None else {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def subscription_variable_product_selection(self, subscriptionId: int | str, data: dict[str, Any] | None = None) -> Any:
        """Subscription volume product selection.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_subscription_variable_product_selection"]
        path_params = {"subscriptionId": subscriptionId}
        query = {}
        payload = data if data is not None else {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def asubscription_variable_product_selection(self, subscriptionId: int | str, data: dict[str, Any] | None = None) -> Any:
        """Subscription volume product selection.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_subscription_variable_product_selection"]
        path_params = {"subscriptionId": subscriptionId}
        query = {}
        payload = data if data is not None else {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def wishlist_add(self, productId: Any = None, wishlistId: Any = None, data: dict[str, Any] | None = None) -> Any:
        """Add product to wishlist.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_wishlist_add"]
        path_params = {}
        query = {}
        payload: dict[str, Any] = {"productId": productId, "wishlistId": wishlistId}
        payload = {k: v for k, v in payload.items() if v is not None}
        if data:
            payload.update(data)
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def awishlist_add(self, productId: Any = None, wishlistId: Any = None, data: dict[str, Any] | None = None) -> Any:
        """Add product to wishlist.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_wishlist_add"]
        path_params = {}
        query = {}
        payload: dict[str, Any] = {"productId": productId, "wishlistId": wishlistId}
        payload = {k: v for k, v in payload.items() if v is not None}
        if data:
            payload.update(data)
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def wishlist_remove(self, productId: Any = None, wishlistId: Any = None, data: dict[str, Any] | None = None) -> Any:
        """Remove product from wishlist.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_wishlist_remove"]
        path_params = {}
        query = {}
        payload: dict[str, Any] = {"productId": productId, "wishlistId": wishlistId}
        payload = {k: v for k, v in payload.items() if v is not None}
        if data:
            payload.update(data)
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def awishlist_remove(self, productId: Any = None, wishlistId: Any = None, data: dict[str, Any] | None = None) -> Any:
        """Remove product from wishlist.

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_wishlist_remove"]
        path_params = {}
        query = {}
        payload: dict[str, Any] = {"productId": productId, "wishlistId": wishlistId}
        payload = {k: v for k, v in payload.items() if v is not None}
        if data:
            payload.update(data)
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)

    def dynamic_path(self, dynamicPath: int | str, data: dict[str, Any] | None = None) -> Any:
        """Dynamic store path (resource guide, RC sections, etc.).

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_dynamic_path"]
        path_params = {"dynamicPath": dynamicPath}
        query = {}
        payload = data if data is not None else {}
        return self._client._api_request(spec, path_params=path_params, query=query, data=payload)

    async def adynamic_path(self, dynamicPath: int | str, data: dict[str, Any] | None = None) -> Any:
        """Dynamic store path (resource guide, RC sections, etc.).

        Args:
            See method parameters for path, query, and body fields.

        Returns:
            Parsed API response.

        Raises:
            OliveTreeAPIError: If the API returns an error status.
            OliveTreeAuthError: If authentication or HMAC signing fails.
        """
        spec = OPERATIONS["store_dynamic_path"]
        path_params = {"dynamicPath": dynamicPath}
        query = {}
        payload = data if data is not None else {}
        return await self._client._aapi_request(spec, path_params=path_params, query=query, data=payload)
