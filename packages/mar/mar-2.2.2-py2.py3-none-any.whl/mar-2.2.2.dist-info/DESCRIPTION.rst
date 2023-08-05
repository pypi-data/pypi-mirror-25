========
Overview
========



Package for handling Mozilla Archive files. MAR file format is documented at https://wiki.mozilla.org/Software_Update:MAR

* Free software: MPL 2.0 license

Usage
=====

To list the contents of a mar::

    mar -t complete.mar

To list the contents of a mar with extra detail::

    mar -T complete.mar

To extract a mar::

    mar -x complete.mar

To extract, and uncompress a bz2 compressed mar::

    mar -j -x complete.mar

To verify a mar::

    mar -k :mozilla-nightly -v complete.mar

To create a mar, using bz2 compression::

    mar -j -c complete.mar *

To create a mar, using xz compression::

    mar -J -c complete.mar *

To create a signed mar::

    mar -J -c complete.mar -k private.key -H nightly -V 123 tests

Installation
============

::

    pip install mar

Documentation
=============

https://mar.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox


Changelog
=========

2.0 (2016-12-16)
-----------------------------------------

* First release on PyPI.


