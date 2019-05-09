import builtins
import numpy as np

class Vars():
    ###Data variables### -- RK4
    t=float
    T=float
    T_global=float
    Lat=float
    Lat2=float

    ###Dynamical variables### 
    start_time=float
    orbitals=float
    orbtable=float
    Noise=float
    ForcingTracker=[0,0]
    CO2Tracker=[0,0]
    meridional=list
    tempdif=list

    ###Fixed Variables###
    Solar=list
    Area=list
    bounds=list
    latlength=list
    External_time_start=float
    CO2_time_start=float

    ###Readout parameters###
    cL=list
    C=list
    F=list
    v=list
    P=list
    Transfer=list
    BudTransfer=list
    alpha=list
    Rin=list
    Rout=list
    ExternalOutput=list
    CO2Forcing=list
    Read=[cL,C,F,v,P,Transfer,alpha,BudTransfer,Solar,Noise,Rin,Rout,ExternalOutput,CO2Forcing]
    ExternalInput=list
    CO2=list
    


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
        self.Noise=float
        self.ForcingTracker=[0,0]
        self.CO2Tracker=[0,0]
        self.meridional=list
        self.tempdif=list

        self.Solar=list
        self.Area=list
        self.bounds=list
        self.latlength=list
        self.External_time_start=float
        self.CO2_time_start=float

        self.cL=list
        self.C=list
        self.F=list
        self.v=list
        self.P=list
        self.Transfer=list
        self.BudTransfer=list
        self.alpha=list
        self.Rin=list
        self.Rout=list
        self.ExternalOutput=list
        self.CO2Forcing=list
        self.Read=[self.cL,self.C,self.F,self.v,self.P,self.Transfer,self.alpha,self.BudTransfer,self.Solar,self.Noise,self.Rin,self.Rout,self.ExternalOutput,self.CO2Forcing]
        self.ExternalInput=list
        self.CO2=list
        

def reset(x):
    classreset=Vars()
    exec("Vars.%s=classreset.%s" % (x,x))

def datareset():
    classreset=Vars()
    Vars.t=classreset.t
    Vars.T=classreset.T
    Vars.T_global=classreset.T_global
    Vars.Lat=classreset.Lat
    Vars.Lat2=classreset.Lat2

def variable_importer(config):

    builtin_importer(config['rk4input'])
    initial_importer(config['initials'])
    output_importer()

def builtin_importer(rk4input):
    
    #Writing systemparameters into builtin-module to make them globally callable
    #Overview given in Readme.txt
    
    keys=list(rk4input.keys())
    values=list(rk4input.values())
    for i in range(len(keys)):
        exec("builtins.%s=%f" % (keys[i],values[i]))
    builtins.Runtime_Tracker=0
    builtins.Noise_Tracker=0
    builtins.parallelization=False

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
    if (number_of_integration) % data_readout == 0:
        #Assigning dynamical variables in Variables Package with initial values from var
        Vars.cL,Vars.C,Vars.F,Vars.v,Vars.P,Vars.Transfer,Vars.alpha,Vars.BudTransfer,Vars.Solar,Vars.Noise,Vars.Rin,Vars.Rout,Vars.ExternalOutput,Vars.CO2Forcing=np.array([[0]*int(number_of_integration/data_readout)]*len(Vars.Read),dtype=object)
    else: 
        Vars.cL,Vars.C,Vars.F,Vars.v,Vars.P,Vars.Transfer,Vars.alpha,Vars.BudTransfer,Vars.Solar,Vars.Noise,Vars.Rin,Vars.Rout,Vars.ExternalOutput,Vars.CO2Forcing=np.array([[0]*(int(number_of_integration/data_readout)+1)]*len(Vars.Read),dtype=object)
    Vars.ExternalOutput=np.array([Vars.ExternalOutput for i in range(int(number_of_externals))],dtype=object)
    Vars.External_time_start=np.array([0 for i in range(int(number_of_externals))],dtype=object)
    Vars.ForcingTracker=np.array([[0,0] for i in range(int(number_of_externals))],dtype=object)
    Vars.ExternalInput=np.array([0 for i in range(int(number_of_externals))],dtype=object)
    Vars.Read=[Vars.cL,Vars.C,Vars.F,Vars.v,Vars.P,Vars.Transfer,Vars.alpha,Vars.BudTransfer,               Vars.Solar,Vars.Noise,Vars.Rin,Vars.Rout,Vars.ExternalOutput,Vars.CO2Forcing]


def variable_importer_parameterfit(config,fitconfig):

    builtin_importer(config['rk4input'])
    builtin_importer_parameterfit(fitconfig)
    initial_importer_parameterfit(config['initials'],fitconfig)
    output_importer()    
    #output_importer_parameterfit(fitconfig)

def initial_importer_parameterfit(initials,fitconfig):
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

def output_importer_parameterfit():
    if (number_of_integration) % data_readout == 0:
        #Assigning dynamical variables in Variables Package with initial values from var
        Vars.cL,Vars.C,Vars.F,Vars.v,Vars.P,Vars.Transfer,Vars.alpha,Vars.BudTransfer,Vars.Solar,Vars.Noise,Vars.Rin,Vars.Rout,Vars.ExternalOutput,Vars.CO2Forcing=np.array([[0]*int(number_of_integration/data_readout)]*len(Vars.Read),dtype=object)
    else: 
        Vars.cL,Vars.C,Vars.F,Vars.v,Vars.P,Vars.Transfer,Vars.alpha,Vars.BudTransfer,Vars.Solar,Vars.Noise,Vars.Rin,Vars.Rout,Vars.ExternalOutput,Vars.CO2Forcing=np.array([[[0]*number_of_parameters]*(int(number_of_integration/data_readout)+1)]*len(Vars.Read),dtype=object)
    Vars.ExternalOutput=np.array([Vars.ExternalOutput for i in range(int(number_of_externals))],dtype=object)
    Vars.External_time_start=np.array([0 for i in range(int(number_of_externals))],dtype=object)
    Vars.ForcingTracker=np.array([[0,0] for i in range(int(number_of_externals))],dtype=object)
    Vars.ExternalInput=np.array([0 for i in range(int(number_of_externals))],dtype=object)
    Vars.Read=[Vars.cL,Vars.C,Vars.F,Vars.v,Vars.P,Vars.Transfer,Vars.alpha,Vars.BudTransfer,               Vars.Solar,Vars.Noise,Vars.Rin,Vars.Rout,Vars.ExternalOutput,Vars.CO2Forcing]

def builtin_importer_parameterfit(setup):
    
    #Writing systemparameters into builtin-module to make them globally callable
    #Overview given in Readme.txt
    
    keys=list(setup.keys())
    values=list(setup.values())
    for i in range(len(keys)):
        exec("builtins.%s=%i" % (keys[i],values[i]))
    builtins.parallelization=True

    return
    
