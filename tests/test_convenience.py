"""Convenience methods: backup, notes, highlights, clips, status, library (sync and async)."""

from __future__ import annotations

import asyncio
import sqlite3

import httpx
import pytest

from pyolivetree import AsyncOliveTree, DataSet, OliveTreeError
from pyolivetree.constants import STORE

NOTE = {
    "annotation_type_id": 1,
    "title": "Jhn 3:16",
    "content": "God so loved",
    "book_begin": 43,
    "chapter_begin": 3,
    "verse_begin": 16,
}
HIGHLIGHT = {
    "annotation_type_id": 16,
    "highlighter_id": 1,
    "content": "In the beginning",
    "book_begin": 1,
    "chapter_begin": 1,
    "verse_begin": 1,
}
CLIP = {
    "annotation_type_id": 256,
    "content": "The Lord is my shepherd",
    "book_begin": 19,
    "chapter_begin": 23,
    "verse_begin": 1,
}


def row(id_, seq, table="annotations", **datum):
    return {"id": id_, "table_name": table, "sequence_number": seq, "deleted": 0, "datum": datum}


@pytest.fixture
def server(rec):
    state = {
        "rows": [
            row(1, 1, **NOTE),
            row(2, 2, **HIGHLIGHT),
            row(3, 3, **CLIP),
            row(9, 4, table="highlighters", client_id=1, name="Yellow"),
        ]
    }

    def status(_):
        latest = max(r["sequence_number"] for r in state["rows"])
        seqs = {"annotations": latest, "library": 0, "daily_reading": 0, "bookshelf": 0}
        return httpx.Response(
            200,
            json={
                "customer": {"user_id": 42, "master_sequence_numbers": seqs},
                "server": {"system_status": "online"},
            },
        )

    def page(r):
        above = int(r.url.params["above"])
        return httpx.Response(
            200, json={"syncables": [x for x in state["rows"] if x["sequence_number"] > above]}
        )

    rec.route("/status.json", status)
    rec.route("/syncables.json", page)
    return state


@pytest.fixture
def db(tmp_path):
    return str(tmp_path / "ot.db")


def pulls(rec):
    return [r for r in rec.requests if r.url.path == "/syncables.json"]


class TestBackup:
    def test_all_data_sets(self, ot, server, db):
        assert ot.backup(db) == {"annotations": 4, "library": 0, "daily_reading": 0, "bookshelf": 0}
        assert sqlite3.connect(db).execute("SELECT count(*) FROM syncables").fetchone() == (4,)

    def test_selected_data_sets(self, ot, server, db):
        assert ot.backup(db, [DataSet.ANNOTATIONS, "library"]) == {"annotations": 4, "library": 0}

    def test_default_db_path(self, ot, server, tmp_path):
        ot.backup()
        assert (tmp_path / "olivetree.db").exists()  # tests run in tmp_path


class TestAnnotationHelpers:
    def test_notes(self, ot, server, db):
        notes = ot.notes(db)
        assert [(n["ref"], n["content"], n["type"]) for n in notes] == [("John 3:16", "God so loved", "note")]

    def test_highlights_have_color(self, ot, server, db):
        hl = ot.highlights(db)
        assert [(h["ref"], h["color"]) for h in hl] == [("Genesis 1:1", "Yellow")]

    def test_clips(self, ot, server, db):
        assert [c["content"] for c in ot.clips(db)] == ["The Lord is my shepherd"]

    def test_refresh_only_syncs_annotations(self, ot, server, rec, db):
        ot.notes(db)
        sets = {r.url.params["managed_data_set"] for r in pulls(rec)}
        assert sets == {"managed_annotations"}

    def test_second_call_is_incremental(self, ot, server, rec, db):
        ot.notes(db)
        n = len(pulls(rec))
        ot.highlights(db)
        assert len(pulls(rec)) == n  # nothing new on the server, so no page fetch

    def test_picks_up_new_and_deleted_rows(self, ot, server, db):
        ot.notes(db)
        server["rows"].append(row(4, 5, **{**NOTE, "content": "Second", "verse_begin": 17}))
        server["rows"].append({**row(1, 6), "deleted": 1})
        assert [n["content"] for n in ot.notes(db)] == ["Second"]

    def test_offline(self, ot, server, rec, db):
        ot.notes(db)
        count = len(rec.requests)
        server["rows"].append(row(5, 7, **NOTE))
        assert len(ot.notes(db, refresh=False)) == 1  # new server row not fetched
        assert len(rec.requests) == count

    def test_offline_without_backup_raises(self, ot, rec, db, tmp_path):
        with pytest.raises(OliveTreeError, match="run backup"):
            ot.notes(db, refresh=False)
        assert rec.requests == [] and not (tmp_path / "ot.db").exists()

    def test_offline_with_non_backup_file_raises(self, ot, tmp_path):
        other = tmp_path / "other.db"
        sqlite3.connect(other).execute("CREATE TABLE t(x)")
        with pytest.raises(OliveTreeError, match="not a pyolivetree backup"):
            ot.highlights(str(other), refresh=False)


class TestStatusAndLibrary:
    def test_status(self, ot, server):
        assert ot.status()["server"]["system_status"] == "online"

    def test_library_walks_pages(self, ot, rec):
        pages = [f"{STORE}/purchased/{i}" for i in range(2)]
        rec.route("/purchased/1", httpx.Response(200, json={"product_results": [{"productId": 2}]}))
        rec.route(
            "/store/purchased",
            httpx.Response(200, json={"product_results": [{"productId": 1}], "pages": pages}),
        )
        assert [p["productId"] for p in ot.library()] == [1, 2]

    def test_library_empty(self, ot, rec):
        rec.route("/store/purchased", httpx.Response(200, json={"total_count": 0}))
        assert ot.library() == []


class TestAsync:
    @pytest.fixture
    def aot(self, rec):
        return AsyncOliveTree("u@example.com", "pw", device_id="d", transport=httpx.MockTransport(rec))

    def test_all_helpers(self, aot, server, rec, db):
        rec.route("/store/purchased", httpx.Response(200, json={"product_results": [{"productId": 1}]}))

        async def main():
            return (
                await aot.backup(db, [DataSet.ANNOTATIONS]),
                await aot.notes(db),
                await aot.highlights(db),
                await aot.clips(db, refresh=False),
                await aot.status(),
                await aot.library(),
            )

        counts, notes, hl, clips, status, library = asyncio.run(main())
        assert counts == {"annotations": 4}
        assert len(notes) == len(hl) == len(clips) == 1
        assert status["server"]["system_status"] == "online" and library == [{"productId": 1}]
