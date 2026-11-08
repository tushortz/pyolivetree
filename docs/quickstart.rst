Quickstart
==========

Install
-------

.. code-block:: bash

   pip install pyolivetree

Credentials
-----------

The client reads ``OLIVE_TREE_USERNAME`` and ``OLIVE_TREE_PASSWORD`` from the environment or a
``.env`` file in the working directory:

.. code-block:: bash

   OLIVE_TREE_USERNAME=you@example.com
   OLIVE_TREE_PASSWORD=your_password
   OLIVE_TREE_INSTALL_ID=          # optional fixed device id
   OLIVE_TREE_HMAC_KEY=            # optional signing-key override

You can also pass them directly: ``OliveTree("you@example.com", "password")``.

First calls
-----------

.. code-block:: python

   from pyolivetree import OliveTree, OliveTreeError

   with OliveTree() as ot:
       print(ot.sync.status()["customer"]["master_sequence_numbers"])

       owned = list(ot.store.all_products(ot.store.purchased()))
       print(len(owned), "products")

       ot.ai.query("What does the Bible say about patience?", books=["James"])

       try:
           ot.store.product(0)
       except OliveTreeError as e:
           print(e.status, e.code, e.body)

Return values
-------------

* JSON responses come back as ``dict`` or ``list``.
* XML and HTML come back as ``str``.
* Images and other files come back as ``bytes``.

Anything not wrapped can be called with :meth:`~pyolivetree.OliveTree.request`:

.. code-block:: python

   ot.request("POST", "https://www.olivetree.com/store/br5/app/json/store/purchased/1")
