"""Account endpoints: login, tokens, signup and subscriptions."""

from __future__ import annotations

from typing import Any

from pyolivetree.constants import ACCOUNT
from pyolivetree.resources._base import Resource


class Account(Resource):
    """``www.olivetree.com/store/br5/app/json/account``. Available as ``ot.account``."""

    def _creds(self, **kw: Any) -> dict[str, Any]:
        c = self._c
        return {
            "user": c.username,
            "pass": c.password,
            "install_id": c.device_id,
            "supportsAccessToken": 1,
            **kw,
        }

    def login(self, **kw: Any) -> dict:
        """Log in with the client's username and password and store the tokens.

        Args:
            **kw: Extra form fields (e.g. ``subscribe_to_newsletter``).

        Returns:
            ``{"authenticated", "user_id", "authentication_token", "expires", "refresh_token"}``.
        """
        data = self._c.request("POST", f"{ACCOUNT}/account_login", data=self._creds(**kw), auth=False)
        self._c._take_tokens(data)
        return data

    def access_token(self, **kw: Any) -> dict:
        """Exchange credentials for an access token (older login flow). Stores the tokens.

        Returns:
            Same shape as :meth:`login`.
        """
        data = self._c.request("POST", f"{ACCOUNT}/access_token", data=self._creds(**kw), auth=False)
        self._c._take_tokens(data)
        return data

    def refresh_token(self) -> dict:
        """Swap the stored refresh token for a new access token. Stores the new tokens.

        Returns:
            Same shape as :meth:`login`.
        """
        data = self._c.request(
            "POST",
            f"{ACCOUNT}/refresh_token",
            auth=False,
            headers={"OTAuthorization": f"Bearer {self._c.refresh_token}"},
        )
        self._c._take_tokens(data)
        return data

    def signup(self, email: str, password: str, first_name: str = "", **kw: Any) -> dict:
        """Create a new Olive Tree account.

        Args:
            email: Account email.
            password: Account password.
            first_name: Optional first name.
            **kw: Extra fields such as ``subscribe_to_newsletter``.
        """
        return self._c.request(
            "POST",
            f"{ACCOUNT}/account_signup",
            auth=False,
            data={**self._creds(**kw), "user": email, "pass": password, "first_name": first_name},
        )

    def forgot_password(self, email: str) -> dict:
        """Send a password-reset email.

        Args:
            email: Account email.
        """
        return self._c.request("POST", f"{ACCOUNT}/forgot_password", data={"email": email}, auth=False)

    def web_handoff_token(self, storefront_code: str | None = None) -> dict:
        """Get a one-time token for opening olivetree.com already logged in.

        Args:
            storefront_code: Optional storefront code.

        Returns:
            ``{"token": ...}``; pass it to :meth:`~pyolivetree.resources.web.Web.app_to_web_bridge`
            as ``login_handoff_token``.
        """
        return self._c.request(
            "POST", f"{ACCOUNT}/generate_web_handoff_token", data={"storefront_code": storefront_code}
        )

    def subscription(self, subscription_id: int) -> dict:
        """Details of one of your subscriptions.

        Args:
            subscription_id: Subscription id.
        """
        return self._c.request("POST", f"{ACCOUNT}/subscription/{subscription_id}")

    def add_variable_subscription_selections(self, selection_id: int, **data: Any) -> dict:
        """Save product choices for a pick-your-books subscription.

        Args:
            selection_id: Selection id.
            **data: Form fields the store expects.
        """
        return self._c.request(
            "POST", f"{ACCOUNT}/add_variable_subscription_selections/{selection_id}", data=data
        )
