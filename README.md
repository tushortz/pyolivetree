# pyolivetree

Python client for the [Olive Tree Bible Reader API](https://www.olivetree.com), reverse-engineered from the Android app and documented in `swagger.yml`.

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (recommended)

## Install

```bash
uv sync --dev
```

Or from PyPI (when published):

```bash
pip install pyolivetree
```

## Quick start

Copy `.env.example` to `.env` and set your credentials, then:

```python
from pyolivetree import OliveTreeClient

client = OliveTreeClient()
client.account.login()
feed = client.store.home()
print(feed)
```

Async:

```python
import asyncio
from pyolivetree import AsyncOliveTreeClient

async def main():
    async with AsyncOliveTreeClient() as client:
        await client.account.login()
        feed = await client.store.home()
        print(feed)

asyncio.run(main())
```

## Documentation

Build the full manual and API reference:

```bash
make docs
open docs/_build/html/index.html
```

## Development

```bash
make help      # list targets
make test      # lint + unit tests (100% coverage)
make integration  # live API harness (requires .env)
```

See [CHANGELOG.md](CHANGELOG.md) for release history.
