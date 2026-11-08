Notes backup and export
=======================

Command line
------------

.. code-block:: bash

   pyolivetree backup                   # mirror sync data into olivetree.db
   pyolivetree notes --out notes.md     # notes as Markdown, grouped by Bible book
   pyolivetree highlights --out highlights.md
   pyolivetree clips                    # verse text you saved
   pyolivetree library                  # products you own (JSON)
   pyolivetree status                   # sync server status (JSON)

``backup`` stores a cursor per data set, so re-running it only fetches changes.

Python
------

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
