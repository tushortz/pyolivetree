Client
======

.. autoclass:: pyolivetree.OliveTree
   :members: request, login, refresh, ensure_auth, close, token, refresh_token, hmac_key, app_fields

.. autoclass:: pyolivetree.AsyncOliveTree
   :members: request, login, refresh, ensure_auth, aclose, client

.. autoclass:: pyolivetree.async_client.AsyncGroup

``OliveTreeClient`` and ``AsyncOliveTreeClient`` are aliases kept for 1.x code.

Data sets
---------

.. autoclass:: pyolivetree.DataSet
   :members:
   :undoc-members:

Names are normalised with :func:`pyolivetree.constants.data_set_name`.

Exceptions
----------

.. automodule:: pyolivetree.exceptions
   :members:
