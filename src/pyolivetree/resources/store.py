"""Store endpoints: catalog, search, your library and wishlists."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from pyolivetree.constants import STORE
from pyolivetree.resources._base import Resource, ids


class Store(Resource):
    """``www.olivetree.com/store/br5/app/json/store``. Available as ``ot.store``.

    Most list endpoints return a ``product_set``: ``{"product_results": [...], "pages": [urls],
    "total_count": n}``. Use :meth:`all_products` to walk every page.
    """

    def _post(self, path: str, **data: Any) -> Any:
        return self._c.request("POST", f"{STORE}/{path}", data=data)

    # --- catalog and feeds ---------------------------------------------------

    def home(self, **kw: Any) -> dict:
        """Store home feed (``{"rows": [...]}``)."""
        return self._post("home", **kw)

    def banner(self, **kw: Any) -> dict:
        """Current promotional banner."""
        return self._post("banner", **kw)

    def featured_categories(self, **kw: Any) -> dict:
        """Featured store categories (``{"categories": [...]}``)."""
        return self._post("featured_categories", **kw)

    def category(self, category_id: int, **kw: Any) -> dict:
        """Products in a category.

        Args:
            category_id: Category id (from :meth:`featured_categories` or :meth:`home`).
        """
        return self._post(f"cat/{category_id}", **kw)

    def search(self, q: str, **kw: Any) -> dict:
        """Search the store.

        Args:
            q: Search text, e.g. ``"study bible"``.

        Returns:
            A ``product_set``.
        """
        return self._c.request("POST", f"{STORE}/search", params={"q": q}, data=kw)

    def product(self, product_id: int) -> dict:
        """Full details for one product.

        Args:
            product_id: The ``productId`` field from any product listing.
        """
        return self._post(f"product/{product_id}")

    def products(self, *product_ids: int) -> dict:
        """Details for several products at once, as a ``product_set``."""
        return self._post(f"product_set/{ids(product_ids)}")

    def path(self, dynamic_path: str, **kw: Any) -> Any:
        """Open any store page by path (e.g. a home-feed ``path`` value).

        Args:
            dynamic_path: Path below ``/store/br5/app/json/store/``.
        """
        return self._post(dynamic_path.lstrip("/"), **kw)

    def all_products(self, result: dict) -> Iterator[dict]:
        """Yield every product across all pages of a ``product_set``.

        Args:
            result: A first page from :meth:`purchased`, :meth:`search`, :meth:`category`, etc.

        Yields:
            Product dicts (``productId``, ``title``, ``owns_product``, ...).
        """
        yield from result.get("product_results") or []
        for url in (result.get("pages") or [])[1:]:
            yield from self._c.request("POST", url).get("product_results") or []

    # --- your account ----------------------------------------------------------

    def purchased(self, **kw: Any) -> dict:
        """Products you own, as a ``product_set``."""
        return self._post("purchased", **kw)

    def library(self, **kw: Any) -> Any:
        """Library listing shown on first run."""
        return self._post("library", **kw)

    def library_details(self, *product_ids: int) -> Any:
        """Library metadata for owned products."""
        return self._post(f"library_details/{ids(product_ids)}")

    def wishlists(self, **kw: Any) -> Any:
        """Your wishlists (``{"lists": [...]}``)."""
        return self._post("user_wishlists", **kw)

    def wishlist_add(self, product_id: int, wishlist_id: int | None = None) -> Any:
        """Add a product to a wishlist. Changes your account."""
        return self._post("modify_wishlist/add", productId=product_id, wishlistId=wishlist_id)

    def wishlist_remove(self, product_id: int, wishlist_id: int | None = None) -> Any:
        """Remove a product from a wishlist. Changes your account."""
        return self._post("modify_wishlist/remove", productId=product_id, wishlistId=wishlist_id)

    # --- onboarding and marketing ---------------------------------------------

    def first_run_subscriptions(self, **kw: Any) -> Any:
        """Subscriptions offered on first launch."""
        return self._post("first_run_subscriptions", **kw)

    def first_run_interests(self, **kw: Any) -> Any:
        """Interest topics offered on first launch."""
        return self._post("first_run_interests", **kw)

    def first_run_bible_list(self, **kw: Any) -> Any:
        """Free Bibles offered on first launch."""
        return self._post("first_run_bible_list", **kw)

    def need_interests(self, **kw: Any) -> Any:
        """Whether to ask the user for interests."""
        return self._post("need_interests", **kw)

    def paid_features(self, **kw: Any) -> Any:
        """Paid features unlocked on your account."""
        return self._post("paid_features", **kw)

    def paid_features_marketing(self, **kw: Any) -> Any:
        """Marketing copy for paid features."""
        return self._post("paid_features_marketing", **kw)

    def ads(self, **kw: Any) -> Any:
        """In-app ads."""
        return self._post("ads", **kw)

    def product_manifest(self, **kw: Any) -> Any:
        """Product manifest used to check for updates."""
        return self._post("product_manifest", **kw)

    def giveaway(self, code: str) -> Any:
        """Look up or redeem a giveaway code.

        Args:
            code: The giveaway code.
        """
        return self._post(f"giveaway/{code}")

    # --- subscriptions and purchases (change your account) --------------------

    def subscriptions_available(self, **kw: Any) -> Any:
        """Subscriptions you can buy."""
        return self._post("subscriptions_available", **kw)

    def allow_subscription_purchase(self, base_plan_id: str) -> Any:
        """Check whether a subscription plan can be bought."""
        return self._post(f"allow_subscription_purchase/{base_plan_id}")

    def subscription_variable_product_selection(self, subscription_id: int) -> Any:
        """Products to choose from for a pick-your-books subscription."""
        return self._post(f"subscription_variable_product_selection/{subscription_id}")

    def register_subscription(self, **data: Any) -> Any:
        """Register a store purchase receipt. Changes your account.

        Args:
            **data: ``signupSource``, ``receiptData``, ``subscriptionProductId``,
                ``platformToken``, ``packageName``.
        """
        return self._post("register_subscription", **data)

    def validate_google_in_app_purchase(self, **data: Any) -> Any:
        """Validate a Google Play purchase. Changes your account."""
        return self._post("validate_google_in_app_purchase", **data)

    def support_delete_account(self, **data: Any) -> Any:
        """Request deletion of your Olive Tree account. **Irreversible.**"""
        return self._post("support_delete_account", **data)
