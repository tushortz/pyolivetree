Installation
============

Requirements
------------

* Python 3.10 or newer
* `uv <https://docs.astral.sh/uv/>`_ (recommended) or pip

From PyPI
---------

.. code-block:: bash

   pip install pyolivetree

From source
-----------

.. code-block:: bash

   git clone https://github.com/tushortz/pyolivetree.git
   cd pyolivetree
   make install          # uv sync --extra dev --extra docs

Configuration
-------------

Copy ``.env.example`` to ``.env`` and set:

* ``OLIVE_TREE_USERNAME``: account email
* ``OLIVE_TREE_PASSWORD``: account password
* ``OLIVE_TREE_INSTALL_ID``: optional fixed device id (a new UUID is used otherwise)
* ``OLIVE_TREE_HMAC_KEY``: optional hex/base64 key that replaces the built-in signing keys

Values already set in the environment win over ``.env``.
