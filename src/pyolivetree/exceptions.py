"""Exceptions raised by pyolivetree.

All of them derive from :class:`OliveTreeError`, so ``except OliveTreeError`` catches everything.
"""

from __future__ import annotations

from typing import Any


class OliveTreeError(Exception):
    """Base error for pyolivetree.

    Attributes:
        status: HTTP status code (0 if no request was made).
        code: Olive Tree ``errorCode`` from the body, if any (e.g. 1018 = invalid token).
        body: Parsed response body, for inspection.
    """

    def __init__(self, message: str, status: int = 0, code: int | None = None, body: Any = None) -> None:
        super().__init__(message)
        self.status, self.code, self.body = status, code, body

    @property
    def status_code(self) -> int:
        """Same as :attr:`status`."""
        return self.status


class OliveTreeAPIError(OliveTreeError):
    """The server returned an HTTP error (status >= 400 other than 401)."""


class OliveTreeAuthError(OliveTreeError):
    """Login failed, credentials are missing, the token was rejected, or signing failed."""
