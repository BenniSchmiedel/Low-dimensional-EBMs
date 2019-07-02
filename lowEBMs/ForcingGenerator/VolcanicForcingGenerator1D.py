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


def S_to_RF(event1D,lat,aod_lin,aod_nonlin,aod_RF):
    threshold=(aod_nonlin/aod_lin)**3
    RF=np.zeros(len(lat))
    for l in range(len(lat)):
        if event1D[l]<threshold:
            RF[l]=aod_lin*aod_RF*event1D[l]
        else:
            RF[l]=aod_nonlin*aod_RF*event1D[l]**(2/3)
        
    return RF

def S_to_AOD(event1D,lat,aod_lin,aod_nonlin):
    threshold=(aod_nonlin/aod_lin)**3
    AOD=np.zeros(len(lat))
    for l in range(len(lat)):
        if event1D[l]<threshold:
            AOD[l]=aod_lin*event1D[l]
        else:
            AOD[l]=aod_nonlin*event1D[l]**(2/3)
    return AOD

def temporal_evolution(time,SH,NH,tprod,tloss,tmix_av,tres_av):

    if np.isnan(SH)==True:
        SH=np.nan_to_num(SH)
    if np.isnan(NH)==True:
        NH=np.nan_to_num(NH)

    S_H2SO4=32/98
    if SH==0:
        NH=NH*0.57*S_H2SO4
        EQ=0
    elif NH==0:
        SH=SH*S_H2SO4
        EQ=0
    else:
        EQ=(NH+SH)*S_H2SO4
        SH=0
        NH=0

    M4NH=np.zeros(len(time))
    M4NH_new=np.zeros(len(time))
    M2NH=np.zeros(len(time))
    M2NH[0]=NH
    M4SH=np.zeros(len(time))
    M4SH_new=np.zeros(len(time))
    M2SH=np.zeros(len(time))
    M2SH[0]=SH
    M4EQ=np.zeros(len(time))
    M4EQ_new=np.zeros(len(time))
    M2EQ=np.zeros(len(time))
    M2EQ[0]=EQ

    for i in range(1,len(time)):
        M2NH[i]=M2NH[i-1]*np.exp(-1/tprod)*np.exp(-1/tloss)
        M2SH[i]=M2SH[i-1]*np.exp(-1/tprod)*np.exp(-1/tloss)
        M2EQ[i]=M2EQ[i-1]*np.exp(-1/tprod)*np.exp(-1/tloss)
        M4NH_new[i]=M2NH[i-1]*(1-np.exp(-1/tprod))
        M4SH_new[i]=M2SH[i-1]*(1-np.exp(-1/tprod))
        M4EQ_new[i]=M2EQ[i-1]*(1-np.exp(-1/tprod))

    for i in range(1,len(time)):
        m=int(time[i]%365/(365/12))+1
        #print(m)
        M4tot=np.sum([M4NH[i-1],M4SH[i-1],M4EQ[i-1]])
        if M4tot>10:
            tloss_use=((tloss-6)/0.3679)*np.exp(-M4tot/10)+6
        else:
            tloss_use=tloss
        #print(tloss_use)
        mixNH=1/tmix_av*(1+0.75*np.cos((m-1)*np.pi/6))
        resNH=1/tres_av*(1+0.75*np.cos((m-1)*np.pi/6))
        mixSH=1/tmix_av*(1+0.75*np.cos((m-1+6)*np.pi/6))
        resSH=1/tres_av*(1+0.75*np.cos((m-1)*np.pi/6))
        #print(tmixNH,tmixSH)
        #M4NH[i+1]=M4NH[i]+(NH*np.exp(-i/tprod)/tprod-M4NH[i]/tloss+(M4EQ[i]-M4NH[i])/tmixNH+M4EQ[i]/tres)*h
        #M4SH[i+1]=M4SH[i]+(SH*np.exp(-i/tprod)/tprod-M4SH[i]/tloss+(M4EQ[i]-M4SH[i])/tmixSH+M4EQ[i]/tres)*h
        #M4EQ[i+1]=M4EQ[i]+(EQ*np.exp(-i/tprod)/tprod-M4EQ[i]/tloss+M4EQ[i]/tres)*h
        M4NH[i]=(M4NH[i-1]+M4NH_new[i-1])*np.exp(-1/tloss_use)\
                +(M4EQ[i-1]-M4NH[i-1])*mixNH\
                +M4EQ[i]*resNH
        M4SH[i]=(M4SH[i-1]+M4SH_new[i-1])*np.exp(-1/tloss_use)\
                 +(M4EQ[i-1]-M4SH[i-1])*mixSH\
                 +M4EQ[i]/resSH
        M4EQ[i]=(M4EQ[i-1]+M4EQ_new[i-1])*np.exp(-1/tloss_use)\
                 -(M4EQ[i-1]-M4NH[i-1])*mixNH\
                 -(M4EQ[i-1]-M4SH[i-1])*mixSH\
                 -M4EQ[i]*resNH-M4EQ[i]*resSH
                
    return M4NH, M4EQ, M4SH
                
def eruption_spatial(lat,std,mean):
    deg_rad=np.pi/180
    y=np.exp(-(np.sin(lat*deg_rad)-np.sin(mean*deg_rad))**2/(2*np.sin(std*deg_rad)**2))
    y=y/areamean(y,lat)
    return y

def areamean(x,lat):
    deg_rad=np.pi/180
    w=np.cos(lat*deg_rad)
    w = w / np.sum( w )
    area_gmean = np.sum ( w * x )
    
    return area_gmean

def spatio_temporal(M4,lat,std_ET,mean_ET,std_EQ,mean_EQ):
    
    M4_lat=[0]*len(M4[0])#np.zeros(len(M4[0])))
    for i in range(len(M4[0])):
        M4_lat[i]=eruption_spatial(lat,std_EQ,mean_EQ)*M4[1][i]\
                +eruption_spatial(lat,std_ET,mean_ET)*M4[0][i]\
                +eruption_spatial(lat,std_ET,-mean_ET)*M4[2][i]
    
    return np.array(M4_lat)

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

def Generator1D(File,delimiter,header,col_time,col_loc,col_NH,col_SH,Start,Stop,Step,Length_of_evolution,tprod,tloss,tmix_av,tres_av,lat,std_ET,mean_ET,std_EQ,mean_EQ,aod_lin,aod_nonlin,aod_RF):
    
    Raw=ImportData(File,delimiter,header,col_time,col_loc,col_NH,col_SH)
 
    Datatime=Raw[0]
    DataNH=Raw[2]
    DataSH=Raw[3]
    #DataRF=Raw_to_timeRF(Raw)[1]
    #DataAOD=Raw_to_timeAOD(Raw)[1]
    Data=[Datatime,DataNH,DataSH]

    time,NH,SH=datacut(Datatime,Data,Start,Stop)
    

    
    Event_tracker=0
    
    time_event=np.arange(0,365*Length_of_evolution,Step*365)

    Series_time=np.arange(Start,Stop,Step)
    #print(len(Series_time))
    Series_RF=np.zeros(shape=(int((Stop-Start)/Step),len(lat)))
    Series_AOD=np.zeros(shape=(int((Stop-Start)/Step),len(lat)))
    i=0
    while i<len(Series_time):
        looptime=Start+i*Step
        if looptime>=time[Event_tracker]:
            event0D=temporal_evolution(time_event,SH[Event_tracker],NH[Event_tracker],tprod,tloss,tmix_av,tres_av)
            event1D=spatio_temporal(event0D,lat,std_ET,mean_ET,std_EQ,mean_EQ)

            for k in range(len(event1D)):
                Series_RF[i+k]=Series_RF[i+k]+S_to_RF(event1D[k],lat,aod_lin,aod_nonlin,aod_RF)
                Series_AOD[i+k]=Series_AOD[i+k]+S_to_AOD(event1D[k],lat,aod_lin,aod_nonlin)
            Event_tracker+=1
        i+=1
        
        if Event_tracker==len(time):
            break

    #Location=Locationextractor(Series_time,Series_RF,Series_AOD,File,delimiter,header,col_time,col_loc,col_NH,col_SH,Step)

    return Series_time, Series_RF, Series_AOD#, Location
