"""Embedded HMAC keys extracted from the Olive Tree Android app."""

from __future__ import annotations

# ponytail: keys are static app secrets; rotate only when the APK changes.

HMAC_KEYS: dict[str, bytes] = {
    # otTelemetry.Key() — analytics, messages, privacy session, subscription log
    "telemetry": bytes.fromhex(
        "483136e789e9781c4bf4b94a405da7b4c3109a559d1429883e71eb032cfcdc9"
        "ceb3f76381639321b4890449ac0093c3c103e9b4b19e213d3c34f02dc4106a87e"
    ),
    # dl0.E0() — biblesearch-ai query and usage endpoints
    "ai": bytes.fromhex(
        "c69b54518884da105554f4dda9ac30b16d14f1d084318bbc389f00debaa0f37c"
        "3f29b7494afdbe41abb7eab9c7eb5bb234cb02b2f9355cc8997c105756d580a6"
    ),
    # gh0.E0() — consent manifest and receipt signing
    "consent": bytes.fromhex(
        "f91c94eb56d2e0ae31b902828b931243b5a0956c8f99a4ace778655d39f65511"
        "f4f6123046516609630241a879d705c6f02b3d197bbbe78e16265eeaac87f875"
    ),
    # wn0.I0() — signed features/settings files
    "features": bytes.fromhex(
        "d11bde62682b4b41253c4f6eec12d2a0095aa1802f92343e703af16a29168617"
        "081c6859384f960d7680989c0600ba596e2a5d17d0444424fdd4b367ce75402b"
    ),
}

DEFAULT_HMAC_PROFILE = "telemetry"
