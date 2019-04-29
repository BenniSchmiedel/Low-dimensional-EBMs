"""
The ``RK4.py`` packages provides the numerical scheme to iteratively solve ordinary differential equations (ODE), hence the :doc:`model equation <modelequation>` which is parsed by the ``ModelEquation.py`` package initialized with the :doc:`configuration <configuration>` provided by the ``Configuration.py`` package. 

For an example see :doc:`How to use <../howtouse>`.

.. sidebar:: Operating principle RK4

    .. image:: _static/RK4.png

    The scheme operates from the initial step :math:`y_0(t_0)` to the subsequent step :math:`y_1(t_1)` with :math:`t_1=t_0+h` and :math:`y_1=y_0+\phi(t_0,y_0) \cdot h` by using a weighted increment :math:`\phi` calculated from increments :math:`k_1,..,k_4`. This operation is continued with :math:`y_1(t_1)` to estimate :math:`y_2(t_2)` an so on.

The increments :math:`k_1,..,k_4` are obtained by solving the model equation, as defined in the :doc:`physical background <models>` for the dynamical term :math:`\\frac{dT}{dt}`. The increments differ in their choice of inital conditions (point of evaluation of the model equation). One iterative step always goes through a cycle of evaluating the model equation four times. It starts with the calculation of :math:`k_1` at point :math:`y_0(t_0)` with:

.. math::

    k_1= f(t_0,y_0),

where :math:`f(t,y(t))` is given by the deviation of :math:`y(t)`, hence :math:`\\frac{dT}{dt} = \\frac{1}{C}\cdot(R_{in}+R_{out}+...)` at :math:`T_0 (t_0)`.

Now the scheme continues the following procedure:

.. math::

    k_2&= f(t_0+\\frac{h}{2},y_0+ \\frac{h}{2}\cdot k1) \\
    k_3&= f(t_0+\\frac{h}{2},y_0+ \\frac{h}{2}\cdot k2) \\
    k_4&= f(t_0+h,y_0+ h\cdot k3).

As final step of one iterative step the weighted increment :math:`\phi` is calculated by through:

.. math::

    \phi = \\frac{1}{6}\cdot k_1+\\frac{1}{3}\cdot k_2+\\frac{1}{3}\cdot k_3+\\frac{1}{6}\cdot k_4

to estimate :math:`y_1` as final step of one iteration cycle:

.. math::
    
    y_1=y_0+\phi(t_0,y_0)\cdot h . 



"""

from lowEBMs.Packages.ModelEquation import model_equation
from lowEBMs.Packages.Functions import *
from lowEBMs.Packages.Variables import Vars
import numpy as np
import builtins
import time

def rk4alg(func,eqparam,rk4input,funccomp):
    #Start the runtime tracker
    Vars.start_time = time.time()
    #locally defining rk4input parameters
    n,h=int(number_of_integration),stepsize_of_integration
    #Creating an array of the variables t,T,Lat,T_global which will be the outputarray
    data=np.array([[0]*(n+1)]*3 )
    #Filling data with intitial conditions at positions data[.][0]
    data=nal(data)
    data[0][0]=Vars.t #time t
    data[1][0]=Vars.T #Temperature T
    data[2][0]=Vars.T_global #Global mean temperature T_global
    ###Running runge Kutta 4th order n times###
    j=0
    for i in range(1, n + 1):  
        #Calculating increments at 4 positions from the energy balance equation (func)
        T0=Vars.T
        k1 = h * func(eqparam,funccomp)
        builtins.Runtime_Tracker += 1
        Vars.T=T0+0.5*k1
        k2 = h * func(eqparam,funccomp)
        builtins.Runtime_Tracker += 1
        Vars.T=T0+0.5*k2
        k3 = h * func(eqparam,funccomp)
        builtins.Runtime_Tracker += 1
        Vars.T=T0+k3
        k4 = h * func(eqparam,funccomp)
        builtins.Runtime_Tracker += 1
        
        #filling output array "data" with values from the generated increments
        #For the time simply adding the integration stepsize
        Vars.t = Vars.t + h
        if (i) % data_readout == 0: 
            j += 1       
            data[0][j] = Vars.t 
            #The Temperature is an average over the generated increments
            data[1][j] = Vars.T = T0 + (k1 + k2 + k2 + k3 + k3 + k4) / 6  
            #The globalmeantemp calculated from the new generated temperature distribution
            if spatial_resolution>0:
                data[2][j] = Vars.T_global = globalmeantemp()
            else: #if 0 dimensional
                data[2][j] = Vars.T_global = Vars.T
        #Check if the equilibrium condition is fulfilled. If true, break the loop, cut the output array to
        #the current length and move on to return the output data
        if eq_condition==True:
            if Runtime_Tracker > 4*eq_condition_length:
                if SteadyStateConditionGlobal(data[2][j-eq_condition_length:j])==True:
                    for l in range(len(data)):
                        data[l]=data[l][:(j+1)]
                    for m in range(len(Vars.Read)):
                        Vars.Read[m]=Vars.Read[m][:(j)]
                    break
    dataout=[data[0][:(j+1)],data[1][:(j+1)],data[2][:(j+1)]]

    print('Finished!')

    return dataout

