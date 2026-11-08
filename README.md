# pyolivetree

Python client for the **Olive Tree Bible** APIs. Use it to pull your notes and highlights, browse your library, query Smart Search AI, and more.

## Install

```bash
pip install pyolivetree
cp .env.example .env             # put your Olive Tree email + password in it
```

## Client

```python
from pyolivetree import DataSet, OliveTree

with OliveTree() as ot:              # logs in on first call that needs it
    ot.sync.status()                 # latest change numbers for your data
    for row in ot.sync.pull(DataSet.ANNOTATIONS):   # or "annotations"
        print(row["table_name"], row["datum"].get("title"))

    owned = list(ot.store.all_products(ot.store.purchased()))
    ot.store.product(36163)          # product details
    ot.products.download_links(36163)  # XML with product download URLs
    ot.ai.query("What does the Bible say about patience?", books=["James"])
    ot.reading.verse_of_the_day("2026-11-08")
    ot.media.cover(36163)            # bytes (JPEG)
```

Async, with the same groups and methods:

```python
import asyncio
from pyolivetree import AsyncOliveTree

async def main():
    async with AsyncOliveTree() as ot:
        home = await ot.store.home()
        notes = await ot.sync.pull("annotations")   # list

asyncio.run(main())
```

The 1.x names still work: `OliveTreeClient`, `AsyncOliveTreeClient`, `install_id=`, and `a`-prefixed async methods (`await client.store.ahome()`). See [examples/](examples/).

Data sets are `DataSet.ANNOTATIONS`, `LIBRARY`, `DAILY_READING` and `BOOKSHELF`. Every sync method and `backup()` also accept the plain name (`"library"`) or the server name (`"managed_library"`).

Responses come back as JSON (`dict`/`list`), `str` for XML/HTML, or `bytes` for images. Errors raise `OliveTreeAuthError` (login/401) or `OliveTreeAPIError` (other HTTP errors), both subclasses of `OliveTreeError` with `.status`, `.code` and `.body`. An expired token triggers one automatic re-login. `ot.request(method, url, ...)` reaches anything not wrapped.

| Group | Methods |
|---|---|
| `ot.account` | `login`, `access_token`, `refresh_token`, `signup`, `forgot_password`, `web_handoff_token`, `subscription`, `add_variable_subscription_selections` |
| `ot.store` | `home`, `banner`, `featured_categories`, `library`, `purchased`, `wishlists`, `search`, `category`, `product`, `products`, `library_details`, `all_products`, `path`, `subscriptions_available`, `first_run_*`, `need_interests`, `paid_features`, `paid_features_marketing`, `ads`, `product_manifest`, `giveaway`, `allow_subscription_purchase`, `subscription_variable_product_selection`, `wishlist_add`, `wishlist_remove`, `register_subscription`, `validate_google_in_app_purchase`, `support_delete_account` |
| `ot.products` | `download_links`, `info`, `register`, `updates`, `email_signup`, `reading_templates` |
| `ot.sync` | `status`, `page`, `pull`, `table_schema`, `push`, `release_lock`, `possibly_bad_annotation_data` |
| `ot.ai` | `query`, `status`, `set_usage`, `models` |
| `ot.reading` | `daily_reading`, `recommended`, `verse_of_the_day`, `verse_of_the_day_image`, `now_reading`, `completed_message` |
| `ot.media` | `cover`, `cover_stack`, `product_image`, `reading_plan_image`, `reading_plan_list_image`, `stream` |
| `ot.messages` | `list`, `register_device`, `metrics` |
| `ot.telemetry` | `event_manifest`, `get_variant`, `set_variant`, `events`, `session_start`, `consent_receipt`, `location_settings`, `subscription_log_usage` |
| `ot.web` | `timeouts`, `appirater_config`, `app_to_web_bridge`, `product_page`, `bible_study_packs`, `manage_subscriptions`, `eula`, `privacy_policy`, `help_articles`, `help_login` |
| `ot.firebase` | `get`, `root` |

Calls that change your account: `sync.push`, `store.wishlist_*`, `store.register_subscription`, `store.validate_google_in_app_purchase`, `store.support_delete_account` (irreversible), `account.signup`, `ai.set_usage`, and the `telemetry` POSTs.

## Notes backup and export

```bash
pyolivetree backup                   # mirror your sync data into olivetree.db (re-runs fetch only changes)
pyolivetree notes --out notes.md     # your notes as Markdown, grouped by Bible book
pyolivetree highlights --out highlights.md
pyolivetree clips                    # verse text you saved
pyolivetree library                  # products you own
```

```python
from pyolivetree import OliveTree, backup, annotations, to_markdown
with OliveTree() as ot:
    backup(ot, "olivetree.db")
print(to_markdown(annotations("olivetree.db", "note")))
```

`olivetree.db` is SQLite: every row is in `syncables` (`table_name`, `datum` JSON).

## How auth works

- Login: `POST /store/br5/app/json/account/account_login` returns `authentication_token`. The client sends it as `OTAuthorization: Bearer <token>`.
- Store/account form posts include standard client fields (`install_id`, `platform`, `ReaderVersion`, `supportsProductDRM`, …). Without them, `purchased` comes back empty.
- Signed endpoints (`ai`, `messages`, `telemetry.events`, `session_start`) add a `signature` header: uppercase-hex HMAC-SHA512 of the body, using the client keys in `constants.py`. Set `OLIVE_TREE_HMAC_KEY` (hex or base64) or pass `hmac_key=` to use one key for everything.
- `ot.request(..., basic=True)` sends HTTP Basic auth with your username and password.

## Known gaps

- `messages.list` returns 401 until a device is registered via `messages.register_device`. The body format for that call isn't confirmed.
- `sync.possibly_bad_annotation_data` is currently rejected by the server (401/410); `firebase` reads are refused (423/401); the help-center pages may return 403 to non-browser clients.
- Purchased books (study Bibles included) download as encrypted files. This client gets the download links but doesn't decrypt them.

## Development

Needs [uv](https://docs.astral.sh/uv/).

```bash
make install       # .venv with dev + docs extras
make test          # pytest
make coverage      # pytest with coverage report
make lint          # ruff check
make format        # ruff format + black
make docs          # Sphinx HTML in docs/_build/html
make security      # dependency vulnerability scan
make run           # run examples/sync_basic.py
make build check   # build sdist/wheel and validate with twine
make publish-test  # upload to TestPyPI (UV_PUBLISH_TOKEN)
make publish       # upload to PyPI (UV_PUBLISH_TOKEN)
```

Layout: `client.py` (auth, request, signing), `async_client.py`, `resources/` (one module per endpoint group),
`notes.py` (backup + Markdown), `cli.py`, `constants.py`, `exceptions.py`. The OpenAPI description is in `swagger.yml`; the docs manual is in `docs/manual/`.
