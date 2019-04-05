
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
    import os
    os.chdir('/home/benni/Programs/ebms/lowEBMs/Packages')
    from RK4 import rk4alg
    from Configuration import importer
    from Variables import variable_importer

First Step: Import model configuration
======================================

The way this project is built up enables to take any physical function implemented and merge them to create the basis of a desired EBM, which will be our input.
The input will be created manually and is stored in a **configuration.ini** file. Details on how to create and structure this **.ini** file will be given in the :doc:`input <input>`-section. Important is: **the configuration.ini file will provide the physical sense of the EBM!**

For now you can simply use the **0Dconf.ini** file which imports a zero-dimensional EBM with a model run over 1 year and stepsize of integration of 1 day.
To import this file go to your .py or .ipynb file and use::

    


    
