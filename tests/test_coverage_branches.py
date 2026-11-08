"""Branch coverage for generated resources and async transport."""

from __future__ import annotations

import httpx
import pytest
import respx

from pyolivetree import AsyncOliveTreeClient, OliveTreeClient
from pyolivetree._operations import OPERATIONS
from pyolivetree._transport.async_ import AsyncTransport
from pyolivetree._transport.base import OperationSpec
from pyolivetree.auth import AuthManager
from pyolivetree.config import ClientConfig
from tests.operation_registry import OPERATION_CALLS


def test_basic_auth_branches() -> None:
    """Basic auth returns None when credentials are missing on non-sync hosts."""
    with_token = AuthManager(
        ClientConfig(username="u", password="p", install_id="i"),
        access_token="tok",
    )
    assert with_token.basic_auth([{"BasicAuth": []}]) is None
    no_creds = AuthManager(ClientConfig(install_id="i"))
    assert no_creds.basic_auth([{"BasicAuth": []}]) is None
    assert no_creds.basic_auth([{"JenkinsBasicAuth": []}]) is None


def test_client_ensure_auth_without_credentials() -> None:
    """ensure_auth does nothing when credentials are absent."""
    client = OliveTreeClient(config=ClientConfig(install_id="only-install"))
    client.ensure_auth()
    client.close()


@pytest.mark.asyncio
async def test_async_ensure_auth_without_credentials() -> None:
    """Async ensure_auth does nothing when credentials are absent."""
    client = AsyncOliveTreeClient(config=ClientConfig(install_id="only-install"))
    await client.ensure_auth()
    await client.aclose()


@respx.mock
@pytest.mark.asyncio
async def test_async_transport_extra_headers() -> None:
    """Async transport forwards extra headers."""
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
    async with AsyncTransport(auth) as transport:
        await transport.request(spec, extra_headers={"X-Async": "1"})
    assert respx.calls[0].request.headers["X-Async"] == "1"


@pytest.mark.parametrize(
    "module,method,operation_id,kwargs",
    [
        (module, method, operation_id, {k: v for k, v in kwargs.items() if k != "data"})
        for module, method, operation_id, kwargs in OPERATION_CALLS
        if "data" in kwargs and kwargs["data"] != {}
    ],
)
@respx.mock
def test_sync_without_extra_data(module: str, method: str, operation_id: str, kwargs: dict) -> None:
    """Body merge branch is skipped when data is omitted."""
    from tests.test_operations import _mock_response, _url_pattern

    spec = OPERATIONS[operation_id]
    respx.route(method=spec.method.upper(), url__regex=_url_pattern(spec)).mock(
        return_value=_mock_response(operation_id)
    )
    client = OliveTreeClient(
        username="u",
        password="p",
        install_id="i",
        access_token="tok",
    )
    getattr(getattr(client, module), method)(**kwargs)
    client.close()


@pytest.mark.parametrize(
    "module,method,operation_id,kwargs",
    [
        (module, method, operation_id, {k: v for k, v in kwargs.items() if k != "data"})
        for module, method, operation_id, kwargs in OPERATION_CALLS
        if kwargs.get("data") == {}
    ],
)
@respx.mock
def test_sync_empty_form_without_data(
    module: str, method: str, operation_id: str, kwargs: dict
) -> None:
    """Empty form endpoints work when data defaults to None."""
    from tests.test_operations import _mock_response, _url_pattern

    spec = OPERATIONS[operation_id]
    respx.route(method=spec.method.upper(), url__regex=_url_pattern(spec)).mock(
        return_value=_mock_response(operation_id)
    )
    client = OliveTreeClient(
        username="u",
        password="p",
        install_id="i",
        access_token="tok",
    )
    getattr(getattr(client, module), method)(**kwargs)
    client.close()
