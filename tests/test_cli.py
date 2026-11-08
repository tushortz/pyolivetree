"""Command line."""

from __future__ import annotations

import json

import httpx
import pytest

from pyolivetree import OliveTree, backup, cli


@pytest.fixture
def fake_client(monkeypatch, rec):
    """Make the CLI build clients that talk to the mock server."""

    def factory(*a, **kw):
        return OliveTree("u@example.com", "pw", device_id="dev", transport=httpx.MockTransport(rec))

    monkeypatch.setattr(cli, "OliveTree", factory)
    rec.route(
        "/syncables.json",
        httpx.Response(
            200,
            json={
                "syncables": [
                    {
                        "id": 1,
                        "table_name": "annotations",
                        "sequence_number": 1,
                        "deleted": 0,
                        "datum": {
                            "annotation_type_id": 1,
                            "content": "Hi",
                            "book_begin": 43,
                            "chapter_begin": 1,
                            "verse_begin": 1,
                        },
                    }
                ]
            },
        ),
    )
    rec.route(
        "/status.json",
        httpx.Response(200, json={"customer": {"master_sequence_numbers": {"annotations": 1}}}),
    )
    return factory


def test_status(fake_client, capsys):
    cli.main(["status"])
    assert json.loads(capsys.readouterr().out)["customer"]["master_sequence_numbers"]["annotations"] == 1


def test_library_lists_every_product(fake_client, rec, capsys):
    pages = [
        "https://www.olivetree.com/store/br5/app/json/store/purchased/0",
        "https://www.olivetree.com/store/br5/app/json/store/purchased/1",
    ]
    rec.route("/purchased/1", httpx.Response(200, json={"product_results": [{"productId": 2}]}))
    rec.route(
        "/store/purchased", httpx.Response(200, json={"product_results": [{"productId": 1}], "pages": pages})
    )
    cli.main(["library"])
    assert json.loads(capsys.readouterr().out) == [{"productId": 1}, {"productId": 2}]


def test_notes_refresh_flag_syncs_first(fake_client, tmp_path, rec, capsys):
    db = str(tmp_path / "x.db")
    cli.main(["notes", "--db", db, "--refresh"])
    assert "## John 1:1" in capsys.readouterr().out
    assert any(r.url.path == "/syncables.json" for r in rec.requests)


def test_notes_without_backup_shows_error(fake_client, tmp_path, rec, capsys):
    with pytest.raises(SystemExit) as e:
        cli.main(["notes", "--db", str(tmp_path / "missing.db")])
    assert e.value.code == 1
    assert "run backup() first" in capsys.readouterr().err
    assert rec.requests == []


def test_notes_offline_reads_existing_backup(fake_client, tmp_path, rec, capsys):
    db = str(tmp_path / "x.db")
    cli.main(["backup", "--db", db])
    capsys.readouterr()
    n = len(rec.requests)
    cli.main(["notes", "--db", db])
    assert "## John 1:1" in capsys.readouterr().out and len(rec.requests) == n


def test_backup_then_notes(fake_client, tmp_path, capsys):
    db = str(tmp_path / "x.db")
    cli.main(["backup", "--db", db])
    assert json.loads(capsys.readouterr().out)["annotations"] == 1
    out = tmp_path / "notes.md"
    cli.main(["notes", "--db", db, "--out", str(out)])
    assert "## John 1:1" in out.read_text() and "Hi" in out.read_text()


@pytest.mark.parametrize("command", ["highlights", "clips"])
def test_other_exports_print(fake_client, tmp_path, capsys, command):
    db = str(tmp_path / "x.db")
    backup(fake_client(), db)
    cli.main([command, "--db", db])
    assert capsys.readouterr().out.strip() == ""  # only a note exists


def test_rejects_unknown_command():
    with pytest.raises(SystemExit):
        cli.main(["nope"])
