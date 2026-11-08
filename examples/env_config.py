"""Explicit credentials example (no .env file required)."""

from __future__ import annotations

from pyolivetree import OliveTreeClient


def main() -> None:
    """Use constructor credentials instead of environment variables."""
    client = OliveTreeClient(
        username="your@email.com",
        password="your-password",
        install_id="example-install-id",
    )
    try:
        auth = client.login()
        print("Authenticated:", auth.get("authenticated"))
    finally:
        client.close()


if __name__ == "__main__":
    main()
