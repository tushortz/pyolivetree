"""Configuration and environment loading."""

from __future__ import annotations

import os
import uuid
from dataclasses import dataclass
from pathlib import Path

from pyolivetree.hmac_keys import DEFAULT_HMAC_PROFILE, HMAC_KEYS


def _strip_quotes(value: str) -> str:
    """Remove surrounding quotes from an env value.

    Args:
        value: Raw environment variable value.

    Returns:
        Stripped value without outer quotes.
    """
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def load_dotenv(path: Path | None = None) -> None:
    """Load key=value pairs from a .env file into os.environ.

    Existing environment variables are not overwritten.

    Args:
        path: Path to the .env file. Defaults to .env in the current directory.

    Returns:
        None.

    Raises:
        OSError: If the file cannot be read.
    """
    env_path = path or Path(".env")
    if not env_path.is_file():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, raw = line.partition("=")
        key = key.strip()
        if key and key not in os.environ:
            os.environ[key] = _strip_quotes(raw.strip())


@dataclass
class ClientConfig:
    """Runtime configuration for Olive Tree API clients."""

    username: str | None = None
    password: str | None = None
    install_id: str | None = None
    hmac_key: bytes | None = None
    timeout: float = 30.0
    base_url: str = "https://www.olivetree.com"

    def get_hmac_key(self, profile: str = DEFAULT_HMAC_PROFILE) -> bytes:
        """Return the HMAC key for a signing profile.

        Args:
            profile: Key profile name (telemetry, ai, consent, features).

        Returns:
            Raw key bytes.

        Raises:
            ValueError: If the profile is unknown.
        """
        if self.hmac_key is not None:
            return self.hmac_key
        try:
            return HMAC_KEYS[profile]
        except KeyError as exc:
            raise ValueError(f"unknown HMAC profile: {profile}") from exc

    @classmethod
    def from_env(
        cls,
        *,
        username: str | None = None,
        password: str | None = None,
        install_id: str | None = None,
        hmac_key: str | bytes | None = None,
        timeout: float = 30.0,
        base_url: str = "https://www.olivetree.com",
        env_file: Path | None = None,
    ) -> ClientConfig:
        """Build configuration from arguments with environment fallbacks.

        Args:
            username: Olive Tree account email.
            password: Olive Tree account password.
            install_id: Device install identifier. Auto-generated if missing.
            hmac_key: HMAC signing key as hex, base64, or raw bytes.
            timeout: Request timeout in seconds.
            base_url: Default API base URL.
            env_file: Optional path to a .env file.

        Returns:
            Populated ClientConfig instance.

        Raises:
            ValueError: If hmac_key encoding is invalid.
        """
        load_dotenv(env_file)
        resolved_username = username or os.environ.get("OLIVE_TREE_USERNAME")
        resolved_password = password or os.environ.get("OLIVE_TREE_PASSWORD")
        resolved_install = (
            install_id or os.environ.get("OLIVE_TREE_INSTALL_ID") or str(uuid.uuid4())
        )
        raw_hmac = hmac_key if hmac_key is not None else os.environ.get("OLIVE_TREE_HMAC_KEY")
        return cls(
            username=resolved_username,
            password=resolved_password,
            install_id=resolved_install,
            hmac_key=_parse_hmac_key(raw_hmac),
            timeout=timeout,
            base_url=base_url.rstrip("/"),
        )


def _parse_hmac_key(raw: str | bytes | None) -> bytes | None:
    """Parse an HMAC key from hex, base64, or raw bytes.

    Args:
        raw: Key material from config or environment.

    Returns:
        Decoded key bytes, or None if not provided.

    Raises:
        ValueError: If the key encoding is invalid.
    """
    if raw is None or raw == "":
        return None
    if isinstance(raw, bytes):
        return raw
    import base64
    import binascii

    text = raw.strip()
    try:
        return bytes.fromhex(text)
    except ValueError:
        pass
    try:
        return base64.b64decode(text, validate=True)
    except binascii.Error as exc:
        raise ValueError("OLIVE_TREE_HMAC_KEY must be hex or base64 encoded") from exc
