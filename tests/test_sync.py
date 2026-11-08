"""Sync flow: status, paging, pull, push, lock; and store paging."""

from __future__ import annotations

import json

import httpx

from pyolivetree.constants import STORE, SYNC_PROTOCOL


def status(seq: int, user_id: int = 42) -> httpx.Response:
    return httpx.Response(
        200, json={"customer": {"user_id": user_id, "master_sequence_numbers": {"annotations": seq}}}
    )


def rows(*seqs: int) -> list[dict]:
    return [
        {"id": s, "table_name": "annotations", "sequence_number": s, "deleted": 0, "datum": {}} for s in seqs
    ]


class TestStatus:
    def test_does_not_lock_by_default(self, ot, rec):
        ot.sync.status()
        p = rec.last.url.params
        assert p["do_not_lock"] == "true" and p["device_id"] == "dev-1"
        assert p["sync_client_protocol_version"] == str(SYNC_PROTOCOL) and "managed_data_set" not in p

    def test_lock(self, ot, rec):
        ot.sync.status(lock=True, data_set="annotations")
        p = rec.last.url.params
        assert "do_not_lock" not in p and p["managed_data_set"] == "managed_annotations"


class TestPage:
    def test_params_and_rows(self, ot, rec):
        rec.route("/syncables.json", httpx.Response(200, json={"syncables": rows(1, 2)}))
        assert [r["id"] for r in ot.sync.page("bookshelf", 7)] == [1, 2]
        p = rec.last.url.params
        assert (p["above"], p["managed_data_set"], p["platform_id"]) == ("7", "managed_bookshelf", "26")

    def test_missing_key_is_empty(self, ot, rec):
        rec.route("/syncables.json", httpx.Response(200, json={}))
        assert ot.sync.page() == []


class TestPull:
    def test_pages_until_latest(self, ot, rec):
        rec.route("/status.json", status(9))
        pages = {"0": rows(1, 5), "5": rows(9)}
        rec.route(
            "/syncables.json", lambda r: httpx.Response(200, json={"syncables": pages[r.url.params["above"]]})
        )
        assert [r["sequence_number"] for r in ot.sync.pull()] == [1, 5, 9]
        aboves = [r.url.params["above"] for r in rec.api_requests if r.url.path == "/syncables.json"]
        assert aboves == ["0", "5"]

    def test_nothing_new_makes_no_page_request(self, ot, rec):
        rec.route("/status.json", status(9))
        assert list(ot.sync.pull(above=9)) == []
        assert not any(r.url.path == "/syncables.json" for r in rec.requests)

    def test_unknown_data_set_is_empty(self, ot, rec):
        rec.route("/status.json", status(9))
        assert list(ot.sync.pull("not_a_set")) == []

    def test_stops_on_empty_page(self, ot, rec):
        rec.route("/status.json", status(9))
        rec.route("/syncables.json", httpx.Response(200, json={"syncables": []}))
        assert list(ot.sync.pull()) == []

    def test_stops_when_server_does_not_advance(self, ot, rec):
        rec.route("/status.json", status(9))
        rec.route("/syncables.json", httpx.Response(200, json={"syncables": rows(3)}))
        assert len(list(ot.sync.pull(above=3))) == 1
        assert sum(r.url.path == "/syncables.json" for r in rec.requests) == 1

    def test_is_lazy(self, ot, rec):
        rec.route("/status.json", status(9))
        gen = ot.sync.pull()
        assert rec.requests == []
        rec.route("/syncables.json", httpx.Response(200, json={"syncables": rows(9)}))
        assert next(gen)["id"] == 9


class TestPush:
    def test_body_and_release_lock(self, ot, rec):
        ot.sync.push(
            "annotations",
            {"client_id": 3, "title": "t"},
            item_id=10,
            sequence_number=4,
            deleted=True,
            customer_id=42,
        )
        body = json.loads(rec.last.content)
        assert body["table_name"] == "annotations" and body["managed_data_set"] == "managed_annotations"
        assert (body["id"], body["sequence_number"], body["deleted"], body["customer_id"]) == (10, 4, 1, 42)
        assert body["datum"] == {"client_id": 3, "title": "t"} and body["device_id"] == "dev-1"
        assert rec.last.url.params["release_lock"] == "true"

    def test_defaults_create_new_row(self, ot, rec):
        ot.sync.push("annotations", {}, customer_id=1, release_lock=False)
        body = json.loads(rec.last.content)
        assert (body["id"], body["sequence_number"], body["deleted"]) == (-1, -1, 0)
        assert "release_lock" not in rec.last.url.params

    def test_looks_up_customer_id(self, ot, rec):
        rec.route("/status.json", status(0, user_id=777))
        ot.sync.push("annotations", {}, data_set="library")
        body = json.loads(rec.last.content)
        assert body["customer_id"] == 777 and body["managed_data_set"] == "managed_library"

    def test_release_lock_params(self, ot, rec):
        ot.sync.release_lock("library")
        assert rec.last.url.params["managed_data_set"] == "managed_library"


class TestAllProducts:
    def test_walks_pages(self, ot, rec):
        pages = [f"{STORE}/purchased/{i}" for i in range(3)]
        first = {"product_results": [{"productId": 0}], "pages": pages}
        rec.route("/purchased/1", httpx.Response(200, json={"product_results": [{"productId": 1}]}))
        rec.route("/purchased/2", httpx.Response(200, json={"product_results": []}))
        assert [p["productId"] for p in ot.store.all_products(first)] == [0, 1]
        assert [r.method for r in rec.api_requests] == ["POST", "POST"]

    def test_single_page(self, ot, rec):
        assert list(ot.store.all_products({"product_results": [{"productId": 5}]})) == [{"productId": 5}]
        assert rec.requests == []

    def test_empty(self, ot):
        assert list(ot.store.all_products({})) == []
