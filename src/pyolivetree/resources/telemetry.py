"""Analytics, experiments, consent and session endpoints."""

from __future__ import annotations

from typing import Any

from pyolivetree.constants import ANALYTICS, PRIVACY
from pyolivetree.resources._base import Resource


class Telemetry(Resource):
    """``analytics.olivetree.com`` and ``privacy.olivetree.com``. Available as ``ot.telemetry``.

    The POST/PUT methods send data to Olive Tree; wrapped for completeness.
    """

    def event_manifest(self, from_date: str | None = None, to_date: str | None = None) -> dict:
        """Analytics event definitions, optionally for a date range (``YYYY-MM-DD``)."""
        url = (
            f"{ANALYTICS}/event_manifests/from/{from_date}/to/{to_date}"
            if from_date
            else f"{ANALYTICS}/event_manifest"
        )
        return self._c.request("GET", url, auth=False)

    def get_variant(self, experiment_id: str, customer_id: int | None = None) -> Any:
        """A/B experiment variant assigned to this device."""
        return self._c.request(
            "GET",
            f"{ANALYTICS}/variant",
            auth=False,
            params={
                "experiment_id": experiment_id,
                "install_id": self._c.device_id,
                "customer_id": customer_id,
            },
        )

    def set_variant(self, **body: Any) -> Any:
        """Set an experiment variant."""
        return self._c.request("PUT", f"{ANALYTICS}/variant", json=body, auth=False)

    def events(self, events: Any) -> Any:
        """Send analytics events (signed)."""
        return self._c.request("POST", f"{ANALYTICS}/events", json=events, sign="telemetry", auth=False)

    def session_start(self, **body: Any) -> Any:
        """Report an app session start (signed)."""
        return self._c.request("POST", f"{PRIVACY}/session/start", json=body, sign="telemetry", auth=False)

    def consent_receipt(self, **body: Any) -> Any:
        """Record a consent receipt."""
        return self._c.request("POST", f"{PRIVACY}/consent/receipt", json=body, auth=False)

    def location_settings(self, **body: Any) -> dict:
        """Read location-based consent settings; pass fields to change them."""
        if body:
            return self._c.request("POST", f"{PRIVACY}/consent/location/settings", json=body, auth=False)
        return self._c.request("GET", f"{PRIVACY}/consent/location/settings", auth=False)

    def subscription_log_usage(self, **body: Any) -> Any:
        """Log subscription content usage."""
        return self._c.request("POST", f"{PRIVACY}/subscription/log_usage", json=body, auth=False)
