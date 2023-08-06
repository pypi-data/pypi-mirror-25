MigVerify: Test and clean up Migrate-N infile with many sequence loci.
======================================================================

.. image:: https://travis-ci.org/andersgs/migverify.svg?branch=master
    :target: https://travis-ci.org/andersgs/migverify

INTRODUCTION
------------

In our experience, Migrate-N does not work well with monomorphic loci.
``migverify`` will go through your ``infile``, and output an
``infile_clean``.

By default, ``migverify`` will remove all loci that have fewer than two
haplotypes, and will remove loci with samples with more than 10% missing
data. These values can be changed.

INSTALLATION
------------

``migverify`` is written in Python3 (requires version >=3.6). It can be
installed with ``pip``:

::

    `pip3 install migverify`

To get the latest version:

::

    `pip3 install git+https://www.github.com/andersgs/migverify.git`

USAGE
-----

Installation will make available a script called ``run_migverify``,
which should be in your ``PATH``.

You can checkout the help with:

::

    `run_migverify --help`

Running with default settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    `run_migverify infile`

Filter out loci with fewer than 3 haplotypes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    `run_migverify -m 3 infile`

Filter out loci with samples with more than 20% missing data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    `run_migverify -p 0.2 infile`

QUESTIONS or ISSUES
-------------------

`GitHub Issues <https://github.com/andersgs/migverify/issues>`__

.. |Build Status| image:: https://travis-ci.org/andersgs/migverify.svg?branch=master
   :target: https://travis-ci.org/andersgs/migverify
