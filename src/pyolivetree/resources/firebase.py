"""Firebase Realtime Database."""

from __future__ import annotations

from typing import Any

from pyolivetree.constants import FIREBASE
from pyolivetree.resources._base import Resource


class Firebase(Resource):
    """Available as ``ot.firebase``. Requests are unauthenticated."""

    def get(self, path: str = "") -> Any:
        """Read a node, e.g. ``get("config")``. The server may refuse access (HTTP 423 or 401).

        Args:
            path: Node path; empty for the root.
        """
        return self._c.request("GET", f"{FIREBASE}/{path.strip('/')}.json", auth=False)

    def root(self) -> Any:
        """Read the database root (``/.json``)."""
        return self.get()
