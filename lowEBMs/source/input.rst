
*****
Input
*****

All the input required to run an EBM with this source code is provided by a **configuration.ini** file which you have to create. 
As already mentioned in the section :doc:`How to use <howtouse>`:

.. Important::

   The configuration.ini file will provide the model setup and physical sense of the EBM!

Here shown is, how this file is structured and which syntax has to be maintained to make it readable to the ``importer`` function.

There are four main components of the file, the modelequation parameters ``eqparam``, the runge-kutta parameters ``rk4input``, the initial condition parameters ``initials`` and a compilation of physical functions with their specific parameters ``funccomp``.

If you want to put together a new model simply create a textfile with the suffix **.ini**. These four main components will be used as header of a section, whereas the headers the ``funccomp`` has to be replaced by ``func0``, ``func1``,... depending on how many functions you want to include. It will look like this::

    #Initial model setup & algorithm parameters 
    #------------------------------------------
    [eqparam]

    [rk4input]
    
    [initials]

    #Model structure & physical equation parameters
    #----------------------------------------------
    [func1]
    
    [func2]
    .
    .
    [func_]

.. Note::

   The order of your sections doesn't matter as long as the headers are correctly labeled.

.. Important::
    
   To define which function you add, insert the name of the function as parameter ``func=name``, then add the required parameters below (see :doc:`Functions <code/functions>`).

Now each section has to be filled with parameters. ``eqparam``, ``rk4input`` and ``initials`` always contain the same parameters since they define **how** the algorithm runs. The func-sections have to be modified since they define **which** model equation the algorithm solves. 

A detailed definition of the parameters for the model setup can be looked up here:

.. toctree::
    :maxdepth: 2
    
    configdescription

Example Input 0D EBM
====================

For a 0D-EBM (the *EBM0D_simple_config.ini*), the model setup might look like this::

    #Initial model setup & algorithm parameters 
    #------------------------------------------
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
    zmt=273+17
    gmt=273+17
    latitude_c=0
    latitude_b=0
    initial_temperature_cosine=True
    initial_temperature_amplitude=30
    initial_temperature_noise=True
    initial_temperature_noise_amplitude=5

If you now want to give a model structure with a downward radiative energy flux and a upward radiative energy flux, this might look like this::

    #Model structure & physical equation parameters
    #----------------------------------------------
    [func0]
    func=flux_down.insolation
    Q=342
    m=1
    dQ=0

    albedo=albedo.static 
    albedoread=True           
    albedoparam=[0.3] 

    noise=False
    noiseamp=342*0.03
    noisedelay=1
    seed=True
    seedmanipulation=0

    sinusodial=False
    convfactor=1
    timeunit='annualmean'
    orbital=False   
    orbitalyear=0

    [func1]
    func=flux_up.planck
    grey=0.612
    sigma=const.sigma



