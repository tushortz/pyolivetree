# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-06-27

### Added

- Initial release of the `pyolivetree` Python client covering all 86 Olive Tree Bible Reader API operations from OpenAPI spec 1.0.0.
- Synchronous `OliveTreeClient` and asynchronous `AsyncOliveTreeClient`.
- Credential loading from constructor arguments or `.env` file.
- Bearer, Basic, and HMAC authentication support.
- Sphinx documentation and usage examples.
- Integration harness for live API validation.
