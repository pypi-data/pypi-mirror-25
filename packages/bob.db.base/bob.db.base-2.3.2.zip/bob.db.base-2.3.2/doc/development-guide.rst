.. vim: set fileencoding=utf-8 :
.. Andre Anjos <andre.anjos@idiap.ch>

.. _bob.db.base_devguide:

===================
 Development Guide
===================

The best way to create a new database for |project| is by first looking at
examples of working databases that are similar to the dataset you want to
create an API for.  The name of database interface packages for |project|
usually start with ``bob.db.``. Take a look at our `available packages`_ list
to find available |project| db packages.

In this development guide, we provide a list of guidelines on how to structure
your database and solve common development issues. We'll use the example on the
:ref:`bob.db.base_userguide` of the Samples database (see:
:ref:`bob.db.base_sampledb`) inside this guide.

.. warning::

   This development guide is **not** a replacement for our official
   :ref:`bob.extension` guide, which explains how to structure packages. It
   only contains *additional* guidelines you should consider when developing db
   packages.


Naming Convention
-----------------

All database packages should be named ``bob.db.<dataset-slug>`` where
``<dataset-slug>`` corresponds to a short name for the dataset you're trying to
bind. As a general recommendation, use small and catchy names. Avoid long names
which are confusing and difficult to type and remember.

Examples of good, catchy names:

  * ``atnt``: for the AT&T faces database (see ``bob.db.atnt``)
  * ``iris``: for Fisher's Iris flower dataset (see ``bob.db.iris``)
  * ``mobio``: for the Mobio biometric database (see ``bob.db.mobio``)

Examples of more inappropriate names (avoid these):

  * ``database_cut1_whatnot`` (avoid very long package names)
  * ``test-mine`` (avoid dashes - they don't play well with python)
  * ``set_v2`` (avoid version names)


Module Organization
-------------------

Most people find it beneficial to share a common module organization so that it is
easy for everyone to maintain different databases. This is our typical
directory organization, which you should try to adhere to:

.. code-block:: text

   bob.db.<dataset-slug>
   +-- bob
       +-- __init__.py #namespace init for "bob"
       +-- db
           +-- __init__.py #namespace init for "bob.db"
           +-- <dataset-slug>
               +-- __init__.py
               +-- models.py
               +-- query.py
               +-- driver.py
               +-- test.py


The file ``models.py`` include all classes and functions that represent the
task described by the database. If, for example, the database is composed of
image samples and associated tags, possible classes in ``models.py`` may
include ``Sample`` and ``Tag``. See an example at
:py:mod:`bob.db.base.tests.sample.Sample`.

The file ``query.py`` normally only contains the definition of the ``Database``
class. Finally, the file ``driver.py`` contains the connector allowing the
command-line program ``bob_dbmanage.py`` to interface with your python API for
specific tasks.

It is conventional that all elements inside ``models.py`` and ``query.py`` are
imported into the package's ``__init__.py`` to avoid obliging the user to understand
implementation specificities.

The ``driver.py`` should declare a database with a name matching
``<dataset-slug>`` and implement at least the following methods from
:py:class:`bob.db.base.driver.Interface`:

* :py:meth:`bob.db.base.driver.Interface.name`: Here, insert the
  ``<dataset-slug>``. See an example in the source code for
  :py:meth:`bob.db.base.tests.sample.driver.Interface.name`
* :py:meth:`bob.db.base.driver.Interface.version`: Here, insert the
  db package version. This is typically done by using ``pkg_resources``. See an
  example in the source code for
  :py:meth:`bob.db.base.tests.sample.driver.Interface.version`
* :py:meth:`bob.db.base.driver.Interface.files`: Here, insert the metafiles this
  package contains (see :ref:`bob.db.base_metafiles`)
* :py:meth:`bob.db.base.driver.Interface.type`: Returns the type of the backend
  implementation. The return value of this function on your driver
  implementation will allow ``bob_dbmanage.py`` to provide specialized actions
  for SQL-backend db package implementations. The value returned should be
  either ``builtin`` or ``sqlite``

The file ``test.py`` should contain basic test units for all functionality
shipped with the database. This should contain, at least:

* Tests for reading out samples,
* Tests for sub-selection of samples using parameters of the ``objects()``
  method.

Documentation should accompany the package and indicate how to use the db
package Python API and its command-line interface, with examples and
appropriate doctests.


File-based Databases
--------------------

If the raw dataset in question is composed of files, it may be beneficial to
re-use (through inheritance) some classes available in this package. Read the
documentation of:

* :py:class:`bob.db.base.File`
* :py:class:`bob.db.base.Database`

In this case, make sure your ``Sample`` objects inherit from ``File``, as is,
for example, the case for :py:class:`bob.db.base.tests.sample.Sample`.
Equivalently, you may also benefit from some database constructions if your
``Database`` inherits from :py:class:`bob.db.base.Database`.


SQL-Backend for File Databases
------------------------------

So far, we have exemplified the implementation and organization of a simple db
package, for which the dataset contained only a few raw image samples and a
single evaluation protocol. For very complex problems, in which datasets
contain many hundreds of raw samples and multiple evaluation protocols, a more
complex modelling of the *internals* of the |project| db package may be
required. In such cases, we recommend prospective developers to consider using
alternative techniques (as opposed to simple file lists) for *implementing* the
*internals* of their db packages. In this guide, we introduce how to handle
database backends using SQLite_ through SQLAlchemy_, for which support is
built into this package.

It is important to note that using a simple or complex *backend* implementation
for storing and retrieving iterables from the database **must** be completely
transparent to the db package user. Users of your |project| db package are
primarily interested in iterating over (sub-selected) samples and executing
their pipelines. The choice of the *backend* to use for a given db package
**must be**, therefore, totally opaque to them.

.. warning::

   Understanding SQL, database structuring, normalization and how to deploy an
   ORM (such as SQLAlchemy_) is beyond the scope of this guide. Search for
   guides and tutorials on the net to familiarize yourself with these subjects
   **before** trying to make a backend based with SQLAlchemy_.


Module Organization for SQLite
==============================

The module organization of typical SQL-backend db packages is very similar to
simple file-based ones:

.. code-block:: text

   bob.db.<dataset-slug>
   +-- bob
       +-- __init__.py #namespace init for "bob"
       +-- db
           +-- __init__.py #namespace init for "bob.db"
           +-- <dataset-slug>
               +-- __init__.py
               +-- models.py
               +-- query.py
               +-- create.py
               +-- driver.py
               +-- db.sql3
               +-- test.py


The file ``models.py`` will contain the definition of the SQL tables for every
component in the database. One possible table in the SQL database will be that
of ``Sample``'s. If you're designing a db package for a dataset with a
one-file-per-sample storage model, ensure your ``Sample`` class also inherits
from :py:class:`bob.db.base.File` to provide a uniform experience to users
already used to bob.db interfaces. Other tables and relationships are optional
and should map your problem alongside its contraints to a proper database
schema.

The file ``query.py`` will contain the definition of the ``Database`` class. We
recommend you consider, in this case, inheriting from
:py:class:`bob.db.base.SQLiteDatabase`, which provides a number of utilities to
handle file-based datasets with an SQLite backend. You'll find examples among
different |project| db packages for this. Typically, elements returned by the
``Database`` class ``objects()`` in this case are ORM objects from SQLAlchemy_,
representing a row in a table of your internal database. However, these objects
behave *exactly* the same as non-SQL ``Sample`` objects and allow the user to
transparently load file contents and meta data using simple API calls.

The file ``driver.py`` will be very similar to other databases, with a few
exceptions:

1. The :py:meth:`bob.db.base.driver.Interface.files` implementation will return
   at least the path to the ``db.sql3`` file, which will contain the db package
   backend information. This will allow ``bob_dbmanage.py`` to download this
   file in installations it misses or upload updated versions of it to our
   central server.
2. SQL-backend db packages normally install a ``create`` command at the driver
   :py:class:`bob.db.base.driver.Interface` allowing developers to create the
   ``db.sql3`` file from scratch. It is important to have a create command so
   that the database can be re-created in case of changes.

The file ``create.py`` typically contains routines for the creation of
``db.sql3`` from scratch and is not required *per se*. Functions and modules
implemented in ``create.py`` are imported into ``driver.py`` for the
instantiation of the ``create`` command. See examples in db packages for
mobio_ or verafinger_.

Finally, the file ``test.py`` should contain the usual set of tests, as for
simpler databases.

The package documentation should contain all information regarding the Python
API, command-line interface and, if possible, the SQL-backend database design
(showing tables, column types and constraints where adequate).


.. _bob.db.base_metafiles:

Metafiles Not Shipped with the Database
---------------------------------------

Very often, |project| db packages require the use of support files which should
exist **inside** the package structure, but are not kept under version control.
Reasons for this may be that these *meta*-files are too large or can be recreated
programmatically. Such files may be of different natures and each developer
should be able to recognize those easily when the situation occurs. Here is a
non-exhaustive list of possible use cases for such metafiles:

* Annotations
* File lists (for example, defining evaluation protocols or such)
* Auxiliary database files (for example, Sqlite database files)
* Samples (in case you want to ship them with your database)

In order to mitigate issues related to management, this package provides a set
of utilies to handle such *meta*-files more easily. To prepare your package for
handling metafiles, you must first make sure that the ``driver.py``
``Interface`` class returns a non-empty list as a result of the ``files()``
method.

Each entry in the list returned by ``files()`` should represent the **full**
path of the file, considering the current installation location. The method
``type()`` of :py:class:`bob.db.base.driver.Interface` should return `sqlite`.

A typical implementation for SQL-backend db packages is like this:

.. code-block:: python

   def files(self):

       from pkg_resources import resource_filename
       raw_files = ('db.sql3',)
       return [resource_filename(__name__, k) for k in raw_files]

   def type(self):

       return 'sqlite'


Metafiles Shipped with the Python Package
=========================================

If you'd like the file ``db.sql3`` to be shipped to PyPI when you publish
your package, make sure to include ``db.sql3`` in the package's ``MANIFEST.in``
file. Otherwise, you are not required to add this file to the package manifest.


Download Missing Files for Large Databases
==========================================

If you declared extra metafiles with your driver's ``files()`` implementation,
it is possible to both store and retrieve metafiles from a central file server
running at Idiap (see http://www.idiap.ch/software/bob/databases/latest). All
metafiles of a package are wrapped into a single tar-ball and copied to the
server upon uploading. The reverse process takes place when downloading.

This mechanism allows third-parties to download sources from the version
control repository and retrieve the metafiles.

To download and install metafiles for a package, do:

.. code-block:: sh

	 $ bob_dbmanage.py <database-name> download

For example, you can use the special database name ``all``, together with the
flag ``--missing`` to download the missing metafiles of all installed databases
like this:

.. code-block:: sh

	 $ bob_dbmanage.py all download --missing


Low and High-Level Interfaces
-----------------------------

Bob database interfaces come in two flavours:

1. **Low-level interfaces** allow developers to create programmatic APIs to
   access samples and metadata available with databases as they are distributed
   by their controllers. Examples of this are the Samples database in this
   package or APIs provided in any other db packages. The main objective of a
   low-level database interface is to provide access to **all** information
   provided with the database, without direct regards to the specific task it
   was originally conceived for. The reasoning behind this design
   choice lies in the fact that databases very often find second lives in different
   tasks than originally intended. By providing access to **all** information
   available from the raw dataset, a developer potentialises such (re-)use
   cases.
2. **High-level interfaces** allow developers to create programmatic APIs to
   *bind* low-level interfaces to frameworks that perform a *specific*
   function. Because each *low-level* databases should be created to export all
   available information, in some cases it is possible to re-use an existing
   db package as input to a different task than it was originally conceived
   for. Here are some examples:

   * Re-use a database for emotion recognition to perform remote
     photo-plethysmographic (see ``bob.db.hci_tagging``)
   * Re-use a face recognition database to train a face detector
   * Re-use a speaker recognition database to do speech recognition

   High-level database interfaces are, therefore, very task specific and
   normally sit together with frameworks doing high-level experimental
   research. Examples of such frameworks are :ref:`bob.bio.base <bob.bio.base>`
   (biometric recognition) and :ref:`bob.pad.base <bob.pad.base>` (presentation
   attack vulnerability and detection). Checkout their user guides for more
   information on specific high-level implementations required by those tasks.


.. Place your references here:
.. _sqlite: https://www.sqlite.org/
.. _sqlalchemy: https://www.sqlalchemy.org/
.. _available packages: http://www.idiap.ch/software/bob/packages/
.. _mobio: https://gitlab.idiap.ch/bob/bob.db.mobio/tree/master/bob/db/mobio
.. _verafinger: https://gitlab.idiap.ch/bob/bob.db.verafinger/tree/master/bob/db/verafinger
