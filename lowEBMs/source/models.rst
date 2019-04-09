.. _PlaSIM: https://www.mi.uni-hamburg.de/en/arbeitsgruppen/theoretische-meteorologie/modelle/plasim.html

*********************************
Physical Background / Model Types
*********************************

With this project different types of EBMs can be used to run simulations. 
However, the versatility of the resolution is limited to low dimensional EBMs from zero to one dimensionsal EBMs and additionally one dimensional EBMs that are resolved over the latitudes. It would be nice and is planned by me to extent this project to higher resolutions (for more information see :doc:`ToDo <todo>`)

Physical Background
===================

In general, Energybalance models describe the behaviour of a planet's energybudget over time (Here, the focus is obviously on the earth's energybudget, but EBMs can simulate the climate of other planets as well which is done by the PlaSIM_ model for example).

.. figure:: _static/EB.png
    :align: center
    :width: 80%
    
    Earth's energybudget [:doc:`IPCC, 2013 <references>`]

Here shown is a zero-dimensional schematic of the earth's energybudget like it is often given in the standard literature. The radiative energyfluxes (in :math:`Wm^{-2}`) of the earth are indicated with their strength and direction. However, EBMs describe the energybalance mostly with the most crucial parts only, which means that small or strongly regional energyfluxes are neglected.

EBMs are commonly restricted to the **incoming radiative energyflux** (:math:`R_{in}`), the **outgoing radiative energyflux** (:math:`R_{out}`) and in some cases of 0D-EBMs an **external forcing energyflux** (:math:`F_{ext}`) (e.g. Carbon Dioxide forcing), or in cases of 1D-EBMs to **latitudinal transfer energyfluxes** (:math:`F_{transfer}`). This is of course no necessity rather than a general identification of EBMs since they are specifically characterized by their simplicity.

The physical basis of EBMs can be expressed in a model equation which commonly has the following form:

.. _above:

.. math::

    C \cdot \frac{dT}{dt} = R_{in}(t) + R_{out}(t) + F (t)

where C is the heatcapacity, :math:`\frac{dT}{dt}` the term to consider that the system is dynamical and :math:`R_{in}`, :math:`R_{out}`, :math:`F` the energyfluxes which are commonly included.

0D-EBM
======

If one is interested in the zero-dimensional case, the model equation above suffices to describe the energybalance over time. However, :math:`F` is neglected in general and only used in specific cases. By using the following discretizations:

.. math::

    R_{in}(t) = \pi \cdot (1-\alpha(t))\cdot Q(t)

    R_{out}(t) = - 4 \pi \cdot \sigma T^4(t)

the simplest form of an EBM is described with:

.. math::

    C \cdot \frac{dT}{dt} = R_{in}(t) + R_{out}(t) = \pi \cdot (1-\alpha(t)) Q(t) - 4 \pi \cdot \sigma T^4(t)

This equation can easily be solved analytically, but to observe the behaviour of the energybalance over time a numerical algorithm can be used to solve this equation.
With the chapter :doc:`How to use <howtouse>` it will be investigated in detail how this project implements such an EBM. Additionally there is a tutorial given once you have :doc:`installed <installation>` this project.

1D-EBM
======

One-dimensional EBMs do not differ much from zero-dimensional ones. In one-dimensional EBMs the earth is commonly described by a grid of latitudinal bands.
The model equation as introduced above_ can directly be transfered to be valid for each latitudinal band seperately. 

As already mentioned, 1D EBMs use latitudinal transfer energyfluxes :math:`F_{transfer}` which consider an exchange of energy between those latitudinal bands. This term is crucial, because the energybudget resolved over the latitudes shows strong differences between equator and poles, which is logical due to the stronger insolation at the equator.

By indentifying each latitudinal band and all its parameters with an index i, the simplest form of an 1D-EBM is described by:

.. math::

    C \cdot \frac{dT_i}{dt} = R_{in,i}(t) + R_{out,i}(t) + F_{transfer,i} (t)

There are many different approaches to discretize all this terms in one dimension.






