"""Async client quickstart example."""

from __future__ import annotations

import asyncio

from pyolivetree import AsyncOliveTreeClient


async def main() -> None:
    """Login and fetch the store home feed asynchronously."""
    async with AsyncOliveTreeClient() as client:
        await client.login()
        home = await client.store.ahome()
        print("Store rows:", len(home.get("rows", [])) if isinstance(home, dict) else home)
        results = await client.store.asearch(q="bible")
        if isinstance(results, dict):
            print("Search total:", results.get("total_count"))


if __name__ == "__main__":
    asyncio.run(main())
