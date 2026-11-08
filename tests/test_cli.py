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


def test_library(fake_client, rec, capsys):
    rec.route("/store/purchased", httpx.Response(200, json={"total_count": 0}))
    cli.main(["library"])
    assert json.loads(capsys.readouterr().out) == {"total_count": 0}


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
