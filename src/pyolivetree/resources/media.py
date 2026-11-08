"""Images and media streams."""

from __future__ import annotations

from typing import Any

from pyolivetree.constants import CDN, MEDIA, WWW
from pyolivetree.resources._base import Resource


class Media(Resource):
    """Available as ``ot.media``. Image methods return ``bytes``."""

    def _get(self, url: str) -> Any:
        return self._c.request("GET", url, auth=False)

    def cover(self, product_id: int) -> bytes:
        """Product cover (JPEG)."""
        return self._get(f"{CDN}/images/covers/{product_id}.jpg")

    def cover_stack(self, product_id: int) -> bytes:
        """Stacked cover for book sets (PNG). 404 for single products."""
        return self._get(f"{CDN}/images/covers/{product_id}_stack.png")

    def product_image(self, product_id: int) -> bytes:
        """Legacy product image (JPEG)."""
        return self._get(f"{MEDIA}/store/images40/{product_id}.jpg")

    def reading_plan_image(self, template_id: int, size: str = "hero") -> bytes:
        """Reading-plan artwork.

        Args:
            template_id: Reading-plan template id.
            size: ``hero``, ``carousel``, ``grid``, ``list`` or ``portrait``.
        """
        return self._get(f"{CDN}/images/reading_plans/{template_id}_{size}.jpg")

    def reading_plan_list_image(self, template_id: int) -> bytes:
        """Reading-plan list thumbnail (JPEG)."""
        return self._get(f"{WWW}/store/images/reading_plans/{template_id}_list.jpg")

    def stream(self, content_id: int, name: str) -> Any:
        """MPEG-DASH manifest for audio/video content you own."""
        return self._c.request("GET", f"{WWW}/media/content/{content_id}/{name}/stream.mpd")
