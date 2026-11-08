"""Offline checks: login, paged pull, SQLite, Markdown, HMAC signing, re-login on stale token."""

from urllib.parse import parse_qs

import httpx

from pyolivetree import OliveTree, annotations, backup, sign_body, to_markdown, verse_ref

NOTE = {
    "annotation_type_id": 1,
    "title": "Love",
    "content": "God so loved",
    "created_date": 1673695338,
    "book_begin": 43,
    "chapter_begin": 3,
    "verse_begin": 16,
    "book_end": 43,
    "chapter_end": 3,
    "verse_end": 17,
}
HL = {"annotation_type_id": 16, "highlighter_id": 1, "book_begin": 1, "chapter_begin": 1, "verse_begin": 1}
PAGES = {
    0: [
        {
            "id": 1,
            "table_name": "annotations",
            "table_version": 1,
            "sequence_number": 5,
            "deleted": 0,
            "datum": NOTE,
        }
    ],
    5: [
        {
            "id": 2,
            "table_name": "annotations",
            "table_version": 1,
            "sequence_number": 9,
            "deleted": 0,
            "datum": HL,
        },
        {
            "id": 3,
            "table_name": "highlighters",
            "table_version": 1,
            "sequence_number": 9,
            "deleted": 0,
            "datum": {"client_id": 1, "name": "Yellow"},
        },
    ],
}
seen = []


def handler(req: httpx.Request) -> httpx.Response:
    seen.append(req)
    if req.url.path.endswith("account_login"):
        return httpx.Response(200, json={"authenticated": True, "authentication_token": "T"})
    assert req.headers["OTAuthorization"] == "Bearer T"
    if req.url.path == "/syncables/status.json":
        seqs = {"annotations": 9, "library": 0, "daily_reading": 0, "bookshelf": 0}
        return httpx.Response(200, json={"customer": {"master_sequence_numbers": seqs}})
    if req.url.path == "/syncables.json":
        return httpx.Response(200, json={"syncables": PAGES[int(req.url.params["above"])]})
    raise AssertionError(req.url)


def test_backup_and_export(tmp_path):
    db = str(tmp_path / "ot.db")
    with OliveTree("u", "p", device_id="dev", transport=httpx.MockTransport(handler)) as ot:
        assert backup(ot, db) == {"annotations": 3, "library": 0, "daily_reading": 0, "bookshelf": 0}
        n = len(seen)
        assert backup(ot, db)["annotations"] == 0  # incremental: cursor at 9, no pull requests
        assert not any(r.url.path == "/syncables.json" for r in seen[n:])

    notes = annotations(db, "note")
    assert [x["ref"] for x in notes] == ["John 3:16-17"]
    md = to_markdown(notes)
    assert "# John" in md and "## John 3:16-17" in md and "God so loved" in md
    assert [(x["type"], x["color"]) for x in annotations(db, None)] == [
        ("highlight", "Yellow"),
        ("note", None),
    ]
    assert (
        verse_ref(
            {
                "book_begin": 19,
                "chapter_begin": 1,
                "verse_begin": 1,
                "book_end": 19,
                "chapter_end": 2,
                "verse_end": 3,
            }
        )
        == "Psalms 1:1 - 2:3"
    )
    assert parse_qs(seen[0].content.decode())["pass"] == ["p"]


def test_signing_and_relogin():
    logins, sent = [], []

    def h(req: httpx.Request) -> httpx.Response:
        if req.url.path.endswith("account_login"):
            logins.append(1)
            return httpx.Response(
                200, json={"authenticated": True, "authentication_token": f"T{len(logins)}"}
            )
        sent.append(req)
        if req.headers["OTAuthorization"] == "Bearer T1":  # first token is "expired"
            return httpx.Response(
                401, json={"authenticated": False, "error": "Invalid Token.", "errorCode": 1018}
            )
        return httpx.Response(200, json={"answer": "ok"})

    with OliveTree("u", "p", device_id="dev", transport=httpx.MockTransport(h)) as ot:
        assert ot.ai.query("patience", books=["James"]) == {"answer": "ok"}
    assert len(logins) == 2
    last = sent[-1]
    assert last.content == b'{"query":"patience","filters":{"books":["James"]}}'
    assert last.headers["signature"] == sign_body(last.content, "ai")
    assert len(last.headers["signature"]) == 128 and last.headers["signature"].isupper()


def test_store_adds_app_fields_and_walks_pages():
    def h(req: httpx.Request) -> httpx.Response:
        if req.url.path.endswith("account_login"):
            return httpx.Response(200, json={"authenticated": True, "authentication_token": "T"})
        form = parse_qs(req.content.decode())
        assert form["install_id"] == ["dev"] and form["supportsProductDRM"] == ["1"]
        page = int(req.url.path.rsplit("/", 1)[-1]) if req.url.path[-1].isdigit() else 0
        return httpx.Response(
            200,
            json={
                "product_results": [{"productId": page}],
                "pages": [
                    f"https://www.olivetree.com/store/br5/app/json/store/purchased/{i}" for i in range(3)
                ],
            },
        )

    with OliveTree("u", "p", device_id="dev", transport=httpx.MockTransport(h)) as ot:
        assert [p["productId"] for p in ot.store.all_products(ot.store.purchased())] == [0, 1, 2]
