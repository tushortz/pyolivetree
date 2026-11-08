Notes backup and export
=======================

Command line
------------

.. code-block:: bash

   pyolivetree backup                   # mirror sync data into olivetree.db
   pyolivetree notes --out notes.md     # notes as Markdown, grouped by Bible book
   pyolivetree notes --refresh          # sync changes first, then export
   pyolivetree highlights --out highlights.md
   pyolivetree clips                    # verse text you saved
   pyolivetree library                  # products you own (JSON)
   pyolivetree status                   # sync server status (JSON)

``backup`` stores a cursor per data set, so re-running it only fetches changes. ``notes``,
``highlights`` and ``clips`` read the backup; add ``--refresh`` to sync first. Without a backup
they exit with "run backup() first".

Python
------

The client has one method per command:

.. code-block:: python

   from pyolivetree import OliveTree, to_markdown

   with OliveTree() as ot:
       ot.backup()                   # all data sets -> olivetree.db
       notes = ot.notes()            # syncs annotation changes, then reads the backup
       highlights = ot.highlights()
       clips = ot.clips(refresh=False)   # offline: backup only
       ot.status()
       owned = ot.library()          # every owned product

   print(to_markdown(notes))

Each item is the row's fields (``title``, ``content``, ``created_date``, ...) plus ``type``,
``ref`` (e.g. ``"John 3:16-17"``) and ``color`` (highlighter name). See
:meth:`pyolivetree.OliveTree.notes`.

The same steps as functions:

.. code-block:: python

   from pyolivetree import DataSet, OliveTree, annotations, backup, to_markdown

   with OliveTree() as ot:
       backup(ot, "olivetree.db")                                  # all data sets
       backup(ot, "olivetree.db", data_sets=[DataSet.ANNOTATIONS])  # or just one

   notes = annotations("olivetree.db", "note")
   open("notes.md", "w").write(to_markdown(notes))

Querying the database
---------------------

``olivetree.db`` is SQLite. Every row is in ``syncables``:

.. code-block:: sql

   SELECT table_name, count(*) FROM syncables GROUP BY 1;

   SELECT json_extract(datum, '$.title'), json_extract(datum, '$.content')
   FROM syncables
   WHERE table_name = 'annotations' AND json_extract(datum, '$.annotation_type_id') = 1;

Annotation types
----------------

``annotation_type_id`` in the ``annotations`` table:

====  ==========  =========================================
Id    Kind        Meaning
====  ==========  =========================================
1     note        Text you wrote (``content``)
16    highlight   Highlighted text; color via ``highlighter_id``
256   clip        Verse text you copied/saved
====  ==========  =========================================

These were mapped from a real account's data; other values may exist.
