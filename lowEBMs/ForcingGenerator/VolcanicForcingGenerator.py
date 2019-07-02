import matplotlib.pyplot as plt
import numpy as np

def datacut(Datatime,Data,Start,Stop):
    j=Datatime[0]
    k=0
    while j<Start:
        k+=1
        j=Datatime[k]
    k_start=k
    while j<Stop:
        k+=1
        if k==len(Datatime):
            break
        j=Datatime[k]

    k_end=k
    
    Data_cut=[0]*len(Data)
    for i in range(len(Data)):  
        Data_cut[i]=Data[i][k_start:k_end]
    return Data_cut

def timeevolution(t,M0,tprod,tloss):
    M=M0*(1-np.exp(-t/tprod))*np.exp(-t/tloss)
    
    #Fmax=np.max((1-np.exp(-t/tprod))*np.exp(-t/tloss))
    #tmax=np.argmax((1-np.exp(-t/tprod))*np.exp(-t/tloss))
    #print(1/Fmax,t[tmax])
    return M#/Fmax

def Conversion(NH,SH):
    if np.isnan(SH)==True:
        SH=np.nan_to_num(SH)
    if np.isnan(NH)==True:
        NH=np.nan_to_num(NH)
    
    if SH==0:
        TotalH2SO4=NH*0.57
    else:
        TotalH2SO4=NH+SH
    #TamboraH2SO4=39.7+45.8
    S_H2SO4=32/98
    TamboraS=TotalH2SO4*S_H2SO4
    return TamboraS

def ImportData(File,delimiter,header,col_time,col_lat,col_NH,col_SH):
    Raw=np.genfromtxt(File,
                          delimiter=delimiter,skip_header=header,usecols=(col_time,col_lat,col_NH,col_SH),
                          unpack=True,encoding='ISO-8859-1')
    sort=np.argsort(Raw[0])
    Raw_sorted=np.array([np.zeros(len(sort))]*4)
    for j in range(4):    
        for i in range(len(sort)):
            #print(sort[i])
            Raw_sorted[j,i]=Raw[j,sort[i]]
    """sort=np.argsort(Raw[0])
    c = np.zeros(len(sort), dtype = int) 
    for i in range(0, len(sort)): 
        c[i]= Raw[0][sort[i]] """
    
    return Raw_sorted


def Raw_to_timeRF(Raw):
    time=Raw[0]
    NH=Raw[2]
    SH=Raw[3]
    A=0.0364
    B=-20
    RF=np.zeros(len(NH))
    for i in range(len(NH)):
        RF[i]=A*B*Conversion(NH[i],SH[i])
    return time,RF

def Raw_to_timeAOD(Raw):
    time=Raw[0]
    NH=Raw[2]
    SH=Raw[3]
    A=0.0364
    B=-20
    AOD=np.zeros(len(NH))
    for i in range(len(NH)):
        AOD[i]=A*Conversion(NH[i],SH[i])
    return time,AOD

def Generator(File,delimiter,header,col_time,col_loc,col_NH,col_SH,Start,Stop,Step,Length_of_evolution):

    Raw=ImportData(File,delimiter,header,col_time,col_loc,col_NH,col_SH)
 
    Datatime=Raw[0]
    DataRF=Raw_to_timeRF(Raw)[1]
    DataAOD=Raw_to_timeAOD(Raw)[1]
    Data=[Datatime,DataRF,DataAOD]

    time,RF,AOD=datacut(Datatime,Data,Start,Stop)
    
    tprod=180
    tloss=330
    
    Series_time=np.arange(Start,Stop,Step)
    #print(len(Series_time))
    Series_RF=np.zeros(int((Stop-Start)/Step))
    Series_AOD=np.zeros(int((Stop-Start)/Step))
    
    Event_tracker=0
    
    time_event=np.arange(0,365*Length_of_evolution,Step*365)
    
    i=0
    while i<len(Series_time):
        looptime=Start+i*Step
        if looptime>=time[Event_tracker]:
            
            eventRF=timeevolution(time_event,RF[Event_tracker],tprod,tloss)
            eventAOD=timeevolution(time_event,AOD[Event_tracker],tprod,tloss)
            for k in range(len(eventRF)):
                Series_RF[i+k]=Series_RF[i+k]+eventRF[k]
                Series_AOD[i+k]=Series_AOD[i+k]+eventAOD[k]
            Event_tracker+=1
        i+=1
        
        if Event_tracker==len(time):
            break

    Location=Locationextractor(Series_time,Series_RF,Series_AOD,File,delimiter,header,col_time,col_loc,col_NH,col_SH,Step)

    return Series_time, Series_RF, Series_AOD, Location

def Synthetic(File,delimiter,header,col_time,col_loc,col_NH,col_SH,Start,Stop,Step,Length_of_evolution,Seed):

    Raw=ImportData(File,delimiter,header,col_time,col_loc,col_NH,col_SH)

    Datatime=Raw[0]
    DataRF=Raw_to_timeRF(Raw)[1]
    DataAOD=Raw_to_timeAOD(Raw)[1]
    if np.min(Datatime)<0:
        Time_shift=Datatime+Datatime[0]+Start
    elif np.min(Datatime)>0:
        Time_shift=Datatime-Datatime[0]+Start
    
    np.random.seed(Seed)
    np.random.shuffle(DataRF)
    np.random.shuffle(DataAOD)
    DataRF_randomized=DataRF
    DataAOD_randomized=DataAOD

    Data_rand=[Time_shift,DataRF_randomized,DataAOD_randomized]

    time,RF,AOD=datacut(Time_shift,Data_rand,Start,Stop)
    
    tprod=180
    tloss=330
    
    Series_time=np.arange(Start,Stop,Step)
    #print(len(Series_time))
    Series_RF=np.zeros(int((Stop-Start)/Step))
    Series_AOD=np.zeros(int((Stop-Start)/Step))
    
    Event_tracker=0
    
    time_event=np.arange(0,365*Length_of_evolution,Step*365)
    
    i=0
    while i<len(Series_time):
        looptime=Start+i*Step
        if looptime>=time[Event_tracker]:
            
            eventRF=timeevolution(time_event,RF[Event_tracker],tprod,tloss)
            eventAOD=timeevolution(time_event,AOD[Event_tracker],tprod,tloss)
            for k in range(len(eventRF)):
                Series_RF[i+k]=Series_RF[i+k]+eventRF[k]
                Series_AOD[i+k]=Series_AOD[i+k]+eventAOD[k]
            Event_tracker+=1
        i+=1
        
        if Event_tracker==len(time):
            break
    
    Location=Locationextractor(Series_time,Series_RF,Series_AOD,File,delimiter,header,col_time,col_loc,col_NH,col_SH,Step)

    return Series_time, Series_RF, Series_AOD, Location

def Locationextractor(Time,RF,AOD,File,delimiter,header,col_time,col_loc,col_NH,col_SH,step):

    Data=ImportData(File,delimiter,header,col_time,col_loc,col_NH,col_SH)
    Trop=np.where(Data[1]==1)[0]
    NH=np.where(Data[1]==2)[0]
    SH=np.where(Data[1]==3)[0]
    #print(Trop)
    Time_int=np.array([0]*len(Time))
    for i in range(len(Time)):
        Time_int[i]=int(Time[i])

    Tropindex=[]
    NHindex=[]
    SHindex=[]
    for j in Trop:
        i=Data[0][j]
        x=np.where(Time_int==i)[0]
        if len(x) > 0:
            Tropindex.append(x[0])
    Troptime=Time[Tropindex]
    for j in NH:
        i=Data[0][j]
        x=np.where(Time_int==i)[0]
        if len(x) > 0:
            NHindex.append(x[0])
    NHtime=Time[NHindex]
    for j in SH:
        i=Data[0][j]
        x=np.where(Time_int==i)[0]
        if len(x) > 0:
            SHindex.append(x[0])
    SHtime=Time[SHindex]

    Trop_RF=[]
    NH_RF=[]
    SH_RF=[]
    step=10/365
    for i in Tropindex:
        Trop_RF.append(RF[i+int(187/365/step)])
    for i in NHindex:
        NH_RF.append(RF[i+int(187/365/step)])
    for i in SHindex:
        SH_RF.append(RF[i+int(187/365/step)])

    Troptime=np.array(Troptime)+187/365
    NHtime=np.array(NHtime)+187/365
    SHtime=np.array(SHtime)+187/365
    RFloc=[[Troptime,Trop_RF],[NHtime,NH_RF],[SHtime,SH_RF]]
    return RFloc
