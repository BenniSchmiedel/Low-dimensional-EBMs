
***********
Source Code
***********

The project is seperated onto 5 python-packages with several submodules. 

The coremodule is the numerical integrator, the Runge-Kutta 4th order scheme defined in the rk4_ package.

The structure of the model is provided by the baseequation_ package. It builds up the physical model from a set of physical functions_ which are specified in the
functions package. 

In order to get a reasonable EBM structure you have to give a configurationfile (for details on how to create it, see Input) which is processed by the :doc:`configuration <code/configuration>` package. Along with the basic configuration of the model many required variables are introduced in the variables_ package, which can be running variables but also variables provided as output (for details on what to print out, see Output).

.. toctree:: 
    :maxdepth: 2
    
    code/rk4
    code/baseequation
    code/functions
    code/configuration
    code/variables
