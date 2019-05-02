"""
In ``lowEBMs.Package.Functions`` all physical equations are defined which describe the energy balance of the earth system.

This module is structured through classes which distinguish the type of energy flux or property definition. The classes contain several functions which follow a different approach of parameterizing the respective type of energy flux/ property.

The classes which define energy fluxes are:

.. autosummary::
    :toctree:

    flux_down
    flux_up
    transfer
    forcing

The classes which contain definitions of earth system properties are:

.. autosummary::
    :toctree: 

    albedo
    earthsystem

Additionally defined are tools for evaluation or simplification in the class:

.. autosummary::
    :toctree: 

    tools


"""

import numpy as np
from climlab import constants as const
from climlab.solar.insolation import daily_insolation
from climlab.solar.orbital import OrbitalTable
#from climlab.solar.orbital import LongOrbitalTable
import scipy
import builtins
import time
from lowEBMs.Packages.Variables import Vars



class flux_down:
    """
    Class defining radiative fluxes directed downwards (towards the surface). 
    
    Because the models in this project don't include atmospheric layers (for now), the only radiative flux directed downwards is the radiative energy coming from the sun. This function is the same for all implemented models and is described in ``flux_down.insolation`` which allows several adjustments.

    .. autosummary::
        :toctree:

        insolation

    **********
    insolation
    **********

    insolation
    ==========

    .. autofunction:: lowEBMs.Packages.Functions.flux_down.insolation

    """

    def insolation(funcparam):
        """
        Function defining the absorbed solar insolation. Physically there is an important difference between the insolation, which is denoted as :math:`Q` and the absorbed insolation, which is the output of this function denoted as :math:`R_{down}`. The absorbed insolation in it's simplest form is written (as introduced in the :doc:`physical background <../models>`): 

        .. math::

            R_{down} = (1-\\alpha)\cdot Q,

        with the albedo :math:`\\alpha` which is the reflected part of the insolation :math:`Q`. 

        The definition of :math:`R_{down}` in this function has several extensions:

        .. math::
    
            R_{down} = m\cdot (1-\\alpha)\cdot (Q + dQ) + z,

        with an energy offset :math:`dQ` on :math:`Q`, a factorial change of absorbed insolation :math:`m` and a random noise factor :math:`z` on the absorbed insolation. :math:`z` is chosen as a normal distributed random number with ``numpy.random.normal``.

        This function allows the observation of the models behaviour to diverse manipulations of the solar insolation.

        Input has to be given as `Dictionaries` supplied by ``lowEBMs.Packages.Configuration.importer`` from a specific **configuration.ini**.

        **Function-call arguments** \n
    
        :param dict funcparams:     a dictionary of the functions parameters directly parsed from ``lowEBMs.Packages.ModelEquation.model_equation``
                                    
                                        * *Q*: The value of solar insolation (only useful for 0D EBMs) 

                                            * type: float
                                            * unit: Watt/m^2
                                            * value: > 0 (standard 342)

                                        * *m*: Factorial change of absorbed insolation

                                            * type: float
                                            * unit: dimensionless
                                            * value: > 0
                                        
                                        * *dQ*: Additive energy offset on :math:`Q`

                                            * type: float
                                            * unit: Watt/m^2
                                            * value: any

                                        * *albedo*: The name of albedo function which is called from ``lowEBMs.Packages.Functions.albedo`` to return the albedo value/distribution. See :doc:`class albedo <functions_code/albedo>`.

                                            * type: string
                                            * unit: -
                                            * value: albedo.static, albedo.static_bud, albedo.dynamic_bud, albedo.smooth, albedo.dynamical_sel

                                        * *albedoread*: Indicates if the albedo is provided as specific output

                                            * type: boolean 
                                            * unit: -
                                            * value: True/Flase

                                        * *albedoparam*: Provides an array of parameters the albedo function (see :doc:`class albedo <../source/code/functions_code/albedo>`)

                                            * type: array 
                                            * unit: -
                                            * value: depending on function chosen

                                        * *noise*: Indicates if solar noise is activated

                                            * type: boolean 
                                            * unit: -
                                            * value: True/False

                                        * *noiseamp*: Determines the strength of the random solar noise as one standard deviation of a normal distribution (for further information see ``numpy.random.normal``)

                                            * type: float 
                                            * unit: Watt/m^2
                                            * value: >0 (e.g. noise with 1 percent of 342 is the value: 0.01*342)

                                        * *noisedelay*: Determines how often this random factor is updated to a new random factor (one factor persists until it is replaced)

                                            * type: int eger
                                            * unit: number of iteration steps
                                            * value: minimum 1 (every iteration cycle)

                                        * *seed*: Indicates if a specific seed is used to ensure that the random numbers are the one created by this specific seed (useful for comparisons to other simulation with the same solar noise)

                                            * type: boolean
                                            * unit: -
                                            * value: True/False

                                        * *seedmanipulation*: Defines the value for the seed

                                            * type: integer
                                            * unit: dimensionless
                                            * value: any (if 0 it is everytime another seed)

                                        * *solarinput*: Indicates if solar insolation distribution from ``climlab.solar.insolation`` are used (recommended for 1D EBMs), which are called from ``lowEBMs.Packages.Functions.earthsystem.solarradiation``

                                            * type: boolean
                                            * unit: -
                                            * value: True/False

                                        * *convfactor*: Determines if a conversation factor is used to change the solar insolation to another unit than Watt/m^2

                                            * type: float
                                            * unit: depending on the conversion applied
                                            * value: > 0

                                        * *timeunit*: Determines which timeunit of the solarradiation shall be used for averaging (depending on how the *stepsize_of_integration* is chosen*)

                                            * type:  string
                                            * unit: -
                                            * value: 'annualmean' (average annualy and give :math:`Q` as Watt/m^2), 'year', 'month', 'day', 'second' 

                                        * *orbital*: Indicates if the solar insolation considers manipulation through orbital parameters over time (this will replace ``lowEBMs.Packages.Functions.earthsystem.solarradiation`` by ``lowEBMs.Packages.Functions.earthsystem.solarradiation_orbital``

                                            * type: boolean
                                            * unit: -
                                            * value: True/False (if False, the year given in *orbitalyear* still matters) 

                                        * *orbitalyear*: Determines for which year (in ky) the orbitalparameters are taken (orbital parameters are provided by ``climlab.solar.orbital`` which is based on Berger (1991) and Laskar (2004)

                                            * type: integer 
                                            * unit: kiloyear
                                            * value: -5000 to 0 (if 0, the year 1950 is used)

        :returns:                   A scalar or distribution of scalars over latitude of absorbed solar insolation :math:`R_{down}` (depending on 0D, 1D and gridresolution)

        :rtype:                     Float / Array(Floats)


        """
        #Incoming radiation with latitudal dependence, albedo transition for T<T_ice, without noise
        #R_ininsolalbedo=[Conversion,alpha_p,T_ice,m]
        key=list(funcparam.keys())
        list_parameters=list(funcparam.values())
        #Loading inputparameters
        Q,factor_solar,dQ,albedofunc,albedoread,albedofuncparam,noise,noiseamp,noisedelay,    seed,seedmanipulation,solarinput,convfactor,timeunit,orbital,orbitalyear=list_parameters#R_ininsolalbedoparam
        
        #Calculating albedo from given albedofunction
        alpha=albedofunc(*albedofuncparam) 
        #Readout to give albedo as output
        if albedoread==True: 
            if Runtime_Tracker % 4*data_readout == 0:    #Only on 4th step (due to rk4)
                Vars.Read[6][int(Runtime_Tracker/(4*data_readout))]=alpha

        #Noise factor z on the solar insolation        
        z=0
        if noise==True:
            #possible noisedelay which indicates a gap between updating the noise factor
            if (int(Vars.t/stepsize_of_integration) % noisedelay)==0: 
                if (Runtime_Tracker % 4*data_readout)==0:
                    #seed if same noise is desired
                    if seed==True:
                        np.random.seed(int(Vars.t)+seedmanipulation)
                    z=np.random.normal(0,noiseamp)
                    #write to builtins and output
                    builtins.Noise_Tracker=z
                    Vars.Read[9][int(Runtime_Tracker/(4*data_readout))]=z
        z=builtins.Noise_Tracker
        
        #Calculating solar insolation distribution from functions using climlab
        
        if spatial_resolution==0:
            Vars.Solar=Q
        if solarinput==True:
            #with orbital variations (if False by default present day)
            if orbital==True:
                if Runtime_Tracker % 4*data_readout == 0:
                    Vars.Solar=earthsystem.solarradiation_orbital(convfactor,orbitalyear)
                    Vars.Read[8][int(Runtime_Tracker/(4*data_readout))]=Vars.Solar
            else:
                if Runtime_Tracker==0:
                    Vars.Solar=earthsystem.solarradiation(convfactor,timeunit,orbitalyear)
        #total solar insolation with possible offset
        Q_total=Vars.Solar+dQ
        
        #Equation of incoming radiation
        R_in=(Q_total+z)*factor_solar*(1-lna(alpha))
        if Runtime_Tracker % 4*data_readout == 0:    #Only on 4th step (due to rk4)
            Vars.Read[10][int(Runtime_Tracker/(4*data_readout))]=R_in
        return R_in

class albedo:
    """
    Class defining the albedo distribution 

    """
    def static(alpha):
        return alpha

    def static_bud(alpha_p,border_1,border_2):
        #Albedo function as used in budyko (1969), with  2albedo transitions fixed to latitudes (border_1, border_2)
        #and fixed albedos, with intermediate case +0.18 and arctic case +0.3
        
        #creating and filling array, depending on the current latitudinal temperature
        albedo=[0]*len(Vars.Lat)
        for i in range(len(Vars.Lat)):
            if np.abs(Vars.Lat[i]) <= border_1:
                albedo[i]=alpha_p
            if np.abs(Vars.Lat[i]) <= border_2 and np.abs(Vars.Lat[i]) > border_1:
                albedo[i]=alpha_p+0.18
            if np.abs(Vars.Lat[i]) <= 90 and np.abs(Vars.Lat[i]) > border_2:
                albedo[i]=alpha_p+0.3
        return albedo

    def dynamic_bud(T_1,T_2,alpha_0,alpha_1,alpha_2):
        #Defining a 3State albedo function, with temperature dependant albedo transitions at T_1 (alpha_0 to 
        #alpha_1) and T_2 (alpha_1 to alpha_2), with alpha_0 ice free, alpha_1 intermediate and alpha_2 ice
        
        #Creating array and filling with values, depending on the current latitudinal temperature
        albedo=[0]*len(Vars.T)
        for j in range(len(Vars.T)):
            if Vars.T[j]>T_1:
                albedo[j]=alpha_0
            if Vars.T[j]<=T_1:
                albedo[j]=alpha_1
            if Vars.T[j]<=T_2:
                albedo[j]=alpha_2
        return albedo

    def smooth(T_ref,alpha_f,alpha_i,steepness):
        #Defining a smooth abledotransition from an icefree albedo alpha_f to an icecovered albedo alpha_i
        #with the steepness gamma and the reference temperature for the transition T_ref, refering to north
        albedo=alpha_i-1/2*(alpha_i-alpha_f)*(1+np.tanh(steepness*(Vars.T-T_ref)))
        return albedo

    def dynamic_sel(Z,b):
        #Defining the albedo function defined by sellers (1969), with a linear dependency 
        
        #Shift of the temperature with the elevation to gain surface temperatures
        Tg=Vars.T-0.0065*Z
        
        #creating and filling array, depending on the current latitudinal temperature
        albedo=[0]*len(Tg)
        for i in range(len(Tg)):
            if Tg[i]<283.16:
                albedo[i]=b[i]-0.009*Tg[i]
            else:
                albedo[i]=b[i]-2.548
            if albedo[i]>0.85:
                albedo[i]=0.85
        return albedo

class flux_up:
    """ 
    Class defining upward radiative fluxes

    """

    def budyko_noclouds(funcparam):     
        #Outgoing radiation, from empirical approximation formula by Budyko (no clouds)
        #R_outbudncparam=[A,B]
        list_parameters=list(funcparam.values())
        A,B=list_parameters
        R_out=-(A+B*(Vars.T-273.15))
        if Runtime_Tracker % 4*data_readout == 0:    #Only on 4th step (due to rk4)
            Vars.Read[11][int(Runtime_Tracker/(4*data_readout))]=R_out
        return R_out

    def budyko_clouds(funcparam):
        #Outgoing radiation, from empirical approximation formula by Budyko (clouds)
        #R_outbudcparam=[A,B,A1,B1,f_c]
        list_parameters=list(funcparam.values())
        A,B,A1,B1,f_c=list_parameters
        R_out=-(A+B*(np.array(Vars.T)-273.15)-(A1+B1*(np.array(Vars.T)-273.15))*f_c)
        if Runtime_Tracker % 4*data_readout == 0:    #Only on 4th step (due to rk4)
            Vars.Read[11][int(Runtime_Tracker/(4*data_readout))]=R_out
        return R_out

    def planck(funcparam):
        #Outgoing radiation, from plancks radiation law
        #R_outplanckparam=[grey,sig]
        list_parameters=list(funcparam.values())
        grey,sig=list_parameters
        R_out=-(grey*sig*Vars.T**4)
        if Runtime_Tracker % 4*data_readout == 0:    #Only on 4th step (due to rk4)
            Vars.Read[11][int(Runtime_Tracker/(4*data_readout))]=R_out
        return R_out

    def sellers(funcparam):
        #Outgoing radiation, from Sellers earth-atmosphere model
        #R_outselparam=[sig,grey,gamma,m]"""
        list_parameters=list(funcparam.values())
        m,sig,gamma,grey=list_parameters
        R_out=-grey*sig*Vars.T**4*(1-m*np.tanh(gamma*Vars.T**6))
        if Runtime_Tracker % 4*data_readout == 0:    #Only on 4th step (due to rk4)
            Vars.Read[11][int(Runtime_Tracker/(4*data_readout))]=R_out
        return R_out





class transfer:
    """
    Class defining latitudinal transfer fluxes

    """
    def budyko(funcparam):
        #Diffusive transfer flow by Budyko
        #A_budpama=[beta]
        list_parameters=list(funcparam.values())
        beta,Read,Activated=list_parameters
        if Activated==True: #with activation statement
            F=beta*(Vars.T_global-Vars.T)        
        else:
            F=0
        #Reading the distribution to give an output
        if Read==True:
            if Runtime_Tracker % 4*data_readout == 0:
                Vars.Read[7][int(Runtime_Tracker/(4*data_readout))]=F
        return F

    def sellers(funcparam):
        #Combined transfer fluxes, Sellers
        #Transfer_Sel=WV_Sel+SH_airSel+SH_oceanSel
        #Transfer_Selparam=[K_wv,g,a,eps,p,e0,L,Rd,dy,dp,K_h,cp,K_o,dz,l_cover,re]
        list_parameters=list(funcparam.values())
        Readout,Activated,K_wv,K_h,K_o,g,a,eps,p,e0,L,Rd,dy,dp     ,cp,dz,l_cover,re,cp_w,dens_w,factor_wv,factor_air,factor_oc,factor_kwv,factor_kair=list_parameters
        if Activated==True:
            #Parameters for different transfer Fluxes+their calculation 

            #WV_Selparam_keys=['K_wv','g','a','eps','p','e0','L','Rd','dy','dp','factor_wv','factor_kwv']
            WV_Selparam=[K_wv,g,a,eps,p,e0,L,Rd,dy,dp,factor_wv,factor_kwv]   
            SH_airSelparam=[K_h,g,a,dy,cp,dp,factor_air,factor_kair]
            SH_oceanSelparam=[K_o,dz,l_cover,dy,cp_w,dens_w,factor_oc]
            
            #calculating the current temperature differences and wind patterns
            Vars.tempdif=earthsystem.temperature_difference_latitudes()
            Vars.meridional=earthsystem.meridionalwind_sel(a,re)
            
            #calculating the 3 transfer components
            Lc=transfer.watervapour_sel(WV_Selparam)
            C=transfer.sensibleheat_air_sel(SH_airSelparam)
            F=transfer.sensibleheat_ocean_sel(SH_oceanSelparam)
            P=Lc+C+F                  
            
            #calculation of gridparameters (for 1st step only)
            if Runtime_Tracker==0:
                Vars.latlength=earthsystem.length_latitudes(re)
                Vars.Area=earthsystem.area_latitudes(re)
                
            #Converting Arrays to two arrays with an one element shift
            P1=np.insert(P,0,0)                       
            P0=np.append(P,0)
            l1=np.insert(Vars.latlength,0,0)
            l0=np.append(Vars.latlength,0)
            
            #resulting latitudinal transfer flow, weighted with the gridparameters
            Transfer=(P1*l1-P0*l0)/Vars.Area
            Readdata=[Lc,C,F,Vars.meridional,P,Transfer]
            
            #reading for output
            if Readout==True:
                if Runtime_Tracker % 4*data_readout == 0:
                    for l in range(6):
                        Vars.Read[l][int(Runtime_Tracker/(4*data_readout))]=Readdata[l]
        else:
            Transfer=0
        return Transfer

    def watervapour_sel(funcparam):
        #Transfer flow of water vapour across latitudinal bands
        #WV_Selparam=[K_wv,g,a,eps,p,e0,L,Rd,dy,dp]
        #list_parameters=list(funcparam.values())
        K_wv,g,a,eps,p,e0,L,Rd,dy,dp,factor_wv,factor_kwv=funcparam
        
        #calculating the specific humidity q and its latitudinal difference dq
        q=earthsystem.specific_saturation_humidity_sel(e0,eps,L,Rd,p)
        dq=earthsystem.humidity_difference(e0,eps,L,Rd,p)
        
        #equation of the water vapour energy transfer
        c=L*(Vars.meridional*q-K_wv*factor_kwv*(dq/(dy)))*((dp*const.mb_to_Pa)/g)*factor_wv
        return c

    def sensibleheat_air_sel(funcparam):
        #Transfer flux due to atmosphere sensible heat transfer across latitudinal bands
        #SH_airSelparam=[K_h,g,a,dy,cp,dp]
        #list_parameters=list(funcparam.values())
        K_h,g,a,dy,cp,dp,factor_air,factor_kair=funcparam
        
        #equation of the atmosphere sensible heat transfer, with dependence on Temperature and Temperature difference
        C=(Vars.meridional*Vars.T[:-1]-K_h**factor_kair*(Vars.tempdif/(dy)))*(cp*dp*const.mb_to_Pa/g)*factor_air
        return C
        
    def sensibleheat_ocean_sel(funcparam):
        #Transer flux due to sensible heat transfer from ocean currents
        #SH_oceanSelparam=[K_o,dz,l_cover,dy,re]
        #list_parameters=list(funcparam.values())
        K_o,dz,l_cover,dy,cp_w,dens_w,factor_oc=funcparam
        
        #equation of ocean sensible heat transfer
        F=-K_o*dz*l_cover*Vars.tempdif/(dy)*cp_w*dens_w*factor_oc
        return F


class forcing:
    """Class defining forcing terms"""
    def random(funcparam):
        list_parameters=list(funcparam.values())
        forcingnumber,start,stop,steps,timeunit,strength,frequency,behaviour,lifetime,seed,sign=list_parameters
        if Runtime_Tracker==0:
            random_events_time=np.arange(start,stop+steps,steps)

            #if BP==True:
            #    random_events_time=-(lna(random_events_time)-start)
            if timeunit=='minute':
                random_events_time=lna(random_events_time)*60
            if timeunit=='hour':
                random_events_time=lna(random_events_time)*60*60
            if timeunit=='day':
                random_events_time=lna(random_events_time)*60*60*24
            if timeunit=='week':
                random_events_time=lna(random_events_time)*60*60*24*7
            if timeunit=='month':
                random_events_time=lna(random_events_time)*60*60*24*365/12
            if timeunit=='year':
                random_events_time=lna(random_events_time)*60*60*24*365

            random_events=[0]*len(random_events_time)
            i=0
            np.random.seed(seed)
            if frequency=='common':
                freq=np.abs(start-stop)/steps*4/100
            if frequency=='intermediate':
                freq=np.abs(start-stop)/steps*12/100
            if frequency=='rare':
                freq=np.abs(start-stop)/steps*30/100
            
            while i<len(random_events):
                current_event=np.random.uniform(0,strength)
                #random_events[i]=current_event
                if behaviour=='step':
                    for k in range(int(lifetime)):
                        if i+k==len(random_events):
                            break
                        random_events[i+k]=current_event
                if behaviour=='exponential':
                    for k in range(int(lifetime*4)):
                        if i+k==len(random_events):
                            break
                        random_events[i+k]=current_event*np.exp(-k/lifetime)
                        
                next_event=np.random.randint(0,freq)
                i=i+next_event
            if sign=='negative':
                Vars.ExternalInput[forcingnumber]=[random_events_time,-lna(random_events)]
            elif sign=='positive':
                Vars.ExternalInput[forcingnumber]=[random_events_time,lna(random_events)]

        while Vars.t>Vars.ExternalInput[forcingnumber][0][Vars.ForcingTracker[forcingnumber][0]]:
            if Vars.ForcingTracker[forcingnumber][0]==(len(Vars.ExternalInput[forcingnumber][0])-1):
                Vars.ForcingTracker[forcingnumber][1]=0
                break
            else:
                Vars.ForcingTracker[forcingnumber][1] = Vars.ExternalInput[forcingnumber][1][Vars.ForcingTracker[forcingnumber][0]]
                Vars.ForcingTracker[forcingnumber][0] += 1
        F=Vars.ForcingTracker[forcingnumber][1]
        if Runtime_Tracker % 4*data_readout == 0:
            Vars.ExternalOutput[forcingnumber][int(Runtime_Tracker/(4*data_readout))]=F
        return F


    def predefined(funcparam):
        list_parameters=list(funcparam.values())
        forcingnumber,datapath,name,delimiter,header,col_time,col_forcing,timeunit,BP,time_start,k=list_parameters
        if Runtime_Tracker==0:
            Vars.ExternalInput[forcingnumber]=np.genfromtxt(str(datapath)+str(name),delimiter=str(delimiter),skip_header=header,usecols=(col_time,col_forcing),unpack=True,encoding='ISO-8859-1')  
            Vars.External_time_start[forcingnumber]=time_start    
            if BP==True:
                Vars.ExternalInput[forcingnumber][0]=-(lna(Vars.ExternalInput[forcingnumber][0])-Vars.External_time_start[forcingnumber])
            if BP==False:
                Vars.ExternalInput[forcingnumber][0]=lna(Vars.ExternalInput[forcingnumber][0])+Vars.External_time_start[forcingnumber]
            if timeunit=='minute':
                Vars.ExternalInput[forcingnumber][0]=lna(Vars.ExternalInput[forcingnumber][0])*60
            if timeunit=='hour':
                Vars.ExternalInput[forcingnumber][0]=lna(Vars.ExternalInput[forcingnumber][0])*60*60
            if timeunit=='day':
                Vars.ExternalInput[forcingnumber][0]=lna(Vars.ExternalInput[forcingnumber][0])*60*60*24
            if timeunit=='week':
                Vars.ExternalInput[forcingnumber][0]=lna(Vars.ExternalInput[forcingnumber][0])*60*60*24*7
            if timeunit=='month':
                Vars.ExternalInput[forcingnumber][0]=lna(Vars.ExternalInput[forcingnumber][0])*60*60*24*365/12
            if timeunit=='year':
                Vars.ExternalInput[forcingnumber][0]=lna(Vars.ExternalInput[forcingnumber][0])*60*60*24*365
        
        while Vars.t>Vars.ExternalInput[forcingnumber][0][Vars.ForcingTracker[forcingnumber][0]]:
            if Vars.ForcingTracker[forcingnumber][0]==(len(Vars.ExternalInput[forcingnumber][0])-1):
                Vars.ForcingTracker[forcingnumber][1]=0
                break
            else:
                Vars.ForcingTracker[forcingnumber][1] = Vars.ExternalInput[forcingnumber][1][Vars.ForcingTracker[forcingnumber][0]]
                Vars.ForcingTracker[forcingnumber][0] += 1
        F=Vars.ForcingTracker[forcingnumber][1]*k
        if Runtime_Tracker % 4*data_readout == 0:
            Vars.ExternalOutput[forcingnumber][int(Runtime_Tracker/(4*data_readout))]=F
        return F


    def co2_myhre(funcparam):
        list_parameters=list(funcparam.values())
        A,C_0,CO2_base,datapath,name,delimiter,header,footer,col_time,col_conc,timeunit,BP,time_start=list_parameters
        if Runtime_Tracker==0:
            Vars.CO2=np.genfromtxt(str(datapath)+str(name),delimiter=str(delimiter),skip_header=header,skip_footer=footer,usecols=(col_time,col_conc),unpack=True,encoding='ISO-8859-1')  
            Vars.CO2_time_start=time_start    
            if BP==True:
                Vars.CO2[0]=-(lna(Vars.CO2[0])-Vars.CO2_time_start)
            if BP==False:
                Vars.CO2[0]=lna(Vars.CO2[0])+Vars.CO2_time_start
            if timeunit=='minute':
                Vars.CO2[0]=lna(Vars.CO2[0])*60
            if timeunit=='hour':
                Vars.CO2[0]=lna(Vars.CO2[0])*60*60
            if timeunit=='day':
                Vars.CO2[0]=lna(Vars.CO2[0])*60*60*24
            if timeunit=='week':
                Vars.CO2[0]=lna(Vars.CO2[0])*60*60*24*7
            if timeunit=='month':
                Vars.CO2[0]=lna(Vars.CO2[0])*60*60*24*365/12
            if timeunit=='year':
                Vars.CO2[0]=lna(Vars.CO2[0])*60*60*24*365
            
            if Vars.CO2[0][0]>Vars.CO2[0][1]:
                Vars.CO2[0]=np.flip(Vars.CO2[0],axis=0)
                Vars.CO2[1]=np.flip(Vars.CO2[1],axis=0)
            Vars.CO2Tracker[1]=A*(np.log(CO2_base/C_0))
        while Vars.t>Vars.CO2[0][Vars.CO2Tracker[0]]:
            if Vars.CO2Tracker[0]==(len(Vars.CO2[0])-1):
                Vars.CO2Tracker[1]=A*(np.log(CO2_base/C_0))
                break
            else:
                
                Vars.CO2Tracker[1] = A*(np.log(Vars.CO2[1][Vars.CO2Tracker[0]]/C_0))
                Vars.CO2Tracker[0] += 1
        F=Vars.CO2Tracker[1]
        if Runtime_Tracker % 4*data_readout == 0:
            Vars.CO2Forcing[int(Runtime_Tracker/(4*data_readout))]=F
        return F


class earthsystem:
    """
    Class defining earthsystem properties
    """
    def globalmean_temperature():
        #Returning the cosine weighted sum of the mean annual latitudal temperature 
        #as global mean annual temperature 
        return np.average(Vars.T, weights=cosd(Vars.Lat))

    def zonalmean_insolation():
        #Calculation of the annual mean solar radiation over latitudes from
        #the climlab package 
        days=np.linspace(0,365,365)
        Q=lna(np.mean(daily_insolation(Vars.Lat,days),axis=1))
        return Q

    def solarradiation(convfactor,timeunit,orbitalyear):
        #Calculation of the mean solar radiation over latitude with time specification
        
        #Adjustment of orbital parameters to specfific year (from climlab), else present day
        if orbitalyear==0:
            Vars.orbitals={'ecc': 0.017236, 'long_peri': 281.37, 'obliquity': 23.446}
        else:
            Vars.orbtable=LongOrbitalTable()
            Vars.orbitals=Vars.orbtable.lookup_parameters(orbitalyear)
            
        #returning the annual mean solar insolation or solar insolations varying over time, depending on the
        #time specified
        if timeunit=='annualmean':
            days=np.linspace(0,365,365)
            Q=lna(np.mean(daily_insolation(Vars.Lat,days,Vars.orbitals),axis=1))
        if timeunit=='year':
            Q=lna(np.mean(daily_insolation(Vars.Lat,np.linspace(            0,((365*int(Vars.t)-1) % 365)*stepsize_of_integration % 365,36),Vars.orbitals),axis=1))*convfactor
        if timeunit=='month':
            Q=lna(np.mean(daily_insolation(Vars.Lat,np.linspace(            (int(Vars.t)*365/12) % 365,(int(Vars.t)*365/12-1) % 365,30),Vars.orbitals),axis=1))*convfactor
        if timeunit=='day':
            Q=lna(daily_insolation(Vars.Lat,int(Vars.t)%365,Vars.orbitals))*convfactor
        if timeunit=='second':
            tconv=60*60*24
            Q=lna(daily_insolation(Vars.Lat,int(Vars.t/tconv)%365,Vars.orbitals))*convfactor
        return Q

    def solarradiation_orbital(convfactor,orbitalyear):
        #Calculation of solar insolations running with variable orbital parameters (for longterm runs)
        #
        year=orbitalyear*1000+Vars.t/365
        days=np.linspace(0,365,365)
        #calculation for first step
        if Runtime_Tracker == 0:
            Vars.orbtable=LongOrbitalTable()
            Vars.orbitals=Vars.orbtable.lookup_parameters(year/1000)
            Q=lna(np.mean(daily_insolation(Vars.Lat,days,Vars.orbitals),axis=1))
        #updating for each kiloyear
        if year % 1000==0:
            print('timeprogress: '+str(year/1000)+'ka')
            Vars.orbitals=Vars.orbtable.lookup_parameters(year/1000)
            Q=lna(np.mean(daily_insolation(Vars.Lat,days,Vars.orbitals),axis=1))
        else:
            Q=Vars.Solar
        return Q

    def meridionalwind_sel(a,re):
        #Calculating the global wind patterns, with the function from sellers (1969)
        #Meriwind_Selparam=[a]"""
        v=[0]*len(Vars.tempdif)
        i=0
        #Globaly averaged temperature difference
        Lat=np.insert(Vars.Lat2[:-1],0,-90)
        T_av=np.average(np.abs(Vars.tempdif),weights=(2*np.pi*re*cosd(Vars.Lat2)))
        #filling the array with values depending on the current latitude
        while Vars.Lat[i]<5:
            i+=1
        for k in range(i):
            v[k]=-a[k]*(Vars.tempdif[k]-T_av)
        for l in range(i,len(Vars.tempdif)):
            v[l]=-a[l]*(Vars.tempdif[l]+T_av)
        return v

    def specific_saturation_humidity_sel(e0,eps,L,Rd,p):
        #equation of specific saturation humidity for WV_sel with the saturation pressure SatPr
        q=eps*earthsystem.saturation_pressure(e0,eps,L,Rd)/p
        return q
        
    def saturation_pressure(e0,eps,L,Rd):
        #temperature dependant equation of saturation pressure
        e=e0*(1-0.5*eps*L*Vars.tempdif/(Rd*Vars.T[1:]**2))
        return e

    def humidity_difference(e0,eps,L,Rd,p):
        #equation of difference in humidity
        e=earthsystem.saturation_pressure(e0,eps,L,Rd)
        dq=eps**2*L*e*Vars.tempdif/(p*Rd*Vars.T[1:]**2)
        return dq
        
    def temperature_difference_latitudes():
        #Returning the temperature difference between the northern and southern latitudinal boundary
        if latitudinal_belt==True:
            dT=Vars.T[1:]-Vars.T[:-1]  
        #Calculation if for sellers it is desired to be defined on the latitudinal circles, 
        #with interpolation towards the poles
        if latitudinal_circle==True:
            f=interpolator(Vars.Lat,Vars.T)
            if both_hemispheres==True:
                Lat_new=np.linspace(-90,90,int(180/spatial_resolution+1))
            else:
                Lat_new=np.linspace(0,90,int(90/spatial_resolution+1))
            dT=f(Lat_new)[1:]-f(Lat_new)[:-1]
        return dT

    def length_latitudes(radius):
        #Returning the length of a latitudinal circle
        r_new=radius*cosd(Vars.Lat2)
        return 2*np.pi*r_new

    def area_latitudes(re):
        #Returning the area of a latitudinal belt
        
        #using latitudinal boundaries from circle defined latitudes 
        lat_southbound=Vars.Lat2
        lat_southbound=np.insert(lat_southbound,0,-90)
        lat_northbound=Vars.Lat2
        lat_northbound=np.append(lat_northbound,90)
        #calculation from the areaportions of a sphere
        S_p=np.pi*re**2*(sind((90-lat_southbound))**2+(1-cosd(90-lat_southbound))**2)-         np.pi*re**2*(np.sin((90-lat_northbound)*np.pi/180)**2+(1-np.cos((90-lat_northbound)*np.pi/180))**2)
        
        #define globally
        Vars.Area=S_p
        Vars.bounds=[lat_southbound,lat_northbound]
        return S_p 
        
class tools:
    """
    Class with useful functions and evaluation tools 
    """
    def lna(a):
        return np.array(a)      #conversion of list to numpy array

    def nal(a):
        return np.ndarray.tolist(a)   #conversion of numpy array to list

    def cosd(Lat):
        #Returning the value of cosine with input in degree    
        return np.cos(Lat*np.pi/180)

    def sind(Lat):
        #Returning the value of sine with input in degree
        return np.sin(Lat*np.pi/180)

    def plotmeanstd(array):
        #calculation of an arrays mean value and standard deviation, with regard to the equilibrium condition chosen
        #Used to process the final output data
        arraymean=np.mean(array[:][-int(eq_condition_length):],axis=0)
        arraystd=np.std(array[:][-int(eq_condition_length):],axis=0)
        
        #for l in range(len(arraynew)):
        #    arraymean.append(np.mean(arraynew[l][-eq_condition_length:]))
        #    arraystd.append(np.std(arraynew[l][-eq_condition_length:]))
        return arraymean, arraystd

    def datasetaverage(dataset):
        #error estimation of the final output data, for now limited to calculate mean values and standard deviations
        #of temperature, but with the possibility to do it for all of the readout data
        Readoutlen=len(dataset[2])
        Readzipk=[]
        Readdataaverage=[]
        for k in range(Readoutlen): 
            Mean_mean=np.mean(dataset[2][k],axis=0)
            Mean_std=np.std(dataset[2][k],axis=0)
            Readdataaverage.append([Mean_mean,Mean_std])
        
        return Readdataaverage

    def interpolator(arrayx,arrayy):
        #Returning the interpolation function (with a polyfit) of a parameter or variable
        z=np.polyfit(arrayx,arrayy,4)
        f=np.poly1d(z)
        return f

    def SteadyStateConditionGlobal(Global):
        #equilibrium condition of the RK4-algorithm, checking if the condition is fulfilled or not
        dT=np.std(Global)
        #if fulfilled, return True to interupt the algorithm and stop with output message
        if dT <= eq_condition_amplitude:
            print('Steady State reached after %s steps, within %s seconds'               %(int(Runtime_Tracker/(4*data_readout)),(time.time() - Vars.start_time)))
            return True
        #if not fulfilled return False, until the integrationnumber is exceeded
        if Runtime_Tracker==(number_of_integration-1)*4:
            print('Transit State within %s seconds' %(time.time() - Vars.start_time))
            return True
        else:
            return False

    def BPtimeplot(time,number):
        time_new = (lna(time)/stepsize_of_integration-Vars.External_time_start[number])
        return time_new
