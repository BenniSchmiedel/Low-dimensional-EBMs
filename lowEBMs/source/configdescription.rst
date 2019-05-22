*****************************
Configuration-Section Options
*****************************

[eqparam], [rk4input] and [initials]
====================================

The options of these sections are always the same and are always required! After the ``Configuration.importer`` function processes the **.ini**-file, these options are distributed to the functions of the model algorithm. For more information about the parameters, for ``[eqparam]`` see :doc:`ModelEquation <code/modelequation>`, for ``[rk4input]`` see :doc:`variable_importer <code/variables>` and for ``[initials]`` see :doc:`variable_importer <code/variables>`::

    [eqparam]
    C_ao=70*4.2e6

    [rk4input]
    number_of_integration=365*10
    stepsize_of_integration=60*60*24
    spatial_resolution=0
    both_hemispheres=True
    latitudinal_circle=True
    latitudinal_belt=False

    eq_condition=False
    eq_condition_length=100
    eq_condition_amplitude=1e-3

    data_readout=1
    number_of_externals=0

    [initials]
    time=0
    zmt=273+15
    gmt=273+15
    latitude_c=0
    latitude_b=0
    initial_temperature_cosine=False
    initial_temperature_amplitude=30
    initial_temperature_noise=True
    initial_temperature_noise_amplitude=5

[func]
======

The options for a ``[func]`` section are all physical functions defined in :doc:`Functions <code/functions>` which describe an Energy flux. There are four classes which contain such functions, ``Functions.flux_down``, ``Functions.flux_up``, ``Functions.transfer`` and ``Functions.forcing``. 

The functions and examples of their required parameters are listed here after their class. 

.. Important::

    There may only be one option each of ``Functions.flux_down``, ``Functions.flux_up`` and  ``Functions.transfer`` be used while multiple functions of ``Functions.forcing`` might be used.

flux_down Options
-----------------

There is only one option, the :ref:`insolation <fluxdown>`::

    [func0]
    func=flux_down.insolation
    Q=1
    m=1
    dQ=0

    albedo=albedo.dynamic_bud
    albedoread=True           
    albedoparam=[273.15-5,273.15-15,0.32,0.5,0.75]  

    noise=False
    noiseamp=342*0.03
    noisedelay=1
    seed=True
    seedmanipulation=0

    sinusodial=True
    convfactor=1
    timeunit='annualmean'
    orbital=False   
    orbitalyear=0

flux_up Options
---------------

Option 1, :ref:`Budyko clear sky <code.functioncode.flux_up.Budykonoclouds>`::

    [func1]
    func=flux_up.budyko_noclouds
    A=230.31
    B=2.2274

Option 2, :ref:`Budyko cloudy sky <code/functioncode/flux_up/Budykoclouds>`::

    [func1]
    func=flux_up.budyko_clouds
    A=230.31
    B=2.2274
    A1=3.0*15.91
    B1=0.1*15.91
    fc=0.5

Option 3, :ref:`Stefan-Boltzmann radiation <fluxdown>`::

    [func1]
    func=flux_up.planck
    grey=0.612
    sigma=const.sigma

Option 4, :ref:`Sellers <Sellersradiation>`::

    [func1]
    func=flux_up.sellers
    grey=0.5
    sig=const.sigma
    gamma=1.9*10**(-15)
    m=1

transfer Options
----------------

Option 1, :ref:`Budyko transfer <Budykotransfer>`::

    [func2]
    func=transfer.budyko
    beta=3.18
    Read=True
    Activated=True

Option 2, :ref:`Sellers transfer <Sellerstransfer>`::

    [func2]
    func=transfer.sellers
    Readout=True
    Activated=True
    K_wv=10**5
    K_h=10**6
    K_o=10**2
    g=9.81
    a=2/100
    eps=0.622
    p=1000
    e0=1700
    L=const.Lhvap/1000
    Rd=const.Rd/1000
    dy=1.11*10**6
    dp=800
    cp=const.cp
    dz=2000
    l_cover=0.5
    radius=const.a
    cp_w=4182
    dens_w=998
    factor_wv=1
    factor_air=1
    factor_oc=1
    factor_kwv=1
    factor_kair=1

forcing Options
---------------

.. Important::
    
    If you use multiple ``forcing.random```and ``forcing.predefiend`` you have to increase the value of the option **forcingnumber** by 1, this will create an additional space in the output-array and an internal counter of the forcings.

Option 1, :ref:`Random forcing <Randomforcing>`::

    [func3]
    func=forcing.random
    forcingnumber=0
    start=1958
    stop=2018
    steps=1/365
    timeunit='year'
    strength=10
    frequency='rare'
    behaviour='exponential'
    lifetime=365
    seed=None
    sign='negative'

Option 2, :ref:`Imported predefined forcing <Predefinedforcing>`::

    [func4]
    func=PredefinedForcing
    forcingnumber=1
    datapath="../Config"
    name="Forcingdata.csv"
    delimiter=","
    header=1
    col_time=1
    col_forcing=2
    timeunit='year'
    BP=False
    time_start=7362.5
    k=1

Option 3, :ref:`Imported CO2 forcing after Myhre <CO2forcing>`::

    [func5]
    func=forcing.co2_myhre
    A=5.35
    C_0=280
    CO2_base=280
    datapath="../Config/Data/"
    name="CO2data.csv"
    delimiter=","
    header=0
    footer=0
    col_time=3
    col_forcing=8
    timeunit='year'
    BP=False
    time_start=0





