meteorology Python package 
==========================

|build-badge| |docs-badge| |coverage-badge| |pypi-badge|

This package provides routines for meteorological calculations.

Principles
++++++++++

Numbers are treated in SI units (except for some documented exceptions).

Routines are tested to work with ``numpy.ndarray`` and floats as input but may
work with lists or other data types as well.

Everything is tested and supposed to return correct values. Warnings are given
if invalid values occur. Unphysical values are masked with ``NaN``.

Capabilities
++++++++++++

Currently, ``meteorology`` can only do very basic things:

- converting between degrees **Celsius** and **Kelvin**
    
.. code:: python
        
    from meteorology.temperature import cel2kel, kel2cel
    cel2kel( np.array( [0,  -20.4,   30.1] ) )
    # array([ 273.15,  252.75,  303.25])
    kel2cel( np.array( [0, 273.15, 345.54] ) )
    # array([-273.15,    0.  ,   72.39])
    
- calculating the **saturation water vapour pressure** at a given temperature
    
.. code:: python
        
    from meteorology.humidity import saturation_water_vapour_pressure as e_s
    e_s( np.array( [273.15,  250.1, 320 ] ) )
    # array([   611.2       ,     76.7876872 ,  10532.91207709])
        
- calculating the **total blackbody radiation** at a given temperature
    
.. code:: python
        
    from meteorology.radiation import blackbody_radiation
    blackbody_radiation( np.array( [0, 273.15,  250.1, 1000 ] ) )
    # array([     0.  ,    315.6574093 ,    221.85332157,  56703.67 ])

- adjusting a **radiation temperature** to **another emissivity**:

.. code:: python

    from meteorology.radiation import \
        adjust_radiation_temperature_to_other_emissivity as adjtemp
    adjtemp( T=300, emissivity_old=0.9, emissivity_new=0.8, T_ambient=285 )
    # 293.92070228214675
        

But stay tuned! More is about to come!

Install
+++++++

This package is on `PyPi <https://pypi.python.org/pypi/meteorology>`_. To
install ``meteorology``, run

.. code:: sh

    pip install --user meteorology

.. note::
    
    You might need to use ``pip3`` or skip the ``--user`` for your setup.


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

