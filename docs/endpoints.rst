Endpoint groups
===============

Each group is an attribute of :class:`~pyolivetree.OliveTree`.

.. list-table::
   :header-rows: 1
   :widths: 15 30 55

   * - Attribute
     - Host
     - What it covers
   * - ``ot.account``
     - www.olivetree.com
     - Login, access/refresh tokens, signup, password reset, web hand-off, subscriptions
   * - ``ot.store``
     - www.olivetree.com
     - Home feed, categories, search, product details, purchased products, wishlists, subscriptions
   * - ``ot.products``
     - www.olivetree.com
     - XML product info, registration and download links
   * - ``ot.sync``
     - sync.olivetree.com
     - Notes, highlights, library and reading-plan data: status, pull, push, table schema, lock
   * - ``ot.ai``
     - biblesearch-ai.olivetree.com
     - Smart Search queries, usage and models
   * - ``ot.reading``
     - www / speech / votd
     - Reading plans, devotionals, recommendations, verse of the day, audio messages
   * - ``ot.media``
     - cdn / media / www
     - Covers, reading-plan images, media streams
   * - ``ot.messages``
     - www.olivetree.com
     - In-app message center (signed)
   * - ``ot.telemetry``
     - analytics / privacy
     - Event manifests, experiments, consent, sessions
   * - ``ot.web``
     - www.olivetree.com
     - Web pages, help center and app config (EULA, privacy policy, product pages, timeouts)
   * - ``ot.firebase``
     - firebaseio.com
     - Firebase Realtime Database reads

Calls that change your account
------------------------------

``sync.push``, ``store.wishlist_add``/``wishlist_remove``, ``store.register_subscription``,
``store.validate_google_in_app_purchase``, ``store.support_delete_account`` (irreversible),
``account.signup``, ``ai.set_usage`` and the ``telemetry`` POST/PUT methods.

Not included
------------

* Decrypting purchased books. :meth:`~pyolivetree.resources.products.Products.download_links`
  returns where to download them; the files are encrypted.

See :doc:`manual/limitations` for endpoints with known server-side restrictions.
