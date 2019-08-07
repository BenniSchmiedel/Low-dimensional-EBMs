
**********
How to use
**********

Here a brief introduction is given on how to get from a given input, which initializes the EBM you want to run, to an output, e.g. the global temperature propagation over time or the temperature distribution over a spatial grid representing the earth.

We will write a small python script, which will do this in a few steps. As it is easier to visualize the output in a plot and modify it, I recommend to perform this steps in a jupyter notebook.

Step 0: Import packages
=======================

Before you can use any module of this package you have to import the core modules::

    import matplotlib as plt
    import numpy as np
    from lowEBMs.Packages.Configuration import importer 
    from lowEBMs.Packages.Variables import variable_importer
    from lowEBMs.Packages.RK4 import rk4alg
    from lowEBMs.Packages.ModelEquation import model_equation

This will import all needed modules.

First Step: Import model configuration
======================================

The way this project is built up enables to take any physical function implemented and merge them to create the basis of a desired EBM, which will be our input.
The input will be created manually and is stored in a **configuration.ini** file. Details on how to create and structure **.ini** files is given in :doc:`input <input>`. 

.. Important::
    The configuration.ini file will provide the physical sense of the EBM!

For now you can simply use the **EBM0D_simple_config.ini** file which imports a 0D EBM with a model run over 10 year and a stepsize of integration of 1 day. A demonstration on how to reproduce this **.ini** file is given in :ref:`Example Input 0D-EBM <0Dconf>`.

To import this file use the ``importer``-function::

    configuration=importer('filename')

.. Note::
    In case you work in another directory than the installation directory of the project or get the error 'File not found', add the additional argument path: **importer('filename',path='path/to/your/configuration.ini')**. The path can be a relative or full path to where your **configuration.ini** is located.
 

``configuration`` is an dictionary which contains all required input parameters. To seperate them for a clearer structure you can use::

    eq=configuration['eqparam']
    rk4=configuration['rk4input']
    fun=configuration['funccomp']
    ini=configuration['initials']

These are four dictionaries which contain the information needed for the base equation, the runge-kutta algorithm, the functions used and the initial conditions.

Second Step: Import variables
=============================

As next step the configuration we just imported has to be distributed on different variables. For example arrays of initals conditions are calculated or arrays for the output will be created. To do so we can simply use the ``variable_importer``::

    variable_importer(configuration)

Third Step: Let the model/algorithm run
=======================================

Now we are ready to run the algorithm with the ``rk4alg`` function. It requires the ``model_equation`` function and the dictionaries we seperated before (maintain the order)::

    outputdata=rk4alg(model_equation,eq,fun)

Depending on your settings the algorithm will need some time until it prints *Finished!*.

Final Step: Evaluating the output
=================================

The function ``rk4alg`` return three arrays, the **Time, zonal mean temperature (ZMT) and global mean temperature (GMT)**. Other variables which are of interest, for example the grid specifications, can be accessed by importing the :doc:`variables <code/variables>` package and additional constants by importing the :doc:`constants <code/constants>` class::

    import Variables as Vars
    from lowEBMs import constants as const

and then return the desired variables by their specified name, for example::

    latitudinal_grid=Vars.Lat

For detailed information about output variables see section :doc:`output <output>`. 

You can plot the global temperature over time with (with time conversion)::

    from lowEBMs import constants as const
    plt.plot(Time/const.time_sec_year,GMT)
    plt.xlabel('time [years]')
    plt.ylabel('GMT [K]')

and you get something like this (for the simple 0D EBM):

.. figure:: _static/GMT12.png
   :align: center
   :width: 70%

   with an initial temperature of 12°C (285K)

.. figure:: _static/GMT17.png
   :align: center
   :width: 70%

   with an initial temperature of 17°C (290K)

Putting it together
===================

The summary of what you need to get the model running. Import packages::

    import matplotlib as plt
    import numpy as np
    from lowEBMs.Packages.Configuration import importer 
    from lowEBMs.Packages.Variables import variable_importer
    from lowEBMs.Packages.RK4 import rk4alg
    from lowEBMs.Packages.ModelEquation import model_equation

and run the specific modules::

    configdic=importer('EBM0D_simple_config.ini')
    eq=configdic['eqparam']
    rk=configdic['rk4input']
    fun=configdic['funccomp']
    variable_importer(configdic)
    Time,ZMT,GMT=rk4alg(model_equation,eq,fun)

This demonstration also exists as a jupyter notebook in the *'Tutorials/'* directive of this project (*EBM0D_simple.ipynb*).




    


    
