.. vim: set fileencoding=utf-8 :
.. Andre Anjos <andre.anjos@idiap.ch>


.. _bob.db.base_userguide:

===========================
 Using |project| Databases
===========================

|project| database packages can be used to query databases for samples and
associated metadata. The queries can be done both in Python or through a
command-line-based application (see :ref:`bob.db.base_devguide`).


Samples
-------

A sample represents one atomic data point from the dataset. For example, this
may mean:

* An image of a person's face in a face recognition database,
* An audio track within a file (with multiple audio tracks) in a speech
  recognition database,
* A row in a large file containing measurements of flower petals (width and
  length),
* A phrase in a collection of documents stored in an SQL server.

Because sample storage varies from dataset to dataset, it is difficult to
provide a one-fits-all set of tools to read out samples from any kind of
support. |project| provides typical readout routines for samples stored in
files (one-file-per-sample model), while other tools for reading subsets of
data from files are provided by third-party libraries or within the Python
standard library.

A programmatic interface to a database represents an abstraction of this
concept and should allow usage of such samples **independently** of the storage
model used by the raw dataset, allowing the user to, as transparently as
possible, access information with minimal setup.

Currently, among all types of samples implemented through different db packages
in the |project| eco-system, file-based samples are probably the most used. In
a file-based storage, typically, one raw sample corresponds to data stored in a
single file on the file system. Very often, samples are organized in
subdirectories and share a common root installation directory.


.. _bob.db.base_sampledb:

Example Database
----------------

We'll use a hypothetical image database to exemplify database usage and
development in this guide. This database is small and its raw files are
included with this package (``tests/sample/data`` directory, on the root
of the package).

This is its directory organization:

.. code-block:: text

   +-- dir1
   |   +-- sample1-1.png
   |   +-- sample1-1.txt
   |   +-- sample1-2.png
   |   +-- sample1-2.txt
   +-- dir2
   |   +-- sample2-1.png
   |   +-- sample2-1.txt
   |   +-- sample2-2.png
   |   +-- sample2-2.txt
   +-- dir3
       +-- sample3-1.png
       +-- sample3-1.txt
       +-- sample3-2.png
       +-- sample3-2.txt


Each sample in this database has the suffix ``.png`` and corresponds to an
image. For each image, there is a matching file containing tag annotations
(2 per image, one tag per line) indicating what the image file contains and
the dominant color. The tag files have a ``.txt`` suffix.

The hypothetical task this database was primarily designed for is "dominant
color recognition": You get an image and you must tell which color is the
dominant color in the image.

The authors of this database defined a usage protocol for the images in the
database to allow different publications to be compared fairly.
Images ending with ``-1.png`` should be used for training and/or validation,
while images ending with ``-2.png`` should be used for testing (i.e., may not
be used for adjusting system hyper-parameters).

Your task is to devise a programmatic python-API allowing users of this db
package interface to easily select ``train`` or ``test`` images for modelling
and testing their classifiers respectively.


The Python API
--------------

There are no firm project standards for the pythonic API of a |project| db
package, though we advise package developers to follow guidelines (see
:ref:`bob.db.base_devguide`) which ensure homogeneity through different
packages. Typically, interfaces provide a ``Database`` class, allowing the user
to build an object that will be used to access raw data samples (and associated
metadata) available in the dataset, possibly constrained to a number of
selector parameters for sub-selecting samples.

The constructor of a database is pretty much database dependent, but it
generally allows the user to set up installation-dependent parameters such as,
for example, the location where raw data files may be stored, in case those are
not shipped with the |project| db package. Examples in this guide try to
abstract away from such specificities in order to provide a general understanding
of the framework. When specific information is required about a db package
interface, we recommend you read the specific API documentation for that
package.

The usage of a db package API normally goes through 3 stages:

1. Construct a ``Database`` object
2. Use the ``Database.objects()`` method to query for samples
3. Use the returned list of samples in your application.

Here is an example of a |project| db package interface in use:

.. doctest:: interface

   >>> from bob.db.base.tests.sample import Database
   >>> db = Database()
   >>> for sample in db.objects():
   ...     print(sample)
   Sample("dir1/sample1-1")
   Sample("dir1/sample1-2")
   Sample("dir2/sample2-1")
   Sample("dir2/sample2-2")
   Sample("dir3/sample3-1")
   Sample("dir3/sample3-2")

In this example, the user imports the data package (line 1), instantiates the
database (line 2) and then starts iterating over its objects (line 3). Each
object returned by the ``objects()`` method represents one sample from the
database.

Each sample in the database in turn provides a number of methods
to access information about its raw or meta-data, allowing the user to create a
*continuous processing* pipeline.

Database sample objects often provide a ``load()`` allowing the
pointed object to be loaded in memory:

.. doctest:: interface

   >>> all_samples = list(db.objects())
   >>> f = all_samples[0] #get only sample 0
   >>> type(f)
   <class 'bob.db.base.tests.sample.Sample'>


Each "sample" returned by :py:meth:`bob.db.base.tests.sample.Database.objects`
is actually an object of class :py:class:`bob.db.base.tests.sample.Sample`,
representing the abstraction of a single (raw) dataset file. File objects in
this package also contain a ``path`` variable that point to their relative
location with respect to a database root directory:

.. doctest:: interface

   >>> f.path # doctest: +ELLIPSIS
   'dir1/sample1-1'


You may use the method :py:meth:`bob.db.base.tests.sample.Sample.make_path` to
construct paths which contain both a prefix directory and a suffix extension.
For example, to build a full path to an installed image in the raw dataset,
call this method without any parameters:

.. code-block:: python

   >>> f.make_path()
   '/installation/path/.../dir1/sample1-1.png'

You may override the default directory and extensions that are attached to the
return path. For example:

.. doctest:: interface

   >>> f.make_path('/another/path', '.hdf5')
   '/another/path/dir1/sample1-1.hdf5'

You may load the contents of the image file pointed by this database entry
using the :py:meth:`bob.db.base.tests.sample.Sample.load` method:

.. doctest:: interface

   >>> import bob.io.image
   >>> image = f.load()
   >>> type(image) #doctest: +ELLIPSIS
   <... 'numpy.ndarray'>
   >>> image.shape
   (3, 128, 128)
   >>> image.dtype
   dtype('uint8')


Pipelines
=========

In data processing pipelines, it is typical to save the intermediate result of
processing images to temporary files you'll need to load later. In Bob, those
files are normally HDF5 files (see :ref:`bob.io.base`). You can easily create a
processing pipeline re-using the database interface like this:

.. code-block:: python
   :linenos:

   >>> image = f.load()
   >>> processed = processor(image)
   >>> f.save(processed, '/path/to/processed', '.hdf5')
   # stores "processed" in an HDF5 file file named /path/to/processed/s1/9.hdf5

Line 1 loads the image. Line 2 processes the image and generates a processed
version of the image (e.g. as a :py:class:`numpy.ndarray`). Line 3 uses
this db package interface to save the resulting file, *respecting* the original
database structure. This is convenient because of two reasons:

1. You can manually inspect the directory containing processed images and
   quickly find the processed version of any original image in the database;
2. You can re-use :py:meth:`bob.db.base.tests.sample.Sample.load` to reload the
   processed file and continue the pipelining indefinitely.

For example, suppose one would like to re-process the processed image above, it
is possible to repeat the coding pattern above, now defining input and output
directories:

.. code-block:: python

   >>> processed = f.load('/path/to/processed', '.hdf5')
   >>> reprocessed = reprocessor(processed)
   >>> f.save(reprocessed, '/path/to/reprocessed', '.hdf5')


Selectors
=========

You may iterate over a subset of samples from the sample database using
parameters to :py:meth:`bob.db.base.tests.sample.Database.objects` (check its
documentation for details). For example, to iterate over all the training
images, one can write:

.. doctest:: interface

   >>> training_images = []
   >>> for sample in db.objects(group='train'):
   ...   training_images.append(sample.load())


Command-line Interface
----------------------

The command-line interface allows users to check or export information encoded
in Python API via the console. Its main purpose is to allow quick
administrative and sanity verifications. The most important command-line option
for the main database program is ``--help``. If you pass it to the main
program, it prints a list of all currently installed databases:

.. code-block:: sh

   $ bob_dbmanage.py --help
   usage: bob_dbmanage.py [-h] {samples,all} ...

   This script drives all commands from the specific database subdrivers.

   optional arguments:
     -h, --help     show this help message and exit

   databases:
     {samples,all}
       samples      Samples dataset
       all          Drive commands to all (above) databases in one shot

     For a list of available databases:
     >>> bob_dbmanage.py --help

     For a list of actions on a database:
     >>> bob_dbmanage.py <database-name> --help


From the example above, one observes a single db package is installed on that
environment, called ``samples`` (our example database). The entry ``all``
refers to a *shortcut* allowing the user to interact with all installed
databases at once.

Each database interface implementation is free to set up any number of commands
that may be required for command-line usage. To access the list of commands
available for the ``samples`` use the ``--help`` command-line option again:

.. code-block:: sh

   $ bob_dbmanage.py samples --help
   usage: bob_dbmanage.py samples [-h] {version,files,dumplist,checkfiles} ...

   optional arguments:
     -h, --help            show this help message and exit

   subcommands:
     {version,files,dumplist,checkfiles}
       version             Outputs the database version
       files               Prints the current location of raw database files.
       dumplist            Dumps list of files based on your criteria
       checkfiles          Check if the files exist, based on your criteria


Each of the commands produces a different output and runs different routines. The
``version`` command, for example, prints the version of the database:

.. code-block:: sh

   $ bob_dbmanage.py samples version
   samples == 2.2.1b0

The command ``dumplist`` dumps a list of files that belong to the database:

.. code-block:: sh

   $ bob_dbmanage.py samples dumplist --directory='' --extension=''
   dir1/sample1-1
   dir1/sample1-2
   dir2/sample2-1
   dir2/sample2-2
   dir3/sample3-1
   dir3/sample3-2

The interface provided by the samples db package also allows the user to filter
down the printed list of files, to only print, for instance, files that belong
to the train set using the command-line option ``--group``:

.. code-block:: sh

   $ bob_dbmanage.py samples dumplist --group=train --directory='' --extension=''
   dir1/sample1-1
   dir2/sample2-1
   dir3/sample3-1

The command ``checkfiles`` runs a file search to make sure all files for the
database (or a given ``group``) are available on a base directory. This is
useful, for example, to check the completeness of a pipeline after it was run.
Suppose, for instance, that we ran through the samples database, a script to
process all images and extract color histograms which we saved in a directory
called ``histograms``. Now, we would like to check if all files have been correctly
processed. In this case, we can simply do:

.. code-block:: sh

   $ bob_dbmanage.py samples checkfiles --directory='histograms' --extension='.hdf5'
   Cannot find file "histograms/dir1/sample1-2.hdf5"
   Cannot find file "histograms/dir2/sample2-1.hdf5"
   2 files (out of 6) were not found at "histograms"

The example output shown above indicates that our earlier pipeline possibly missed
two files.
