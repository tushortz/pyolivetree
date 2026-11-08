"""Tests for configuration loading."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from pyolivetree.config import ClientConfig, _parse_hmac_key, load_dotenv


def test_load_dotenv(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Environment file values are loaded when not already set."""
    monkeypatch.delenv("OLIVE_TREE_USERNAME", raising=False)
    monkeypatch.delenv("OLIVE_TREE_PASSWORD", raising=False)
    env_file = tmp_path / ".env"
    env_file.write_text('OLIVE_TREE_USERNAME="from-file"\n# comment\nOLIVE_TREE_PASSWORD=pass\n')
    load_dotenv(env_file)
    assert os.environ["OLIVE_TREE_USERNAME"] == "from-file"
    assert os.environ["OLIVE_TREE_PASSWORD"] == "pass"


def test_load_dotenv_missing_file(tmp_path: Path) -> None:
    """Missing .env files are ignored."""
    load_dotenv(tmp_path / "missing.env")


def test_load_dotenv_does_not_override(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Existing environment variables are not overwritten."""
    monkeypatch.setenv("OLIVE_TREE_USERNAME", "existing")
    env_file = tmp_path / ".env"
    env_file.write_text("OLIVE_TREE_USERNAME=new\n")
    load_dotenv(env_file)
    assert os.environ["OLIVE_TREE_USERNAME"] == "existing"


def test_parse_hmac_key_hex() -> None:
    """Hex-encoded HMAC keys are parsed."""
    assert _parse_hmac_key("ab" * 32) == bytes.fromhex("ab" * 32)


def test_parse_hmac_key_base64() -> None:
    """Base64-encoded HMAC keys are parsed."""
    import base64

    raw = b"test-key"
    encoded = base64.b64encode(raw).decode()
    assert _parse_hmac_key(encoded) == raw


def test_parse_hmac_key_bytes() -> None:
    """Raw bytes pass through unchanged."""
    raw = b"key"
    assert _parse_hmac_key(raw) is raw


def test_parse_hmac_key_none() -> None:
    """Empty values return None."""
    assert _parse_hmac_key(None) is None
    assert _parse_hmac_key("") is None


def test_parse_hmac_key_invalid() -> None:
    """Invalid encodings raise ValueError."""
    with pytest.raises(ValueError):
        _parse_hmac_key("not-valid!!!")


def test_client_config_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Configuration reads credential values from the environment."""
    monkeypatch.setenv("OLIVE_TREE_USERNAME", "env-user")
    monkeypatch.setenv("OLIVE_TREE_PASSWORD", "env-pass")
    monkeypatch.setenv("OLIVE_TREE_INSTALL_ID", "env-install")
    monkeypatch.setenv("OLIVE_TREE_HMAC_KEY", "ab" * 32)
    cfg = ClientConfig.from_env()
    assert cfg.username == "env-user"
    assert cfg.password == "env-pass"
    assert cfg.install_id == "env-install"
    assert cfg.get_hmac_key() == bytes.fromhex("ab" * 32)


def test_get_hmac_key_embedded_profiles() -> None:
    """Embedded HMAC profiles resolve without configuration."""
    cfg = ClientConfig(install_id="i")
    assert len(cfg.get_hmac_key("telemetry")) == 64
    assert len(cfg.get_hmac_key("ai")) == 64
    assert cfg.get_hmac_key("telemetry") != cfg.get_hmac_key("ai")


def test_strip_quotes() -> None:
    """Quoted values are stripped when loading dotenv files."""
    from pyolivetree.config import _strip_quotes

    assert _strip_quotes('"value"') == "value"
    assert _strip_quotes("'value'") == "value"


def test_client_config_generates_install_id(monkeypatch: pytest.MonkeyPatch) -> None:
    """Install ID is generated when missing."""
    monkeypatch.delenv("OLIVE_TREE_INSTALL_ID", raising=False)
    cfg = ClientConfig.from_env()
    assert cfg.install_id
    assert len(cfg.install_id) >= 32
