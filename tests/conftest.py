"""Shared pytest fixtures."""

from __future__ import annotations

import pytest

from pyolivetree.auth import AuthManager
from pyolivetree.config import ClientConfig


@pytest.fixture
def config() -> ClientConfig:
    """Return a test client configuration.

    Returns:
        ClientConfig with sample credentials.
    """
    return ClientConfig(
        username="user@example.com",
        password="secret",
        install_id="install-123",
        timeout=5.0,
    )


@pytest.fixture
def auth(config: ClientConfig) -> AuthManager:
    """Return an auth manager for tests.

    Args:
        config: Test configuration fixture.

    Returns:
        AuthManager instance with sample session tokens.
    """
    return AuthManager(
        config,
        access_token="token-abc",
        refresh_token="refresh-xyz",
    )
