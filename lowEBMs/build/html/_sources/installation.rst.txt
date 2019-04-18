
************
Installation
************

Python Package
==============

The simplest way to install ``lowEBMs`` is from source. 
To download and install ``lowEBMs`` with all its dependencies, go to the command line and type::
    
    pip install lowEBMs


Alternatively, you can clone the git repository of the source code with::

    git clone https://github.com/BenniSchmiedel/Climate-Modelling 

and manually run the setup.py which installs the package with all its dependencies::

    python setup.py install

(keep in mind to change to the directory where you cloned the repository to).

Dependecies
===========

To properly use this package there are several other packages required:

- Python (2.7 should work but I recommend higher versions, 3.5, 3.6 ...)
- ``numpy`` (for mathematical calculations)
- ``climlab`` (to import distributions of solar radiation)
- ``xarray`` (required by climlab)
- ``attrdict`` (required by climlab)

- ``matplotlib`` (for plotting)
- ``netCDF4`` (for comparison to observational data stored as netCDF-files)


