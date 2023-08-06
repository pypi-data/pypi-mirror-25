Overview
========



Various unsorted Python utilities.

Installation
------------

::

    pip install seveno_pyutil

Documentation
-------------

::

    python setup.py build_sphinx

Tests
-----

::

    py.test

or against multiple Python versions

::

    pip install tox
    tox

Development mode
----------------

Install

::

    python setup.py develop --uninstall

Install with extra dev packages

::

    pip install -e .[dev]

Uninstall

::

    python setup.py develop --uninstall

Changelog
=========

0.2.0 (2017-10-06)
------------------

* Added SQL log coloring formatter (for Django logs)

0.1.1 (2017-10-02)
------------------

* DynamicContextFormatter now keeps context in thread local.

0.1.0 (2017-09-26)
------------------

* Initial release


