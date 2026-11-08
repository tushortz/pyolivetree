"""In-app XML endpoints: product registration, info and download links."""

from __future__ import annotations

from typing import Any

from pyolivetree.constants import XML
from pyolivetree.resources._base import Resource, ids


class Products(Resource):
    """``www.olivetree.com/store/br5/app/in-app/xml``. Available as ``ot.products``.

    These return XML as ``str``.
    """

    def _post(self, path: str, **kw: Any) -> Any:
        return self._c.request("POST", f"{XML}/{path}", **kw)

    def download_links(self, *product_ids: int) -> str:
        """``<documents>`` XML describing each owned product and its download URLs.

        Purchased book files are encrypted; this returns where to fetch them, not readable text.
        """
        return self._post(f"download_products/{ids(product_ids)}")

    def register(self, **data: Any) -> str:
        """Register products installed on this device."""
        return self._post("register_products", data=data)

    def info(self, **data: Any) -> str:
        """Product info for installed products."""
        return self._post("product_info", data=data)

    def updates(self, body: Any = None) -> str:
        """Check installed products for updates.

        Args:
            body: JSON body describing installed products.
        """
        return self._post("product_updates", json=body or {}, auth=False)

    def email_signup(self, email: str, bibles: str = "", token: str = "") -> str:
        """Sign an email up for free Bibles / newsletters."""
        return self._post("email_signup", data={"email": email, "bibles": bibles, "token": token})

    def reading_templates(self, *template_ids: int) -> str:
        """Reading-plan template XML.

        Args:
            *template_ids: Template ids (``reading_template_id`` in your reading plans).
        """
        return self._c.request(
            "GET", f"{XML}/download_reading_templates", params={"templateIds": ids(template_ids)}, auth=False
        )
