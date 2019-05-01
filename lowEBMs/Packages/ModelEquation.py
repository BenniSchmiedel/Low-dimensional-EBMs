"""
In ``lowEBMs.Packages.ModelEquation`` modules are defined which build the EBM from functions given to it. The operation of this modules is adding the given functions :math:`F_1,F_2,...F_i` according to the following scheme (compare :doc:`physical background <../models>`):

.. math::

    y= \\frac{1}{C_{ao}} \cdot (F_1 + F_2 + ... + F_i),


with the deviation function :math:`y=\\frac{dT}{dt}` required by the ``lowEBMs.Packages.RK4.rk4alg`` and :math:`C_{ao}` the heat capacity of the system which is passed to the right side of the model equation.


"""

def model_equation(eqparam,funccomp):
    """
    The module which builds and evaluates the EBM by adding functions parsed through the **funccomp**.

    Input has to be given as `Dictionaries` supplied by ``lowEBMs.Packages.Configuration.importer`` from a specific **configuration.ini**.

    **Function-call arguments** \n

    :param dict eqparam:        Configuration dictionary containing additional information for the model equation:
                                
                                    * C_ao: The systems heat capacity (times the height of the system)

                                        * type: float
                                        * unit: Joule*Meter/Kelvin
                                        * value: > 0

    :param dict funccomp:       Configuration 2D dictionary containing function names and function parameters used:

                                    * funcnames: a dictionary of names of functions defined in ``lowEBMs.Packages.Functions`` which are added up. See :doc:`here <functions>` for a list of functions

                                    * funcparams: a dictionary of functions parameters corresponding to the functions chosen within **funcnames**. For details on the parameters see the specific function :doc:`here <functions>`

    :returns:                   The temperature gradient :math:`\\frac{dT}{dt}` (Kelvin/seconds) 
                                   

    :rtype:                     float or array(float), depending on 0D EBM or 1D EBM. In 1D, output is an array containing the temperature gradient for each latitudinal belt.

    """
    y=0                    	            #variable which can be used to sum up functions
    funclist=funccomp['funclist']             #Extracting needed arrays from the funccomp array
    funcparam=funccomp['funcparam']
    C_ao=eqparam['c_ao']                    #Extracting Equationparameters
    for i in range(len(funclist)):
            y += funclist['func'+str(i)](funcparam['func'+str(i)])    #Calling the selected function and sum them up 
    return y/C_ao           #output of y, weighted with the heat capacity

