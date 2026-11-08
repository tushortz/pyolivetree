Usage
=====

Synchronous client
------------------

.. code-block:: python

   from pyolivetree import OliveTree

   with OliveTree(username="you@example.com", password="secret") as ot:
       home = ot.store.home()
       results = ot.store.search("faith")
       owned = list(ot.store.all_products(ot.store.purchased()))

Asynchronous client
-------------------

:class:`~pyolivetree.AsyncOliveTree` has the same groups and methods; every call is awaited.
Methods that yield in the sync client (``sync.pull``, ``store.all_products``) return lists.

.. code-block:: python

   import asyncio
   from pyolivetree import AsyncOliveTree

   async def main():
       async with AsyncOliveTree() as ot:
           await ot.login()
           home = await ot.store.home()
           notes = await ot.sync.pull("annotations")

   asyncio.run(main())

The 1.x names still work: ``OliveTreeClient``, ``AsyncOliveTreeClient``, and ``a``-prefixed
async methods such as ``await client.store.ahome()``.

Resource groups
---------------

Endpoints are grouped on the client; see :doc:`../endpoints` for the full list.

* ``ot.account``: login, signup, tokens, subscriptions
* ``ot.store``: catalog, search, purchases, wishlists
* ``ot.products``: XML product info and download links
* ``ot.sync``: notes, highlights, library and reading-plan data
* ``ot.ai``: Smart Search AI
* ``ot.reading``: reading plans, devotionals, verse of the day
* ``ot.media``: covers and media streams
* ``ot.messages``: in-app message center
* ``ot.telemetry``: analytics, experiments, consent
* ``ot.web``: web pages, help center and config files
* ``ot.firebase``: Firebase Realtime Database

Data sets
---------

Sync data is split into data sets, listed in :class:`~pyolivetree.DataSet`:

=========================  =====================  ==================================================
Member                     Value                  Contents
=========================  =====================  ==================================================
``DataSet.ANNOTATIONS``    ``"annotations"``      Notes, highlights, clips, categories, highlighters
``DataSet.LIBRARY``        ``"library"``          Library categories, document details, last-read
``DataSet.DAILY_READING``  ``"daily_reading"``    Reading plans and progress
``DataSet.BOOKSHELF``      ``"bookshelf"``        Recently opened text and audio locations
=========================  =====================  ==================================================

Every method that takes a data set accepts the member, its value, or the server name, so these
are equivalent:

.. code-block:: python

   from pyolivetree import DataSet

   ot.sync.page(DataSet.LIBRARY)
   ot.sync.page("library")
   ot.sync.page("managed_library")

Members are strings (``DataSet.LIBRARY == "library"``), so they also work as dict keys and in
JSON.

Reading your notes
------------------

.. code-block:: python

   with OliveTree() as ot:
       for row in ot.sync.pull(DataSet.ANNOTATIONS):
           d = row["datum"]
           if row["table_name"] == "annotations" and d.get("annotation_type_id") == 1:
               print(d["title"], "-", d.get("content"))

See :doc:`../notes` for backing up to SQLite and exporting Markdown.

Raw requests
------------

Anything not wrapped can be sent with :meth:`~pyolivetree.OliveTree.request`, which adds the
token, client fields and signature for you:

.. code-block:: python

   ot.request("POST", "https://www.olivetree.com/store/br5/app/json/store/purchased/1")
   ot.request("POST", "https://biblesearch-ai.olivetree.com/api/v1/query",
              json={"query": "grace"}, sign="ai")

Response types
--------------

* JSON endpoints return ``dict`` or ``list``
* HTML/XML endpoints return ``str``
* Images and audio return ``bytes``

Errors
------

.. code-block:: python

   from pyolivetree import OliveTreeError

   try:
       ot.store.product(0)
   except OliveTreeError as e:
       print(e.status, e.code, e.body)
