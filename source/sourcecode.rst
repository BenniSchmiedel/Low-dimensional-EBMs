
***********
Source Code
***********

The project is seperated onto 5 python-packages with several submodules. 

The coremodule is the numerical integrator, the Runge-Kutta 4th order scheme.
.. toctree:: 
    :maxdepth: 2
    
    rk4

The structure of the model is provided by the baseequation package, configuration through a configurationfile (for details see Input). 
.. toctree::
    :maxdepth: 2

    configuration
    variables

In order to get a reasonable EBM, a set of physical functions are specified in the 
 
