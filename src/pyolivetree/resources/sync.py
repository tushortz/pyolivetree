"""Sync endpoints: your notes, highlights, library and reading-plan data."""

from __future__ import annotations

import platform
from collections.abc import Iterator
from typing import Any

from pyolivetree.constants import PLATFORM_ID, SYNC, SYNC_PROTOCOL, DataSet, data_set_name
from pyolivetree.resources._base import Resource


class Sync(Resource):
    """``sync.olivetree.com``. Available as ``ot.sync``.

    Data is split into data sets (:class:`~pyolivetree.DataSet`; plain strings also work). Each row looks like
    ``{"id", "table_name", "table_version", "sequence_number", "deleted", "datum": {...}}``.
    Every change gets a higher ``sequence_number``, so you can fetch only what's new.

    Main tables in ``annotations``: ``annotations`` (notes, highlights, clips; text in
    ``datum.content``), ``annotation_locations``, ``annotation_categories``, ``highlighters``.
    """

    def _q(self, **kw: Any) -> dict[str, Any]:
        return {"device_id": self._c.device_id, "sync_client_protocol_version": SYNC_PROTOCOL, **kw}

    def status(self, lock: bool = False, data_set: DataSet | str | None = None) -> dict:
        """Server status and the latest sequence number per data set.

        Args:
            lock: Take the write lock (needed before :meth:`push`). Default leaves it alone.
            data_set: Optional data set to scope the lock to.

        Returns:
            ``{"customer": {"user_id", "master_sequence_numbers": {...}}, "server": {...}}``.
        """
        q = self._q(
            managed_data_set=_managed(data_set) if data_set else None,
            do_not_lock=None if lock else "true",
            reader_version=self._c.reader_version,
        )
        return self._c.request("GET", f"{SYNC}/syncables/status.json", params=q)

    def page(self, data_set: DataSet | str = DataSet.ANNOTATIONS, above: int = 0) -> list[dict]:
        """One page of rows changed after sequence number ``above``.

        Args:
            data_set: A :class:`~pyolivetree.DataSet` or its name, e.g. ``"library"``.
            above: Return rows with a higher sequence number than this.
        """
        q = self._q(
            platform_id=PLATFORM_ID,
            above=above,
            managed_data_set=_managed(data_set),
            reader_version=self._c.reader_version,
        )
        return self._c.request("GET", f"{SYNC}/syncables.json", params=q).get("syncables") or []

    def pull(self, data_set: DataSet | str = DataSet.ANNOTATIONS, above: int = 0) -> Iterator[dict]:
        """Yield every row changed after ``above``, fetching pages until caught up.

        Args:
            data_set: Data set to read (:class:`~pyolivetree.DataSet` or name).
            above: Start after this sequence number (0 = everything).

        Yields:
            Sync rows. Rows with ``deleted == 1`` were removed on another device.
        """
        latest = self.status()["customer"]["master_sequence_numbers"].get(data_set_name(data_set), 0)
        while above < latest:
            page = self.page(data_set, above)
            if not page:
                break
            yield from page
            top = max(int(i["sequence_number"]) for i in page)
            if top <= above:  # server didn't advance; stop instead of looping
                break
            above = top

    def table_schema(self, data_set: DataSet | str, table: str, version: int = 0) -> dict:
        """The server's SQLite schema for a synced table.

        Returns:
            ``{"managed_data_set", "table_name", "table_version", "sqlite3_schema"}``.
        """
        return self._c.request(
            "GET",
            f"{SYNC}/syncables/get_table_schema/{_managed(data_set)}/{table}/{version}.json",
            params={"sync_client_protocol_version": SYNC_PROTOCOL},
        )

    def push(
        self,
        table: str,
        datum: dict,
        *,
        data_set: DataSet | str = DataSet.ANNOTATIONS,
        item_id: int = -1,
        sequence_number: int = -1,
        deleted: bool = False,
        customer_id: int | None = None,
        release_lock: bool = True,
    ) -> dict:
        """Create or update one row on the server. **Changes your real account.**

        The expected flow is ``status(lock=True)``, then one ``push`` per row, with
        ``release_lock=True`` on the last one.

        Args:
            table: Table name, e.g. ``"annotations"``.
            datum: Row fields, shaped like ``datum`` from :meth:`pull` (``client_id`` = local id).
            data_set: Data set the table belongs to.
            item_id: Server row id; ``-1`` creates a new row.
            sequence_number: Current sequence number of the row; ``-1`` for new rows.
            deleted: Mark the row deleted.
            customer_id: Your user id. Looked up via :meth:`status` if omitted.
            release_lock: Release the write lock after this push.

        Returns:
            ``{"syncable": {...}}`` with the saved row, or ``{"exception": {...}}``.
        """
        if customer_id is None:
            customer_id = self.status()["customer"]["user_id"]
        body = {
            "device_id": self._c.device_id,
            "device_model": "pyolivetree",
            "device_os": platform.release(),
            "sync_client_protocol_version": SYNC_PROTOCOL,
            "managed_data_set": _managed(data_set),
            "table_name": table,
            "deleted": int(deleted),
            "id": item_id,
            "customer_id": customer_id,
            "sequence_number": sequence_number,
            "datum": datum,
        }
        q = {"sync_client_protocol_version": SYNC_PROTOCOL, "release_lock": "true" if release_lock else None}
        return self._c.request("POST", f"{SYNC}/syncables/syncitem.json", params=q, json=body)

    def release_lock(self, data_set: DataSet | str = DataSet.ANNOTATIONS) -> Any:
        """Release the write lock taken by ``status(lock=True)``."""
        return self._c.request(
            "PUT", f"{SYNC}/syncables/release_lock", params=self._q(managed_data_set=_managed(data_set))
        )

    def possibly_bad_annotation_data(self) -> Any:
        """Annotations the server flagged as possibly corrupt.

        The server currently rejects this request (HTTP 401 with a token, 410 Gone with Basic auth).
        """
        return self._c.request("GET", f"{SYNC}/syncables/get_possibly_bad_annotation_data.json")


def _managed(data_set: DataSet | str) -> str:
    """Server form of a data set name: ``"managed_annotations"``."""
    return f"managed_{data_set_name(data_set)}"
