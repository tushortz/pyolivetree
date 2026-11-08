"""Tests for .env loading, signing helpers and response parsing."""

from __future__ import annotations

import base64
import hashlib
import hmac
import os

import httpx
import pytest

from pyolivetree import OliveTreeAPIError, OliveTreeAuthError, OliveTreeError, sign_body
from pyolivetree._http import load_dotenv, parse_hmac_key, parse_response
from pyolivetree.constants import HMAC_KEYS


def _resp(status: int = 200, **kw) -> httpx.Response:
    return httpx.Response(status, request=httpx.Request("GET", "https://example.com/x"), **kw)


class TestLoadDotenv:
    def test_reads_values_and_strips_quotes(self, tmp_path, monkeypatch):
        monkeypatch.delenv("PYOT_A", raising=False)
        monkeypatch.delenv("PYOT_B", raising=False)
        (tmp_path / ".env").write_text("# comment\nPYOT_A = 'one'\nPYOT_B=\"two=2\"\nnot a pair\n")
        load_dotenv(str(tmp_path / ".env"))
        assert os.environ["PYOT_A"] == "one"
        assert os.environ["PYOT_B"] == "two=2"

    def test_does_not_override_existing(self, tmp_path, monkeypatch):
        monkeypatch.setenv("PYOT_A", "kept")
        (tmp_path / ".env").write_text("PYOT_A=new\n")
        load_dotenv(str(tmp_path / ".env"))
        assert os.environ["PYOT_A"] == "kept"

    def test_missing_file_is_ignored(self, tmp_path):
        load_dotenv(str(tmp_path / "nope.env"))

    def test_commented_assignment_is_skipped(self, tmp_path, monkeypatch):
        monkeypatch.delenv("PYOT_C", raising=False)
        (tmp_path / ".env").write_text("  # PYOT_C=1\n")
        load_dotenv(str(tmp_path / ".env"))
        assert "PYOT_C" not in os.environ


class TestSignBody:
    @pytest.mark.parametrize("profile", sorted(HMAC_KEYS))
    def test_matches_hmac_sha512_upper_hex(self, profile):
        expected = hmac.new(HMAC_KEYS[profile], b"body", hashlib.sha512).hexdigest().upper()
        assert sign_body(b"body", profile) == expected

    def test_key_override(self):
        assert sign_body(b"x", "ai", key=b"k") == hmac.new(b"k", b"x", hashlib.sha512).hexdigest().upper()

    def test_unknown_profile(self):
        with pytest.raises(OliveTreeAuthError, match="Unknown HMAC profile"):
            sign_body(b"x", "nope")

    def test_profiles_have_distinct_keys(self):
        assert len({sign_body(b"x", p) for p in HMAC_KEYS}) == len(HMAC_KEYS)


class TestParseHmacKey:
    def test_hex(self):
        assert parse_hmac_key("0aff") == b"\x0a\xff"

    def test_base64(self):
        assert parse_hmac_key(base64.b64encode(b"secret!").decode()) == b"secret!"

    def test_bytes_pass_through(self):
        assert parse_hmac_key(b"raw") == b"raw"

    @pytest.mark.parametrize("raw", [None, "", b""])
    def test_empty_means_no_override(self, raw):
        assert parse_hmac_key(raw) is None

    def test_invalid(self):
        with pytest.raises(ValueError, match="hex or base64"):
            parse_hmac_key("not valid!!")


class TestParseResponse:
    def test_json_by_content_type(self):
        assert parse_response(_resp(json={"a": 1})) == {"a": 1}

    def test_json_without_content_type(self):
        assert parse_response(_resp(content=b"[1, 2]")) == [1, 2]

    def test_broken_json_falls_back_to_text(self):
        r = _resp(content=b"{oops", headers={"content-type": "application/json"})
        assert parse_response(r) == "{oops"

    @pytest.mark.parametrize("ctype", ["text/html; charset=utf-8", "application/xml", "text/plain"])
    def test_text_types(self, ctype):
        assert parse_response(_resp(content=b"<a/>", headers={"content-type": ctype})) == "<a/>"

    def test_binary(self):
        assert (
            parse_response(_resp(content=b"\xff\xd8", headers={"content-type": "image/jpeg"})) == b"\xff\xd8"
        )

    def test_401_is_auth_error(self):
        with pytest.raises(OliveTreeAuthError) as e:
            parse_response(_resp(401, json={"error": "Invalid Token.", "errorCode": 1018}))
        assert (e.value.status, e.value.code, e.value.status_code) == (401, 1018, 401)
        assert "Invalid Token." in str(e.value)

    def test_authenticated_false_is_auth_error_even_on_200(self):
        with pytest.raises(OliveTreeAuthError) as e:
            parse_response(_resp(json={"authenticated": False, "error": "Login failed", "errorCode": 1000}))
        assert e.value.code == 1000

    def test_other_errors_are_api_errors(self):
        with pytest.raises(OliveTreeAPIError) as e:
            parse_response(_resp(500, content=b"boom", headers={"content-type": "text/plain"}))
        assert e.value.status == 500 and e.value.body == "boom" and e.value.code is None
        assert isinstance(e.value, OliveTreeError)
