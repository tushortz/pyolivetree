"""Backup to SQLite, reading annotations back, Markdown export, verse references."""

from __future__ import annotations

import json
import sqlite3

import httpx
import pytest

from pyolivetree import annotations, backup, to_markdown, verse_ref
from pyolivetree.notes import ANNOTATION_TYPES, BOOKS


def row(id_, seq, table="annotations", deleted=0, **datum):
    return {
        "id": id_,
        "table_name": table,
        "table_version": 1,
        "sequence_number": seq,
        "deleted": deleted,
        "datum": datum,
    }


NOTE = dict(
    annotation_type_id=1,
    title="Jhn 3:16",
    content="God so loved",
    created_date=1673695338,
    book_begin=43,
    chapter_begin=3,
    verse_begin=16,
    book_end=43,
    chapter_end=3,
    verse_end=17,
)
HIGHLIGHT = dict(
    annotation_type_id=16,
    highlighter_id=1,
    content="In the beginning",
    book_begin=1,
    chapter_begin=1,
    verse_begin=1,
)
CLIP = dict(
    annotation_type_id=256, content="The Lord is my shepherd", book_begin=19, chapter_begin=23, verse_begin=1
)


@pytest.fixture
def server(rec):
    """Sync server with annotations at seq 1..4, then a later change at seq 5."""
    state = {
        "latest": 4,
        "rows": [
            row(1, 1, **NOTE),
            row(2, 2, **HIGHLIGHT),
            row(3, 3, **CLIP),
            row(100, 4, table="highlighters", client_id=1, name="Yellow"),
        ],
    }

    def status(_):
        seqs = {"annotations": state["latest"], "library": 0, "daily_reading": 0, "bookshelf": 0}
        return httpx.Response(200, json={"customer": {"user_id": 42, "master_sequence_numbers": seqs}})

    def page(r):
        above = int(r.url.params["above"])
        return httpx.Response(
            200, json={"syncables": [x for x in state["rows"] if x["sequence_number"] > above]}
        )

    rec.route("/status.json", status)
    rec.route("/syncables.json", page)
    return state


class TestVerseRef:
    @pytest.mark.parametrize(
        ("datum", "expected"),
        [
            ({"book_begin": 43, "chapter_begin": 3, "verse_begin": 16}, "John 3:16"),
            ({**NOTE}, "John 3:16-17"),
            (
                {
                    "book_begin": 19,
                    "chapter_begin": 1,
                    "verse_begin": 1,
                    "book_end": 19,
                    "chapter_end": 2,
                    "verse_end": 3,
                },
                "Psalms 1:1 - 2:3",
            ),
            (
                {
                    "book_begin": 1,
                    "chapter_begin": 1,
                    "verse_begin": 1,
                    "book_end": 1,
                    "chapter_end": 1,
                    "verse_end": 1,
                },
                "Genesis 1:1",
            ),
            ({"book_begin": 66, "chapter_begin": 22, "verse_begin": 21}, "Revelation 22:21"),
            ({"book_begin": 70, "chapter_begin": 1, "verse_begin": 1}, "Book70 1:1"),
            ({"book_begin": 43}, "John ?:?"),
            ({}, ""),
            ({"book_begin": 0}, ""),
        ],
    )
    def test_formats(self, datum, expected):
        assert verse_ref(datum) == expected

    def test_sixty_six_books(self):
        assert len(BOOKS) == 66 and BOOKS[0] == "Genesis" and BOOKS[42] == "John"


class TestBackup:
    def test_writes_rows_and_cursor(self, ot, server, tmp_path):
        db = str(tmp_path / "ot.db")
        assert backup(ot, db) == {"annotations": 4, "library": 0, "daily_reading": 0, "bookshelf": 0}
        con = sqlite3.connect(db)
        assert con.execute("SELECT count(*) FROM syncables").fetchone() == (4,)
        assert dict(con.execute("SELECT data_set, above FROM cursor")) == {
            "annotations": 4,
            "library": 0,
            "daily_reading": 0,
            "bookshelf": 0,
        }
        datum = json.loads(con.execute("SELECT datum FROM syncables WHERE id=1").fetchone()[0])
        assert datum["content"] == "God so loved"

    def test_incremental(self, ot, server, rec, tmp_path):
        db = str(tmp_path / "ot.db")
        backup(ot, db)
        n = len(rec.requests)
        assert backup(ot, db)["annotations"] == 0
        assert not any(r.url.path == "/syncables.json" for r in rec.requests[n:])

        server["rows"].append(row(1, 5, deleted=1))  # note deleted on another device
        server["latest"] = 5
        assert backup(ot, db)["annotations"] == 1
        assert [a["type"] for a in annotations(db, None)] == ["highlight", "clip"]

    def test_only_selected_data_sets(self, ot, server, tmp_path):
        assert backup(ot, str(tmp_path / "ot.db"), data_sets=("annotations",)) == {"annotations": 4}


class TestAnnotations:
    @pytest.fixture
    def db(self, ot, server, tmp_path):
        path = str(tmp_path / "ot.db")
        backup(ot, path)
        return path

    def test_kinds(self, db):
        assert [a["content"] for a in annotations(db, "note")] == ["God so loved"]
        assert [a["content"] for a in annotations(db, "highlight")] == ["In the beginning"]
        assert [a["content"] for a in annotations(db, "clip")] == ["The Lord is my shepherd"]
        assert annotations(db, "unknown") == []

    def test_bible_order_and_extras(self, db):
        items = annotations(db, None)
        assert [a["ref"] for a in items] == ["Genesis 1:1", "Psalms 23:1", "John 3:16-17"]
        assert items[0]["color"] == "Yellow" and items[2]["color"] is None

    def test_unknown_type_id_kept_as_string(self, ot, rec, tmp_path):
        rec.route(
            "/status.json",
            httpx.Response(200, json={"customer": {"master_sequence_numbers": {"annotations": 1}}}),
        )
        rec.route(
            "/syncables.json", httpx.Response(200, json={"syncables": [row(1, 1, annotation_type_id=999)]})
        )
        db = str(tmp_path / "x.db")
        backup(ot, db, data_sets=("annotations",))
        assert annotations(db, None)[0]["type"] == "999"

    def test_type_map(self):
        assert ANNOTATION_TYPES == {1: "note", 16: "highlight", 256: "clip"}


class TestMarkdown:
    def test_groups_by_book(self):
        items = [
            {"type": "highlight", "ref": "Genesis 1:1", "content": "In the beginning ", "color": "Yellow"},
            {
                "type": "note",
                "ref": "John 3:16",
                "title": "Jhn 3:16",
                "content": "Love",
                "created_date": 1673695338,
            },
            {"type": "note", "ref": "John 3:17", "content": ""},
        ]
        md = to_markdown(items)
        headings = [line for line in md.splitlines() if line.startswith("# ")]
        assert headings == ["# Genesis", "# John"]
        assert "## Genesis 1:1\nhighlight · Yellow\n" in md and "In the beginning\n" in md
        assert "*Jhn 3:16* — note · 2023-01-1" in md
        assert "**" not in md

    def test_no_verse(self):
        md = to_markdown([{"type": "note", "ref": "", "title": "Loose note", "content": "x"}])
        assert "# Other" in md and "## Loose note" in md

    def test_empty(self):
        assert to_markdown([]) == ""
