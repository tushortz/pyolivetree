"""Reading plans, devotionals, recommendations and verse of the day."""

from __future__ import annotations

from typing import Any

from pyolivetree.constants import SPEECH, VOTD, WWW
from pyolivetree.resources._base import Resource


class Reading(Resource):
    """Available as ``ot.reading``. No login needed."""

    def daily_reading(self, type: str = "featured", **params: Any) -> Any:
        """Reading plans and devotionals.

        Args:
            type: ``"featured"``, ``"template_versions"``, ...
            **params: ``template_ids``, ``template_id``, ``num_recommended``, ``q``.
        """
        return self._c.request(
            "GET",
            f"{WWW}/api/daily_reading_v2.php",
            auth=False,
            params={"type": type, "supportsDevotionalPlans": "true", **params},
        )

    def recommended(self, **data: Any) -> Any:
        """Recommended content for the home screen."""
        return self._c.request("POST", f"{WWW}/api/recommended.php", data=data, auth=False)

    def verse_of_the_day(self, date: str, version: str | None = None) -> str:
        """Verse of the day page.

        Args:
            date: ``YYYY-MM-DD``.
            version: Optional Bible version code.
        """
        return self._c.request(
            "GET", f"{WWW}/votd/index.php", auth=False, params={"date": date, "version": version}
        )

    def verse_of_the_day_image(self, month: int, day: int, product_id: int) -> bytes:
        """Verse of the day image (bytes)."""
        return self._c.request("GET", f"{VOTD}/{month}/{day}/{product_id}", auth=False)

    def now_reading(self, locale: str, path: str) -> Any:
        """Text-to-speech audio for an audio reading plan."""
        return self._c.request("GET", f"{SPEECH}/nowreading/{locale}/{path}", auth=False)

    def completed_message(self, locale: str = "en") -> dict:
        """Audio played when a reading is completed (``{"urls": [...]}``)."""
        return self._c.request("GET", f"{SPEECH}/messages/{locale}/completed", auth=False)
