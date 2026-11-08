"""Smart Search AI endpoints."""

from __future__ import annotations

from typing import Any

from pyolivetree.constants import AI_API, AI_STAGING_API
from pyolivetree.resources._base import Resource


class AI(Resource):
    """``biblesearch-ai.olivetree.com``. Available as ``ot.ai``. Requests are HMAC-signed."""

    def query(self, query: str, books: list[str] | None = None) -> Any:
        """Ask Smart Search a question. Uses your Smart Search quota.

        Args:
            query: Question or topic, e.g. ``"verses about patience"``.
            books: Limit results to these books, e.g. ``["Romans", "James"]``.
        """
        body: dict[str, Any] = {"query": query}
        if books:
            body["filters"] = {"books": books}
        return self._c.request("POST", f"{AI_API}/query", json=body, sign="ai")

    def status(self) -> dict:
        """Your Smart Search usage and limits (``user_limits``, ``status``, ...)."""
        return self._c.request("GET", f"{AI_API}/status")

    def set_usage(self, input_tokens: int, output_tokens: int, requests: int) -> Any:
        """Report Smart Search usage. Changes your usage record."""
        return self._c.request(
            "PUT",
            f"{AI_API}/set-my-usage",
            sign="ai",
            json={"input_tokens": input_tokens, "output_tokens": output_tokens, "requests": requests},
        )

    def models(self) -> list:
        """Available AI models."""
        return self._c.request("GET", f"{AI_STAGING_API}/models", auth=False)
