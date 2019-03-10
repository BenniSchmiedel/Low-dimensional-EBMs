
# coding: utf-8

# In[1]:


def BaseEquation(EQparam,funccomp):
    y=0                                #variable which can be used to sum up functions
    funclist=funccomp[0]               #Extracting needed arrays from the funccomp array
    funcparam=funccomp[1]
    C_ao=EQparam[0]                    #Extracting Equationparameters
    for i in range(len(funclist)):
            y += funclist[i](funcparam[i])    #Calling the selected function and sum them up 
    return y/C_ao           #output of y, weighted with the heat capacity

