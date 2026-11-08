Authentication
==============

The Olive Tree API supports several authentication schemes:

Login and session tokens
------------------------

Per the OpenAPI spec, bearer tokens are obtained from account endpoints — not from
environment variables. Configure only ``OLIVE_TREE_USERNAME`` and
``OLIVE_TREE_PASSWORD`` in ``.env``, then call :py:meth:`OliveTreeClient.login`.

``account_login`` (with ``supportsAccessToken=1``) returns an
:py:class:`~pyolivetree.models.AccountAuthResponse` containing:

* ``authentication_token`` — sent as ``OTAuthorization: Bearer {token}``
* ``refresh_token`` — stored in memory for your session

The client keeps both tokens in memory on :py:class:`~pyolivetree.auth.AuthManager`
after a successful login. Call :py:meth:`OliveTreeClient.refresh` to renew tokens
via ``account_refresh_token`` when needed.

Bearer token (``OTAuthorization``)
----------------------------------

After login, the client sends:

.. code-block:: text

   OTAuthorization: Bearer {authentication_token}

Basic auth
----------

When no bearer token is available, store endpoints accept HTTP Basic auth
with your olivetree.com credentials until you log in.

HMAC signing
------------

Messages, analytics batches, privacy telemetry, consent receipts, and Smart
Search query endpoints require an HMAC-SHA512 ``signature`` header over the raw
request body. The client embeds the same keys as the official Android app and
selects the correct profile per endpoint (``telemetry``, ``ai``, or ``consent``).

Optionally set ``OLIVE_TREE_HMAC_KEY`` to override all profiles with a single
key (hex or base64) for testing.

Automatic login
---------------

When credentials are configured, authenticated endpoints call :py:meth:`OliveTreeClient.login`
automatically before the first bearer-protected request.

.. code-block:: python

   from pyolivetree import OliveTreeClient

   client = OliveTreeClient()  # reads username/password from .env
   client.login()              # obtains authentication_token + refresh_token
   feed = client.store.home()  # uses in-memory bearer token
