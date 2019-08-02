"""
Package with functions which configure the model setup.

.. autosummary::
    :toctree:
    :nosignatures:

    importer
    dict_to_list
    parameterimporter
    parameterinterpolator
    parameterinterpolatorstepwise
    add_sellersparameters
    import_parallelparameter
    allocate_parallelparameter
    write_parallelparameter
"""
import configparser
import os
import sys
from lowEBMs.Packages.Functions import *
from lowEBMs.Packages.Variables import *

def importer(filename,*args,**kwargs): 
    """
    Reads a **configuration.ini-file** and creates the model run setup in a dictionary. It is one of the coremodules of this project, mostly called as first step, because it gathers all information about the model setup and summarizes it.

    .. Note::

        The file from which the information is imported has to have a specific structure, please read :ref:`Input <../input>` first to see how the **configuration.ini-files** are created.

    The specificaton of the path to the filedirectory is optional. If none is given some standard diretories will be tried (python sys.paths and relative paths like '../', '../Config/',..)

    **Function-call arguments** \n

    :param string filename:         The name of the **configuration.ini-file**
                                
                                        * type: string 
                                        * value: example: 'Configuration.ini'
                                
    :param args:        

    :param kwargs:                  Optional Keyword arguments:

                                    * *path*: The directory path where the **configuration.ini-file** is located.

                                        * type: string
                                        * value: **full path** ('/home/user/dir0/dir1/filedir/') or **relative path** ('../../filedir/')
                                    

    :returns:                       configdic: Dictionary of model setup parameters distributed over several subdictionaries

    :rtype:                         Dictionary
 
    """
    path=kwargs.get('path',None)
    
    #Importing the configfile.ini from path
    if path == None:
        possible_paths=['','Config/','../Config/']
        for i in sys.path:
            possible_paths.append(i+'/lowEBMs/Tutorials/Config/')
        for trypath in possible_paths:
            exists = os.path.isfile(trypath+filename)
            if exists:
                path=trypath
                print('Loading Configuration from: '+path+filename)
                config=configparser.ConfigParser()  
                config.read(path+filename)    
                break 
            if trypath==possible_paths[-1]:
                sys.exit('Error: File not found, please specify the path of the configuration.ini.  importer(filename,path= " ... ")')
    else:
    #Importing the configfile.ini
        exists = os.path.isfile(path+filename)
        if exists:
            print('Loading Configuration from: '+path)
            config=configparser.ConfigParser()  
            config.read(path+filename) 
        else:         
            sys.exit('Error: File not found, please specify the path of the configuration.ini.  importer(filename,path= " ... ")')                  
    #Creating arrays for the sections in the configfile 
    keys=config.options('eqparam')  
    values=[]      
    for j in range(len(keys)):        
        values.append(eval(config['eqparam'][keys[j]]))
    eqparamd=dict(zip(keys,values))
    
    keys=config.options('rk4input')  
    values=[]      
    for j in range(len(keys)):        
        values.append(eval(config['rk4input'][keys[j]]))
    rk4inputd=dict(zip(keys,values))

    keys=config.options('initials')  
    values=[]      
    for j in range(len(keys)):        
        values.append(eval(config['initials'][keys[j]]))
    initialsd=dict(zip(keys,values))

    #Creating a dictionary of functions included 
    funclistd={}
    funcparamd={}
    i=0
    while 'func'+str(i) in config:
        funclistd['func'+str(i)]=eval(config['func'+str(i)]['func'])

        keys=config.options('func'+str(i))[1:]  
        values=[]      
        for j in range(len(keys)):        
            values.append(eval(config['func'+str(i)][keys[j]]))
        funcparamd['func'+str(i)]=dict(zip(keys,values))
        i+=1
    
    #packing the function components into one dictionary
    funccompd={'funclist':funclistd,'funcparam':funcparamd} 
    #converting to list-type to allow indexing
    #funccomp=dict_to_list(funccompd)     
    #eqparam=dict_to_list(eqparamd)     
    #rk4input=dict_to_list(rk4inputd)
    #initials=dict_to_list(initialsd)     
    #creating output array
    #configa=[eqparam, rk4input, funccomp, initials]
    configad=[eqparamd, rk4inputd, funccompd, initialsd]
    #creating array with the names of configa
    configdicnames=lna(['eqparam','rk4input','funccomp','initials'])
    configdic=dict(zip(configdicnames,configad))
    
    #Importing the Variables and initial conditions    
    #Variable_importer()

    #returning the arrays with all needed system parameters and variables
    #return configa, configdic
    return configdic

def dict_to_list(dic):
    """
    Converts dictionaries returned from ``Configuration.importer`` into a list with the same structure. This allows calling the content by index not keyword. It works for a maximum of 3 dimensions of dictionaries (dictionary inside a dictionary).

    **Function-call arguments** \n

    :param dict dic:            The dictionary to convert
                 
    :returns:                   List with same structure as input dictionary

    :rtype:                     List
    """
    dic_to_list=list(dic.values())
    to_list=dic_to_list
    #print(to_list)
    
    i=0
    while type(to_list[i]) == dict:
        to_list[i]=list(to_list[i].values())
        j=0
        while type(to_list[i][j])==dict:
            to_list[i][j]=list(to_list[i][j].values())
            k=0
            while type(to_list[i][j][k])==dict:
                to_list[i][j][k]=list(to_list[i][j][k].values())
                if k<len(to_list[i][j])-1:
                    k+=1
            if j<len(to_list[i])-1:
                j+=1
                
        if i<len(to_list)-1:
            i+=1
    return to_list

###Function to import parameters for the Sellers-EBM from a parameterfile
###with arrays of values
def parameterimporter(filename,*args,**kwargs):
    """
    A function purpose-built to import 1-dimensional parameters for the sellers-type functions. The standard parameters (:ref:`Sellers 1969`) are written into a **.ini-file** and will be extracted to override the 0-dimensional parameters with 1-dimensional ones.

    .. Important::

        This function is inbound into ``Configuration.parameterinterpolater`` or ``Configuration.parameterinterpolaterstepwise`` which interpolate the parameters to the gridresolution. **To import, interpolate and overwrite these parameter use** ``Configuration.add_sellersparameters``.     

    Parameters which are imported 1-dimensionally:

        * *b*: Empirical constant to estimate the albedo
        * *Z*: Zonal mean altitude 
        * *Q*: Solar insolation
        * *dp*: The tropospheric pressure depth
        * *dz*: The average zonal ocean depth
        * *Kh*: The thermal diffusivity of the atmospheric sensible heat term
        * *Kwv*: The thermal diffusivity of the watervapour term
        * *Ko*: The thermal diffusivity of the oceanic sensible heat term
        * *a*: Empricial constant to calculate the meridional windspeed

    The parameters are divided into two types, one defined on a latitudinal circle (gridlines) and one defined on a latitudinal belt (center point between two latitudinal circles/gridlines)

    .. Note::

        The standard parameters from :ref:`Sellers (1969)` are already provided with this project in 'lowEBMs/Tutorials/Config/Data/'. By specifying no path (**path=None**) they can directly be used (advised since the parameters are structured in a special way).

    **Function-call arguments** \n

    :param string filename:         The name of the **parameter.ini-file**
                                
                                        * type: string 
                                        * value: standard: 'SellersParameterization.ini'
                                
    :param args:        

    :param kwargs:                  Optional Keyword arguments:

                                    * *path*: The directory path where the **parameter.ini-file** is located.

                                        * type: string
                                        * value: **full path** ('/home/user/dir0/dir1/filedir/') or **relative path** ('../../filedir/')
                                    

    :returns:                       circlecomb, beltcomb: List of parameters defined on a latitudinal circle, and latitudinal belt

    :rtype:                         List, List

    """
    path=kwargs.get('path',None)
    
    #Importing the paras.ini from path
    if path == None:
        possible_paths=['','Config/Data/','../Config/Data/']
        for i in sys.path:
            possible_paths.append(i+'/lowEBMs/Tutorials/Config/Data/')
        for trypath in possible_paths:
            exists = os.path.isfile(trypath+filename)
            if exists:
                path=trypath
                print('Loading Parameters from: '+path+filename)
                paras=configparser.ConfigParser()  
                paras.read(path+filename)    
                break 
            if trypath==possible_paths[-1]:
                sys.exit('Error: File not found, please specify the path of the configuration.ini.  parameterimporter(filename,path= " ... ")')
    else:
    #Importing the configfile.ini
        exists = os.path.isfile(path+filename)
        if exists:
            print('Loading parameters from: '+path)
            paras=configparser.ConfigParser()  
            paras.read(path+filename) 
        else:         
            sys.exit('Error: File not found, please specify the path of the parameter.ini.  parameterimporter(filename,path= " ... ")')                  
    
    #Creating and filling arrays with values for latitudinal belts
    belt=paras.options('belt')
    for i in range(int(len(paras.options('belt')))):
        belt[i]=eval(paras['belt'][belt[i]])
    
    #Creating and filling arrays with values for latitudinal circles
    circle=paras.options('circle')
    for i in range(int(len(paras.options('circle')))):
        circle[i]=eval(paras['circle'][circle[i]])
    
    #Splitting the arrays to get the arrays for northern and southern hemisphere splitted
    beltn,belts=belt[:int(len(belt)/2)],belt[int(len(belt)/2):]
    circlen,circles=circle[:int(len(circle)/2)],circle[int(len(circle)/2):]
    
    #Recombining arrays. Needed because the arrays belt and circle are not
    #ordered from -90° to 90°
    beltcomb=[0]*len(beltn)
    circlecomb=[0]*len(circlen)
    for i in range(len(beltn)):
        belts[i].reverse()
        beltcomb[i]=belts[i]+beltn[i]
    for i in range(len(circlen)):
        circles[i].reverse()
        circlecomb[i]=circles[i]+circlen[i]
    
    #Returning the ordered arrays with systemparameters for latitudinal circles and belts
    return circlecomb, beltcomb


###Function to interpolate the parameterizations given from sellers, into an interpolated
####output with higher resolution
def parameterinterpolator(filename,*args,**kwargs):
    """
    An interpolation method fitting a polynomial of degree 10 to the parameter distributions. This creates parameter distributions suitable for the gridresolution (necessary if a higher resolution than 10° is used.

    This function includes the function ``Configuration.parameterimporter`` and takes the same arguments.

    **Function-call arguments** \n

    :param string filename:         The name of the **parameter.ini-file**
                                
                                        * type: string 
                                        * value: standard: 'SellersParameterization.ini'
                                
    :param args:        

    :param kwargs:                  Optional Keyword arguments:

                                    * *path*: The directory path where the **parameter.ini-file** is located.

                                        * type: string
                                        * value: **full path** ('/home/user/dir0/dir1/filedir/') or **relative path** ('../../filedir/')
                                    

    :returns:                       newcircle, newbelt: List of interpolated parameters defined on a latitudinal circle, and latitudinal belt

    :rtype:                         List, List
    """
    path=kwargs.get('path',None)
    #Importing parameters 
    inputparas=parameterimporter(filename,path=path)
    
    #defining new latitudinal arrays
    if both_hemispheres==True:    
        Latrange=180
        latnewc=np.linspace(-90,90,int(Latrange/spatial_resolution+1))
        latnewb=np.linspace(-90,90-spatial_resolution,                               int(Latrange/spatial_resolution))+spatial_resolution/2
        latnewb=np.insert(latnewb,0,-90)
        latnewb=np.append(latnewb,90)
    else:
        Latrange=90     
        latnewc=np.linspace(0,90-spatial_resolution,                                int(Latrange/spatial_resolution))
        latnewb=np.linspace(0,90-spatial_resolution,                                int(Latrange/spatial_resolution))+spatial_resolution/2
        latnewb=np.insert(latnewb,0,0)
        latnewb=np.append(latnewb,90)
        
    #Interpolation of circle parameters
    newcircle=[0]*len(inputparas[0])
    lat10c=np.linspace(-80,80,17)
    for i in range(len(inputparas[0])):
        zc=np.polyfit(lat10c,inputparas[0][i],10)
        fc=np.poly1d(zc)
        newcircle[i]=fc(latnewc)
        newcircle[i]=newcircle[i][1:]
        newcircle[i]=newcircle[i][:-1]

    #Interpolation of belt parameters
    newbelt=[0]*len(inputparas[1])
    lat10b=np.linspace(-85,85,18)
    for i in range(len(inputparas[1])):
        zb=np.polyfit(lat10b,inputparas[1][i],10)
        fb=np.poly1d(zb)
        newbelt[i]=fb(latnewb)
        newbelt[i]=newbelt[i][1:]
        newbelt[i]=newbelt[i][:-1]
    
    return newcircle, newbelt


###Function to interpolate the parameterizations given from sellers, into an interpolated
####output with higher resolution with stepwise interpolation and averaging
def parameterinterpolatorstepwise(filename,*args,**kwargs):
    """
    An interpolation method stepwise fitting and averaging a polynomial of degree 2 to the parameter distribution.

    The interpolation method is more advanced compared to ``Configuration.parameterinterpolator``. For each point (over the latitudes) a polynomial fit of degree 2 is made over the point plus the neighbouring points and estimates for the new gridresolution between these neighbouring points are stored. This is done for every point of the original parameters (except the endpoints). Because the interpolations overlap, the values are averaged to obtain a best estimate from multiple interpolations.  

    This function includes the function ``Configuration.parameterimporter`` and takes the same arguments.

    **Function-call arguments** \n

    :param string filename:         The name of the **parameter.ini-file**
                                
                                        * type: string 
                                        * value: standard: 'SellersParameterization.ini'
                                
    :param args:        

    :param kwargs:                  Optional Keyword arguments:

                                    * *path*: The directory path where the **parameter.ini-file** is located.

                                        * type: string
                                        * value: **full path** ('/home/user/dir0/dir1/filedir/') or **relative path** ('../../filedir/')
                                    

    :returns:                       newcircle, newbelt: List of interpolated parameters defined on a latitudinal circle, and latitudinal belt

    :rtype:                         List, List
    """
    path=kwargs.get('path',None)
    #Importing parameters 
    inputparas=parameterimporter(filename,path=path)

    #Defining new latitudinal arrays
    if both_hemispheres==True:    
        Latrange=180
        latnewc=np.linspace(-90+spatial_resolution,                            90-spatial_resolution,int(Latrange/spatial_resolution-1))
        latnewb=np.linspace(-90,90-spatial_resolution,                            int(Latrange/spatial_resolution))+spatial_resolution/2
            
    else:
        Latrange=90     
        latnewc=np.linspace(0,90-spatial_resolution,                                int(Latrange/spatial_resolution))
        latnewb=np.linspace(0,90-spatial_resolution,                                int(Latrange/spatial_resolution))+spatial_resolution/2
        latnewb=np.insert(latnewb,0,0)
        latnewb=np.append(latnewb,90)

    ###Interpolation of circle parameters###
    
    #Array for output
    newcircle=np.array([[0]*len(latnewc)]*len(inputparas[0]),dtype=float)
    #Array with 10° latitudal dependence
    lat10c=np.linspace(-80,80,17)
    
    #Loop over each circleparameter
    for k in range(len(inputparas[0])):
        #Loop over the length of latitudes (2nd element to one before last element)
        for i in range(1,len(lat10c)-1):
            #Do a polyfit 2nd order over the element +-1 element (left and right)
            zc=np.polyfit(lat10c[i-1:(i+2)],inputparas[0][k][i-1:(i+2)],2)
            fc=np.poly1d(zc)
            
            #Endpoints are set to the value of the inputparameter (no polyfit here)
            if i == 1:
                for l in range(int(10/spatial_resolution)):
                    newcircle[k][l]=inputparas[0][k][0]
            if i == (len(lat10c)-2):
                for l in range(int((i+2)*10/spatial_resolution-1),int((i+3)*10/spatial_resolution-1)):
                    newcircle[k][l]=inputparas[0][k][-1]
            
            #Write for the new latitudal dependence the corresponding values 
            #from the polyfit into the given outputarray
            #Loop over the element to the right of i-1 to the element to left of i+1
            for j in range(int(2*10/spatial_resolution-1)):  
                if newcircle[k][int(i*10/spatial_resolution+j)] == 0:
                    newcircle[k][int((i)*10/spatial_resolution+j)]=                    fc(latnewc[int((i)*10/spatial_resolution+j)])
                
                #The inbetween value are calculated twice (from left and right) which are now
                #averaged to give a smooth new parameterization
                else:
                    newcircle[k][int((i)*10/spatial_resolution+j)]=np.mean([fc(latnewc                    [int((i)*10/spatial_resolution+j)]),newcircle[k][int((i)*10/spatial_resolution+j)]])
                
                   
    ###Interpolation of belt parameters###
    
    #Array for output
    newbelt=np.array([[0]*len(latnewb)]*len(inputparas[1]),dtype=float)
    #Array with 10° latitudal dependence
    lat10b=np.linspace(-85,85,18)  
    
    #Loop over each beltparameter
    for k in range(len(inputparas[1])):
        #Loop over the length of latitudes (2nd element to one before last element)
        for i in range(1,len(lat10b)-1):
            #Do a polyfit 2nd order over the element +-1 element (left and right)
            zb=np.polyfit(lat10b[i-1:(i+2)],inputparas[1][k][i-1:(i+2)],2)
            fb=np.poly1d(zb)
            
            #Endpoints are set to the value of the inputparameter (no polyfit here)
            if i == 1:
                for l in range(int(0.5*10/spatial_resolution)):
                    newbelt[k][l]=inputparas[1][k][0]
            if i == (len(lat10b)-2):
                for l in range(int((i+0.5)*10/spatial_resolution),len(newbelt[k])):
                    newbelt[k][l]=inputparas[1][k][-1]
            
            #Write for the new latitudal dependence the corresponding values 
            #from the polyfit into the given outputarray
            #Loop over the element to the right of i-1 to the element to left of i+1
            for j in range(int(2*10/spatial_resolution)):  
                if newbelt[k][int((i-0.5)*10/spatial_resolution+j)] == 0:
                    newbelt[k][int((i-0.5)*10/spatial_resolution+j)]=                    fb(latnewb[int((i-0.5)*10/spatial_resolution+j)])
                
                #The inbetween value are calculated twice (from left and right) which are now
                #averaged to give a smooth new parameterization
                else:
                    newbelt[k][int((i-0.5)*10/spatial_resolution+j)]=np.mean([fb(latnewb                    [int((i-0.5)*10/spatial_resolution+j)]),newbelt[k][int((i-0.5)*10/spatial_resolution+j)]])
                    
    return newcircle, newbelt


#Function to rewrite parameters with arrays of parameters from the Sellers parameterinterpolator
#Hardcoded! So take care on which index the sellers functions are placed, standard is:
#func0 = Incoming Radiation , func1 = Outgoing Radiation, func2 = Transfer, ...
def add_sellersparameters(config,importer,file,transfernumber,downwardnumber,solar,albedo,*args,**kwargs): 
    """
    Overwrites the model setup with one-dimensional sellers parameters. It takes a model configuration with 0D sellers parameters, the filename of new parameters and a method of interpolation.

    This function uses either the method ``Configuration.parameterinterpolator`` or ``Configuration.parameterinterpolatorstepwise`` which both use the import function ``Configuration.parameterimporter``, therefore it requires their attributes too.

    **Function-call arguments** \n

    :param dict config:             The original config dictionary to overwrite
                                
                                        * type: dictionary 
                                        * value: created by ``Configuration.importer``

    :param function importer:       The name of the interpolator method
                                
                                        * type: functionname 
                                        * value: **parameterinterpolator** or **parameterinterpolatorstepwise**     

    :param string file:             The name of the **parameter.ini-file**
                                
                                        * type: string 
                                        * value: standard: 'SellersParameterization.ini'

    :param integer transfernumber:  The [func] header-number in the **configuration.ini-file** which describes the transfer flux 
                                
                                        * type: integer 
                                        * value: any  

    :param integer incomingnumber:  The [func] header-number in the **configuration.ini-file** which describes the downward flux 
                                
                                        * type: integer 
                                        * value: any    

    :param boolean solar:           Indicates whether the insolation by Sellers is used
                                
                                        * type: boolean 
                                        * value: True / False

    :param boolean albedo:          Indicates whether the albedo parameters by Sellers are used
                                    
                                        * type: boolean 
                                        * value: True / False                        

    :param args:        

    :param kwargs:                  Optional Keyword arguments:

                                    * *path*: The directory path where the **parameter.ini-file** is located.

                                        * type: string
                                        * value: **full path** ('/home/user/dir0/dir1/filedir/') or **relative path** ('../../filedir/')
                                    

    :returns:                       configuration, parameters

    :rtype:                         Dictionary, List
    """
    from lowEBMs.Packages.Variables import Vars
    #solar and albedo are to be set to True or False 

    path=kwargs.get('path',None)
    #importing the new parameter arrays
    paras=[[dp,dz,K_h,K_wv,K_o,a],[b,Z,Q]]=importer(file,path=path)
    
    #rewriting the transfer parameters with conversion to SI units
    funct=config['funccomp']['funcparam']['func'+str(transfernumber)]
    funct['k_wv']=lna(K_wv)*10**5
    funct['k_h']=lna(K_h)*10**6
    funct['k_o']=lna(K_o)*10**2
    funct['a']=lna(a)/100
    funct['dp']=lna(dp)
    funct['dz']=lna(dz)*1000
    
    #rewriting the incoming radiation parameters with conversion + choice to be activated or not
    funcin=config['funccomp']['funcparam']['func'+str(downwardnumber)]
    if albedo==True:
        funcin['albedoparam'][0]=lna(Z)
        funcin['albedoparam'][1]=lna(b)
    if solar==True:
        Vars.Solar=lna(Q)*1.327624658#1.2971#
    configout=config
    configout['funccomp']['funcparam']['func'+str(transfernumber)]=funct
    configout['funccomp']['funcparam']['func'+str(downwardnumber)]=funcin
    return configout, paras
    
def import_parallelparameter(parallelconfig_filename,*args,**kwargs):
    """
    Imports information from a .ini-file to create a setup of parallelized simulations. This shall allow time-efficient creation of ensemble run, focused to run simulations with various parameters to gain best-fit parameters.    

    **Function-call arguments** \n


    :param string parallelconfig_filename:      The name of the **Parallelization.ini-file** for parallelization
                                    
                                                * type: string 
                                                * value: standard: 'Parallelization.ini'                      

    :param args:        

    :param kwargs:                              Optional Keyword arguments:

                                                * *path*: The directory path where the **Parallelization.ini-file** is located.

                                                    * type: string
                                                    * value: **full path** ('/home/user/dir0/dir1/filedir/') or **relative path** ('../../filedir/')
                                                

    :returns:                                   raw parallelization setup

    :rtype:                                     Dictionary
    """
    path=kwargs.get('path',None)
    
    #Importing the configfile.ini from path
    if path == None:
        possible_paths=['','Config/Parallelization/','../Config/Parallelization/','/Tutorials/Config/Parallelization/','../Tutorials/Config/Parallelization/']
        for i in sys.path:
            possible_paths.append(i+'/lowEBMs/Tutorials/Config/Parallelization/')
        for trypath in possible_paths:
            exists = os.path.isfile(trypath+parallelconfig_filename)
            if exists:
                path=trypath
                print('Loading fit-configuration from: '+path+parallelconfig_filename)
                fitconfigini=configparser.ConfigParser()  
                fitconfigini.read(path+parallelconfig_filename)    
                break 
            if trypath==possible_paths[-1]:
                sys.exit('Error: File not found, please specify the path of the fitconfiguration.ini.  importer(filename,path= " ... ")')
    else:
    #Importing the configfile.ini
        exists = os.path.isfile(path+parallelconfig_filename)
        if exists:
            print('Loading fit-configuration from: '+path)
            fitconfigini=configparser.ConfigParser()  
            fitconfigini.read(path+parallelconfig_filename) 
        else:         
            sys.exit('Error: File not found, please specify the path of the configuration.ini.  importer(filename,path= " ... ")')                  
       
    fitparams={}
    for i in fitconfigini.sections():     
        fitparams.update({str(i):dict()})
        for j in fitconfigini.options(i):
            fitparams[i].update({str(j):eval(fitconfigini[i][j])})
    return fitparams

def allocate_parallelparameter(parameter_raw):
    """
    Transforms parameters for parallelization from tuple *[start,end]* to list *[start,...,end]* of length *number_of_cycles*. This shall create lists of parameters to be tested in parallelized simulations.

    **Function-call arguments** \n


    :param dict parameter_raw:        A dictionary with parameters to allocate. The values of the parameters should have the form [start,end] to create *[start,...,end]* of length *number_of_cycles*
                                    
                                                * type: dictionary 
                                                * value: as returned by **configuration.import_parallelparameter**               


    :returns:                               allocated parallelization setup, parallelization information 

    :rtype:                                 Dictionary, Dictionary
    """
    num_params=parameter_raw['parametersetup']['number_of_parameters']
    num_cycles=parameter_raw['parametersetup']['number_of_cycles']
    parametersetup=parameter_raw.pop('parametersetup')
    parametersetup = dict((k,int(v)) for k,v in parametersetup.items())

    parameter_raw_minus=parameter_raw
    parameter_allocated=dict()
    for i in list(parameter_raw_minus.keys()):
        parameter_allocated.update({i:dict()})
        for j in list(parameter_raw_minus[i].keys()):
            paramrange=np.linspace(parameter_raw_minus[i][j][0],
                                   parameter_raw_minus[i][j][1],num_cycles)
            parameter_allocated[i].update({j:paramrange})
    return parameter_allocated, parametersetup

def write_parallelparameter(config,parameter,parametersetup):
    """
    Overwrites the single run model setup with a parallelized model setup. This function uses the allocated parallelization setup as returned by ``Configuration.allocate_parallelparameter``. Depending on the number of paramters **n** to parallelize, a **n-dimensional** matrix is created. This matrix will be transformed to a **one-dimensional** list by placing one row after another.  

    **Function-call arguments** \n


    :param dict config:                 The original config dictionary to overwrite
                                
                                            * type: dictionary 
                                            * value: created by ``Configuration.importer`` 

    :param dict parameter:              A dictionary with allocated parameters for parallelization. First element returned by ``Configuration.allocate_parallelparameter``.
                                
                                            * type: dictionary 
                                            * value: as returned by ``Configuration.allocate_parallelparameter`` 

    :param dict parametersetup:         A dictionary with information about parallelization. Second element returned by ``Configuration.allocate_parallelparameter``.
                                
                                            * type: dictionary 
                                            * value: as returned by ``Configuration.allocate_parallelparameter`` 


    :returns:                           config: Updated dictionary of model setup parameters for parallelization

    :rtype:                             Dictionary
    """
    num_params=parametersetup['number_of_parameters']
    num_cycles=parametersetup['number_of_cycles']

    #for s in range(num_cycles):
    paralleldict=dict()

    funckey=list(parameter.keys()) 
    for key in funckey:
        paralleldict.update({key:dict()})
        for paramkey in list(parameter[key].keys()):
            paralleldict[key].update({paramkey:dict()})
    
    keylen=len(funckey)
    paramkey=[]
    for l in funckey:
        paramkey.append(list(parameter[l].keys()))
    
    #for o in range(num_cycles):
    for n in range(num_cycles):
        for m in range(num_cycles):
        #for o in range(num_cycles):
            num=0
            par=0
            x=paralleldict[funckey[num]]
            #if m==0:
            if n==0 and m==0:# and o==0:
                x.update({paramkey[num][par]:[]})
                
            x.update({paramkey[num][par]:np.append(x.get(paramkey[num][par]),
                                                parameter[funckey[num]][paramkey[num][par]][m])})
            
            paralleldict.update({funckey[num]:x})
        

            num=0
            par=1
            y=paralleldict[funckey[num]]
            if n==0 and m==0:# and o==0:
                y.update({paramkey[num][par]:[]})
            
            y.update({paramkey[num][par]:np.append(y.get(paramkey[num][par]),
                                                parameter[funckey[num]][paramkey[num][par]][n])})
            paralleldict.update({key[num]:y})
            """    
                num=0
                par=2
                z=paralleldict[funckey[num]]
                if n==0 and m==0 and o==0:
                    z.update({paramkey[num][par]:[]})
                
                z.update({paramkey[num][par]:np.append(z.get(paramkey[num][par]),
                                                    parameter[funckey[num]][paramkey[num][par]][o])})
                paralleldict.update({key[num]:z})"""
            
    #eq=paralleldict.pop('eqparam')
    """for eqkey in list(eq.keys()):
        if bool(eq)==False:
            break
        config['eqparam'][eqkey]=eq[eqkey]
        print('hi')"""
    for key in funckey:
        for paramkey in list(paralleldict[key].keys()):
            config['funccomp']['funcparam'][key][paramkey]=paralleldict[key][paramkey]

    #for key in parallel
    #    config['funccomp']['funcparam'][funcnumber][parametername]=parameter
    
    return config

