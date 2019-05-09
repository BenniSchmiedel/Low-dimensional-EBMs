
************
Installation
************

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

Python Package
==============

The simplest way to install ``lowEBMs`` is from source. 
To download and install ``lowEBMs`` with all its dependencies, go to the command line and type::
    
    pip install lowEBMs


Alternatively, you can clone the git repository of the source code and manually run the setup.py which installs the package with all its dependencies::

    git clone https://github.com/BenniSchmiedel/Climate-Modelling 

    python setup.py install

(keep in mind to change to the directory where you cloned the repository to).


Export Tutorial Files
=====================

``lowEBMs`` comes with a :doc:`list of tutorial files <tutorials>` supplemented in a subfolder of the package. When the package is installed via pip, it is automatically inbound in your specific python environment. To easily extract this tutorial files, a copy function is added which allows you to export the *jupyter notebooks* and *configuration.ini* files to your prefered directory.

There are two options:
Go to the command line, change your directory to the one where you want the files and use::

     python -c "from lowEBMs import Tutorial_copy; Tutorial_copy()"

Or go to the command line and add your prefered path to the funtion::

     python -c "from lowEBMs import Tutorial_copy; Tutorial_copy(path='/insert/your/path/here')"


