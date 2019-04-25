import matplotlib.pyplot as plt
import numpy as np
from lowEBMs.Packages.Configuration import importer, add_sellersparameters, parameterinterpolatorstepwise, parameterimporter
from lowEBMs.Packages.Variables import variable_importer
from lowEBMs.Packages.RK4 import rk4alg
from lowEBMs.Packages.ModelEquation import model_equation

def main():
    configdic=importer('EBM1D_Sellers_dynamic_config.ini')
    variable_importer(configdic)
    configdic1,paras=add_sellersparameters(configdic,parameterinterpolatorstepwise,'SellersParameterization.ini',2,0,True,True)
    eq=configdic1['eqparam']
    rk=configdic1['rk4input']
    fun=configdic1['funccomp']
    outputdata=rk4alg(model_equation,eq,rk,fun)
    return outputdata

