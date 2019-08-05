.. _PlaSIM: https://www.mi.uni-hamburg.de/en/arbeitsgruppen/theoretische-meteorologie/modelle/plasim.html

*********************************
Physical Background / Model Types
*********************************

With this project different types of EBMs can be used to run simulations. 
However, the versatility of the resolution is limited to low dimensional EBMs from zero dimensionsal EBMs to one one dimensional EBMs resolved over the latitudes. It would be nice and is planned by me to extend this project to higher resolutions (for more information see :doc:`ToDo <todo>`)

Physical Background
===================

In general, energy balance models describe the behaviour of a planet's energy balance over time. Here, the focus is obviously on the earth's energy balance, but EBMs are generally not restricted to describe the earth's energy balance.

.. figure:: _static/EB.png
    :align: center
    :width: 80%
    
    Earth's energy balance [:doc:`IPCC, 2013 <references>`]

Here shown is a 0D schematic of the earth's energy balance like it is often given in the standard literature. The radiative energy fluxes (in :math:`Wm^{-2}`) of the earth are indicated with their strength and direction. However, EBMs describe the energy balance mostly with the crucial parts only, which means that small or strongly regional energy fluxes are neglected.

EBMs are commonly restricted to the **downward radiative energy flux** (:math:`R_{down}`), the **upward radiative energy flux** (:math:`R_{up}`), in the case of the treated 1D-EBMs to the **latitudinal transfer energy fluxes** (:math:`F_{transfer}`) and in some cases of to additional **forcing energy flux** (:math:`F_{forced}`) (e.g. Carbon Dioxide forcing). This is of course no necessity rather than a general identification of EBMs since they are specifically characterized by their simplicity.

The physical basis of EBMs can be expressed in a model equation which commonly has the following form:

.. _above:

.. math::

    C \cdot \frac{dT}{dt} = R_{down} + R_{up} + F 

where C is the heatcapacity, :math:`\frac{dT}{dt}` the term to consider that the system is dynamical and :math:`R_{down}`, :math:`R_{up}`, :math:`F` the energy fluxes which are included.

Model Types
===========

0D-EBM
------

If one is interested in the 0D case, the model equation above suffices to describe the energy balance over time. However, :math:`F` is neglected in general and only used in specific cases. By using the following discretizations:

.. math::

    R_{down} & = (1-\alpha)\cdot Q \\
    R_{up} & = - \epsilon\sigma T^4

with the albedo :math:`\alpha`, the solar insolation :math:`Q`, the Stefan-Boltzmann constant :math:`\sigma`, and the emissivity :math:`\epsilon`, the simplest form of an EBM is described by:

.. math::

    C \cdot \frac{dT}{dt} = R_{down} + R_{up} = (1-\alpha) \cdot Q - \epsilon\sigma T^4

This equation can easily be solved analytically, but to observe the behaviour of the energy balance over time a numerical algorithm can be used to solve this equation.
With the chapter :doc:`How to use <howtouse>` it will be investigated in detail how this project implements such an EBM. Additionally there is a demonstration file given once you have :doc:`installed <installation>` this project.

.. Note::

    The dependencies of parameters like :math:`\alpha` on variables like the temperature :math:`T` are strongly related to the inbound type of :doc:`Functions <code/functions>` and is therefore not specified while formulating this model equations.

1D-EBM
------

The description of 1D EBMs does not differ much from 0D EBMs. In 1D EBMs the earth is commonly described by a grid of latitudinal bands.
The model equation as introduced above_ can directly be transfered to be valid for each latitudinal band seperately. 

As already mentioned, 1D EBMs use latitudinal transfer energy fluxes :math:`F_{transfer}` which consider an exchange of energy between latitudinal bands. This term is crucial, because the energy balance resolved over the latitudes shows strong differences between equator and poles due to the stronger insolation at the equator.

By identifying each latitudinal band and all its parameters with an index i, the simplest form of an 1D-EBM is described by:

.. math::

    C \cdot \frac{dT_i}{dt} = R_{down,i} + R_{up,i} + F_{transfer,i}

There are many different approaches to discretize these terms in 1D. Because this project was started to implement two specific EBMs, one developed by :doc:`Michail Budyko <references>` and one by :doc:`William Seller  <references>`, both published in the late 1960s, these two discretizations will be shown. 

Budyko-type model
^^^^^^^^^^^^^^^^^

This EBM constructed by :doc:`Michail Budyko  <references>` uses various assumptions, supported by global earth observation data. The key features of this model are:

- An empirically determined upward radiation flux with linear dependence on temperature, in its simplest form described by :math:`R_{up}=- (A+B\cdot T)`.

- An albedo seperated into three different regions with dependence on latitude (or by customization on temperature), with high albedo values towards the polar regions and low albedo values in the equatorial regions.

- A symmetric diffusive transfer energy flux with dependence on the difference of zonal (ZMT) to global (GMT) mean temperature.

- A grid resolving latitudinal bands of any width (in this project mostly used is a width of 1°)

The detailed physical formulation of the terms (and additional extensions) can be viewed along with the implementations (:doc:`Functions <code/functions>`).

An example zonal mean temperature distribution:

.. figure:: _static/Budyko_ZMT.png


Sellers-type model
^^^^^^^^^^^^^^^^^^

The EBM constructed by :doc:`William Seller  <references>` is adapted even more to global earth observation data than the Budyko-type model and thereby is constructed with more complex terms. The key features of this model are:

- The Stefan-Boltzmann radiation law as upward radiation flux extended with a term considering atmospheric attenuation.

- An albedo described by an empircal law with linear dependence on temperature and surface elevation.

- A transfer energy flux *P* seperated into three different components, the atmospheric water vapour transfer, the atmospheric sensible heat transfer and the oceanic sensible heat transfer. The total transfer energy flux :math:`F` of one gridbox is given by the difference of northward and southward transfer energy flux :math:`P` (the sum of those three components from the northern/southern boundary).

- A grid resolving the earth with latitudinal bands of 10° width. Hence, the earth is resolved by 18 latitudinal bands.

The detailed physical formulation of the terms (and additional extensions) can be viewed along with the implementations (:doc:`Functions <code/functions>`).

An example zonal mean temperature distribution:

.. figure:: _static/Sellers_ZMT.png


