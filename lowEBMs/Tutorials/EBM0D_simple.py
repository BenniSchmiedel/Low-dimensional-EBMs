import matplotlib.pyplot as plt
import numpy as np
from lowEBMs.Packages.Configuration import importer 
from lowEBMs.Packages.Variables import variable_importer
from lowEBMs.Packages.RK4 import rk4alg
from lowEBMs.Packages.ModelEquation import model_equation

def main():
    configdic=importer('EBM0D_simple_config.ini')
    eq=configdic['eqparam']
    rk=configdic['rk4input']
    fun=configdic['funccomp']
    variable_importer(configdic)
    outputdata=rk4alg(model_equation,eq,rk,fun)
    return outputdata



