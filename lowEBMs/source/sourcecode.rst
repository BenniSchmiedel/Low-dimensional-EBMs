
***********
Source Code
***********

The project is seperated onto 5 python-packages with several submodules. 

The coremodule is the numerical integrator, the Runge-Kutta 4th order scheme defined in ``lowEBMs.Packages.RK``.

The structure of the model is provided by ``lowEBMs.Packages.ModelEquation``. It builds up the EBM from a set of physical functions, specified in ``lowEBMs.Packages.Function``. 

In order to get a reasonable EBM structure you have to give a configurationfile (for details on how to create it, see :doc:`Input <input>`) which is processed by ``lowEBMs.Packages.Configuration``. Along with the basic configuration of the model many required variables are defined in ``lowEBMs.Packages.Variables``, which may be running variables but also variables provided for later output (for details on what to print out, see :doc:`Output <output>`).

lowEBMs.Packages
================

.. toctree:: 
    :maxdepth: 2
    
    code/rk4
    code/modelequation
    code/functions
    code/configuration
    code/variables
