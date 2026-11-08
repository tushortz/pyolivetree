"""Shared fixtures: an OliveTree client wired to a recording mock transport."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import httpx
import pytest

from pyolivetree import OliveTree

LOGIN = {
    "authenticated": True,
    "user_id": 42,
    "authentication_token": "tok-1",
    "expires": 1,
    "refresh_token": "ref-1",
}
STATUS = {
    "customer": {
        "user_id": 42,
        "master_sequence_numbers": {"annotations": 0, "library": 0, "daily_reading": 0, "bookshelf": 0},
    },
    "server": {"system_status": "online"},
}


class Recorder:
    """Mock HTTP server. Records requests and answers from registered routes (first match wins)."""

    def __init__(self) -> None:
        self.requests: list[httpx.Request] = []
        self.routes: list[tuple[Callable[[httpx.Request], bool], Any]] = []
        self.logins = 0

    def route(self, path: str, response: Any) -> None:
        """Answer requests whose URL path ends with ``path``. ``response`` may be a callable."""
        self.routes.append((lambda r: r.url.path.endswith(path), response))

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        for match, response in self.routes:
            if match(request):
                return response(request) if callable(response) else response
        if request.url.path.endswith("/account_login"):
            self.logins += 1
            return httpx.Response(200, json=LOGIN)
        if request.url.path == "/syncables/status.json":
            return httpx.Response(200, json=STATUS)
        return httpx.Response(200, json={"ok": True})

    @property
    def api_requests(self) -> list[httpx.Request]:
        """Requests other than login."""
        return [r for r in self.requests if not r.url.path.endswith("/account_login")]

    @property
    def last(self) -> httpx.Request:
        return self.api_requests[-1]


@pytest.fixture(autouse=True)
def isolated_env(tmp_path, monkeypatch):
    """Run every test in an empty folder with no OLIVE_TREE_* variables, so a real .env is never read."""
    monkeypatch.chdir(tmp_path)
    for key in ("OLIVE_TREE_USERNAME", "OLIVE_TREE_PASSWORD", "OLIVE_TREE_INSTALL_ID", "OLIVE_TREE_HMAC_KEY"):
        monkeypatch.delenv(key, raising=False)


@pytest.fixture
def rec() -> Recorder:
    return Recorder()


@pytest.fixture
def ot(rec: Recorder):
    client = OliveTree("user@example.com", "pw", device_id="dev-1", transport=httpx.MockTransport(rec))
    yield client
    client.close()
