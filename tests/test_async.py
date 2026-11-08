"""AsyncOliveTree: same API with await."""

from __future__ import annotations

import asyncio

import httpx
import pytest

from pyolivetree import AsyncOliveTree, AsyncOliveTreeClient, OliveTreeAPIError
from pyolivetree.async_client import GROUPS


def run(coro):
    return asyncio.run(coro)


@pytest.fixture
def aot(rec):
    return AsyncOliveTree("u@example.com", "pw", device_id="dev-1", transport=httpx.MockTransport(rec))


def test_alias():
    assert AsyncOliveTreeClient is AsyncOliveTree


def test_groups_match_sync_client(aot):
    assert set(GROUPS) == {
        "account",
        "store",
        "products",
        "sync",
        "ai",
        "reading",
        "media",
        "messages",
        "telemetry",
        "web",
        "firebase",
    }
    for name in GROUPS:
        assert getattr(aot, name)._group is getattr(aot.client, name)


def test_method_call(aot, rec):
    async def main():
        async with aot as ot:
            return await ot.store.home()

    assert run(main()) == {"ok": True}
    assert rec.last.url.path.endswith("/store/home") and aot.client.http.is_closed


def test_legacy_a_prefix(aot, rec):
    run(aot.store.ahome())
    run(aot.store.asearch(q="faith"))
    assert rec.last.url.params["q"] == "faith"


def test_name_starting_with_a_is_not_stripped(aot, rec):
    run(aot.store.ads())
    assert rec.last.url.path.endswith("/store/ads")


def test_generators_become_lists(aot, rec):
    rec.route(
        "/status.json",
        httpx.Response(200, json={"customer": {"master_sequence_numbers": {"annotations": 1}}}),
    )
    rec.route("/syncables.json", httpx.Response(200, json={"syncables": [{"id": 1, "sequence_number": 1}]}))
    assert run(aot.sync.pull()) == [{"id": 1, "sequence_number": 1}]
    assert run(aot.store.all_products({"product_results": [1]})) == [1]


def test_concurrent_calls(aot, rec):
    async def main():
        return await asyncio.gather(*(aot.web.timeouts() for _ in range(5)))

    assert len(run(main())) == 5


def test_login_refresh_request(aot, rec):
    run(aot.login())
    assert aot.token == "tok-1"
    rec.route("/refresh_token", httpx.Response(200, json={"authentication_token": "tok-2"}))
    run(aot.refresh())
    assert aot.token == "tok-2"
    assert run(aot.request("GET", "https://example.com/x", auth=False)) == {"ok": True}


def test_ensure_auth(aot, rec):
    run(aot.ensure_auth())
    run(aot.ensure_auth())
    assert rec.logins == 1


def test_attribute_passthrough(aot):
    assert aot.device_id == "dev-1" and aot.app_fields["install_id"] == "dev-1"
    assert aot.store.__class__.__name__ == "AsyncGroup"


def test_errors_propagate(aot, rec):
    rec.route("/eula", httpx.Response(500, text="down"))
    with pytest.raises(OliveTreeAPIError):
        run(aot.web.eula())


def test_unknown_method(aot):
    with pytest.raises(AttributeError):
        aot.store.does_not_exist  # noqa: B018
    with pytest.raises(AttributeError):
        aot.store.anything_else  # noqa: B018


def test_non_callable_attribute_passthrough(aot):
    assert aot.store._c is aot.client
