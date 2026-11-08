# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-11-08

### Added

- `ot.sync.pull`, `page`, `push` and `table_schema` for notes, highlights, library and reading-plan data.
- `backup`, `annotations` and `to_markdown` for a local SQLite backup and Markdown export.
- `pyolivetree` command line (`backup`, `notes`, `highlights`, `clips`, `status`, `library`).
- `ot.store.all_products` to walk every page of a product listing.
- Smart Search `ot.ai.query` with book filters.
- `DataSet` enum for sync data sets; plain names still work.
- Automatic re-login and retry on expired tokens.

### Changed

- Hand-written client organised by endpoint group (`account`, `store`, `products`, `sync`, `ai`,
  `reading`, `media`, `messages`, `telemetry`, `web`, `firebase`). Main class is `OliveTree`;
  `OliveTreeClient`, `AsyncOliveTreeClient` and `a`-prefixed async methods still work.
- Store and account requests include standard client fields, fixing empty `purchased` results.
- Sync requests use the bearer token.

## [1.0.0] - 2026-06-27

### Added

- Initial release of the `pyolivetree` Python client covering the Olive Tree Bible Reader API operations in OpenAPI spec 1.0.0.
- Synchronous `OliveTreeClient` and asynchronous `AsyncOliveTreeClient`.
- Credential loading from constructor arguments or `.env` file.
- Bearer, Basic, and HMAC authentication support.
- Sphinx documentation and usage examples.
