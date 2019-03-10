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
    meridional=list
    tempdif=list

    ###Fixed Variables###
    Solar=list
    Area=list
    bounds=list
    latlength=list
    External_time_start=float

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
    Read=[cL,C,F,v,P,Transfer,alpha,BudTransfer,Solar,Noise,Rin,Rout,ExternalOutput]
    ExternalInput=list


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
        self.meridional=list
        self.tempdif=list

        self.Solar=list
        self.Area=list
        self.bounds=list
        self.latlength=list
        self.External_time_start=float

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
        self.Read=[self.cL,self.C,self.F,self.v,self.P,self.Transfer,self.alpha,self.BudTransfer,self.Solar,self.Noise,self.Rin,self.Rout,self.ExternalOutput]
        self.ExternalInput=list

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

def Variable_importer(config):
    EQparam, rk4input, funccomp, var= config

    Builtin_importer(rk4input)
    Var_importer(var)
    Output_importer(var)

def Builtin_importer(rk4input):

    #Writing systemparameters into builtin-module to make them globally callable
    #Overview given in Readme.txt
    
    builtins.num_of_integration=rk4input[0]     
    builtins.stepsize_of_integration=rk4input[1] 
    builtins.latitude_stepsize=rk4input[2]      
    builtins.latitude_NS=rk4input[3]
    builtins.latitude_circle=rk4input[4]
    builtins.latitude_belt=rk4input[5]
    builtins.Tempstart_cosine=rk4input[6]
    builtins.Tempstart_amplitude=rk4input[7]
    builtins.Tempstart_noise=rk4input[8]
    builtins.Tempstart_noiseamplitude=rk4input[9]    
    builtins.Runtime_Tracker=rk4input[10]
    builtins.Noise_Tracker=rk4input[11]
    builtins.Condition=rk4input[12]
    builtins.ConditionLength=rk4input[13]
    builtins.ConditionValue=rk4input[14]
    builtins.ReadoutStep=rk4input[15]
    builtins.NumberofExternals=rk4input[16]

def Var_importer(var):

    ###filling the running variables with values depending on the systemconfiguration in rk4input###
    if latitude_stepsize==0:
        dim=0
        print('0D')
    else:
        dim=1
       #NS==True corresponds to southpole to northpole representation (180 Degrees)
        if latitude_NS==True:    
            Latrange=180

            #Checking if Temperature and Latitude is set on a latitudal circle (0°,10°,..if step=10)
            #or on a latitudinal belt and therefore right between the boundaries (5°,15°,..if step=10)

            #circle==True and belt==False says on the latitudinal circle
            if latitude_circle==True and latitude_belt==False:      
                var[3]=np.linspace(-90+latitude_stepsize,90-latitude_stepsize,int(Latrange/latitude_stepsize-1))
                var[4]=np.linspace(-90,90-latitude_stepsize,int(Latrange/latitude_stepsize))+latitude_stepsize/2
                var[1]=np.array([var[1]]*int(Latrange/latitude_stepsize-1))
                #Checking if the Temperature for each latitude starts with the same value or a 
                #cosine shifted value range
                if Tempstart_cosine==True:
                    var[1]=var[1]+Tempstart_amplitude*(cosd(var[3])-1)

            #circle==False and belt==True say on the latitudinal belt
            if latitude_circle==False and latitude_belt==True:
                var[4]=np.linspace(-90+latitude_stepsize,90-latitude_stepsize,int(Latrange/latitude_stepsize-1))
                var[3]=np.linspace(-90,90-latitude_stepsize,int(Latrange/latitude_stepsize))+latitude_stepsize/2
                var[1]=np.array([var[1]]*int(Latrange/latitude_stepsize))
                if Tempstart_cosine==True:
                    if Tempstart_noise==True:
                        z=[0]*len(var[3])
                        for k in range(len(var[3])):
                            z[k]=np.random.normal(0,Tempstart_noiseamplitude)
                    else: 
                        z=0
                    var[1]=var[1]+Tempstart_amplitude*(cosd(var[3])-1)+lna(z)

        #Not from southpole to northpole rather equator to pole
        else:
            Latrange=90     
            if latitude_circle==True and latitude_belt==False:
                var[3]=np.linspace(0,90-latitude_stepsize,int(Latrange/latitude_stepsize))
                var[4]=np.linspace(0,90-latitude_stepsize,int(Latrange/latitude_stepsize))+latitude_stepsize/2
                var[1]=np.array([var[1]]*int(Latrange/latitude_stepsize))
                if Tempstart_cosine==True:
                    var[1]=var[1]+Tempstart_amplitude*(cosd(var[3])-1)
            if latitude_circle==False and latitude_belt==True:
                var[4]=np.linspace(0,90-latitude_stepsize,int(Latrange/latitude_stepsize))
                var[3]=np.linspace(0,90-latitude_stepsize,int(Latrange/latitude_stepsize))+latitude_stepsize/2
                var[1]=np.array([var[1]]*int(Latrange/latitude_stepsize))
                if Tempstart_cosine==True:
                    var[1]=var[1]+Tempstart_amplitude*(cosd(var[3])-1)


def Output_importer(var):
    #Assigning dynamical variables in Variables Package with initial values from var
    Vars.t,Vars.T,Vars.T_global,Vars.Lat,Vars.Lat2=var
    Vars.cL,Vars.C,Vars.F,Vars.v,Vars.P,Vars.Transfer,Vars.alpha,Vars.BudTransfer,Vars.Solar,Vars.Noise,Vars.Rin,Vars.Rout,Vars.ExternalOutput=    np.array([[0]*int(num_of_integration/ReadoutStep)]*len(Vars.Read),dtype=object)
    Vars.ExternalOutput=np.array([Vars.ExternalOutput for i in range(NumberofExternals)],dtype=object)
    Vars.External_time_start=np.array([0 for i in range(NumberofExternals)],dtype=object)
    Vars.ForcingTracker=np.array([[0,0] for i in range(NumberofExternals)],dtype=object)
    Vars.ExternalInput=np.array([0 for i in range(NumberofExternals)],dtype=object)
    Vars.Read=[Vars.cL,Vars.C,Vars.F,Vars.v,Vars.P,Vars.Transfer,Vars.alpha,Vars.BudTransfer,               Vars.Solar,Vars.Noise,Vars.Rin,Vars.Rout,Vars.ExternalOutput]





