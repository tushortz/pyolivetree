Authentication
==============

Credentials
-----------

Set ``OLIVE_TREE_USERNAME`` and ``OLIVE_TREE_PASSWORD`` in the environment or ``.env``, or pass
them to :class:`~pyolivetree.OliveTree`. The client logs in on the first call that needs a token;
you can also call :meth:`~pyolivetree.OliveTree.login` yourself.

.. code-block:: python

   from pyolivetree import OliveTree

   ot = OliveTree()          # reads username/password from .env
   ot.login()                # stores authentication_token + refresh_token
   feed = ot.store.home()    # sent with the bearer token

Login and tokens
----------------

``POST /store/br5/app/json/account/account_login`` with ``user``, ``pass``, ``install_id`` and
``supportsAccessToken=1`` returns:

* ``authentication_token``: kept in :attr:`~pyolivetree.OliveTree.token`
* ``refresh_token``: kept in :attr:`~pyolivetree.OliveTree.refresh_token`

Both stay in memory for the session. :meth:`~pyolivetree.OliveTree.refresh` swaps the refresh
token for a new access token. To reuse a token across runs, pass ``token=...`` to the client.

Bearer token
------------

Authenticated requests, including everything on ``sync.olivetree.com``, send:

.. code-block:: text

   OTAuthorization: Bearer <authentication_token>

If the server answers 401 or ``errorCode`` 1018/1020, the client logs in again and retries once.

Basic auth
----------

:meth:`~pyolivetree.OliveTree.request` accepts ``basic=True`` to send HTTP Basic auth with the
configured username and password, for endpoints that expect it.

Client fields
-------------

Every store/account form post includes a fixed set of client fields (``platform``,
``install_id``, ``ReaderVersion``, ``supportsProductDRM``, ...). They are in
:attr:`~pyolivetree.OliveTree.app_fields`. Without them some endpoints, such as
``store.purchased``, return empty results.

HMAC signing
------------

Smart Search, messages, analytics events and session telemetry need a ``signature`` header: the
uppercase-hex HMAC-SHA512 of the exact request body. The client picks the key per service
(``telemetry``, ``ai``, ``consent``, ``features``); see :func:`pyolivetree.sign_body` and
:data:`pyolivetree.constants.HMAC_KEYS`.

Set ``OLIVE_TREE_HMAC_KEY`` (hex or base64), or pass ``hmac_key=...``, to sign every request with
one key instead.

Errors
------

* :class:`~pyolivetree.OliveTreeAuthError`: missing credentials, failed login, HTTP 401 or
  ``{"authenticated": false}``.
* :class:`~pyolivetree.OliveTreeAPIError`: any other HTTP error.

Both derive from :class:`~pyolivetree.OliveTreeError` and carry ``status``, ``code`` and ``body``.
