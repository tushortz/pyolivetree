Usage
=====

Synchronous client
------------------

.. code-block:: python

   from pyolivetree import OliveTreeClient

   with OliveTreeClient(username="you@example.com", password="secret") as client:
       client.login()
       home = client.store.home()
       results = client.store.search(q="faith")

Asynchronous client
-------------------

.. code-block:: python

   import asyncio
   from pyolivetree import AsyncOliveTreeClient

   async def main():
       async with AsyncOliveTreeClient() as client:
           await client.login()
           home = await client.store.ahome()

   asyncio.run(main())

Resource groups
---------------

Operations are grouped by OpenAPI tag on the client:

* ``client.store`` — store JSON API
* ``client.account`` — login, signup, tokens
* ``client.sync`` — annotation sync (``sync.olivetree.com``)
* ``client.smart_search`` — AI search (``biblesearch-ai.olivetree.com``)
* ``client.analytics``, ``client.privacy``, ``client.speech``, ``client.cdn``, etc.

Each sync method has an async counterpart prefixed with ``a`` (e.g. ``home`` / ``ahome``).

Response types
--------------

* JSON endpoints return ``dict`` or ``list``
* HTML/XML endpoints return ``str``
* Images and audio return ``bytes``

Errors
------

Failed HTTP responses raise :py:exc:`pyolivetree.OliveTreeAPIError` with
``status_code``, ``operation_id``, and ``body`` attributes.
