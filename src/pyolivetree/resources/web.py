"""Olive Tree web pages and client config files."""

from __future__ import annotations

from typing import Any

from pyolivetree.constants import HELP, WWW
from pyolivetree.resources._base import Resource


class Web(Resource):
    """Available as ``ot.web``. Returns HTML (``str``) or JSON."""

    def _get(self, url: str, **params: Any) -> Any:
        return self._c.request("GET", url, params=params, auth=False)

    def timeouts(self) -> dict:
        """Recommended network timeouts."""
        return self._get(f"{WWW}/static/app_assets/timeouts.json")

    def appirater_config(self) -> dict:
        """Rate-this-app prompt settings."""
        return self._get(f"{WWW}/api/appirater_config.json")

    def app_to_web_bridge(self, **params: Any) -> str:
        """Open a store page in the browser, optionally logged in.

        Args:
            **params: ``platform``, ``ReaderVersion``, ``OEM``, ``clickId``, ``productid``,
                ``login_handoff_token`` (from
                :meth:`~pyolivetree.resources.account.Account.web_handoff_token`).
        """
        return self._get(f"{WWW}/store/br5/app_to_web_bridge.php", **params)

    def product_page(self, product_id: int) -> str:
        """Store web page for a product (HTML)."""
        return self._get(f"{WWW}/store/product.php", productid=product_id)

    def bible_study_packs(self) -> str:
        """Bible study packs page (HTML)."""
        return self._get(f"{WWW}/store/biblestudypacks.php")

    def manage_subscriptions(self) -> str:
        """Manage-subscriptions page (HTML)."""
        return self._get(f"{WWW}/store/manage_subscriptions.php")

    def eula(self) -> str:
        """End-user license agreement (HTML)."""
        return self._get(f"{WWW}/eula")

    def privacy_policy(self) -> str:
        """Privacy policy (HTML)."""
        return self._get(f"{WWW}/privacy_policy")

    def help_articles(self) -> str:
        """Help-center section for the mobile app (HTML)."""
        return self._get(f"{HELP}/hc/en-us/sections/360000034263-Android-OLIVE-TREE-BIBLE-APP-7-1")

    def help_login(self) -> str:
        """Help article on logging in (HTML)."""
        return self._get(f"{HELP}/hc/en-us/articles/210270643-Get-Started-Logging-In")
