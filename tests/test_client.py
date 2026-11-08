"""Tests for client wrappers."""

from __future__ import annotations

import httpx
import pytest
import respx

from pyolivetree import AsyncOliveTreeClient, OliveTreeAPIError, OliveTreeClient
from pyolivetree.exceptions import OliveTreeAuthError


@respx.mock
def test_client_login_and_store() -> None:
    """Client login caches tokens and calls store endpoints."""
    respx.post("https://www.olivetree.com/store/br5/app/json/account/account_login").mock(
        return_value=httpx.Response(
            200,
            json={"authenticated": True, "authentication_token": "tok", "refresh_token": "ref"},
        )
    )
    respx.post("https://www.olivetree.com/store/br5/app/json/store/home").mock(
        return_value=httpx.Response(200, json={"rows": []})
    )
    client = OliveTreeClient(username="u", password="p", install_id="i")
    with client:
        result = client.store.home()
    assert result == {"rows": []}


@respx.mock
def test_client_login_method() -> None:
    """Explicit login stores tokens."""
    respx.post("https://www.olivetree.com/store/br5/app/json/account/account_login").mock(
        return_value=httpx.Response(
            200,
            json={"authenticated": True, "authentication_token": "tok"},
        )
    )
    client = OliveTreeClient(username="u", password="p", install_id="i")
    data = client.login()
    assert data["authentication_token"] == "tok"
    client.close()


@respx.mock
def test_client_login_auth_failure() -> None:
    """Failed login raises OliveTreeAuthError."""
    respx.post("https://www.olivetree.com/store/br5/app/json/account/account_login").mock(
        return_value=httpx.Response(200, json={"authenticated": False})
    )
    client = OliveTreeClient(username="u", password="p", install_id="i")
    with pytest.raises(OliveTreeAuthError):
        client.login()
    client.close()


@respx.mock
@pytest.mark.asyncio
async def test_async_client_login_and_store() -> None:
    """Async client login and store call work together."""
    respx.post("https://www.olivetree.com/store/br5/app/json/account/account_login").mock(
        return_value=httpx.Response(
            200,
            json={"authenticated": True, "authentication_token": "tok"},
        )
    )
    respx.post("https://www.olivetree.com/store/br5/app/json/store/home").mock(
        return_value=httpx.Response(200, json={"rows": []})
    )
    async with AsyncOliveTreeClient(username="u", password="p", install_id="i") as client:
        await client.login()
        result = await client.store.ahome()
    assert result == {"rows": []}


@respx.mock
def test_client_refresh() -> None:
    """Client refresh updates in-memory tokens."""
    respx.post("https://www.olivetree.com/store/br5/app/json/account/refresh_token").mock(
        return_value=httpx.Response(
            200,
            json={"authenticated": True, "authentication_token": "new-tok"},
        )
    )
    client = OliveTreeClient(install_id="i", access_token="old-tok")
    data = client.refresh()
    assert data["authentication_token"] == "new-tok"
    assert client._auth.access_token == "new-tok"
    client.close()


@respx.mock
@pytest.mark.asyncio
async def test_async_client_refresh() -> None:
    """Async client refresh updates in-memory tokens."""
    respx.post("https://www.olivetree.com/store/br5/app/json/account/refresh_token").mock(
        return_value=httpx.Response(
            200,
            json={"authenticated": True, "authentication_token": "new-tok"},
        )
    )
    client = AsyncOliveTreeClient(install_id="i", access_token="old-tok")
    data = await client.refresh()
    assert data["authentication_token"] == "new-tok"
    assert client._auth.access_token == "new-tok"
    await client.aclose()


@respx.mock
def test_client_context_manager() -> None:
    """Context manager closes the underlying transport."""
    client = OliveTreeClient(username="u", password="p", install_id="i", access_token="tok")
    with client:
        assert client._auth.access_token == "tok"


def test_api_error_attributes() -> None:
    """API errors expose status and operation metadata."""
    err = OliveTreeAPIError("fail", status_code=400, operation_id="store_home", body={"error": "x"})
    assert err.status_code == 400
    assert err.operation_id == "store_home"
    assert err.body == {"error": "x"}
