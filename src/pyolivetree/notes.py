"""Back up your sync data to SQLite and export notes and highlights as Markdown.

The backup is a plain SQLite file with one table, ``syncables``, holding every synced row
(``data_set``, ``table_name``, ``id``, ``sequence_number``, ``deleted``, ``datum`` as JSON),
plus a ``cursor`` table so later runs only fetch changes.
"""

from __future__ import annotations

import datetime as dt
import json
import sqlite3
from collections.abc import Iterable
from typing import Any

from pyolivetree.client import OliveTree
from pyolivetree.constants import DATA_SETS, DataSet, data_set_name

# annotation_type_id is a bit flag on the server. NOTE: mapped from a real account's data
# (1 = typed note text, 16 = has highlighter_id, 256 = copied verse text); other bits may exist.
#: ``annotation_type_id`` -> kind name.
ANNOTATION_TYPES = {1: "note", 16: "highlight", 256: "clip"}
#: Book names in canonical order; ``book_begin`` is a 1-based index into this.
BOOKS = (
    "Genesis Exodus Leviticus Numbers Deuteronomy Joshua Judges Ruth 1Samuel 2Samuel 1Kings "
    "2Kings 1Chronicles 2Chronicles Ezra Nehemiah Esther Job Psalms Proverbs Ecclesiastes "
    "SongOfSolomon Isaiah Jeremiah Lamentations Ezekiel Daniel Hosea Joel Amos Obadiah Jonah "
    "Micah Nahum Habakkuk Zephaniah Haggai Zechariah Malachi Matthew Mark Luke John Acts Romans "
    "1Corinthians 2Corinthians Galatians Ephesians Philippians Colossians 1Thessalonians "
    "2Thessalonians 1Timothy 2Timothy Titus Philemon Hebrews James 1Peter 2Peter 1John 2John "
    "3John Jude Revelation"
).split()


def verse_ref(d: dict[str, Any]) -> str:
    """Format a row's verse range.

    Args:
        d: A ``datum`` with ``book_begin``/``chapter_begin``/``verse_begin`` (and optional ``_end``).

    Returns:
        e.g. ``"John 3:16-18"`` or ``"Psalms 1:1 - 2:3"``; ``""`` if there is no book.
    """
    b = d.get("book_begin")
    if not b:
        return ""
    name = BOOKS[b - 1] if 0 < b <= len(BOOKS) else f"Book{b}"
    ref = f"{name} {d.get('chapter_begin', '?')}:{d.get('verse_begin', '?')}"
    end = (d.get("book_end"), d.get("chapter_end"), d.get("verse_end"))
    if end[2] and end != (b, d.get("chapter_begin"), d.get("verse_begin")):
        ref += f"-{end[2]}" if end[:2] == (b, d.get("chapter_begin")) else f" - {end[1]}:{end[2]}"
    return ref


def backup(
    ot: OliveTree, db_path: str = "olivetree.db", data_sets: Iterable[DataSet | str] = DATA_SETS
) -> dict[str, int]:
    """Mirror your sync data into a SQLite file, fetching only what changed since the last run.

    Args:
        ot: A client.
        db_path: SQLite file to create or update.
        data_sets: Data sets to back up (:class:`~pyolivetree.DataSet` members or names).

    Returns:
        Rows fetched per data set, e.g. ``{"annotations": 12, "library": 0, ...}``.
    """
    db = sqlite3.connect(db_path)
    db.executescript("""CREATE TABLE IF NOT EXISTS syncables(
             data_set TEXT, table_name TEXT, id INTEGER, sequence_number INTEGER,
             table_version INTEGER, deleted INTEGER, datum TEXT,
             PRIMARY KEY(table_name, id));
           CREATE TABLE IF NOT EXISTS cursor(data_set TEXT PRIMARY KEY, above INTEGER);""")
    counts = {}
    try:
        for ds in map(data_set_name, data_sets):
            row = db.execute("SELECT above FROM cursor WHERE data_set=?", (ds,)).fetchone()
            above, n = (row[0] if row else 0), 0
            for item in ot.sync.pull(ds, above):
                seq = int(item["sequence_number"])
                db.execute(
                    "INSERT OR REPLACE INTO syncables VALUES(?,?,?,?,?,?,?)",
                    (
                        ds,
                        item["table_name"],
                        int(item["id"]),
                        seq,
                        item.get("table_version"),
                        int(item.get("deleted") or 0),
                        json.dumps(item.get("datum") or {}),
                    ),
                )
                above, n = max(above, seq), n + 1
            # Commit per data set so an interrupted run keeps what it already downloaded.
            db.execute("INSERT OR REPLACE INTO cursor VALUES(?,?)", (ds, above))
            db.commit()
            counts[ds] = n
    finally:
        db.close()
    return counts


def annotations(db_path: str = "olivetree.db", kind: str | None = "note") -> list[dict[str, Any]]:
    """Read annotations from a backup, in Bible order. Deleted rows are skipped.

    Args:
        db_path: SQLite file made by :func:`backup`.
        kind: ``"note"``, ``"highlight"``, ``"clip"``, or ``None`` for all.

    Returns:
        Each row's ``datum`` plus ``type``, ``ref`` (see :func:`verse_ref`) and ``color``
        (highlighter name). Text is in ``content``, the verse label in ``title``.
    """
    db = sqlite3.connect(db_path)
    try:
        rows = db.execute(
            "SELECT datum FROM syncables WHERE table_name='annotations' AND deleted=0"
            " ORDER BY json_extract(datum,'$.book_begin'), json_extract(datum,'$.chapter_begin'),"
            " json_extract(datum,'$.verse_begin'), json_extract(datum,'$.created_date')"
        ).fetchall()
        colors = dict(
            db.execute(
                "SELECT json_extract(datum,'$.client_id'), json_extract(datum,'$.name')"
                " FROM syncables WHERE table_name='highlighters'"
            ).fetchall()
        )
    finally:
        db.close()
    out = []
    for (datum,) in rows:
        d = json.loads(datum)
        kind_of = ANNOTATION_TYPES.get(d.get("annotation_type_id"), str(d.get("annotation_type_id")))
        if kind is None or kind_of == kind:
            out.append(
                {
                    **d,
                    "type": kind_of,
                    "ref": verse_ref(d),
                    "color": colors.get(d.get("highlighter_id")),
                }
            )
    return out


def to_markdown(items: list[dict[str, Any]]) -> str:
    """Render annotations as Markdown, one ``#`` section per Bible book.

    Args:
        items: Output of :func:`annotations`.
    """
    parts, book = [], None
    for it in items:
        b = it["ref"].split(" ")[0] or "Other"
        if b != book:
            book = b
            parts.append(f"# {book}\n")
        when = dt.datetime.fromtimestamp(it["created_date"]).date() if it.get("created_date") else ""
        meta = " · ".join(str(x) for x in (it["type"], it.get("color"), when) if x)
        title = f"*{it['title']}* — " if it.get("title") else ""
        parts.append(f"## {it['ref'] or it.get('title') or 'Untitled'}\n{title}{meta}\n")
        parts.append((it.get("content") or "").strip() + "\n")
    return "\n".join(parts)
