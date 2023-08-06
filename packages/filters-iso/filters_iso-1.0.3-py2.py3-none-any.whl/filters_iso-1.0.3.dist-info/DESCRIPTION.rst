.. image:: https://travis-ci.org/eflglobal/filters-iso.svg?branch=master
   :target: https://travis-ci.org/eflglobal/filters-iso
.. image:: https://readthedocs.org/projects/filters/badge/?version=latest
   :target: http://filters.readthedocs.io/

===========
ISO Filters
===========
Adds filters for interpreting standard codes and identifiers, including:

- ISO 3166-1 alpha-2 and alpha-3 country codes.
- ISO 4217 currency codes.
- IETF Language Tags (aka BCP 47).

------------
Installation
------------
This package is an extension for the `Filters library`, so you can install it
as an extra to ``filters``:

.. code:: bash

   pip install filters[iso]


If desired, you can install this package separately.  This allows you to control
the package version separately from ``filters``.

.. code:: bash

   pip install filters-iso


.. _Filters library: https://pypi.python.org/pypi/filters


