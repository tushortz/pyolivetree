"""DataSet enum: every sync method and backup() accept a member, its value, or the server name."""

from __future__ import annotations

import json
import sqlite3

import httpx
import pytest

from pyolivetree import AsyncOliveTree, DataSet, backup
from pyolivetree.constants import DATA_SETS, data_set_name

# Same data set written three ways; all must behave identically.
FORMS = [DataSet.LIBRARY, "library", "managed_library"]
FORM_IDS = ["enum", "str", "managed-str"]


class TestEnum:
    def test_members(self):
        assert [d.value for d in DataSet] == ["annotations", "library", "daily_reading", "bookshelf"]
        assert DATA_SETS == tuple(DataSet)

    def test_is_a_string(self):
        assert DataSet.ANNOTATIONS == "annotations"
        assert isinstance(DataSet.ANNOTATIONS, str)
        assert str(DataSet.DAILY_READING) == f"{DataSet.DAILY_READING}" == "daily_reading"
        assert json.dumps({"ds": DataSet.BOOKSHELF}) == '{"ds": "bookshelf"}'

    def test_lookup_by_value(self):
        assert DataSet("library") is DataSet.LIBRARY
        with pytest.raises(ValueError):
            DataSet("nope")

    @pytest.mark.parametrize(
        ("given", "expected"),
        [
            (DataSet.ANNOTATIONS, "annotations"),
            ("annotations", "annotations"),
            ("managed_annotations", "annotations"),
            (DataSet.DAILY_READING, "daily_reading"),
            ("sync_system_test", "sync_system_test"),  # unknown names pass through
        ],
    )
    def test_data_set_name(self, given, expected):
        assert data_set_name(given) == expected


@pytest.mark.parametrize("ds", FORMS, ids=FORM_IDS)
class TestSyncAcceptsAllForms:
    def test_status(self, ot, rec, ds):
        ot.sync.status(lock=True, data_set=ds)
        assert rec.last.url.params["managed_data_set"] == "managed_library"

    def test_page(self, ot, rec, ds):
        ot.sync.page(ds)
        assert rec.last.url.params["managed_data_set"] == "managed_library"

    def test_pull(self, ot, rec, ds):
        seqs = {"library": 2}
        rec.route(
            "/status.json",
            httpx.Response(200, json={"customer": {"master_sequence_numbers": seqs}}),
        )
        rec.route(
            "/syncables.json",
            httpx.Response(200, json={"syncables": [{"id": 1, "sequence_number": 2}]}),
        )
        assert [r["id"] for r in ot.sync.pull(ds)] == [1]
        assert rec.last.url.params["managed_data_set"] == "managed_library"

    def test_table_schema(self, ot, rec, ds):
        ot.sync.table_schema(ds, "categories", 1)
        assert rec.last.url.path == "/syncables/get_table_schema/managed_library/categories/1.json"

    def test_push(self, ot, rec, ds):
        ot.sync.push("categories", {}, data_set=ds, customer_id=1)
        assert json.loads(rec.last.content)["managed_data_set"] == "managed_library"

    def test_release_lock(self, ot, rec, ds):
        ot.sync.release_lock(ds)
        assert rec.last.url.params["managed_data_set"] == "managed_library"


def test_defaults_are_annotations(ot, rec):
    ot.sync.page()
    assert rec.last.url.params["managed_data_set"] == "managed_annotations"
    ot.sync.release_lock()
    assert rec.last.url.params["managed_data_set"] == "managed_annotations"


@pytest.mark.parametrize("ds", FORMS, ids=FORM_IDS)
def test_backup_accepts_all_forms(ot, rec, tmp_path, ds):
    rec.route(
        "/status.json",
        httpx.Response(200, json={"customer": {"master_sequence_numbers": {"library": 1}}}),
    )
    rec.route(
        "/syncables.json",
        httpx.Response(
            200,
            json={"syncables": [{"id": 7, "table_name": "categories", "sequence_number": 1, "datum": {}}]},
        ),
    )
    db = str(tmp_path / "ot.db")
    counts = backup(ot, db, data_sets=[ds])
    assert counts == {"library": 1}
    assert all(type(k) is str for k in counts)  # plain keys, not enum members
    con = sqlite3.connect(db)
    assert con.execute("SELECT data_set FROM syncables").fetchall() == [("library",)]
    assert con.execute("SELECT data_set, above FROM cursor").fetchall() == [("library", 1)]


def test_backup_mixed_forms_share_one_cursor(ot, rec, tmp_path):
    db = str(tmp_path / "ot.db")
    backup(ot, db, data_sets=[DataSet.BOOKSHELF])
    backup(ot, db, data_sets=["bookshelf"])
    con = sqlite3.connect(db)
    assert con.execute("SELECT count(*) FROM cursor").fetchone() == (1,)


def test_async_accepts_enum(rec):
    import asyncio

    aot = AsyncOliveTree("u@example.com", "pw", device_id="d", transport=httpx.MockTransport(rec))
    asyncio.run(aot.sync.page(DataSet.BOOKSHELF))
    assert rec.last.url.params["managed_data_set"] == "managed_bookshelf"
