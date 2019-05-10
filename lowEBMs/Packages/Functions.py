"""
In ``lowEBMs.Package.Functions`` all physical equations are defined which describe the energy balance of the earth system.

This module is structured through classes which distinguish the type of energy flux or property definition. The classes contain several functions which follow a different approach of parameterizing the respective type of energy flux/ property.

The classes which define energy fluxes are:

.. Important::

    These contain the physical functions available for the EBM. To correctly run them they need parameters as input which are parsed by ``Configuration.importer`` but **have to be given manually into the configuration.ini**. To add a function, extend your *configuration.ini* with a [func] section and insert all parameters below which are given in documentation here of the specific function. As example see :doc:`Input <../input>`, where ``flux_down.insolation`` is added.

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
from climlab.solar.orbital import LongOrbitalTable
import scipy
import builtins
import time
from lowEBMs.Packages.Variables import Vars



class flux_down:
    """
    Class defining radiative fluxes directed downwards. 
    
    Because the models in this project don't include atmospheric layers (for now), the only radiative flux directed downwards is the radiative energy coming from the sun. This function is the same for all implemented models and is described in ``flux_down.insolation`` which allows several adjustments.

    .. autosummary::
        :toctree:
        :nosignatures:

        insolation

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
                                            * unit: :math:`Watt\cdot meter^{-2}`
                                            * value: > 0 (standard 342)

                                        * *m*: Factorial change of absorbed insolation

                                            * type: float
                                            * unit: -
                                            * value: > 0
                                        
                                        * *dQ*: Additive energy offset on :math:`Q`

                                            * type: float
                                            * unit: :math:`Watt\cdot meter^{-2}`
                                            * value: any

                                       ..  _albedo:

                                        * *albedo*: The name of albedo function which is called from ``lowEBMs.Packages.Functions.albedo`` to return the albedo value/distribution. See :doc:`class albedo <functions_code/albedo>`.

                                            * type: string
                                            * unit: -
                                            * value: albedo.static, albedo.static_bud, albedo.dynamic_bud, albedo.smooth, albedo.dynamical_sel

                                        * *albedoread*: Indicates whether the albedo is provided as specific output

                                            * type: boolean 
                                            * unit: -
                                            * value: True/Flase

                                        * *albedoparam*: Provides an array of parameters the albedo function (see :doc:`class albedo <../source/code/functions_code/albedo>`)

                                            * type: array 
                                            * unit: -
                                            * value: depending on function chosen

                                        * *noise*: Indicates whether solar noise is activated or not

                                            * type: boolean 
                                            * unit: -
                                            * value: True/False

                                        * *noiseamp*: Determines the strength of the random solar noise as one standard deviation of a normal distribution (for further information see ``numpy.random.normal``)

                                            * type: float 
                                            * unit: :math:`Watt\cdot meter^{-2}`
                                            * value: >0 (e.g. noise with 1 percent of 342 is the value: 0.01*342)

                                        * *noisedelay*: Determines how often this random factor is updated to a new random factor (one factor persists until it is replaced)

                                            * type: int eger
                                            * unit: number of iteration steps
                                            * value: minimum 1 (every iteration cycle)

                                        * *seed*: Indicates whether a specific seed is used to ensure that the random numbers are the one created by this specific seed (useful for comparisons to other simulation with the same solar noise)

                                            * type: boolean
                                            * unit: -
                                            * value: True/False

                                        * *seedmanipulation*: Defines the value for the seed

                                            * type: integer
                                            * unit: -
                                            * value: any (if 0 it is everytime another seed)

                                        * *solarinput*: Indicates whether the solar insolation distribution from ``climlab.solar.insolation`` are used (recommended for 1D EBMs), which are called from ``lowEBMs.Packages.Functions.earthsystem.solarradiation``

                                            * type: boolean
                                            * unit: -
                                            * value: True/False

                                        * *convfactor*: Determines whether a conversation factor is used to change the solar insolation to another unit than Watt/m^2

                                            * type: float
                                            * unit: depending on the conversion applied
                                            * value: > 0

                                        * *timeunit*: Determines which timeunit of the solarradiation shall be used for averaging (depending on how the *stepsize_of_integration* is chosen*)

                                            * type:  string
                                            * unit: -
                                            * value: 'annualmean' (average annually and give :math:`Q` as Watt/m^2), 'year', 'month', 'day', 'second' 

                                        * *orbital*: Indicates whether the solar insolation considers manipulation through orbital parameters over time (this will replace ``lowEBMs.Packages.Functions.earthsystem.solarradiation`` by ``lowEBMs.Packages.Functions.earthsystem.solarradiation_orbital``

                                            * type: boolean
                                            * unit: -
                                            * value: True/False (if False, the year given in *orbitalyear* still matters) 

                                        * *orbitalyear*: Determines for which year (in ky) the orbitalparameters are taken (orbital parameters are provided by ``climlab.solar.orbital`` which is based on Berger (1991) and Laskar (2004)

                                            * type: integer 
                                            * unit: :math:`kyear`
                                            * value: -5000 to 0 (if 0, the year 1950 is used)

        :returns:                   The absorbed solar insolation :math:`R_{down}`

        :rtype:                     float / array(floats)  (0D / 1D)


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
                    Vars.Solar=earthsystem.solarradiation_orbital(convfactor,orbitalyear,timeunit)
                    Vars.Read[8][int(Runtime_Tracker/(4*data_readout))]=Vars.Solar
            else:
                if Runtime_Tracker==0:
                    Vars.Solar=earthsystem.solarradiation(convfactor,timeunit,orbitalyear)
                    if parallelization==True:
                        Vars.Solar=np.array([Vars.Solar]*(number_of_parallels))
        #total solar insolation with possible offset
        Q_total=Vars.Solar+dQ
            
        
        #Equation of incoming radiation
        #print(Q_total.shape,alpha.shape,type(Q_total),type(alpha),factor_solar.shape)
        
        R_in=np.transpose((np.transpose(Q_total)+z)*factor_solar*(1-np.transpose(alpha)))
        if Runtime_Tracker % 4*data_readout == 0:    #Only on 4th step (due to rk4)
            Vars.Read[10][int(Runtime_Tracker/(4*data_readout))]=R_in
        return R_in

class albedo:
    """
    Class defining the albedo distributions 

    .. autosummary::
        :nosignatures:
        :toctree:

        static
        static_bud
        dynamic_bud
        smooth
        dynamic_sel

    .. Note::

        These are special functions which are used by ``flux_down.insolation``. In the *configuration.ini* they have to be inserted in its [func]-section with the parameters used (see :ref:`albedo <albedo>`). 

    .. autofunction:: lowEBMs.Packages.Functions.albedo.static

    .. autofunction:: lowEBMs.Packages.Functions.albedo.static_bud

    .. autofunction:: lowEBMs.Packages.Functions.albedo.dynamic_bud

    .. autofunction:: lowEBMs.Packages.Functions.albedo.smooth

    .. autofunction:: lowEBMs.Packages.Functions.albedo.dynamic_sel
    """
    def static(alpha):
        """
        Function defining a static albedo value

        **Function-call arguments** \n
    
        :param float alpha:     the globally averaged albedo value

                                    * type: float
                                    * unit: -
                                    * value: 0 :math:`\leq` alpha :math:`\leq` 1

        :returns:                   The globally averaged albedo value

        :rtype:                     float (0D)      
        """
        return alpha

    def static_bud(alpha_p,border_1,border_2):
        """
        A static albedo distribution as used in :ref:`Budyko <Budyko>`. 
        
        The albedo distribution is described through three zones of albedo values.

        +------------------------+-----------------------------------------------+
        | Latitude of transition | Albedo value alhpa                            | 
        +------------------------+-----------------------------------------------+
        | < *border_1*           | low albedo zone: alpha= *alpha_p*             |
        +------------------------+-----------------------------------------------+
        | > *border_1*           | intermediate zone: alpha= *alpha_p* +0.18     |
        +------------------------+-----------------------------------------------+
        | > *border_2*           | high albedo zone: alpha= *alpha_p* +0.3       |
        +------------------------+-----------------------------------------------+

        **Function-call arguments** \n
    
        :param array albedoparam:         albedo distribution parameters *[alpha_p,border_1,border_2]*
                
                                                * *alpha_p*: The low albedo zone value

                                                    * type: float
                                                    * unit: -
                                                    * value: 0 :math:`\leq` albedo :math:`\leq` 1 (standard 0.3)
        
                                                * *border_1*: Latitude of low to intermediate albedo zone transition

                                                    * type: float
                                                    * unit: Unit of latitude (degree)
                                                    * value: 0 :math:`\leq` border_1 :math:`\leq` 90 (standard 60)
        
                                                * *border_2*: Latitude of intermediate to high albedo zone transition

                                                    * type: float
                                                    * unit: Unit of latitude (degree)
                                                    * value: 0 :math:`\leq` border_2 :math:`\leq` 1 (standard 70)

        :returns:                   The latitudinal albedo distribution

        :rtype:                     array(floats)  (1D) 
        """
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

        """
        A temperature dependant albedo distribution with three albedo regions. Approach as used in :ref:`Budyko <Budyko>` but complemented with albedo transition depending on temperature. 
        
        The albedo distribution is described through three zones of albedo values.

        +---------------------------+-----------------------------------------------+
        | Temperature of transition | Albedo value alpha                            | 
        +---------------------------+-----------------------------------------------+
        | > *T_1*                   | low albedo zone: alpha= *alpha_0*             |
        +---------------------------+-----------------------------------------------+ 
        | < *T_1* & > *T_2*         | intermediate zone: alpha= *alpha_1*           |
        +---------------------------+-----------------------------------------------+
        | < *T_2*                   | high albedo zone: alpha= *alpha_2*            |
        +---------------------------+-----------------------------------------------+

        **Function-call arguments** \n
    
        :param array albedoparam:       albedo distribution parameters *[T_1,T_2,alpha_0,alpha_1,alpha_2]*
                
                                            * *T_1*: Temperature of low to intermediate albedo zone transition

                                                * type: float
                                                * unit: :math:`Kelvin`
                                                * value: > 0 in Kelvin (standard 273.15)
    
                                            * *T_2*: Temperature of intermediate to high albedo zone transition

                                                * type: float
                                                * unit: :math:`Kelvin`
                                                * value: > 0 in kelvin (standard 263.15)
    
                                            * *alpha_0*: The low albedo zone value

                                                * type: float
                                                * unit: -
                                                * value: 0 :math:`\leq` alpha_0 :math:`\leq` 1 (standard 0.32)

                                            * *alpha_1*: The intermediate albedo zone value

                                                * type: float
                                                * unit: -
                                                * value: 0 :math:`\leq` alpha_1 :math:`\leq` 1 (standard 0.5)

                                            * *alpha_2*: The high albedo zone value

                                                * type: float
                                                * unit: -
                                                * value: 0 :math:`\leq` alpha_2 :math:`\leq` 1 (standard 0.62)

        :returns:                   The latitudinal albedo distribution

        :rtype:                     array(floats) (1D)
  
        """        

        #Defining a 3State albedo function, with temperature dependant albedo transitions at T_1 (alpha_0 to 
        #alpha_1) and T_2 (alpha_1 to alpha_2), with alpha_0 ice free, alpha_1 intermediate and alpha_2 ice
        
        #Creating array and filling with values, depending on the current latitudinal temperature
        if parallelization==True:
            
            albedo=np.array([[0]*len(Vars.Lat)]*number_of_parallels)
            if len(T_1)==number_of_parallels:  
                for i in range(number_of_parallels):          
                    for j in range(len(Vars.Lat)):
                        if Vars.T[i,j]>T_1[i]:
                            albedo[i,j]=alpha_0[i]
                        if Vars.T[i,j]<=T_1[i]:
                            albedo[i,j]=alpha_1[i]
                        if Vars.T[j]<=T_2[i]:
                            albedo[i,j]=alpha_2[i]
            else:
                for i in range(number_of_parallels):          
                    for j in range(len(Vars.Lat)):
                        if Vars.T[i,j]>T_1:
                            albedo[i,j]=alpha_0
                        if Vars.T[i,j]<=T_1:
                            albedo[i,j]=alpha_1
                        if Vars.T[j]<=T_2:
                            albedo[i,j]=alpha_2
        else:
            albedo=[0]*len(Vars.Lat)
            for j in range(len(Vars.Lat)):
                if Vars.T[j]>T_1:
                    albedo[j]=alpha_0
                if Vars.T[j]<=T_1:
                    albedo[j]=alpha_1
                if Vars.T[j]<=T_2:
                    albedo[j]=alpha_2
        return np.array(albedo)

    def smooth(T_ref,alpha_f,alpha_i,steepness):
        """
        A temperature dependant albedo distribution with tangens hyperbolicus transition. A common approach in climate modelling (for example see :ref:`North <North>`)
        
        The albedo of one latitude is defined by:

        .. math::

            \\alpha(\phi)=\\alpha_i-\\frac{1}{2}(\\alpha_i-\\alpha_f)\cdot (1+tanh(\\gamma \cdot (T(\phi)-T_{ref})))

        with the albedo value :math:`\\alpha(\phi)` and temperature :math:`T(\phi)` of latitude :math:`\phi`, an ice-covered/ice-free albedo value :math:`\\alpha_i / \\alpha_f`, the reference temperature of transition :math:`T_{ref}` and the steepness of the transition :math:`\gamma`.

        
        **Function-call arguments** \n
    
        :param array albedoparam:       albedo distribution parameters *[T_ref,alpha_f,alpha_i,steepness]*
                
                                            * *T_ref*: Reference transition temperature from ice-free to ice-covered albedo

                                                * type: float
                                                * unit: :math:`Kelvin`
                                                * value: > 0 in Kelvin (standard 273.15)
    
                                            * *alpha_i*: The ice-covered albedo value

                                                * type: float
                                                * unit: -
                                                * value: 0 :math:`\leq` alpha_i :math:`\leq` 1 (standard 0.7)
    
                                            * *alpha_f*: The ice-free albedo value

                                                * type: float
                                                * unit: -
                                                * value: 0 :math:`\leq` alpha_f :math:`\leq` 1 (standard 0.3)

                                            * *steepness*: The steepness of albedo transition (:math:`$\gamma$`)

                                                * type: float
                                                * unit: :math:`Kelvin^{-1}`
                                                * value: 0 :math:`\leq` steepness :math:`\leq` 1 (standard 0.3)

        :returns:                   The latitudinal albedo distribution

        :rtype:                     float / array(floats)  (0D / 1D)
  
        """
        #Defining a smooth abledotransition from an icefree albedo alpha_f to an icecovered albedo alpha_i
        #with the steepness gamma and the reference temperature for the transition T_ref, refering to north
        albedo=alpha_i-1/2*(alpha_i-alpha_f)*(1+np.tanh(steepness*(Vars.T-T_ref)))
        return albedo

    def dynamic_sel(Z,b):
        """
        A albedo distribution with linear temperature dependence. Approach as used by :ref:`Sellers <Sellers>`.
        
        The albedo of one latitude is defined by:

        .. math::

            &T_g(\phi)=T(\phi)-0.0065\cdot Z (\phi) \\\\
            If\;T_g(\phi)<283.15:&\quad \\alpha(\phi)=b(\phi)-0.009\cdot T_g(\phi)   \\\\
            If\;T_g(\phi)> 283.15:&\quad \\alpha(\phi)= b(\phi)-2.548

        with the albedo value :math:`\\alpha(\phi)` (maximum of 0.85) and temperature :math:`T(\phi)` of latitude :math:`\phi`, the altitude weighted temperature :math:`T_g` with the zonal mean altitude :math:`Z(\phi)` and empirical constants :math:`b(\phi)`.
        
        **Function-call arguments** \n
    
        :param array albedoparam:       albedo distribution parameters *[Z,b]*
                
                                            * *Z*: Zonal mean altitude (provided by ``Configuration.add_sellersparameters``)

                                                * type: array(float)
                                                * unit: :math:`Kelvin \cdot meter^{-1}`
                                                * value: > 0
    
                                            * *b*: Empirical constant to estimate the albedo (provided by ``Configuration.add_sellersparameters``)

                                                * type: float
                                                * unit: -
                                                * value: > 0 
    

        :returns:                   The latitudinal albedo distribution

        :rtype:                     array(floats)  (1D)
  
        """
        #Defining the albedo function defined by sellers (1969), with a linear dependency 
        
        #Shift of the temperature with the elevation to gain surface temperatures
        Tg=Vars.T-0.0065*Z

        #creating and filling array, depending on the current latitudinal temperature
        if parallelization==True:
            albedo=np.array([[0]*len(Vars.Lat)]*number_of_parallels)
            if len(Z)==number_of_parallels:  
                for i in range(number_of_parallels):                
                    for j in range(len(Vars.Lat)):
                        if Tg[i,j]<283.16:
                            albedo[i,j]=b[i,j]-0.009*Tg[i,j]
                        else:
                            albedo[i,j]=b[i,j]-2.548
                        if albedo[i,j]>0.85:
                            albedo[i,j]=0.85
            else:
                for i in range(number_of_parallels):                
                    for j in range(len(Vars.Lat)):
                        if Tg[i,j]<283.16:
                            albedo[i,j]=b[j]-0.009*Tg[i,j]
                        else:
                            albedo[i,j]=b[j]-2.548
                        if albedo[i,j]>0.85:
                            albedo[i,j]=0.85
        else:
            albedo=[0]*len(Tg)
            for j in range(len(Tg)):
                if Tg[j]<283.16:
                    albedo[j]=b[j]-0.009*Tg[j]
                else:
                    albedo[j]=b[j]-2.548
                if albedo[j]>0.85:
                    albedo[j]=0.85
        return np.array(albedo)

class flux_up:
    """ 
    Class defining radiative fluxes directed upwards.

    The equations used here are, expect from ``flux_up.planck``, are estimated empirically and the standard parameters are mostly tailored to specific applications where they are used by the authors. 

    .. autosummary::
        :toctree:
        :nosignatures:

        budyko_noclouds
        budyko_clouds
        planck
        sellers

    .. autofunction:: lowEBMs.Packages.Functions.flux_up.budyko_noclouds

    .. autofunction:: lowEBMs.Packages.Functions.flux_up.budyko_clouds

    .. autofunction:: lowEBMs.Packages.Functions.flux_up.planck

    .. autofunction:: lowEBMs.Packages.Functions.flux_up.sellers

    """

    def budyko_noclouds(funcparam):  
        """ 
        An empirically determined upward radiative energy flux which approximates the top of the atmosphere radiation emitted to space to be dependant linear on temperature. The presence of clouds is not specifically taken into account.

        The upward radiative energy flux :math:`R_{up}` of latitude :math:`\phi` is given by:
    
        .. math::

            R_{up}(\phi) = - (A + B \cdot T(\phi))
                
        with the temperature :math:`T(\phi)` and empirical constants :math:`A` and :math:`B`. The Temperature is hereby converted to Celcius because the constants are optimized for Celcius not Kelvin. 
        
        **Function-call arguments** \n

        :param dict funcparams:     a dictionary of the function's parameters directly parsed from ``lowEBMs.Packages.ModelEquation.model_equation``
                                    
                                        * *A*: Empirical offset parameter

                                            * type: float 
                                            * unit: :math:`Watt\cdot meter^{-2}`
                                            * value: any (standard 222.74)
                                    
                                        * *B*: Empirical gradient parameter

                                            * type: float 
                                            * unit: :math:`Watt\cdot meter^{-2}\cdot °Celcius^{-1}`
                                            * value: any (standard 2.23)

        :returns:                   The upward radiative energy flux :math:`R_{up}`

        :rtype:                     float / array(floats)  (0D / 1D) 

        """
        #Outgoing radiation, from empirical approximation formula by Budyko (no clouds)
        #R_outbudncparam=[A,B]
        list_parameters=list(funcparam.values())
        A,B=list_parameters
        R_out=np.transpose(-(A+B*(np.transpose(Vars.T)-273.15)))
        if Runtime_Tracker % 4*data_readout == 0:    #Only on 4th step (due to rk4)
            Vars.Read[11][int(Runtime_Tracker/(4*data_readout))]=R_out
        return R_out

    def budyko_clouds(funcparam):
        """ 
        An empirically determined upward radiative energy flux which approximates the top of the atmosphere radiation emitted to space to be dependant linear on temperature. The presence of clouds is specifically taken into account with a second temperature dependant term.

        The upward radiative energy flux :math:`R_{up}` of latitude :math:`\phi` is given by:
    
        .. math::

            R_{up}(\phi) = - ((A + B \cdot T(\phi)) - f_c\cdot (A_1+B_1\cdot T(\phi)))
                
        with the temperature :math:`T(\phi)` and empirical constants :math:`A`, :math:`B`, :math:`A_1` and :math:`B_1`. The Temperature is hereby converted to Celcius because the constants are optimized for Celcius not Kelvin 
        
        **Function-call arguments** \n

        :param dict funcparams:     a dictionary of the function's parameters directly parsed from ``lowEBMs.Packages.ModelEquation.model_equation``
                                    
                                        * *A*: Empirical offset parameter

                                            * type: float 
                                            * unit: :math:`Watt\cdot meter^{-2}`
                                            * value: any (standard 222.74)
                                    
                                        * *B*: Empirical gradient parameter

                                            * type: float 
                                            * unit: :math:`Watt\cdot meter^{-2}\cdot °Celcius^{-1}`
                                            * value: any (standard 2.23)

                                        * *A1*: Empirical offset parameter cloud term

                                            * type: float 
                                            * unit: :math:`Watt\cdot meter^{-2}`
                                            * value: any (standard 47.73)

                                        * *B1*: Empirical gradient parameter cloud term

                                            * type: float 
                                            * unit: :math:`Watt\cdot meter^{-2}\cdot °Celcius^{-1}`
                                            * value: any (standard 1.59)

                                        * *f_c*: Cloud fraction

                                            * type: float 
                                            * unit: -
                                            * value: 0 :math:`\leq` f_c :math:`\leq` 1 (standard 0.5)

        :returns:                   The upward radiative energy flux :math:`R_{up}`

        :rtype:                     float / array(floats)  (0D / 1D) 
        """
        #Outgoing radiation, from empirical approximation formula by Budyko (clouds)
        #R_outbudcparam=[A,B,A1,B1,f_c]
        list_parameters=list(funcparam.values())
        A,B,A1,B1,f_c=list_parameters
        R_out=np.transpose(-(A+B*(np.transpose(Vars.T)-273.15)-(A1+B1*(np.transpose(Vars.T)-273.15))*f_c))
        if Runtime_Tracker % 4*data_readout == 0:    #Only on 4th step (due to rk4)
            Vars.Read[11][int(Runtime_Tracker/(4*data_readout))]=R_out
        return R_out

    def planck(funcparam):
        """ 
        The stefan-boltzmann radiation for a grey body as radiative energy flux directed upward. The ideal stefan-boltzmann radiation with a temperature to the power of 4 scaled with an emissivity factor :math:`\epsilon`.

        The upward radiative energy flux :math:`R_{up}` of latitude :math:`\phi` is given by:
    
        .. math::

            R_{up}(\phi) = - \epsilon \cdot \sigma \cdot T(\phi)^4
                
        with the temperature :math:`T(\phi)`, the emissivity :math:`\epsilon` and stefan-boltzmann constant :math:`\sigma`.
        
        **Function-call arguments** \n

        :param dict funcparams:     a dictionary of the function's parameters directly parsed from ``lowEBMs.Packages.ModelEquation.model_equation``
                                    
                                        * *grey*: The emissivity (greyness)

                                            * type: float 
                                            * unit: -
                                            * value: 0 :math:`\leq` grey :math:`\leq` 1 (standard 0.612)
                                    
                                        * *sigma*: Stefan-boltzmann constant

                                            * type: float 
                                            * unit: :math:`Watt\cdot meter^{-2}\cdot Kelvin^{-4}`
                                            * value: :math:`5,67\cdot 10^{-8}` (use const.sigma to load it from ``climlab.constants``)

        :returns:                   The upward radiative energy flux :math:`R_{up}`

        :rtype:                     float / array(floats)  (0D / 1D) 

        """
        #Outgoing radiation, from plancks radiation law
        #R_outplanckparam=[grey,sig]
        list_parameters=list(funcparam.values())
        grey,sig=list_parameters
        R_out=np.transpose(-(grey*sig*np.transpose(Vars.T**4)))
        if Runtime_Tracker % 4*data_readout == 0:    #Only on 4th step (due to rk4)
            Vars.Read[11][int(Runtime_Tracker/(4*data_readout))]=R_out
        return R_out

    def sellers(funcparam):
        """ 
        An empirically, by :ref:`William Sellers <Sellers>` adjusted stefan-boltzmann radiation as radiative energy flux directed upward. The ideal stefan-boltzmann radiation with a temperature to the power of 4 and an additional tangens hyperbolicus term with the temperature to the power of 6 to take into account that cloud formation is temperature dependant.
 
        The upward radiative energy flux :math:`R_{up}` of latitude :math:`\phi` is given by:
    
        .. math::

            R_{up}(\phi) = - \sigma \cdot T(\phi)^4 \cdot (1-m\cdot tanh(\gamma \cdot T(\phi)^6)
                
        with the temperature :math:`T(\phi)`, the stefan-boltzmann constant :math:`\sigma`, the atmospheric attenuation :math:`m` and an empirical constant :math:`\gamma`. 

        To make this function more adjustable there is an additional emissivity introduced (similar to ``flux_up.planck``).
        
        **Function-call arguments** \n

        :param dict funcparams:     a dictionary of the function's parameters directly parsed from ``lowEBMs.Packages.ModelEquation.model_equation``
                                    
                                        * *m*: The atmospheric attenuation

                                            * type: float 
                                            * unit: -
                                            * value: 0 :math:`\leq` m :math:`\leq` 1 (standard 0.5)
                                    
                                        * *sigma*: Stefan-boltzmann constant

                                            * type: float 
                                            * unit: :math:`Watt\cdot meter^{-2}\cdot Kelvin^{-4}`
                                            * value: :math:`5,67\cdot 10^{-8}` (use const.sigma to load it from ``climlab.constants``)
                                    
                                        * *gamma*: Empirical constant in the cloud term

                                            * type: float 
                                            * unit: :math:`Kelvin^{-6}`
                                            * value: :math:`1.9\cdot 10^{-15}`
                                    
                                        * *grey*: The emissivity (greyness)

                                            * type: float 
                                            * unit: -
                                            * value: 0 :math:`\leq` grey :math:`\leq` 1 (standard 1)

        :returns:                   The upward radiative energy flux :math:`R_{up}`

        :rtype:                     float / array(floats)  (0D / 1D) 

        """
        #Outgoing radiation, from Sellers earth-atmosphere model
        #R_outselparam=[sig,grey,gamma,m]"""
        list_parameters=list(funcparam.values())
        m,sigma,gamma,grey=list_parameters
        R_out=np.transpose(-grey*sigma*np.transpose(Vars.T)**4*(1-m*np.tanh(gamma*np.transpose(Vars.T)**6)))
        if Runtime_Tracker % 4*data_readout == 0:    #Only on 4th step (due to rk4)
            Vars.Read[11][int(Runtime_Tracker/(4*data_readout))]=R_out
        return R_out





class transfer:
    """ 
    Class defining latitudinal energy transfer transfer fluxes.

    The equations used here are estimated empirically based on research of :ref:`Michail Budyko <Budyko>` and :ref:`William Sellers <Sellers>`. 

    .. autosummary::
        :toctree:
        :nosignatures:

        budyko
        sellers
        watervapour_sel
        sensibleheat_air_sel
        sensibleheat_ocean_sel

    Only ``transfer.budyko`` and ``transfer.sellers`` are transfer fluxes fully representing the globes meridional energy transfer, where ``transfer.sellers`` is built up from the three specific transfer fluxes ``transfer.watervapour_sel``, ``transfer.sensibleheat_air_sel`` and ``transfer.sensibleheat_ocean_sel``. 

    .. autofunction:: lowEBMs.Packages.Functions.transfer.budyko

    .. autofunction:: lowEBMs.Packages.Functions.transfer.sellers

    .. autofunction:: lowEBMs.Packages.Functions.transfer.watervapour_sel

    .. autofunction:: lowEBMs.Packages.Functions.transfer.sensibleheat_air_sel

    .. autofunction:: lowEBMs.Packages.Functions.transfer.sensibleheat_ocean_sel

    """
    def budyko(funcparam):
        """ 
        A poleward energy transfer flux based on the local to global temperature difference introduced by :ref:`Michail Budyko <Budyko>`.

        It can be shown that it is equivalent to the diffusive heat transfer of the globe (North, 1975b). 
 
        It is given by:
    
        .. math::

            F_{transfer}= \\beta\cdot(T(\phi)-T_g)
                
        with the temperature :math:`T(\phi)` of latitude :math:`\phi`, the global mean temperature :math:`T_g` and the transport parameter :math:`\\beta`. 
        
        **Function-call arguments** \n

        :param dict funcparams:     a dictionary of the function's parameters directly parsed from ``lowEBMs.Packages.ModelEquation.model_equation``
                                  
                                        * *beta*: The transport parameter

                                            * type: float 
                                            * unit: :math:`Watt\cdot meter^{-2} \cdot Kelvin^{-1}`
                                            * value: any (standard 3.74)
                                  
                                        * *Read*: Indicates whether the transfer flux is specifically provided as output

                                            * type: boolean 
                                            * unit:  -
                                            * value: True/False (standard True)
                                  
                                        * *Activated*: Indicates whether the transfer flux is actually activated

                                            * type: boolean 
                                            * unit: -
                                            * value: True/False (standard True)

        :returns:                   The Budyko energy transfer flux :math:`F_{transfer}`

        :rtype:                     array(floats)  (1D) 

        """
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
        """ 
        A energy transfer flux based on a combination of several transfer fluxes introduced by :ref:`William Sellers <Sellers>`.

        It is defined as the difference of a sum of northward and a sum of southward transfer fluxes of one latitudinal belt. The sum (in one direction) :math:`P` consists of ``transfer.watervapour_sel``, ``transfer.sensibleheat_air_sel`` and ``transfer.sensibleheat_ocean_sel``:
    
        .. math::

            P(\phi)= L\cdot c_{wv}(\phi) + C_{air}(\phi) + F_{oc}(\phi)
                
        with the energy transfer through watervapour :math:`c_{wv}(\phi)`, the energy transfer through atmospheric sensible heat :math:`C_{air}(\phi)` and  the energy transfer through oceanic sensible heat :math:`F_{oc}(\phi)` of latitude :math:`\phi` and the latent heat of condensation :math:`L`.
        
        The total energy flux, the difference of the southward and northward flux :math:`P(\phi)` weighted with the length of a latitudinal circle :math`l(\phi)` and the area of the latitudinal belt :math:`A(\phi)`, is given by:

        .. math::

            F_{transfer} = (P(\phi)\cdot l(\phi) - P (\phi+d\phi)\cdot l (\phi+d\phi))\cdot \\frac{1}{A(\phi)}

        where :math:`P(\phi)\cdot l(\phi)` is the sum of energy transfer from the latitudinal belt to the southern boundary and :math:`P (\phi+d\phi)\cdot l (\phi+d\phi)` the one to the nothern boundary (:math:`d\phi` indicates the step to the next northern gridpoint).
        
        .. Note::

            The Sellers energy transfer flux comes with a large set of parameters, some given as scalars and some as distribution over the latitudes. In order to simplify the input of these parameters, the module ``lowEBMs.Packages.Configuration.add_sellersparameters`` can be called before running the algorithm which imports the parameter distributions into the *funcparam* dictionary. **Scalars are not included there!** The easiest way is to copy the prewritten configuration of this function from the *FunctionCalls.txt* in *lowEBMs/Turotials* and use ``Configuration.add_sellersparameters``.  

        **Function-call arguments** \n

        :param dict funcparams:     a dictionary of the function's parameters directly parsed from ``lowEBMs.Packages.ModelEquation.model_equation``
                                  
                                        * *Readout*: Indicates whether **all** sellers transfer fluxes are provided as output

                                            * type: boolean 
                                            * unit: -
                                            * value: True/False (standard True)
                                  
                                        * *Activated*: Indicates if the transfer flux is actually activated

                                            * type: boolean 
                                            * unit: -
                                            * value: True/False (standard True)
                                  
                                        * *K_wv*: The thermal diffusivity of the watervapour term

                                            * type: float 
                                            * unit: :math:`meter^2\cdot second^{-1}`
                                            * value: :math:`10^5` (imported by ``Configuration.add_sellersparameters``)
                                  
                                        * *K_h*: The thermal diffusivity of the atmospheric sensible heat term

                                            * type: float 
                                            * unit: :math:`meter^2 \cdot second^{-1}`
                                            * value: :math:`10^6` (imported by ``Configuration.add_sellersparameters``)
                                  
                                        * *K_o*: The thermal diffusivity of the oceanic sensible heat term

                                            * type: float 
                                            * unit: :math:`meter^2\cdot second^{-1}`
                                            * value: :math:`10^2` (imported by ``Configuration.add_sellersparameters``)
                                  
                                        * *g*: The gravitational acceleration

                                            * type: float 
                                            * unit: :math:`meter\cdot second^{-2}`
                                            * value: :math:`9.81`
                                  
                                        * *a*: Empricial constant to calculate the meridional windspeed

                                            * type: float 
                                            * unit: :math:`meter\cdot second^{-1}\cdot °Celcius^{-1}`
                                            * value: :math:`10^-2` (imported by ``Configuration.add_sellersparameters``)
                                  
                                        * *eps*: Empirical constant of the saturation specific humidity

                                            * type: float 
                                            * unit: -
                                            * value: 0.622
                                  
                                        * *p*: The average sea level pressure

                                            * type: float 
                                            * unit: :math:`mbar`
                                            * value: 1000
                                  
                                        * *e0*: The mean sea level saturation vapour pressure

                                            * type: float 
                                            * unit: :math:`mbar`
                                            * value: 17
                                  
                                        * *L*: The latent heat of condensation

                                            * type: float 
                                            * unit: :math:`Joule\cdot gramm^{-1}`
                                            * value: :math:`2.5\cdot 10^3`
                                  
                                        * *Rd*: The gas constant

                                            * type: float 
                                            * unit: :math:`Joule\cdot gramm^{-1}\cdot Kelvin^{-1}`
                                            * value: :math:`0.287`
                                  
                                        * *dy*: The width of an latitudinal belt

                                            * type: float 
                                            * unit: :math:`meter`
                                            * value: :math:`1.11\cdot 10^6`
                                  
                                        * *dp*: The tropospheric pressure depth

                                            * type: float 
                                            * unit: :math:`mbar`
                                            * value: 700-900 (imported by ``Configuration.add_sellersparameters``)
                                  
                                        * *cp*: The specific heat capacity of air at constant pressure

                                            * type: float 
                                            * unit: :math:`Joule\cdot gramm^{-1}\cdot Kelvin^{-1}`
                                            * value: :math:`1.004`
                                  
                                        * *dz*: The average zonal ocean depth

                                            * type: float 
                                            * unit: :math:`meter`
                                            * value: 1000-4000 (imported by ``Configuration.add_sellersparameters``)
                                  
                                        * *l_cover*: The proportion of ocean covered surface

                                            * type: float 
                                            * unit: -
                                            * value: 0.5
                                  
                                        * *re*: The earth's radius

                                            * type: float 
                                            * unit: :math:`meter`
                                            * value: :math:`6.371\cdot 10^6`
                                  
                                        * *cp_w*: The specific heat capacity of sea water

                                            * type: float 
                                            * unit: :math:`Joule\cdot gramm^{-1}\cdot Kelvin^{-1}`
                                            * value: :math:`4182`
                                  
                                        * *dens_w*: The density of water

                                            * type: float 
                                            * unit: :math:`gramm\cdot meter^{-3}`
                                            * value: :math:`0.997\cdot 10^6`
                                  
                                        * *factor_wv*: A tuning factor applied to the watervapour term

                                            * type: float 
                                            * unit: -
                                            * value: any
                                  
                                        * *factor_air*: A tuning factor applied to the atmospheric sensible heat term

                                            * type: float 
                                            * unit: -
                                            * value: any
                                  
                                        * *factor_oc*: A tuning factor applied to the oceanic sensible heat term (or it's diffusivity)

                                            * type: float 
                                            * unit: -
                                            * value: any
                                  
                                        * *factor_kwv*: A tuning factor applied to the thermal diffusivity of the watervapour term

                                            * type: float 
                                            * unit: -
                                            * value: any
                                  
                                        * *factor_kair*: A tuning factor applied to the thermal diffusivity of the atmospheric sensible heat term

                                            * type: float 
                                            * unit: -
                                            * value: any

        :returns:                   The Sellers energy transfer flux :math:`F_{transfer}`

        :rtype:                     array(floats)  (1D) 

        """
        #Combined transfer fluxes, Sellers
        #Transfer_Sel=WV_Sel+SH_airSel+SH_oceanSel
        #Transfer_Selparam=[K_wv,g,a,eps,p,e0,L,Rd,dy,dp,K_h,cp,K_o,dz,l_cover,re]
        list_parameters=list(funcparam.values())
        Readout,Activated,K_wv,K_h,K_o,g,a,eps,p,e0,L,Rd,dy,dp     ,cp,dz,l_cover,re,cp_w,dens_w,factor_wv,factor_air,factor_oc,factor_kwv,factor_kair=list_parameters
        if Activated==True:
            #Parameters for different transfer Fluxes+their calculation 

            #WV_Selparam_keys=['K_wv','g','a','eps','p','e0','L','Rd','dy','dp','factor_wv','factor_kwv']
            WV_Selparam=[K_wv,g,eps,p,e0,L,Rd,dy,dp,factor_wv,factor_kwv]   
            SH_airSelparam=[K_h,g,dy,cp,dp,factor_air,factor_kair]
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
            #Apply parallelization if activated
            if parallelization==True: 
                P1=[0]*number_of_parallels
                P0=[0]*number_of_parallels
                for i in range(number_of_parallels):
                    P_1=np.insert(P[i],0,0)                     
                    P_0=np.append(P[i],0)
                    P1[i]=P_1
                    P0[i]=P_0            
            else:
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
        """ 
        The energy transfer flux through watervapour used in ``transfer.sellers``.
        
        It is based on the transport of watervapour to another latitudinal belt and it's condensation which releases energy. It is described through:

        .. math::

            c_{wv}=(v q - K_{wv}\\frac{\Delta q}{\Delta y})\cdot \\frac{\Delta p}{g}

        with the meridional windspeed :math:`v` provided by ``earthsstem.meridionalwind_sel``, the specific saturation humidity :math:`q` provided by ``earthsystem.specific_saturation_humidity_sel`` and the humidity difference :math:`dq` provided by ``earthsystem.humidity_difference``. Additional parameters are the thermal diffusivity of watervapour :math:`K_{wv}`, the width of the latitudinal belts :math:`\Delta y`, the tropospheric pressure depth :math:`\Delta p` and the gravitational acceleration :math:`g`.

        For purposes of tuning, :math:`c_{wv}` and :math:`K_{wv}` are provided with the scaling factors *factor_wv* and *factor_kwv*.

        **Function-call arguments** \n

        :param dict funcparams:     * *K_wv*: The thermal diffusivity of the watervapour term

                                        * type: float 
                                        * unit: :math:`meter^2\cdot second^{-1}`
                                        * value: :math:`10^5` (imported by ``Configuration.add_sellersparameters``)
                              
                                    * *g*: The gravitational acceleration

                                        * type: float 
                                        * unit: :math:`meter\cdot second^{-2}`
                                        * value: :math:`9.81`
                              
                                    * *eps*: Empirical constant of the saturation specific humidity

                                        * type: float 
                                        * unit: -
                                        * value: 0.622
                              
                                    * *p*: The average sea level pressure

                                        * type: float 
                                        * unit: :math:`mbar`
                                        * value: 1000
                              
                                    * *e0*: The mean sea level saturation vapour pressure

                                        * type: float 
                                        * unit: :math:`mbar`
                                        * value: 17
                              
                                    * *L*: The latent heat of condensation

                                        * type: float 
                                        * unit: :math:`Joule\cdot gramm^{-1}`
                                        * value: :math:`2.5\cdot 10^3`
                              
                                    * *Rd*: The gas constant

                                        * type: float 
                                        * unit: :math:`Joule\cdot gramm^{-1}\cdot Kelvin^{-1}`
                                        * value: :math:`0.287`
                              
                                    * *dy*: The width of an latitudinal belt

                                        * type: float 
                                        * unit: :math:`meter`
                                        * value: :math:`1.11\cdot 10^6`
                              
                                    * *dp*: The tropospheric pressure depth

                                        * type: float 
                                        * unit: :math:`mbar`
                                        * value: 700-900 (imported by ``Configuration.add_sellersparameters``)
                              
                                    * *factor_wv*: A tuning factor applied to the watervapour term

                                        * type: float 
                                        * unit: -
                                        * value: any
                              
                                    * *factor_kwv*: A tuning factor applied to the thermal diffusivity of the watervapour term

                                        * type: float 
                                        * unit: -
                                        * value: any
                                  

        :returns:                   The watervapour energy transfer flux :math:`c_{wv}`

        :rtype:                     array(floats)  (1D) 

        """
        #Transfer flow of water vapour across latitudinal bands
        #WV_Selparam=[K_wv,g,a,eps,p,e0,L,Rd,dy,dp]
        #list_parameters=list(funcparam.values())
        K_wv,g,eps,p,e0,L,Rd,dy,dp,factor_wv,factor_kwv=funcparam
        
        #calculating the specific humidity q and its latitudinal difference dq
        q=earthsystem.specific_saturation_humidity_sel(e0,eps,L,Rd,p)
        dq=earthsystem.humidity_difference(e0,eps,L,Rd,p)
        if parallelization==True:
        #equation of the water vapour energy transfer
            a1=Vars.meridional*q
            a2=K_wv*factor_kwv*dq/dy
            a3=dp*const.mb_to_Pa/g
            cL=L*(a1-a2)*a3*factor_wv
        else:
            cL=L*(Vars.meridional*q-K_wv*factor_kwv*dq/dy)*(dp*const.mb_to_Pa/g)*factor_wv
        return cL

    def sensibleheat_air_sel(funcparam):
        """ 
        The energy transfer flux through atmospheric sensible heat used in ``transfer.sellers``.

        It is based on the heat transport through wind and convection to another latitudinal belt. It is described through:

        .. math::

            C_{air}=(v T - K_h\\frac{\Delta T}{\Delta y})\cdot \\frac{c_p}{g} \Delta p

        with the meridional windspeed :math:`v` provided by ``earthsstem.meridionalwind_sel``, and the temperature difference :math:`\Delta T` provided by ``earthsystem.tempdif``. Additional parameters are the temperature :math:`T`, the thermal diffusivity of air :math:`K_{h}`, the width of the latitudinal belts :math:`\Delta y`, the tropospheric pressure depth :math:`\Delta p`, the specific heat capacity of air :math:`c_p` and the gravitational acceleration :math:`g`.

        For purposes of tuning, :math:`C_{air}` and :math:`K_{h}` are provided with the scaling factors *factor_air* and *factor_kair*.

        **Function-call arguments** \n

        :param dict funcparams:     * *K_h*: The thermal diffusivity of the atmospheric sensible heat term

                                        * type: float 
                                        * unit: :math:`meter^2\cdot second^{-1}`
                                        * value: :math:`10^6` (imported by ``Configuration.add_sellersparameters``)
                                                                
                                    * *g*: The gravitational acceleration

                                        * type: float 
                                        * unit: :math:`meter\cdot second^{-2}`
                                        * value: :math:`9.81`

                                    * *dy*: The width of an latitudinal belt

                                        * type: float 
                                        * unit: :math:`meter`
                                        * value: :math:`1.11\cdot 10^6`
                              
                                    * *dp*: The tropospheric pressure depth

                                        * type: float 
                                        * unit: :math:`mbar`
                                        * value: 700-900 (imported by ``Configuration.add_sellersparameters``)
                              
                                    * *cp*: The specific heat capacity of air at constant pressure

                                        * type: float 
                                        * unit: :math:`Joule\cdot gramm^{-1}\cdot Kelvin^{-1}`
                                        * value: :math:`1.004`
                              
                                    * *factor_air*: A tuning factor applied to the atmospheric sensible heat term

                                        * type: float 
                                        * unit: -
                                        * value: any
                              
                                    * *factor_kair*: A tuning factor applied to the thermal diffusivity of the atmospheric sensible heat term

                                        * type: float 
                                        * unit: -
                                        * value: any

        :returns:                   The atmospheric sensible heat energy transfer flux :math:`C_{air}`

        :rtype:                     array(floats)  (1D) 

        """
        #Transfer flux due to atmosphere sensible heat transfer across latitudinal bands
        #SH_airSelparam=[K_h,g,a,dy,cp,dp]
        #list_parameters=list(funcparam.values())
        K_h,g,dy,cp,dp,factor_air,factor_kair=funcparam
        
        #equation of the atmosphere sensible heat transfer, with dependence on Temperature and Temperature difference
        if parallelization==True:
            a1=Vars.meridional*Vars.T[:,:-1]
            a2=K_h*factor_kair*Vars.tempdif/dy
            a3=cp*dp*const.mb_to_Pa/g
            C=(a1-a2)*a3*factor_air
        else:
            C=(Vars.meridional*Vars.T[:-1]-K_h*factor_kair*(Vars.tempdif/(dy)))*(cp*dp*const.mb_to_Pa/g)*factor_air
        return C
        
    def sensibleheat_ocean_sel(funcparam):
        """ 
        The energy transfer flux through oceanic sensible heat used in ``transfer.sellers``.

        It is based on the heat transport through oceanic convection to another latitudinal belt. It is described through:

        .. math::

            F_{oc}= - K_o l_{cover}\Delta z\\frac{\Delta T}{\Delta y}\cdot C_{p,w}\rho_{w}

        with the temperature difference :math:`\Delta T` provided by ``earthsystem.tempdif``. Additional parameters are the thermal diffusivity of the ocean :math:`K_{o}`, the width of the latitudinal belts :math:`\Delta y`, the average ocean depth :math:`\Delta z`, the proportion of ocean cover :math:`l_{cover}`, the specific heat capacity of water :math:`c_{p,w}` and the densitiy of water :math:`\\rho_w`.

        For purposes of tuning, a scaling factors *factor_oc* is provided.

        **Function-call arguments** \n

        :param dict funcparams:     * *K_o*: The thermal diffusivity of the oceanic sensible heat term

                                        * type: float 
                                        * unit: :math:`meter^2\cdot second^{-1}`
                                        * value: :math:`10^2` (imported by ``Configuration.add_sellersparameters``)
                              
                                    * *dz*: The average zonal ocean depth

                                        * type: float 
                                        * unit: :math:`meter`
                                        * value: 1000-4000 (imported by ``Configuration.add_sellersparameters``)
                              
                                    * *l_cover*: The proportion of ocean covered surface

                                        * type: float 
                                        * unit: -
                                        * value: 0.5
                              
                                    * *cp_w*: The specific heat capacity of sea water

                                        * type: float 
                                        * unit: :math:`Joule\cdot gramm^{-1}\cdot Kelvin^{-1}`
                                        * value: :math:`4182`
                              
                                    * *dens_w*: The density of water

                                        * type: float 
                                        * unit: :math:`gramm\cdot meter^{-3}`
                                        * value: :math:`0.997\cdot 10^6`
                              
                                    * *factor_oc*: A tuning factor applied to the oceanic sensible heat term (or it's diffusivity)

                                        * type: float 
                                        * unit: -
                                        * value: any

        :returns:                   The oceanic sensible heat energy transfer flux :math:`F_{oc}`

        :rtype:                     array(floats)  (1D) 

        """
        #Transer flux due to sensible heat transfer from ocean currents
        #SH_oceanSelparam=[K_o,dz,l_cover,dy,re]
        #list_parameters=list(funcparam.values())
        K_o,dz,l_cover,dy,cp_w,dens_w,factor_oc=funcparam
        
        #equation of ocean sensible heat transfer
        if parallelization==True:
            F=-K_o*dz*l_cover*Vars.tempdif/dy*cp_w*dens_w*factor_oc
        else:
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
                freqmin=0
                freqmax=np.abs(start-stop)/steps*4/100
            if frequency=='intermediate':
                freqmin=np.abs(start-stop)/steps*4/100
                freqmax=np.abs(start-stop)/steps*12/100
            if frequency=='rare':
                freqmin=np.abs(start-stop)/steps*12/100
                freqmax=np.abs(start-stop)/steps*30/100
            if frequency=='superrare':
                freqmin=np.abs(start-stop)/steps*30/100
                freqmax=np.abs(start-stop)/steps*60/100
            
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
                        
                next_event=np.random.randint(freqmin,freqmax)
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

  
    .. autofunction:: lowEBMs.Packages.Functions.earthsystem.globalmean_temperature

    .. autofunction:: lowEBMs.Packages.Functions.earthsystem.zonalmean_insolation

    .. autofunction:: lowEBMs.Packages.Functions.earthsystem.solarradiation

    .. autofunction:: lowEBMs.Packages.Functions.earthsystem.solarradiation_orbital

    .. autofunction:: lowEBMs.Packages.Functions.earthsystem.meridionalwind_sel

    .. autofunction:: lowEBMs.Packages.Functions.earthsystem.specific_saturation_humidity_sel

    .. autofunction:: lowEBMs.Packages.Functions.earthsystem.saturation_pressure

    .. autofunction:: lowEBMs.Packages.Functions.earthsystem.humidity_difference

    .. autofunction:: lowEBMs.Packages.Functions.earthsystem.temperature_difference_latitudes

    .. autofunction:: lowEBMs.Packages.Functions.earthsystem.length_latitudes

    .. autofunction:: lowEBMs.Packages.Functions.earthsystem.area_latitudes

    """
    def globalmean_temperature():
        #Returning the cosine weighted sum of the mean annual latitudal temperature 
        #as global mean annual temperature 
        if parallelization==True:
            GMT=np.average(Vars.T, weights=cosd(Vars.Lat),axis=1)
        else:
            GMT=np.average(Vars.T, weights=cosd(Vars.Lat))
        return GMT

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

    def solarradiation_orbital(convfactor,orbitalyear,unit):
        #Calculation of solar insolations running with variable orbital parameters (for longterm runs)
        #
        
        year=orbitalyear*1000+Vars.t
        days=np.linspace(0,365,365)
        #calculation for first step
        if Runtime_Tracker == 0:
            Vars.orbtable=LongOrbitalTable()
            Vars.orbitals=Vars.orbtable.lookup_parameters(year/1000)
            Q=lna(np.mean(daily_insolation(Vars.Lat,days,Vars.orbitals),axis=1))
        #updating for each kiloyear
        if unit=='year':            
            if year % 1000==0:
                print('timeprogress: '+str(year/1000)+'ka')
                Vars.orbitals=Vars.orbtable.lookup_parameters(year/1000)
                Q=lna(np.mean(daily_insolation(Vars.Lat,days,Vars.orbitals),axis=1))
            else:
                Q=Vars.Solar
        else:
            if year % 100==0:
                print('timeprogress: '+str(year/1000)+'ka')
            else:
                Q=Vars.Solar
        return Q

    def meridionalwind_sel(a,re):
        #Calculating the global wind patterns, with the function from sellers (1969)
        #Meriwind_Selparam=[a]"""
        
        if parallelization==True:
            v=np.array([[0]*len(Vars.Lat2)]*number_of_parallels,dtype=float)
            T_av=np.average(np.abs(Vars.tempdif),weights=(2*np.pi*re*cosd(Vars.Lat2)),axis=1)

        else: 
            v=np.array([0]*len(Vars.Lat2),dtype=float)

            T_av=np.average(np.abs(Vars.tempdif),weights=(2*np.pi*re*cosd(Vars.Lat2)))
        #Globaly averaged temperature difference
        
        #filling the array with values depending on the current latitude
        i=0        
        while Vars.Lat[i]<5:
            i+=1
        k=i

        if parallelization==True:
            for l in range(number_of_parallels):
                if len(a)==number_of_parallels:
                    for j in range(k):
                        v[l,j]=-a[l,j]*(Vars.tempdif[l,j]-T_av[l])
                    for j in range(k,len(v[l])):
                        v[l,j]=-a[l,j]*(Vars.tempdif[l,j]+T_av[l])
                else:
                    for j in range(k):
                        v[l,j]=-a[j]*(Vars.tempdif[l,j]-T_av[l])
                    for j in range(k,len(v[l])):
                        v[l,j]=-a[j]*(Vars.tempdif[l,j]+T_av[l])
        else:
            for j in range(k):
                
                v[j]=-a[j]*(Vars.tempdif[j]-T_av)
                    
            for j in range(k,len(v)):
                v[j]=-a[j]*(Vars.tempdif[j]+T_av)
        return v

    def specific_saturation_humidity_sel(e0,eps,L,Rd,p):
        #equation of specific saturation humidity for WV_sel with the saturation pressure SatPr
        q=eps*earthsystem.saturation_pressure(e0,eps,L,Rd)/p
        return q
        
    def saturation_pressure(e0,eps,L,Rd):
        #temperature dependant equation of saturation pressure
        if parallelization==True:
            e=e0*(1-0.5*eps*L*Vars.tempdif/(Rd*Vars.T[:,1:]**2))
        else:
            e=e0*(1-0.5*eps*L*Vars.tempdif/(Rd*Vars.T[1:]**2))
        return e

    def humidity_difference(e0,eps,L,Rd,p):
        #equation of difference in humidity
        
        e=earthsystem.saturation_pressure(e0,eps,L,Rd)
        if parallelization==True:
            dq=eps**2*L*e*Vars.tempdif/(p*Rd*Vars.T[:,1:]**2)
        else:
            dq=eps**2*L*e*Vars.tempdif/(p*Rd*Vars.T[1:]**2)
        return dq
        
    def temperature_difference_latitudes():
        #Returning the temperature difference between the northern and southern latitudinal boundary
        if latitudinal_belt==True:
            if parallelization==True:
                dT=Vars.T[:,1:]-Vars.T[:,:-1]  
            else:
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
        
#class tools:
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
