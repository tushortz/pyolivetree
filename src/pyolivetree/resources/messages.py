"""In-app message center."""

from __future__ import annotations

from typing import Any

from pyolivetree.constants import WWW
from pyolivetree.resources._base import Resource

_BASE = f"{WWW}/api/messages/v1"


class Messages(Resource):
    """Available as ``ot.messages``. Requests are HMAC-signed.

    The server answers 401 until the device is registered with :meth:`register_device`.
    """

    def list(self) -> Any:
        """Messages for this device."""
        return self._c.request(
            "POST",
            f"{_BASE}/messages.php",
            sign="telemetry",
            auth=False,
            json={"install_id": self._c.device_id},
        )

    def register_device(self, **body: Any) -> Any:
        """Register this device for messages. Body fields are not documented."""
        return self._c.request("POST", f"{_BASE}/devices.php", json=body, sign="telemetry", auth=False)

    def metrics(self, message_id: int, metrics: dict) -> Any:
        """Report that a message was seen/clicked.

        Args:
            message_id: Message id from :meth:`list`.
            metrics: Metric values to report.
        """
        return self._c.request(
            "POST",
            f"{_BASE}/metrics.php",
            sign="telemetry",
            auth=False,
            json={"install_id": self._c.device_id, "message_id": message_id, "metrics": metrics},
        )
