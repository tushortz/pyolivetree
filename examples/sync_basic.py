"""Sync client quickstart example."""

from __future__ import annotations

from pyolivetree import OliveTreeClient


def main() -> None:
    """Login and fetch the store home feed."""
    with OliveTreeClient() as client:
        client.login()
        home = client.store.home()
        print("Store rows:", len(home.get("rows", [])) if isinstance(home, dict) else home)
        results = client.store.search(q="bible")
        if isinstance(results, dict):
            print("Search total:", results.get("total_count"))


if __name__ == "__main__":
    main()
