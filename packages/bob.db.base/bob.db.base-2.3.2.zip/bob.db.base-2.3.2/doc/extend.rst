.. vim: set fileencoding=utf-8 :
.. Thu 13 Oct 2016 10:34:35 CEST

.. _annotations:

Annotations
-----------

Many databases come with additional information about their data.  For image
databases, e.g., the locations of hand-labeled facial landmarks are provided.
Usually, these data is stored in additional text files.  For most of the
available ``bob.db`` databases, there is exactly one text file for each data
file.

The function :py:func:`bob.db.base.read_annotation_file` can be used to read
annotation files of different types.  It will output the data as a dictionary,
containing a ``key`` and the interpreted read data.  For landmark locations,
the data is returned in **the common way** for bob, which is ``(y, x)``!  The
following formats are currently accepted:

* ``'eyecenter'`` (for face images): Each file contains **only** the
  locations of the two eyes, in one row, as follows: ``re_x re_y le_x le_y``.
  The keys will be ``'reye'`` and ``'leye'``.

* ``'named'`` (for face images): Each   file contains lines with the
  landmark name and the two landmark locations,   e.g. ``reye re_x re_y``.

* ``'idiap'`` (for face images): The file format to   read Idiap specific
  annotation files. It will return up to 24 key points. 22 of these are read
  from the file, and the ``'reye'`` and ``'leye'`` are   estimated from the
  inner and outer corners of the eyes (if available).

.. note::

   ``Left`` and ``Right`` positions are always expected to be from the subject
   perspective.  This means that, e.g., the ``'leye'`` landmark usually has a
   **higher** x-coordinate than the ``'reye'``.
