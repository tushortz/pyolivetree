"""Small helpers: .env loading, request signing and response parsing."""

from __future__ import annotations

import base64
import binascii
import hashlib
import hmac
import os
from pathlib import Path
from typing import Any

import httpx

from pyolivetree.constants import HMAC_KEYS
from pyolivetree.exceptions import OliveTreeAPIError, OliveTreeAuthError


def load_dotenv(path: str = ".env") -> None:
    """Load ``KEY=VALUE`` lines into :data:`os.environ`, keeping values already set.

    Args:
        path: File to read. Missing files are ignored.
    """
    if not os.path.isfile(path):
        return
    for line in Path(path).read_text().splitlines():
        key, sep, val = line.partition("=")
        if sep and not line.lstrip().startswith("#"):
            os.environ.setdefault(key.strip(), val.strip().strip("\"'"))


def sign_body(body: bytes, profile: str = "telemetry", key: bytes | None = None) -> str:
    """Compute the ``signature`` header required by signed endpoints.

    Args:
        body: Exact request body bytes.
        profile: Key name in :data:`~pyolivetree.constants.HMAC_KEYS`
            (``"telemetry"``, ``"ai"``, ``"consent"`` or ``"features"``).
        key: Use this key instead of the profile's key.

    Returns:
        Uppercase hex HMAC-SHA512 digest.

    Raises:
        OliveTreeAuthError: If ``profile`` is unknown and no ``key`` is given.
    """
    if key is None:
        try:
            key = HMAC_KEYS[profile]
        except KeyError:
            raise OliveTreeAuthError(f"Unknown HMAC profile: {profile!r}") from None
    return hmac.new(key, body, hashlib.sha512).hexdigest().upper()


def parse_hmac_key(raw: str | bytes | None) -> bytes | None:
    """Decode an HMAC key given as hex, base64 or raw bytes.

    Args:
        raw: Key material, e.g. from ``OLIVE_TREE_HMAC_KEY``. Empty means no override.

    Returns:
        Key bytes, or ``None`` if ``raw`` is empty.

    Raises:
        ValueError: If a string is neither hex nor base64.
    """
    if not raw:
        return None
    if isinstance(raw, bytes):
        return raw
    text = raw.strip()
    try:
        return bytes.fromhex(text)
    except ValueError:
        pass
    try:
        return base64.b64decode(text, validate=True)
    except binascii.Error:
        raise ValueError("OLIVE_TREE_HMAC_KEY must be hex or base64") from None


def parse_response(r: httpx.Response) -> Any:
    """Decode a response by content type and raise on errors.

    Args:
        r: The HTTP response.

    Returns:
        Parsed JSON, ``str`` for text/XML/HTML, otherwise ``bytes``.

    Raises:
        OliveTreeAuthError: On HTTP 401 or ``{"authenticated": false}``.
        OliveTreeAPIError: On any other HTTP status >= 400.
    """
    ctype = r.headers.get("content-type", "")
    body: Any = r.content
    if "json" in ctype or r.content[:1] in (b"{", b"["):
        try:
            body = r.json()
        except ValueError:
            body = r.text
    elif ctype.startswith("text/") or "xml" in ctype or "html" in ctype:
        body = r.text
    failed = isinstance(body, dict) and body.get("authenticated") is False
    if r.status_code >= 400 or failed:
        code = body.get("errorCode") if isinstance(body, dict) else None
        msg = body.get("error") if isinstance(body, dict) else str(body)[:200]
        cls = OliveTreeAuthError if failed or r.status_code == 401 else OliveTreeAPIError
        raise cls(
            f"{r.request.method} {r.request.url.path}: HTTP {r.status_code}: {msg}",
            r.status_code,
            code,
            body,
        )
    return body
