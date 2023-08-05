========
Overview
========



Minimal state machine

* Free software: BSD license

Installation
============

::

    pip install fsmpy

Documentation
=============

https://pyfsm.readthedocs.org/

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

0.1.3 (2017-15-09)
-----------------------------------------

* Updated docs
* Corrections to code
* ci updated


0.1.0 (2016-04-18)
-----------------------------------------

* First release on PyPI.


