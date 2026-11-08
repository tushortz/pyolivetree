"""Tests for authentication helpers."""

from __future__ import annotations

import pytest

from pyolivetree.auth import AuthManager
from pyolivetree.config import ClientConfig
from pyolivetree.exceptions import OliveTreeAuthError


def test_set_and_get_tokens(auth: AuthManager) -> None:
    """Tokens can be stored and retrieved."""
    auth.set_tokens("new-access", "new-refresh")
    assert auth.access_token == "new-access"
    assert auth.refresh_token == "new-refresh"


def test_update_from_response(auth: AuthManager) -> None:
    """Auth response updates stored tokens."""
    auth.update_from_response(
        {"authenticated": True, "authentication_token": "tok", "refresh_token": "ref"}
    )
    assert auth.access_token == "tok"
    assert auth.refresh_token == "ref"


def test_update_from_response_failure(auth: AuthManager) -> None:
    """Failed authentication raises OliveTreeAuthError."""
    with pytest.raises(OliveTreeAuthError):
        auth.update_from_response({"authenticated": False})


def test_auth_headers_bearer(auth: AuthManager) -> None:
    """Bearer token is added to headers when configured."""
    headers = auth.auth_headers([{"OTBearerAuth": []}])
    assert headers["OTAuthorization"] == "Bearer token-abc"


def test_basic_auth_when_no_token() -> None:
    """Basic auth is offered when bearer token is missing."""
    cfg = ClientConfig(username="u", password="p", install_id="i")
    manager = AuthManager(cfg)
    creds = manager.basic_auth([{"BasicAuth": []}])
    assert creds == ("u", "p")


def test_basic_auth_sync_prefers_basic_with_token() -> None:
    """Sync endpoints use basic auth even when a bearer token is set."""
    cfg = ClientConfig(username="u", password="p", install_id="i")
    manager = AuthManager(cfg, access_token="tok")
    security = [{"OTBearerAuth": []}, {"BasicAuth": []}]
    sync_url = "https://sync.olivetree.com"
    assert manager.basic_auth(security, server_url=sync_url) == ("u", "p")
    assert manager.auth_headers(security, server_url=sync_url) == {}


def test_basic_auth_jenkins() -> None:
    """Jenkins basic auth uses configured credentials."""
    cfg = ClientConfig(username="jenkins", password="secret", install_id="i")
    manager = AuthManager(cfg)
    creds = manager.basic_auth([{"JenkinsBasicAuth": []}])
    assert creds == ("jenkins", "secret")


def test_needs_bearer() -> None:
    """Bearer requirement is detected when token is absent."""
    cfg = ClientConfig(username="u", password="p", install_id="i")
    manager = AuthManager(cfg)
    assert manager.needs_bearer([{"OTBearerAuth": []}, {"BasicAuth": []}])


def test_needs_hmac(auth: AuthManager) -> None:
    """HMAC requirement is detected from security schemes."""
    assert auth.needs_hmac([{"HMACSignature": []}])


def test_sign_body(auth: AuthManager) -> None:
    """Request bodies are signed with HMAC-SHA512 uppercase hex."""
    signature = auth.sign_body(b'{"test": true}')
    assert len(signature) == 128
    assert signature == signature.upper()


def test_sign_body_ai_profile(auth: AuthManager) -> None:
    """AI endpoints use the ai HMAC profile."""
    telemetry = auth.sign_body(b"payload", profile="telemetry")
    ai = auth.sign_body(b"payload", profile="ai")
    assert telemetry != ai


def test_sign_body_override() -> None:
    """A configured hmac_key overrides all profiles."""
    override = bytes.fromhex("cd" * 32)
    manager = AuthManager(ClientConfig(install_id="i", hmac_key=override))
    assert manager.sign_body(b"data", profile="ai") == manager.sign_body(
        b"data", profile="telemetry"
    )


def test_sign_body_unknown_profile() -> None:
    """Unknown HMAC profiles raise OliveTreeAuthError."""
    manager = AuthManager(ClientConfig(install_id="i"))
    with pytest.raises(OliveTreeAuthError):
        manager.sign_body(b"data", profile="missing")


def test_encode_basic() -> None:
    """Basic credentials are base64 encoded."""
    assert AuthManager.encode_basic("user", "pass") == "dXNlcjpwYXNz"
