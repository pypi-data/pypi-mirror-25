========
Overview
========



A tool to work with tModLoader .tmod files.

* Free software: ISC license

Installation
============

::

    pip install tmod

Documentation
=============

https://python-tmod-tools.readthedocs.io/

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

0.1.0 (2017-09-29)
------------------

* First release on PyPI.


