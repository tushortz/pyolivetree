Limitations
===========

This client is generated from a reverse-engineered OpenAPI specification.
Keep in mind:

* Request/response shapes reflect Android client expectations; servers may accept additional fields.
* Dynamic store paths (resource guide, RC sections) use server-driven URL suffixes via :py:meth:`pyolivetree.resources.store.StoreResource.dynamic_path`.
* HMAC endpoints require a device-specific key not available without reverse engineering.
* DRM license URLs are fetched dynamically from media manifests and are not covered here.
* Most store endpoints use ``POST`` with ``application/x-www-form-urlencoded`` bodies.
