"""Tests for transport utilities and HTTP layers."""

from __future__ import annotations

import httpx
import pytest
import respx

from pyolivetree._transport.async_ import AsyncTransport
from pyolivetree._transport.base import (
    OperationSpec,
    build_url,
    encode_body,
    parse_response,
)
from pyolivetree._transport.sync import SyncTransport
from pyolivetree.auth import AuthManager
from pyolivetree.config import ClientConfig
from pyolivetree.exceptions import OliveTreeAPIError


def test_build_url() -> None:
    """Path parameters are substituted into URLs."""
    url = build_url("https://example.com", "/items/{id}", {"id": 42})
    assert url == "https://example.com/items/42"


def test_encode_form_body() -> None:
    """Form bodies are urlencoded."""
    body, ctype = encode_body("application/x-www-form-urlencoded", {"a": "1"})
    assert body == b"a=1"
    assert ctype == "application/x-www-form-urlencoded"


def test_encode_json_body() -> None:
    """JSON bodies are serialized compactly for HMAC compatibility."""
    body, ctype = encode_body("application/json", {"a": 1})
    assert body == b'{"a":1}'
    assert ctype == "application/json"


def test_encode_bytes_body() -> None:
    """Raw bytes pass through unchanged."""
    body, ctype = encode_body("application/octet-stream", b"raw")
    assert body == b"raw"


def test_encode_body_invalid_type() -> None:
    """Invalid payload types raise TypeError."""
    with pytest.raises(TypeError):
        encode_body("application/x-www-form-urlencoded", ["bad"])


def test_parse_response_json() -> None:
    """JSON responses are parsed to dict."""
    spec = OperationSpec("op", "get", "/", "s", "t")
    data = parse_response("op", 200, b'{"ok": true}', "application/json", spec=spec)
    assert data == {"ok": True}


def test_parse_response_binary() -> None:
    """Binary responses return bytes."""
    spec = OperationSpec("op", "get", "/", "s", "t", response_binary=True)
    data = parse_response("op", 200, b"\x89PNG", "image/png", spec=spec)
    assert data == b"\x89PNG"


def test_parse_response_text() -> None:
    """Text responses return strings."""
    spec = OperationSpec("op", "get", "/", "s", "t", response_text=True)
    data = parse_response("op", 200, b"<html/>", "text/html", spec=spec)
    assert data == "<html/>"


def test_parse_response_error() -> None:
    """HTTP errors raise OliveTreeAPIError."""
    spec = OperationSpec("op", "get", "/", "s", "t")
    with pytest.raises(OliveTreeAPIError) as exc:
        parse_response("op", 404, b'{"error":"x"}', "application/json", spec=spec)
    assert exc.value.status_code == 404


@respx.mock
def test_sync_transport_json(auth: AuthManager) -> None:
    """Sync transport performs JSON requests."""
    route = respx.post("https://www.olivetree.com/store/br5/app/json/store/home").mock(
        return_value=httpx.Response(200, json={"rows": []})
    )
    spec = OperationSpec(
        "store_home",
        "post",
        "/store/br5/app/json/store/home",
        "home",
        "Store",
        security=[{"OTBearerAuth": []}],
        content_type="application/x-www-form-urlencoded",
    )
    with SyncTransport(auth) as transport:
        result = transport.request(spec, data={})
    assert result == {"rows": []}
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_async_transport_hmac() -> None:
    """Async transport signs HMAC requests with embedded keys."""
    auth = AuthManager(ClientConfig(install_id="i"))
    route = respx.post("https://analytics.olivetree.com/api/v1/events").mock(
        return_value=httpx.Response(200, json={"ok": True})
    )
    spec = OperationSpec(
        "analytics_events",
        "post",
        "/api/v1/events",
        "events",
        "Analytics",
        security=[{"HMACSignature": []}],
        server_url="https://analytics.olivetree.com",
        content_type="application/json",
    )
    async with AsyncTransport(auth) as transport:
        result = await transport.request(spec, data={"events": []})
    assert result == {"ok": True}
    assert route.calls[0].request.headers["signature"]
    assert route.calls[0].request.headers["signature"].isupper()


@respx.mock
def test_sync_transport_hmac_signs_by_default() -> None:
    """HMAC requests sign automatically using embedded keys."""
    auth = AuthManager(ClientConfig(install_id="i"))
    route = respx.post("https://analytics.olivetree.com/api/v1/events").mock(
        return_value=httpx.Response(200, json={"ok": True})
    )
    spec = OperationSpec(
        "analytics_events",
        "post",
        "/api/v1/events",
        "events",
        "Analytics",
        security=[{"HMACSignature": []}],
        server_url="https://analytics.olivetree.com",
        content_type="application/json",
    )
    with SyncTransport(auth) as transport:
        transport.request(spec, data={"events": []})
    assert route.called
    assert route.calls[0].request.headers["signature"].isupper()


@respx.mock
def test_sync_transport_api_error(auth: AuthManager) -> None:
    """Transport propagates API errors."""
    respx.post("https://www.olivetree.com/store/br5/app/json/store/home").mock(
        return_value=httpx.Response(500, text="fail")
    )
    spec = OperationSpec("store_home", "post", "/store/br5/app/json/store/home", "home", "Store")
    with SyncTransport(auth) as transport, pytest.raises(OliveTreeAPIError):
        transport.request(spec, data={})
