"""Additional tests for full branch coverage."""

from __future__ import annotations

import httpx
import pytest
import respx

from pyolivetree import OliveTreeClient
from pyolivetree._transport.base import (
    OperationSpec,
    _is_binary,
    _is_text,
    encode_body,
    parse_response,
)
from pyolivetree._transport.sync import SyncTransport
from pyolivetree.auth import AuthManager
from pyolivetree.config import ClientConfig


def test_encode_body_default_list() -> None:
    """Lists without content type encode as compact JSON."""
    body, ctype = encode_body(None, [1, 2])
    assert body == b"[1,2]"
    assert ctype == "application/json"


def test_encode_body_unsupported() -> None:
    """Unsupported content types raise TypeError."""
    with pytest.raises(TypeError):
        encode_body("text/plain", {"a": 1})


def test_parse_response_redirect() -> None:
    """302 responses return decoded text."""
    spec = OperationSpec("browser", "get", "/", "s", "Browser")
    assert parse_response("browser", 302, b"redirect", None, spec=spec) == "redirect"


def test_parse_response_empty_body() -> None:
    """Empty successful responses return an empty dict."""
    spec = OperationSpec("op", "get", "/", "s", "t")
    assert parse_response("op", 200, b"", "application/json", spec=spec) == {}


def test_parse_response_invalid_json() -> None:
    """Non-JSON text falls back to string decoding."""
    spec = OperationSpec("op", "get", "/", "s", "t")
    assert parse_response("op", 200, b"plain", "application/json", spec=spec) == "plain"


def test_is_binary_and_text_helpers() -> None:
    """MIME helper functions handle missing and known types."""
    assert _is_binary(None) is False
    assert _is_binary("image/jpeg") is True
    assert _is_text(None) is False
    assert _is_text("application/xml") is True


def test_auth_empty_security_and_install_id() -> None:
    """Auth helpers handle empty security and missing install IDs."""
    manager = AuthManager(ClientConfig(install_id=None))
    assert manager.install_id == ""
    assert manager.auth_headers([]) == {}
    assert manager.basic_auth([]) is None
    assert manager.needs_bearer([]) is False
    assert manager.needs_hmac([]) is False
    manager.set_tokens("access-only")
    assert manager.refresh_token is None


def test_auth_update_without_tokens() -> None:
    """Auth update succeeds when response omits token fields."""
    manager = AuthManager(ClientConfig(install_id="i"))
    manager.update_from_response({"authenticated": True})
    assert manager.access_token is None


@respx.mock
def test_transport_extra_headers() -> None:
    """Extra headers are forwarded to the HTTP client."""
    auth = AuthManager(ClientConfig(install_id="i"), access_token="tok")
    respx.get("https://www.olivetree.com/static/app_assets/timeouts.json").mock(
        return_value=httpx.Response(200, json={"ok": True})
    )
    spec = OperationSpec(
        "static_timeouts",
        "get",
        "/static/app_assets/timeouts.json",
        "timeouts",
        "Static",
    )
    with SyncTransport(auth) as transport:
        transport.request(spec, extra_headers={"X-Test": "1"})
    assert respx.calls[0].request.headers["X-Test"] == "1"


@respx.mock
def test_client_ensure_auth_skips_when_token_present() -> None:
    """ensure_auth is a no-op when a token is already configured."""
    client = OliveTreeClient(username="u", password="p", install_id="i", access_token="tok")
    client.ensure_auth()
    client.close()


def test_models_import() -> None:
    """Generated models module is importable."""
    from pyolivetree.models import AccountAuthResponse, ProductListItem

    assert AccountAuthResponse.__annotations__
    assert ProductListItem.__annotations__
