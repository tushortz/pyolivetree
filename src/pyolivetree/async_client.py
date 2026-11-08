"""The :class:`AsyncOliveTree` client: the same API as :class:`~pyolivetree.OliveTree`, with ``await``."""

from __future__ import annotations

import asyncio
import functools
import inspect
from typing import Any

from pyolivetree.client import OliveTree

#: Endpoint groups mirrored from :class:`~pyolivetree.OliveTree`.
GROUPS = (
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
)


class AsyncGroup:
    """Async view of one endpoint group. Every method becomes a coroutine.

    Methods that yield (``sync.pull``, ``store.all_products``) return a list instead.
    The 1.x names with an ``a`` prefix (``ahome``, ``asearch``) also work.
    """

    def __init__(self, group: Any) -> None:
        self._group = group

    def __getattr__(self, name: str) -> Any:
        fn = getattr(self._group, name, None)
        if fn is None and name.startswith("a"):
            fn = getattr(self._group, name[1:], None)
        if fn is None:
            raise AttributeError(name)
        if not callable(fn):
            return fn

        @functools.wraps(fn)
        async def call(*args: Any, **kwargs: Any) -> Any:
            if inspect.isgeneratorfunction(fn):
                return await asyncio.to_thread(lambda: list(fn(*args, **kwargs)))
            return await asyncio.to_thread(fn, *args, **kwargs)

        return call


class AsyncOliveTree:
    """Async client. Takes the same arguments as :class:`~pyolivetree.OliveTree`.

    Example:
        >>> async with AsyncOliveTree() as ot:            # doctest: +SKIP
        ...     home = await ot.store.home()
        ...     notes = await ot.sync.pull("annotations")

    NOTE: each call runs the synchronous client in a worker thread (``asyncio.to_thread``), so
    concurrency is limited by the default thread pool and calls share one connection pool and token.
    Upgrade path if that becomes a bottleneck: a native ``httpx.AsyncClient`` transport.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        #: The wrapped synchronous client (token, device id, settings live here).
        self.client = OliveTree(*args, **kwargs)
        for name in GROUPS:
            setattr(self, name, AsyncGroup(getattr(self.client, name)))

    def __getattr__(self, name: str) -> Any:
        # Settings such as token, device_id and app_fields come from the wrapped client.
        return getattr(self.client, name)

    async def __aenter__(self) -> AsyncOliveTree:
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        """Close the underlying HTTP connection pool."""
        await asyncio.to_thread(self.client.close)

    async def login(self) -> dict:
        """Log in. See :meth:`OliveTree.login`."""
        return await asyncio.to_thread(self.client.login)

    async def refresh(self) -> dict:
        """Renew the access token. See :meth:`OliveTree.refresh`."""
        return await asyncio.to_thread(self.client.refresh)

    async def ensure_auth(self) -> None:
        """Log in now if there is no token yet."""
        await asyncio.to_thread(self.client.ensure_auth)

    async def request(self, method: str, url: str, **kwargs: Any) -> Any:
        """Send one request. Same arguments as :meth:`OliveTree.request`."""
        return await asyncio.to_thread(self.client.request, method, url, **kwargs)


#: Name used by pyolivetree 1.x.
AsyncOliveTreeClient = AsyncOliveTree
