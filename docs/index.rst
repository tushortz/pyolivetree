pyolivetree
===========

Python client for the **Olive Tree Bible**. Pull your notes and highlights, browse your library, query Smart Search AI, and call any
Olive Tree endpoint.

.. code-block:: python

   from pyolivetree import OliveTree

   with OliveTree() as ot:
       for row in ot.sync.pull("annotations"):
           print(row["datum"].get("title"), row["datum"].get("content"))

.. toctree::
   :maxdepth: 2
   :caption: Guide

   manual/installation
   quickstart
   manual/usage
   manual/authentication
   endpoints
   notes
   manual/limitations

.. toctree::
   :maxdepth: 2
   :caption: API reference

   api/client
   api/resources
   api/notes
   api/internals
