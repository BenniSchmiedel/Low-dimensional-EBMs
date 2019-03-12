
# coding: utf-8

# In[1]:


def BaseEquation(eqparam,funccomp):
    y=0                    	            #variable which can be used to sum up functions
    funclist=funccomp['funclist']             #Extracting needed arrays from the funccomp array
    funcparam=funccomp['funcparam']
    C_ao=eqparam['c_ao']                    #Extracting Equationparameters
    for i in range(len(funclist)):
            y += funclist['func'+str(i)](funcparam['func'+str(i)])    #Calling the selected function and sum them up 
    return y/C_ao           #output of y, weighted with the heat capacity

