.. _PlaSIM: https://www.mi.uni-hamburg.de/en/arbeitsgruppen/theoretische-meteorologie/modelle/plasim.html

******
Models
******

With this project different types of EBMs can be used to run simulations. 
However, the versatility of the resolution is limited to low dimensional EBMs from zero to one dimensionsal EBMs and additionally one dimensional EBMs that are resolved over the latitudes. It would be nice and is planned by me to extent this project to higher resolutions (for more information see :doc:`ToDo <todo>`)

The physical basis
==================

In general, Energybalance models describe the behaviour of a planet's energybudget over time (Here, the focus is obviously on the earth's energybudget, but EBMs can simulate the climate of other planets as well which is done by the PlaSIM_ model for example).

.. figure:: _static/EB.png
    :align: center
    :width: 80%
    
    Earth's energybudget [:doc:`IPCC, 2013 <references>`]

Figure 1 shows a zero-dimensional schematic of the earth's energybudget like it is often given in the standard literature. The radiative energyfluxes (in :math:`Wm^{-2}`) of the earth are indicated with their strength and direction. However, EBMs describe the energybalance mostly with the most crucial parts only, which means that small or strongly regional energyfluxes are neglected.

EBMs are commonly confined to the **incoming radiative energyflux (:math:`R_{in}`)**, the **outgoing radiative energyflux (:math:`R_{out}`)** and in some cases of 0D-EBMs an **external forcing energyflux (:math:`F_{ext}`)** (e.g. due to Carbon Dioxide forcing), or in cases of 1D-EBMs to **latitudinal transfer energyfluxes (:math:`F_{transfer}`)**. This is of course no necessity rather than a general identification of EBMs since the are specifically characterized by their simplicity.

The physical basis of EBMs can be expressed in a model equation which commonly has the following form:

.. math::

    C \cdot \frac{dT}{dt} = R_{in}(t) + R_{out}(t) + F (t)

C is the heatcapacity, :math:`\frac{dT}{dt}` the term to consider a dynamical system and :math:`R_{in}`, :math:`R_{out}` and :math:`F` the energyfluxes included.


    

