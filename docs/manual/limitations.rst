Limitations
===========

* Request and response shapes are not officially documented; servers may accept or return
  additional fields.
* Dynamic store paths (home-feed rows, resource guides) come from the server; open them with
  :meth:`~pyolivetree.resources.store.Store.path` or :meth:`~pyolivetree.OliveTree.request`.
* Most store endpoints use ``POST`` with ``application/x-www-form-urlencoded`` bodies.
* ``messages.list`` returns 401 until the device is registered with ``messages.register_device``,
  whose body fields are not documented.
* ``sync.possibly_bad_annotation_data`` is currently rejected by the server (401/410).
* ``firebase`` reads are refused by the database (HTTP 423 Locked or 401).
* ``web.help_articles`` and ``web.help_login`` may return 403 to non-browser clients.
* Purchased books are delivered as encrypted files.
  :meth:`~pyolivetree.resources.products.Products.download_links` returns where to download them;
  this client does not decrypt them. DRM license URLs for media streams are not covered.
* :class:`~pyolivetree.AsyncOliveTree` runs the synchronous client in worker threads, so
  concurrency is bounded by the default thread pool.
