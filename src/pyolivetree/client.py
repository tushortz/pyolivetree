"""The :class:`OliveTree` client: auth, request signing and endpoint groups."""

from __future__ import annotations

import json as jsonlib
import os
import platform
import uuid
from collections.abc import Iterable
from typing import Any

import httpx

from pyolivetree import notes as _notes
from pyolivetree._http import load_dotenv, parse_hmac_key, parse_response, sign_body
from pyolivetree.constants import DATA_SETS, PLATFORM_ID, TOKEN_ERRORS, WWW, DataSet
from pyolivetree.exceptions import OliveTreeAuthError, OliveTreeError
from pyolivetree.resources import (
    AI,
    Account,
    Firebase,
    Media,
    Messages,
    Products,
    Reading,
    Store,
    Sync,
    Telemetry,
    Web,
)


class OliveTree:
    """Client for the Olive Tree Bible app APIs.

    Endpoints are grouped as attributes: :attr:`account`, :attr:`store`, :attr:`products`,
    :attr:`sync`, :attr:`ai`, :attr:`reading`, :attr:`media`, :attr:`messages`,
    :attr:`telemetry`, :attr:`web` and :attr:`firebase`. The client logs in on the
    first call that needs it. :class:`AsyncOliveTree` offers the same API with ``await``.

    Convenience methods cover the common jobs: :meth:`backup`, :meth:`notes`,
    :meth:`highlights`, :meth:`clips`, :meth:`status` and :meth:`library`.

    Example:
        >>> with OliveTree() as ot:                       # doctest: +SKIP
        ...     notes = list(ot.sync.pull("annotations"))
        ...     owned = list(ot.store.all_products(ot.store.purchased()))

    Args:
        username: Olive Tree email. Defaults to ``OLIVE_TREE_USERNAME`` (env or ``.env``).
        password: Password. Defaults to ``OLIVE_TREE_PASSWORD``.
        device_id: Install id sent to the server. Defaults to ``OLIVE_TREE_INSTALL_ID`` or a new UUID.
        install_id: Same as ``device_id`` (1.x name).
        token: An existing ``authentication_token`` to reuse instead of logging in.
        hmac_key: Signing key (hex, base64 or bytes) used for every signed endpoint instead of the
            built-in per-service keys. Defaults to ``OLIVE_TREE_HMAC_KEY``.
        transport: Custom :mod:`httpx` transport (e.g. :class:`httpx.MockTransport` in tests).
        timeout: Request timeout in seconds.
    """

    def __init__(
        self,
        username: str | None = None,
        password: str | None = None,
        *,
        device_id: str | None = None,
        install_id: str | None = None,
        token: str | None = None,
        hmac_key: str | bytes | None = None,
        transport: httpx.BaseTransport | None = None,
        timeout: float = 300,
    ) -> None:
        load_dotenv()
        self.username = username or os.environ.get("OLIVE_TREE_USERNAME", "")
        self.password = password or os.environ.get("OLIVE_TREE_PASSWORD", "")
        self.device_id = (
            device_id or install_id or os.environ.get("OLIVE_TREE_INSTALL_ID") or str(uuid.uuid4())
        )
        #: Current access token (``authentication_token``), or ``None`` before login.
        self.token: str | None = token
        #: Refresh token from the last login, used by :meth:`refresh`.
        self.refresh_token: str | None = None
        #: Signing key override, or ``None`` to use the built-in per-service keys.
        self.hmac_key: bytes | None = parse_hmac_key(
            hmac_key if hmac_key is not None else os.environ.get("OLIVE_TREE_HMAC_KEY")
        )
        self.reader_version = f"pyolivetree_OS_{platform.release()}"
        #: Standard client fields sent with every store/account form post.
        #: Without them some endpoints, e.g. ``store.purchased``, return empty results.
        self.app_fields: dict[str, Any] = {
            "platform": PLATFORM_ID,
            "platudid": self.device_id,
            "OS": "14",
            "language": "en",
            "install_id": self.device_id,
            "supportsAccessToken": 1,
            "ReaderVersion": "7.20",
            "model": "pyolivetree",
            "supportsOtPub": 1,
            "supportsProductDRM": 1,
            "supportsAudio": 1,
            "supportsSubscription": 1,
            "supportsBookSets": 1,
        }
        self.http = httpx.Client(
            timeout=timeout,
            transport=transport,
            follow_redirects=True,
            headers={"Accept": "application/json, */*"},
        )

        self.account = Account(self)  #: Login, tokens, signup, subscriptions.
        self.store = Store(self)  #: Catalog, search, purchases, wishlists.
        self.products = Products(self)  #: XML product info and download links.
        self.sync = Sync(self)  #: Notes, highlights, library and reading-plan data.
        self.ai = AI(self)  #: Smart Search AI.
        self.reading = Reading(self)  #: Reading plans, devotionals, verse of the day.
        self.media = Media(self)  #: Covers and media streams.
        self.messages = Messages(self)  #: In-app message center.
        self.telemetry = Telemetry(self)  #: Analytics, experiments, consent.
        self.web = Web(self)  #: Web pages and app config files.
        self.firebase = Firebase(self)  #: Firebase Realtime Database.

    def __enter__(self) -> OliveTree:
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()

    def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        self.http.close()

    def login(self) -> dict:
        """Log in with the configured credentials. Same as :meth:`Account.login`.

        Raises:
            OliveTreeAuthError: If credentials are missing or rejected.
        """
        if not (self.username and self.password):
            raise OliveTreeAuthError("Set OLIVE_TREE_USERNAME and OLIVE_TREE_PASSWORD (or pass them in).")
        return self.account.login()

    def refresh(self) -> dict:
        """Renew the access token with the stored refresh token. Same as :meth:`Account.refresh_token`."""
        return self.account.refresh_token()

    def ensure_auth(self) -> None:
        """Log in now if there is no token yet."""
        if not self.token:
            self.login()

    # --- convenience --------------------------------------------------------

    def backup(
        self, db: str = "olivetree.db", data_sets: Iterable[DataSet | str] = DATA_SETS
    ) -> dict[str, int]:
        """Mirror your sync data into a local SQLite file, fetching only changes since the last run.

        Args:
            db: SQLite file to create or update.
            data_sets: Data sets to back up (:class:`~pyolivetree.DataSet` members or names).

        Returns:
            Rows fetched per data set, e.g. ``{"annotations": 12, "library": 0, ...}``.
        """
        return _notes.backup(self, db, data_sets)

    def notes(self, db: str = "olivetree.db", *, refresh: bool = True) -> list[dict]:
        """Your notes, in Bible order.

        Args:
            db: Local backup file (created if missing).
            refresh: Sync annotation changes into ``db`` first. ``False`` reads ``db`` offline.

        Returns:
            One dict per note: the row's fields (``title``, ``content``, ``created_date``, ...) plus
            ``type``, ``ref`` (e.g. ``"John 3:16-17"``) and ``color``.
        """
        return self._annotations("note", db, refresh)

    def highlights(self, db: str = "olivetree.db", *, refresh: bool = True) -> list[dict]:
        """Your highlights, in Bible order. ``color`` is the highlighter name. See :meth:`notes`."""
        return self._annotations("highlight", db, refresh)

    def clips(self, db: str = "olivetree.db", *, refresh: bool = True) -> list[dict]:
        """Verse text you saved, in Bible order. See :meth:`notes`."""
        return self._annotations("clip", db, refresh)

    def status(self) -> dict:
        """Sync server status and latest change numbers. Same as ``sync.status()``."""
        return self.sync.status()

    def library(self) -> list[dict]:
        """Every product you own, across all pages (``productId``, ``title``, ...)."""
        return list(self.store.all_products(self.store.purchased()))

    def _annotations(self, kind: str, db: str, refresh: bool) -> list[dict]:
        if refresh:
            _notes.backup(self, db, [DataSet.ANNOTATIONS])
        return _notes.annotations(db, kind)

    def _take_tokens(self, data: dict) -> None:
        self.token = data.get("authentication_token") or self.token
        self.refresh_token = data.get("refresh_token") or self.refresh_token

    def request(
        self,
        method: str,
        url: str,
        *,
        params: dict | None = None,
        data: dict | None = None,
        json: Any = None,
        headers: dict | None = None,
        auth: bool = True,
        sign: str | None = None,
        basic: bool = False,
    ) -> Any:
        """Send one request. Every endpoint method goes through here; use it for anything unwrapped.

        ``None`` values in ``params`` and ``data`` are dropped.

        Args:
            method: HTTP method.
            url: Full URL.
            params: Query string values.
            data: Form fields. Store/account URLs also get :attr:`app_fields`.
            json: JSON body (sent compact, so the signature matches the bytes sent).
            headers: Extra headers.
            auth: Send ``OTAuthorization: Bearer <token>``, logging in first if needed.
            sign: HMAC key profile for a ``signature`` header (``"telemetry"``, ``"ai"``, ...).
            basic: Send HTTP Basic auth with :attr:`username` / :attr:`password`.

        Returns:
            Parsed JSON, ``str`` for text/XML/HTML, or ``bytes``.

        Raises:
            OliveTreeError: On HTTP errors. After a token error the client logs in again and
                retries once before raising.
        """
        if url.startswith(f"{WWW}/store/br5/app/") and json is None:
            data = {**self.app_fields, **(data or {})}
        params, data, hdrs = _drop_none(params), _drop_none(data), dict(headers or {})
        content = None
        if json is not None:
            content = jsonlib.dumps(json, separators=(",", ":")).encode()
            hdrs["Content-Type"] = "application/json"
        if sign:
            hdrs["signature"] = sign_body(content or b"", sign, self.hmac_key)
        basic_auth = (self.username, self.password) if basic else None
        for attempt in (1, 2):
            if auth:
                self.ensure_auth()
                hdrs["OTAuthorization"] = f"Bearer {self.token}"
            r = self.http.request(
                method, url, params=params, data=data, content=content, headers=hdrs, auth=basic_auth
            )
            try:
                return parse_response(r)
            except OliveTreeError as e:
                stale = e.code in TOKEN_ERRORS or e.status == 401
                if not (auth and attempt == 1 and stale):
                    raise
                self.token = None  # log in again and retry once


def _drop_none(d: dict | None) -> dict | None:
    return {k: v for k, v in d.items() if v is not None} if d else None


#: Name used by pyolivetree 1.x.
OliveTreeClient = OliveTree
