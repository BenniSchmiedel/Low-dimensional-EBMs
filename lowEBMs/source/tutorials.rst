*********
Tutorials
*********

Here given are tutorials/demonstrations of the EBMs listed below. 

All of them are supplemented within the installation directory under *~/lowEBMs/Tutorials/* or can otherwise be accessed from the git repository under 
https://github.com/BenniSchmiedel/Climate-Modelling/tree/master/lowEBMs/Tutorials.

.. contents:: EBM tutorial files:

For the physical background see :doc:`Model types <models>` and the explanation of usage see :doc:`How to use <howtouse>`. The explanation of additional functions and ther usage can be looked up in the :doc:`functions' definitions <code/functions>`. 

0D EBM (simple)
===============

A 0D EBM equipped with:

- constant incoming solar radiation flux

- outgoing radiation flux according to the Stefan-Boltzmann law


0D EBM (:math:`CO_2` forced)
============================

A 0D EBM equipped with:

- constant incoming solar radiation flux

- outgoing radiation flux according to the Stefan-Boltzmann law

- :math:`CO_2` radiative forcing according to estimates by :doc:`Myhre <references>`

The tutorial-file of this EBM uses a :math:`CO_2`-forcing based on 1958 - present atmospheric :math:`CO_2`-concentrations (the :cod:`Keeling-curve <references:Keeling-curve>`)

0D EBM (volcanic forced)
========================

A 0D EBM equipped with:

- constant incoming solar radiation flux

- outgoing radiation flux according to the Stefan-Boltzmann law

- volcanic radiative forcing given by the difference in :math:`Wm^{-2}`

The tutorial-file of this EBM uses a randomly generated radiative forcing as volcanic-forcing. To truly consider volcanic radiative forcing the gas concentrations have to be converted into the amount of radiative forcing which is not implemented for now.

1D EBM Budyko-type (static albedo)
==================================

A 1D EBM equipped with:

- constant incoming solar radiation flux

    - static albedo distribution with three regions of albedo regions 

- outgoing radiation flux according to Budyko's radiation law

- a symmetric diffusive transfer energy flux according to Budyko

The parameters of the tutorial-file are chosen to reproduce the EBM how it was introduced by :doc:`Budyko 1968 <references>`.


1D EBM Budyko-type (temperature-dependant albedo)
=================================================

1D EBM Sellers-type (static albedo)
===================================

1D EBM Sellers-type (temperature-dependant albedo)
==================================================

