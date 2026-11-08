Installation
============

Requirements
------------

* Python 3.10 or newer
* `uv <https://docs.astral.sh/uv/>`_ (recommended) or pip

From source
-----------

.. code-block:: bash

   git clone https://github.com/pyolivetree/pyolivetree.git
   cd pyolivetree
   uv sync --extra dev

From PyPI
---------

.. code-block:: bash

   pip install pyolivetree

Configuration
-------------

Copy ``.env.example`` to ``.env`` and set:

* ``OLIVE_TREE_USERNAME`` — account email
* ``OLIVE_TREE_PASSWORD`` — account password
* ``OLIVE_TREE_INSTALL_ID`` — optional device ID (auto-generated if omitted)
* ``OLIVE_TREE_HMAC_KEY`` — optional hex/base64 key for signed endpoints
