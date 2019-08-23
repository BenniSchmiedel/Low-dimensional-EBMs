
************
Installation
************

Dependecies
===========

To properly use this package there are several other packages required:

- Python (2.7 should work but I recommend higher versions, 3.5, 3.6 ...)
- ``numpy`` (for mathematical calculations)

- ``matplotlib`` (for plotting)
- ``netCDF4`` (for comparison to observational data stored as netCDF-files)
- ``tqdm`` (for progress visualization)
Python Package
==============

The simplest way to install ``lowEBMs`` is from source. 
To download and install ``lowEBMs`` with all its dependencies, go to the command line and type::
    
    pip install lowEBMs

or (if you have python 2 and python 3 installed and want to install it on python 3)::

	pip install lowEBMs

Alternatively, you can clone the git repository of the source code and manually run the setup.py which installs the package with all its dependencies::

    git clone https://github.com/BenniSchmiedel/Low-dimensional-EBMs.git

    python setup.py install

(keep in mind to change to the directory where you cloned the repository to).


Export Tutorial Files
=====================

``lowEBMs`` comes with a :doc:`list of tutorial files <tutorials>` supplemented in a subfolder of the package. When the package is installed via pip, it is automatically inbound in your specific python environment. To easily extract those *jupyter notebooks* and *configuration.ini* files to your preferred directory, do the following:

Open the terminal, change your directory to the one where you want the files and use::

     python -c "from lowEBMs import Tutorial_copy; Tutorial_copy()"

.. Note::
	You can specify the output directory as argument with ``Tutorial_copy(path='/outputdir')``

Export Forcing Files
====================

There are also PMIP3 forcing datasets included which can be exported the same way as the tutorial files.

Open the terminal, change your directory to the one where you want the files and use::

     python -c "from lowEBMs import Forcing_copy; Forcing_copy()"

.. Note::
	You can specify the output directory as argument with ``Forcing_copy(path='/outputdir')``
