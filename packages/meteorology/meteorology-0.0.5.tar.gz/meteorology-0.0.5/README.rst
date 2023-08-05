meteorology Python package 
==========================

|build-badge| |docs-badge| |coverage-badge| |pypi-badge|

This package provides routines for meteorological calculations.

Principles
++++++++++

Numbers are treated in SI units (except for some documented exceptions).

Routines expect ``numpy.ndarray`` as input but may work with lists or floats as
well.

Capabilities
++++++++++++

Currently, ``meteorology`` can't do much :-)

But stay tuned! More is about to come!

Install
+++++++

This package is on `PyPi <https://pypi.python.org/pypi/meteorology>`_. To
install ``meteorology``, run

.. code:: sh

    pip install --user meteorology

.. note::
    
    You might need to use ``pip3`` for your setup.


Documentation
+++++++++++++

You can find detailed documentation of this package 
`here on on Gitlab <https://nobodyinperson.gitlab.io/python3-meteorology/>`_.

Development
+++++++++++

The following might only be interesting for developers

Local installation
------------------

Install this module from the repository root via :code:`pip`:

.. code:: sh

    # local user library under ~/.local
    pip3 install --user .
    # in "editable" mode
    pip3 install --user -e .

Testing
-------

.. code:: sh

    # Run all tests
    ./setup.py test

.. code:: sh

    # install coverage
    pip3 install --user coveralls
    # Run all tests and determine a test coverage
    make coverage

Versioning
----------

- ``make increase-patch`` to increase the patch version number
- ``make increase-minor`` to increase the minor version number
- ``make increase-major`` to increase the major version number


.. |build-badge| image:: https://gitlab.com/nobodyinperson/python3-meteorology/badges/master/build.svg
    :target: https://gitlab.com/nobodyinperson/python3-meteorology/commits/master
    :alt: Build

.. |docs-badge| image:: https://img.shields.io/badge/docs-sphinx-brightgreen.svg
    :target: https://nobodyinperson.gitlab.io/python3-meteorology/
    :alt: Documentation

.. |coverage-badge| image:: https://gitlab.com/nobodyinperson/python3-meteorology/badges/master/coverage.svg
    :target: https://nobodyinperson.gitlab.io/python3-meteorology/coverage-report
    :alt: Coverage

.. |pypi-badge| image:: https://badge.fury.io/py/meteorology.svg
   :target: https://badge.fury.io/py/meteorology
   :alt: PyPi

