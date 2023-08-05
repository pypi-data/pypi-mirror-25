========
Overview
========



Estimate hyper-parameter search using evolutionary algorithms

* Free software: MIT license

Installation
============

::

    pip install auto-tune

Documentation
=============

https://auto-tune.readthedocs.io/

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

0.0.1 (2017-09-01)
------------------

* First release on PyPI.


