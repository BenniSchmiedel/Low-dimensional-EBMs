.. doc documentation master file, created by
   sphinx-quickstart on Thu Mar 28 23:47:15 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to doc's documentation!
===============================

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
.. include:: Configuration.rst

Configuration
-------------
.. automodule:: Packages.Configuration

.. autofunction:: importer

.. literalinclude:: ../Packages/Configuration.py
    :pyobject: importer

Numerical Method (Runge Kutta 4th order)
----------------------------------------
.. automodule:: Packages.RK4

Functions
---------
.. automodule:: Packages.Functions
    :members:
    :private-members:
    :special-members:

.. literalinclude:: ../Packages/Functions.py
    :pyobject: R_ininsolalbedo


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
