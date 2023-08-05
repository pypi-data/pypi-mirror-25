.. vim: set fileencoding=utf-8 :
.. Thu 13 Oct 2016 10:34:35 CEST

.. _bob.db.base:

====================
 |project| Database
====================

A |project| db package (or *database*) contains a set of interfaces (API) to
programmatically query and access samples and metadata from raw data (usually)
stored on disk. Because of the growing number of packages of this nature, we
decided to centralise common functionality and management routines in this
package, to avoid constant re-writing of basic functionality. This guide
explains basic concepts of db packages, the common functionality that is available, how to
create your own and how to connect db packages to real-world applications.

A |project| db package is normally named ``bob.db.<name>``, where ``<name>``
corresponds to the original database name or an acronym. So, for example, for
the `Iris Flower Dataset`_, the corresponding db package is named
``bob.db.iris``. You should choose the name of your db package carefully so it
is relatively easy to figure out its relationship with the original raw data it
programmatically accesses.

The raw data of a database is, normally, not shipped with the equivalent
|project| db package. The reasons for these are twofold:

1. More often than not, raw data is very voluminous and cannot be stored on the
   Python Package Index (PyPI), where we post our packages.
2. Occasionally, data is subject to end-user license agreements, which must be
   undertaken between processors and data controllers directly. In this case,
   we're simply not entitled to distribute these raw data files.

In cases where both reasons 1 and 2, above, are non-issues, the |project| db package
*may* include the raw data. This decision is made by the package developer and
varies from case to case.

A |project| db package is a normal Bob package and should, without exceptions,
be developed by following the guidelines for any other package available at
:ref:`bob.extension`. To simplify maintenance and improve homogeneity between
different db packages, we further suggest you follow our
:ref:`bob.db.base_devguide`.


Documentation
-------------

.. toctree::
   :maxdepth: 2

   user-guide
   development-guide
   extend
   py_api


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. include:: links.rst
