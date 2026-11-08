"""Tests for OliveTree: configuration, auth, request building, retries."""

from __future__ import annotations

import base64
import json
from urllib.parse import parse_qs

import httpx
import pytest

from pyolivetree import OliveTree, OliveTreeAPIError, OliveTreeAuthError, OliveTreeClient, sign_body
from pyolivetree.constants import STORE, WWW


def make(rec, **kw) -> OliveTree:
    kw.setdefault("device_id", "dev-1")
    return OliveTree("u@example.com", "pw", transport=httpx.MockTransport(rec), **kw)


class TestConfig:
    def test_reads_env_and_dotenv(self, tmp_path, monkeypatch):
        (tmp_path / ".env").write_text("OLIVE_TREE_USERNAME=env@example.com\nOLIVE_TREE_PASSWORD=secret\n")
        monkeypatch.setenv("OLIVE_TREE_INSTALL_ID", "inst-9")
        ot = OliveTree()
        assert (ot.username, ot.password, ot.device_id) == ("env@example.com", "secret", "inst-9")

    def test_arguments_win_over_env(self, monkeypatch):
        monkeypatch.setenv("OLIVE_TREE_USERNAME", "env@example.com")
        assert OliveTree("arg@example.com", "pw").username == "arg@example.com"

    def test_generates_device_id(self):
        a, b = OliveTree("u", "p"), OliveTree("u", "p")
        assert a.device_id and a.device_id != b.device_id

    def test_install_id_alias(self):
        assert OliveTree("u", "p", install_id="legacy").device_id == "legacy"

    def test_app_fields_use_device_id(self):
        ot = OliveTree("u", "p", device_id="d")
        assert ot.app_fields["install_id"] == ot.app_fields["platudid"] == "d"

    def test_hmac_key_from_env(self, monkeypatch):
        monkeypatch.setenv("OLIVE_TREE_HMAC_KEY", "abcd")
        assert OliveTree("u", "p").hmac_key == b"\xab\xcd"

    def test_hmac_key_argument(self):
        assert OliveTree("u", "p", hmac_key=base64.b64encode(b"k").decode()).hmac_key == b"k"

    def test_legacy_alias(self):
        assert OliveTreeClient is OliveTree

    def test_groups_present(self):
        ot = OliveTree("u", "p")
        for name in (
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
        ):
            assert getattr(ot, name)._c is ot

    def test_context_manager_closes(self, rec):
        with make(rec) as ot:
            pass
        assert ot.http.is_closed


class TestAuth:
    def test_login_stores_tokens(self, ot, rec):
        data = ot.login()
        assert data["user_id"] == 42
        assert (ot.token, ot.refresh_token) == ("tok-1", "ref-1")
        form = parse_qs(rec.requests[0].content.decode())
        assert form["user"] == ["user@example.com"] and form["pass"] == ["pw"]
        assert form["install_id"] == ["dev-1"] and form["supportsAccessToken"] == ["1"]
        assert "OTAuthorization" not in rec.requests[0].headers

    def test_login_without_credentials(self, rec):
        ot = OliveTree(transport=httpx.MockTransport(rec))
        with pytest.raises(OliveTreeAuthError, match="OLIVE_TREE_USERNAME"):
            ot.login()
        assert rec.requests == []

    def test_failed_login_raises(self, ot, rec):
        rec.route("/account_login", httpx.Response(200, json={"authenticated": False, "errorCode": 1000}))
        with pytest.raises(OliveTreeAuthError):
            ot.login()
        assert ot.token is None

    def test_auto_login_once(self, ot, rec):
        ot.store.home()
        ot.store.banner()
        assert rec.logins == 1
        assert all(r.headers["OTAuthorization"] == "Bearer tok-1" for r in rec.api_requests)

    def test_existing_token_skips_login(self, rec):
        ot = make(rec, token="given")
        ot.sync.status()
        assert rec.logins == 0 and rec.last.headers["OTAuthorization"] == "Bearer given"

    def test_ensure_auth(self, ot, rec):
        ot.ensure_auth()
        ot.ensure_auth()
        assert rec.logins == 1

    def test_refresh_uses_refresh_token(self, ot, rec):
        ot.login()
        rec.route(
            "/refresh_token",
            httpx.Response(200, json={"authentication_token": "tok-2", "refresh_token": "ref-2"}),
        )
        ot.refresh()
        assert rec.last.headers["OTAuthorization"] == "Bearer ref-1"
        assert (ot.token, ot.refresh_token) == ("tok-2", "ref-2")

    @pytest.mark.parametrize(
        "body",
        [
            {"authenticated": False, "error": "Invalid Token.", "errorCode": 1018},
            {"authenticated": False, "error": "Access Token required", "errorCode": 1020},
        ],
    )
    def test_relogin_and_retry_on_token_error(self, rec, body):
        ot = make(rec, token="stale")
        rec.route(
            "/syncables/status.json",
            lambda r: (
                httpx.Response(401, json=body)
                if r.headers["OTAuthorization"] == "Bearer stale"
                else httpx.Response(200, json={"ok": 1})
            ),
        )
        assert ot.sync.status() == {"ok": 1}
        assert rec.logins == 1 and ot.token == "tok-1"

    def test_gives_up_after_one_retry(self, ot, rec):
        rec.route("/store/home", httpx.Response(401, json={"errorCode": 1018}))
        with pytest.raises(OliveTreeAuthError):
            ot.store.home()
        assert len(rec.api_requests) == 2 and rec.logins == 2

    def test_no_retry_for_unauthenticated_calls(self, ot, rec):
        rec.route("/eula", httpx.Response(401, text="no"))
        with pytest.raises(OliveTreeAuthError):
            ot.web.eula()
        assert rec.logins == 0 and len(rec.api_requests) == 1

    def test_no_retry_for_other_errors(self, ot, rec):
        rec.route("/store/home", httpx.Response(500, json={"error": "down"}))
        with pytest.raises(OliveTreeAPIError):
            ot.store.home()
        assert len(rec.api_requests) == 1


class TestRequest:
    def test_drops_none_params_and_data(self, ot, rec):
        ot.request(
            "POST", "https://example.com/x", params={"a": 1, "b": None}, data={"c": None, "d": 2}, auth=False
        )
        assert dict(rec.last.url.params) == {"a": "1"}
        assert parse_qs(rec.last.content.decode()) == {"d": ["2"]}

    def test_app_fields_only_on_store_and_account(self, ot, rec):
        ot.request("POST", f"{STORE}/home", data={"extra": "x"})
        form = parse_qs(rec.last.content.decode())
        assert form["supportsProductDRM"] == ["1"] and form["platform"] == ["26"] and form["extra"] == ["x"]
        ot.request("POST", f"{WWW}/api/recommended.php", data={"extra": "x"}, auth=False)
        assert parse_qs(rec.last.content.decode()) == {"extra": ["x"]}

    def test_caller_data_overrides_app_fields(self, ot, rec):
        ot.request("POST", f"{STORE}/home", data={"language": "fr"})
        assert parse_qs(rec.last.content.decode())["language"] == ["fr"]

    def test_json_body_is_compact(self, ot, rec):
        ot.request("POST", "https://example.com/j", json={"a": [1, 2], "b": "c"}, auth=False)
        assert rec.last.content == b'{"a":[1,2],"b":"c"}'
        assert rec.last.headers["Content-Type"] == "application/json"

    def test_json_not_mixed_with_app_fields(self, ot, rec):
        ot.request("POST", f"{STORE}/x", json={"a": 1})
        assert json.loads(rec.last.content) == {"a": 1}

    def test_signature(self, ot, rec):
        ot.request("POST", "https://example.com/s", json={"q": 1}, sign="ai", auth=False)
        assert rec.last.headers["signature"] == sign_body(b'{"q":1}', "ai")

    def test_signature_empty_body(self, ot, rec):
        ot.request("GET", "https://example.com/s", sign="telemetry", auth=False)
        assert rec.last.headers["signature"] == sign_body(b"", "telemetry")

    def test_signature_with_override_key(self, rec):
        ot = make(rec, hmac_key=b"override")
        ot.request("POST", "https://example.com/s", json={}, sign="ai", auth=False)
        assert rec.last.headers["signature"] == sign_body(b"{}", key=b"override")

    def test_basic_auth(self, ot, rec):
        ot.request("GET", "https://example.com/b", auth=False, basic=True)
        expected = "Basic " + base64.b64encode(b"user@example.com:pw").decode()
        assert rec.last.headers["Authorization"] == expected

    def test_extra_headers(self, ot, rec):
        ot.request("GET", "https://example.com/h", headers={"X-Test": "1"}, auth=False)
        assert rec.last.headers["X-Test"] == "1"

    def test_auth_false_sends_no_token(self, ot, rec):
        ot.request("GET", "https://example.com/n", auth=False)
        assert "OTAuthorization" not in rec.last.headers and rec.logins == 0
