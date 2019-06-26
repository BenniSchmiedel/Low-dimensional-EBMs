"""
Package which defines a large set of variables and functions to process them.

The variables defined are divided into three types:

    *Running variables: they store information which is overwritten in each following iteration step
    *Static variables: they are non-changing system properties 
    *Storage variables: these are lists filled with system properties during a model run

The centre piece of this package is the class ``Variables.Vars``:

.. autosummary::
    :toctree:
    :nosignatures:

    Vars

All variables defined in ``Variable.Vars`` can be read and written with::
    
    from lowEBMs.Packages.Variable import Vars

    Vars.x          #returns the current value of variable x in Vars
    Vars.x = y      #variable x in Vars is permanently set to value y

Functions to process variables before a simulation run are, for single simulations

.. autosummary::
    :toctree:
    :nosignatures:

    variable_importer
    builtin_importer
    initial_importer
    output_importer
    
and for parallelized ensemble simulations

.. autosummary::
    :toctree:
    :nosignatures:

    variable_importer_parallelized
    builtin_importer_parallelized
    initial_importer_parallelized
    output_importer_parallelized

.. Important::
    
    ``Variables.variable_importer`` and executes the in the list following processing functions which has to be executed before a simulation can be run for more information see :doc:`How to use <howtouse>`). For parallelized simulations this can be swapped to ``Variables.variable_importer_parallelized``.

Functions to process variables during or after a simulation run are:

.. autosummary::
    :toctree:
    :nosignatures:

    reset
    datareset

"""
import builtins
import numpy as np

class Vars():
    """
    ``Variables.Vars`` defines any variable desired to store and access from another module's functions.

    There are three different types of variables defined.

    **Running variables:**

    +---------------+-----------------------------------------------------------------------+
    | t             | The time in the simulation (in steps of the stepsize_of_integration)  |
    +---------------+-----------------------------------------------------------------------+
    | T             | The ZMT temperature                                                   |
    +---------------+-----------------------------------------------------------------------+
    | T_global      | The GMT temperature                                                   |
    +---------------+-----------------------------------------------------------------------+   
    | orbitals      | The orbital parameters for the current simulation time t              |
    +---------------+-----------------------------------------------------------------------+   
    | noise         | The noise factor on the solar insolation term                         |
    +---------------+-----------------------------------------------------------------------+   
    | ForcingTracker| The current index and value of the external forcing's input list      |
    +---------------+-----------------------------------------------------------------------+   
    | CO2Tracker    | The current index and value of the CO2 forcing's input list           |
    +---------------+-----------------------------------------------------------------------+   
    | meridional    | The meridional wind pattern (from ``earthsystem.meridionalwind_sel``) |
    +---------------+-----------------------------------------------------------------------+   
    | tempdif       | The temperature difference between entries of the ZMT                 |
    +---------------+-----------------------------------------------------------------------+         
    
    **Static variables:**

    +-----------------------+-----------------------------------------------------------------------+
    | Lat                   | The latitudes of the gridpoints (or ZMT)                              |
    +-----------------------+-----------------------------------------------------------------------+
    | Lat2                  | The latitudes of the centres between gridpoints (or centered ZMT)     |   
    +-----------------------+-----------------------------------------------------------------------+
    | solar                 | The distribution of solar insolation                                  |
    +-----------------------+-----------------------------------------------------------------------+
    | orbtable              | The lookup-table for orbital parameters (from ``climlab``)            |
    +-----------------------+-----------------------------------------------------------------------+
    | area                  | The area of a latitudinal belt                                        |
    +-----------------------+-----------------------------------------------------------------------+
    | bounds                | The boundary latitudes used to calculate **Area**                     |
    +-----------------------+-----------------------------------------------------------------------+
    | latlength             | The circumference of a latitudinal circle                             |
    +-----------------------+-----------------------------------------------------------------------+   
    | External_time_start   | The simulation time when the external forcing sets in                 |
    +-----------------------+-----------------------------------------------------------------------+   
    | CO2_time_start        | The simulation time when the CO2 forcing sets in                      |
    +-----------------------+-----------------------------------------------------------------------+   
    | start_time            | The real clock time when the simulation was started                   |
    +-----------------------+-----------------------------------------------------------------------+       
 
    **Storage variables:**

    +---------------+-----------------------------------------------------------------------+
    | cL            | The sellers watervapour energy transfer                               |
    +---------------+-----------------------------------------------------------------------+
    | C             | The sellers atmospheric sensible heat energy transfer                 |
    +---------------+-----------------------------------------------------------------------+
    | F             | The sellers oceanic sensible heat energy transfer                     |
    +---------------+-----------------------------------------------------------------------+
    | P             | The total energy transfer , P=cL+C+F (non-weighted, one direction)    |
    +---------------+-----------------------------------------------------------------------+   
    | Transfer      | The total sellers energy transfer for a latitudinal belt              |
    +---------------+-----------------------------------------------------------------------+   
    | BudTransfer   | The budyko energy transfer for a latitudinal belt                     |
    +---------------+-----------------------------------------------------------------------+   
    | alpha         | The alpha value distribution                                          |
    +---------------+-----------------------------------------------------------------------+   
    | Rdown         | The downward radiative energy flux                                    |
    +---------------+-----------------------------------------------------------------------+   
    | Rup           | The upward radiative energy flux                                      |
    +---------------+-----------------------------------------------------------------------+   
    | ExternalOutput| List of radiative forcings                                            |
    +---------------+-----------------------------------------------------------------------+   
    | CO2Output     | The CO2 radiative forcing                                             |
    +---------------+-----------------------------------------------------------------------+   
    | ExternalInput | List of the raw input to calculate the radiative forcing              |
    +---------------+-----------------------------------------------------------------------+   
    | CO2Input      | The raw CO2 input                                                     |
    +---------------+-----------------------------------------------------------------------+             
 
    """
    ###Running variables -- RK4 ###
    t=float
    T=float
    T_global=float


    ###Running variables### 
    orbitals=float
    noise=float
    ForcingTracker=[0,0]
    CO2Tracker=[0,0]
    SolarTracker=[0,0]
    AODTracker=[0,0]
    OrbitalTracker=[0,{'ecc': 0, 'long_peri': 0, 'obliquity': 0}]
    meridional=list
    tempdif=list
    TSI=float
    AOD=float
    
    ###Static variables###
    Lat=float
    Lat2=float
    solar=list    
    orbtable=float
    area=list
    bounds=list
    latlength=list
    External_time_start=float
    CO2_time_start=float
    ExternalOrbitals_time_start=float
    Solar_time_start=float
    AOD_time_start=float
    start_time=float

    ###Storage variables###
    cL=list
    C=list
    F=list
    P=list
    Transfer=list
    BudTransfer=list
    alpha=list
    Rdown=list
    Rup=list
    ExternalOutput=list
    ExternalInput=list
    CO2Output=list  
    CO2Input=list
    ExternalOrbitals=list
    SolarInput=list
    SolarOutput=list
    AODInput=list
    AODOutput=list
    
    Read=dict #{'cL':cL, 'C': C, 'F': F,'P': P,'Transfer': Transfer,'alpha': alpha,'BudTransfer': BudTransfer,'Solar':,Noise,Rdown,Rup,ExternalOutput,CO2Forcing]
    Readnumber=15
    


    ###Variables initial values### (for reset)
    def __init__(self):
        self.t=float
        self.T=float
        self.T_global=float
        self.Lat=float
        self.Lat2=float

        self.start_time=float
        self.orbitals=float
        self.orbtable=float
        self.noise=float
        self.ForcingTracker=[0,0]
        self.CO2Tracker=[0,0]
        self.SolarTracker=[0,0]
        self.AODTracker=[0,0]
        self.OrbitalTracker=[0,{'ecc': 0, 'long_peri': 0, 'obliquity': 0}]
        self.meridional=list
        self.tempdif=list
        self.TSI=float
        self.AOD=float
        
        self.solar=list
        self.area=list
        self.bounds=list
        self.latlength=list
        self.External_time_start=float
        self.CO2_time_start=float
        self.ExternalOrbitals_time_start=float
        self.Solar_time_start=float
        self.AOD_time_start=float
        self.start_time=float
    
        self.cL=list
        self.C=list
        self.F=list
        self.P=list
        self.Transfer=list
        self.BudTransfer=list
        self.alpha=list
        self.Rin=list
        self.Rout=list
        self.ExternalOutput=list 
        self.ExternalInput=list
        self.CO2Output=list
        self.CO2Input=list
        self.ExternalOrbitals=list
        self.SolarInput=list
        self.SolarOutput=list
        self.AODInput=list
        self.AODOutput=list
        
        self.Read=dict #[self.cL,self.C,self.F,self.P,self.Transfer,self.alpha,self.BudTransfer,self.Solar,self.Noise,self.Rin,self.Rout,self.ExternalOutput,self.CO2Forcing]
        self.Readnumber=15

def trackerreset():
    reset('ForcingTracker')
    reset('CO2Tracker')
    reset('SolarTracker')
    reset('OrbitalTracker')
    reset('AODTracker')
    
def reset(x):
    """ 
    Resets the given variable to the initial value specified in Vars.__init__.        

    **Function-call arguments** \n

    :param float/list x:        The variable which shall be reset to the initial value

    :returns:                   No return

    """
    classreset=Vars()
    exec("Vars.%s=classreset.%s" % (x,x))

def datareset():
    """ 
    Resets the *primary variables* to their initial values. The *primary variables* are variables defined under the``[initials]``-section in the *configuration.ini-file*. These are:

        +---------------+-----------------------------------------------------------------------+
        | t             | The time in the simulation (in steps of the stepsize_of_integration)  |
        +---------------+-----------------------------------------------------------------------+
        | T             | The ZMT temperature                                                   |
        +---------------+-----------------------------------------------------------------------+
        | T_global      | The GMT temperature                                                   |
        +---------------+-----------------------------------------------------------------------+
        | Lat           | The latitudes of the gridpoints (or ZMT)                              |
        +---------------+-----------------------------------------------------------------------+
        | Lat2          | The latitudes of the centres between gridpoints (or centered ZMT)     |   
        +---------------+-----------------------------------------------------------------------+
    
    
    """
    classreset=Vars()
    Vars.t=classreset.t
    Vars.T=classreset.T
    Vars.T_global=classreset.T_global
    Vars.Lat=classreset.Lat
    Vars.Lat2=classreset.Lat2

def variable_importer(config,control,*args,**kwargs):
    """ 
    Executes all relevant functions to import variables for a single simulation run. From the *configuration* dictionary, returned by ``Configuration.importer``, the relevant information is extracted and the specific importer functions are executed in the following order:

    .. math::
        
        buliltin \_ importer \quad \\rightarrow \quad initial \_ importer \quad \\rightarrow \quad output \_ importer

    .. Note::

        When doing this manually, maintain the order!

    **Function-call arguments** \n

    :param dict config:         The configuration dictionary returned by ``Configuration.importer``  

    :returns:                   No return

    """
    accuracy,accuracy_number=kwargs.get('accuracy',1e-3),kwargs.get('accuracy_number',1000)
    trackerreset()
    builtin_importer(config['rk4input'],control,accuracy=accuracy,accuracy_number=accuracy_number)
    initial_importer(config['initials'])
    output_importer()

def builtin_importer(rk4input,control,*args,**kwargs):
    """
    Adds the most important variables to the python-builtin functions which are globally accessible. This enables calling and writing variables globally and across different files.

    Variables added to the builtin-functions are all arguments of the ``[rk4input]``-section from the *configuration* dictionary, returned by ``Configuration.importer``, and three additional ones. 
    
    .. Important::
    
        Variables from the ``[rk4input]``-section are added with their key given in the *configuration.ini-file* and can be called by the same one later.

    Here all added variables (``[rk4input]``-variables + additional ones):

    +---------------------------+-----------------------------------------------------------------------+
    | number_of_integration     | Number of iterations to perfom                                        |
    +---------------------------+-----------------------------------------------------------------------+
    | stepsize_of_integration   | Time steps of one iteration steps                                     |   
    +---------------------------+-----------------------------------------------------------------------+
    | spatial_resolution        | Grid resolution (width of one latitudinal band in degree)             |
    +---------------------------+-----------------------------------------------------------------------+
    | both_hemispheres          | Indicates if both hemispheres or northern hemisphere is modeled       |
    +---------------------------+-----------------------------------------------------------------------+
    | latitudinal_circle        | Indicates that the temperature is defined on latitudinal circles      |
    +---------------------------+-----------------------------------------------------------------------+
    | latitudinal_belt          | Indicates that the temperature is defined on latitudinal belts        |
    +---------------------------+-----------------------------------------------------------------------+
    | eq_condition              | Activation/Deactivation of stop criterion (equilibrium condition)     |
    +---------------------------+-----------------------------------------------------------------------+   
    | eq_condition_length       | The number of last datapoints to be compared with the predefined limit|
    +---------------------------+-----------------------------------------------------------------------+   
    | eq_condition_amplitude    | The predefined limiting value which defines the stop criterion        |
    +---------------------------+-----------------------------------------------------------------------+   
    | data_readout              | The number of iterations between data-readout                         |
    +---------------------------+-----------------------------------------------------------------------+    
    | number_of_externals       | The number of external forcings are used                              |
    +---------------------------+-----------------------------------------------------------------------+

    +---------------------------+-----------------------------------------------------------------------+    
    | Runtime_Tracker           | Tracks the iteration and cycle step (number_of_integration*4)         |
    +---------------------------+-----------------------------------------------------------------------+    
    | Noise_Tracker             | Tracks the value of solar noise                                       |
    +---------------------------+-----------------------------------------------------------------------+    
    | parallelization           | Indicates if parallelized simulations are enabled                     |
    +---------------------------+-----------------------------------------------------------------------+

    **Function-call arguments** \n

    :param dict rk4input:       The ``[rk4input]``-section from the configuration dictionary returned by ``Configuration.importer``  

    :returns:                   No return
    """
    #Writing systemparameters into builtin-module to make them globally callable
    #Overview given in Readme.txt
    accuracy,accuracy_number=kwargs.get('accuracy',1e-3),kwargs.get('accuracy_number',1000)
    keys=list(rk4input.keys())
    values=list(rk4input.values())
    for i in range(len(keys)):
        exec("builtins.%s=%f" % (keys[i],values[i]))
    builtins.Runtime_Tracker=0
    builtins.Noise_Tracker=0
    builtins.parallelization=False
    if control==True:
        builtins.eq_condition=True
        builtins.number_of_integration=10000
        builtins.data_readout=1    
        builtins.eq_condition_length=accuracy_number
        builtins.eq_condition_amplitude=accuracy
        print('Starting controlrun with a temperature accuracy of %s K on the GMT over %s datapoints.' %(accuracy,accuracy_number))

    """builtins.number_of_integration=rk4input['number_of_integration']     
    builtins.stepsize_of_integration=rk4input[1] 
    builtins.spatial_resolution=rk4input[2]      
    builtins.both_hemispheres=rk4input[3]
    builtins.latitudinal_circle=rk4input[4]
    builtins.latitudinal_belt=rk4input[5]
    builtins.initials['initial_temperature_cosine']=rk4input[6]
    builtins.initials['initial_temperature_amplitude']=rk4input[7]
    builtins.initials['initial_temperature_noise']=rk4input[8]
    builtins.initials['initial_temperature_noise_amplitude']=rk4input[9]    
    builtins.Runtime_Tracker=rk4input[10]
    builtins.Noise_Tracker=rk4input[11]
    builtins.Condition=rk4input[12]
    builtins.ConditionLength=rk4input[13]
    builtins.ConditionValue=rk4input[14]
    builtins.data_readout=rk4input[15]
    builtins.number_of_externals=rk4input[16]"""

def initial_importer(initials):
    """
    Calculates the initial conditions of the *primary variables* from the ``initials``-section.

    The initial conditions are directly written to their entry in ``Variable.Vars``. 

    **Function-call arguments** \n

    :param dict initials:       The ``[initials]``-section from the configuration dictionary returned by ``Configuration.importer``  

    :returns:                   No return
    """
    from lowEBMs.Packages.Functions import cosd, lna
    ###filling the running variables with values depending on the systemconfiguration in rk4input###

    if spatial_resolution==0:
        dim=0
        print('0D')
    else:
        dim=1
       #NS==True corresponds to southpole to northpole representation (180 Degrees)
        if both_hemispheres==True:    
            Latrange=180

            #Checking if Temperature and Latitude is set on a latitudal circle (0°,10°,..if step=10)
            #or on a latitudinal belt and therefore right between the boundaries (5°,15°,..if step=10)

            #circle==True and belt==False says on the latitudinal circle
            if latitudinal_circle==True and latitudinal_belt==False:      
                initials['latitude_c']=np.linspace(-90+spatial_resolution,90-spatial_resolution,int(Latrange/spatial_resolution-1))
                initials['latitude_b']=np.linspace(-90,90-spatial_resolution,int(Latrange/spatial_resolution))+spatial_resolution/2
                initials['zmt']=np.array([initials['zmt']]*int(Latrange/spatial_resolution-1))
                #Checking if the Temperature for each latitude starts with the same value or a 
                #cosine shifted value range
                if initials['initial_temperature_cosine']==True:
                    initials['zmt']=initials['zmt']+initials['initial_temperature_amplitude']*(cosd(initials['latitude_c'])-1)

            #circle==False and belt==True say on the latitudinal belt
            if latitudinal_circle==False and latitudinal_belt==True:
                initials['latitude_b']=np.linspace(-90+spatial_resolution,90-spatial_resolution,int(Latrange/spatial_resolution-1))
                initials['latitude_c']=np.linspace(-90,90-spatial_resolution,int(Latrange/spatial_resolution))+spatial_resolution/2
                initials['zmt']=np.array([initials['zmt']]*int(Latrange/spatial_resolution))
                if initials['initial_temperature_cosine']==True:
                    if initials['initial_temperature_noise']==True:
                        z=[0]*len(initials['latitude_c'])
                        for k in range(len(initials['latitude_c'])):
                            z[k]=np.random.normal(0,initials['initial_temperature_noise_amplitude'])
                    else: 
                        z=0
                    initials['zmt']=initials['zmt']+initials['initial_temperature_amplitude']*(cosd(initials['latitude_c'])-1)+lna(z)

        #Not from southpole to northpole rather equator to pole
        else:
            Latrange=90     
            if latitudinal_circle==True and latitudinal_belt==False:
                initials['latitude_c']=np.linspace(0,90-spatial_resolution,int(Latrange/spatial_resolution))
                initials['latitude_b']=np.linspace(0,90-spatial_resolution,int(Latrange/spatial_resolution))+spatial_resolution/2
                initials['zmt']=np.array([initials['zmt']]*int(Latrange/spatial_resolution))
                if initials['initial_temperature_cosine']==True:
                    initials['zmt']=initials['zmt']+initials['initial_temperature_amplitude']*(cosd(initials['latitude_c'])-1)
            if latitudinal_circle==False and latitudinal_belt==True:
                initials['latitude_b']=np.linspace(0,90-spatial_resolution,int(Latrange/spatial_resolution))
                initials['latitude_c']=np.linspace(0,90-spatial_resolution,int(Latrange/spatial_resolution))+spatial_resolution/2
                initials['zmt']=np.array([initials['zmt']]*int(Latrange/spatial_resolution))
                if initials['initial_temperature_cosine']==True:
                    initials['zmt']=initials['zmt']+initials['initial_temperature_amplitude']*(cosd(initials['latitude_c'])-1)
    
    Vars.t=initials['time']
    Vars.T=initials['zmt']
    Vars.T_global=initials['gmt']
    Vars.Lat=initials['latitude_c']
    Vars.Lat2=initials['latitude_b']

def output_importer():
    """
    Creates empty lists for the storage-variables which will be filled during the simulation.

    The lists are directly written to their entry in ``Variable.Vars`` and can be returned after the simulation is finished. 

    """
    if (number_of_integration) % data_readout == 0:
        #Assigning dynamical variables in Variables Package with initial values from var
        Vars.cL,Vars.C,Vars.F,Vars.P,Vars.Transfer,Vars.alpha,Vars.BudTransfer,Vars.solar,Vars.noise,Vars.Rdown,Vars.Rup,Vars.ExternalOutput,Vars.CO2Output,Vars.SolarOutput,Vars.AODOutput=np.array([[0]*int(number_of_integration/data_readout)]*Vars.Readnumber,dtype=object)
    else: 
        Vars.cL,Vars.C,Vars.F,Vars.P,Vars.Transfer,Vars.alpha,Vars.BudTransfer,Vars.solar,Vars.noise,Vars.Rdown,Vars.Rup,Vars.ExternalOutput,Vars.CO2Output,Vars.SolarOutput,Vars.AODOutput=np.array([[0]*(int(number_of_integration/data_readout)+1)]*Vars.Readnumber,dtype=object)
    Vars.ExternalOutput=np.array([Vars.ExternalOutput for i in range(int(number_of_externals))],dtype=object)
    Vars.External_time_start=np.array([0 for i in range(int(number_of_externals))],dtype=object)
    Vars.ForcingTracker=np.array([[0,0] for i in range(int(number_of_externals))],dtype=object)
    Vars.ExternalInput=np.array([0 for i in range(int(number_of_externals))],dtype=object)
    Vars.Read={'cL': Vars.cL,'C': Vars.C,'F': Vars.F,'P': Vars.P,'Transfer': Vars.Transfer,'alpha': Vars.alpha,'BudTransfer': Vars.BudTransfer, 'solar': Vars.solar,'noise': Vars.noise,'Rdown': Vars.Rdown,'Rup': Vars.Rup, 'ExternalOutput': Vars.ExternalOutput,'CO2Output': Vars.CO2Output,'SolarOutput':Vars.SolarOutput,'AODOutput':Vars.AODOutput}


def variable_importer_parallelized(config,paral_config):
    """ 
    Executes all relevant functions to import variables for an ensemble simulation run. From the *configuration* dictionary, returned by ``Configuration.importer``, and the *parallelization_config*, returned by ``Configuration.allocate_parallelparameter``, the relevant infomration is extracted and the specific importer functions are executed in the following order:

    .. math::
        
        buliltin \_ importer \quad \\rightarrow  \quad buliltin \_ importer \_ parallelized \quad \\rightarrow  \quad initial \_ importer \_ parallelized \quad \\rightarrow \quad output \_ importer

    .. Note::

        When doing this manually, maintain the order!

    **Function-call arguments** \n

    :param dict config:         The configuration dictionary returned by ``Configuration.importer``

    :param dict paral_config:   The parallelization setup configuration returned by ``Configuration.allocate_parallelparameter`` (second entry of return)  

    :returns:                   No return

    """
    trackerreset()
    builtin_importer(config['rk4input'])
    builtin_importer_parallelized(paral_config)
    initial_importer_parallelized(config['initials'],paral_config)
    output_importer()    
    #output_importer_parameterfit(fitconfig)

def initial_importer_parallelized(initials,paral_config):
    """
    Calculates the initial conditions of the *primary variables* from the ``initials``-section for parallelized simulations.

    The initial conditions are directly written to their entry in ``Variable.Vars``. 

    **Function-call arguments** \n

    :param dict initials:       The ``[initials]``-section from the configuration dictionary returned by ``Configuration.importer``  

    :param dict paral_config:   The parallelization setup configuration returned by ``Configuration.allocate_parallelparameter`` (second entry of return)  

    :returns:                   No return
    """ 
    from lowEBMs.Packages.Functions import cosd, lna
    ###filling the running variables with values depending on the systemconfiguration in rk4input###

    if spatial_resolution==0:
        dim=0
        print('0D')
    else:
        dim=1
       #NS==True corresponds to southpole to northpole representation (180 Degrees)
        if both_hemispheres==True:    
            Latrange=180

            #Checking if Temperature and Latitude is set on a latitudal circle (0°,10°,..if step=10)
            #or on a latitudinal belt and therefore right between the boundaries (5°,15°,..if step=10)

            #circle==True and belt==False says on the latitudinal circle
            if latitudinal_circle==True and latitudinal_belt==False:      
                initials['latitude_c']=np.linspace(-90+spatial_resolution,90-spatial_resolution,int(Latrange/spatial_resolution-1))
                initials['latitude_b']=np.linspace(-90,90-spatial_resolution,int(Latrange/spatial_resolution))+spatial_resolution/2
                initials['zmt']=np.array([initials['zmt']]*int(Latrange/spatial_resolution-1))
                #Checking if the Temperature for each latitude starts with the same value or a 
                #cosine shifted value range
                if initials['initial_temperature_cosine']==True:
                    initials['zmt']=initials['zmt']+initials['initial_temperature_amplitude']*(cosd(initials['latitude_c'])-1)

            #circle==False and belt==True say on the latitudinal belt
            if latitudinal_circle==False and latitudinal_belt==True:
                initials['latitude_b']=np.linspace(-90+spatial_resolution,90-spatial_resolution,int(Latrange/spatial_resolution-1))
                initials['latitude_c']=np.linspace(-90,90-spatial_resolution,int(Latrange/spatial_resolution))+spatial_resolution/2
                initials['zmt']=np.array([initials['zmt']]*int(Latrange/spatial_resolution))
                if initials['initial_temperature_cosine']==True:
                    if initials['initial_temperature_noise']==True:
                        z=[0]*len(initials['latitude_c'])
                        for k in range(len(initials['latitude_c'])):
                            z[k]=np.random.normal(0,initials['initial_temperature_noise_amplitude'])
                    else: 
                        z=0
                    initials['zmt']=initials['zmt']+initials['initial_temperature_amplitude']*(cosd(initials['latitude_c'])-1)+lna(z)

        #Not from southpole to northpole rather equator to pole
        else:
            Latrange=90     
            if latitudinal_circle==True and latitudinal_belt==False:
                initials['latitude_c']=np.linspace(0,90-spatial_resolution,int(Latrange/spatial_resolution))
                initials['latitude_b']=np.linspace(0,90-spatial_resolution,int(Latrange/spatial_resolution))+spatial_resolution/2
                initials['zmt']=np.array([initials['zmt']]*int(Latrange/spatial_resolution))
                if initials['initial_temperature_cosine']==True:
                    initials['zmt']=initials['zmt']+initials['initial_temperature_amplitude']*(cosd(initials['latitude_c'])-1)
            if latitudinal_circle==False and latitudinal_belt==True:
                initials['latitude_b']=np.linspace(0,90-spatial_resolution,int(Latrange/spatial_resolution))
                initials['latitude_c']=np.linspace(0,90-spatial_resolution,int(Latrange/spatial_resolution))+spatial_resolution/2
                initials['zmt']=np.array([initials['zmt']]*int(Latrange/spatial_resolution))
                if initials['initial_temperature_cosine']==True:
                    initials['zmt']=initials['zmt']+initials['initial_temperature_amplitude']*(cosd(initials['latitude_c'])-1)
    
    Vars.t=initials['time']
    Vars.T=np.array([initials['zmt']]*number_of_parallels)
    Vars.T_global=np.array([initials['gmt']]*number_of_parallels)
    Vars.Lat=initials['latitude_c']
    Vars.Lat2=initials['latitude_b']

def output_importer_parallelized():
    """
    Creates empty lists for the storage-variables which will be filled during the ensemble simulation.

    The lists are directly written to their entry in ``Variable.Vars`` and can be returned after the simulation is finished. 

    """
    if (number_of_integration) % data_readout == 0:
        #Assigning dynamical variables in Variables Package with initial values from var
        Vars.cL,Vars.C,Vars.F,Vars.P,Vars.Transfer,Vars.alpha,Vars.BudTransfer,Vars.solar,Vars.noise,Vars.Rdown,Vars.Rup,Vars.ExternalOutput,Vars.CO2Output,Vars.SolarOutput,Vars.AODOutput=np.array([[0]*int(number_of_integration/data_readout)]*Vars.Readnumber,dtype=object)
    else: 
        Vars.cL,Vars.C,Vars.F,Vars.P,Vars.Transfer,Vars.alpha,Vars.BudTransfer,Vars.solar,Vars.noise,Vars.Rdown,Vars.Rup,Vars.ExternalOutput,Vars.CO2Output,Vars.SolarOutput,Vars.AODOutput=np.array([[0]*(int(number_of_integration/data_readout)+1)]*Vars.Readnumber,dtype=object)
    Vars.ExternalOutput=np.array([Vars.ExternalOutput for i in range(int(number_of_externals))],dtype=object)
    Vars.External_time_start=np.array([0 for i in range(int(number_of_externals))],dtype=object)
    Vars.ForcingTracker=np.array([[0,0] for i in range(int(number_of_externals))],dtype=object)
    Vars.ExternalInput=np.array([0 for i in range(int(number_of_externals))],dtype=object)
    Vars.Read={'cL': Vars.cL,'C': Vars.C,'F': Vars.F,'P': Vars.P,'Transfer': Vars.Transfer,'alpha': Vars.alpha,'BudTransfer': Vars.BudTransfer, 'solar': Vars.solar,'noise': Vars.noise,'Rdown': Vars.Rdown,'Rup': Vars.Rup, 'ExternalOutput': Vars.ExternalOutput,'CO2Output': Vars.CO2Output,'SolarOutput':Vars.SolarOutput,'AODOutput':Vars.AODOutput}


def builtin_importer_parallelized(paral_config):
    """
    Adds additional variables from the parallelization setup to the python-builtin functions which are globally accessible.    

    The initial conditions are directly written to their entry in ``Variable.Vars``. 

    **Function-call arguments** \n

    :param dict initials:       The ``[initials]``-section from the configuration dictionary returned by ``Configuration.importer``  

    :param dict paral_config:   The parallelization setup configuration returned by ``Configuration.allocate_parallelparameter`` (second entry of return)  

    :returns:                   No return
    """ 
    #Writing systemparameters into builtin-module to make them globally callable
    #Overview given in Readme.txt
    
    keys=list(paral_config.keys())
    values=list(paral_config.values())
    for i in range(len(keys)):
        exec("builtins.%s=%i" % (keys[i],values[i]))
    builtins.parallelization=True

    return
    
