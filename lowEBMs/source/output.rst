******
Output
******

This chapter describes which variables can be printed out and how.

.. Note::
   
   Since longer model runs can be heavily memory-consuming the general frequency of data-readout can be adjusted in the *configuration.ini*.
   The parameter ``data_readout`` indicates on which step the data is read. 1 for every, 2 for every second ...

There are two types of data to print. 

The first type are the **primary variables**: **time** and **temperature**. They are returned directly by the algorithm (for details see :doc:`How to use <howtouse>` or :doc:`RK4 <code/rk4>`).

The second type are secondary variables, such as the albedo or the insolation, which might be of interest to observe. They are stored by the :doc:`Variables <code/variables>` package within the class ``Vars``. 
Most of them are written into the dictionary ``Vars.Read`` and callable with::

    from Variables import Vars
    Vars.Read

and contains the following variables, callable with::

    cL,C,F,P,Transfer,alpha,BudTransfer,solar,noise,Rdown,Rup,ExternalOutput,CO2Output,SolarOutput,AODOutput

    Insolation_over_time=Vars.Read['solar']

Beneath the variables in ``Vars.Read``, there are additional variables which can be printed, for example the following static variables::

    Area=list
    bounds=list
    latlength=list
    External_time_start=float
    CO2_time_start=float

All of them are callable by::

    from Variables import Vars
    Vars.VARIABLENAME

The description of all output variables is given in chapter :doc:`Variables <code/variables>`. 
