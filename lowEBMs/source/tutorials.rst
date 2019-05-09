..    include:: <isonum.txt>

*********
Tutorials
*********

Here given is a list of tutorial-/demonstration-EBMs which are supplemented within the installation directory under *~/lowEBMs/Tutorials/* or can otherwise be accessed from the git repository under 
https://github.com/BenniSchmiedel/Climate-Modelling/tree/master/lowEBMs/Tutorials.

.. contents:: EBM tutorial files:

For the physical background see :doc:`Model types <models>` and the explanation of usage see :doc:`How to use <howtouse>`. The explanation of additional functions and ther usage can be looked up in the :doc:`functions' definitions <code/functions>` or in the referenced literature. 

0D EBM (simple)
===============

A 0D EBM equipped with:

- constant absorbed downward solar radiation flux

- upward radiation flux according to the Stefan-Boltzmann law


0D EBM (:math:`CO_2` forced)
============================

A 0D EBM equipped with:

- constant absorbed downward solar radiation flux

- upward radiation flux according to the Stefan-Boltzmann law

- :math:`CO_2` radiative forcing according to estimates by :doc:`Myhre <references>`

The tutorial-file of this EBM uses a :math:`CO_2`-forcing based on 1958 - present atmospheric :math:`CO_2`-concentrations (the :ref:`Keeling-curve <Keeling>`)

0D EBM (volcanic forced)
========================

A 0D EBM equipped with:

- constant absorbed downward solar radiation flux

- upward radiation flux according to the Stefan-Boltzmann law

- volcanic radiative forcing given by the difference in :math:`Wm^{-2}`

The tutorial-file of this EBM uses a randomly generated radiative forcing as volcanic-forcing. To truly consider volcanic radiative forcing the gas concentrations have to be converted into the amount of radiative forcing which is not implemented for now.

1D EBM Budyko-type (static albedo)
==================================

A 1D EBM equipped with:

- static albedo distribution with three regions of albedo regions |rarr| constant absorbed downward solar radiation flux  

- upward radiation flux according to Budyko's radiation law

- a symmetric diffusive transfer energy flux according to Budyko

The parameters of the tutorial-file are chosen to reproduce the EBM as it was introduced by :ref:`Budyko (1968) <Budyko>`.


1D EBM Budyko-type (temperature-dependant albedo)
=================================================

A 1D EBM equipped with:

- temperature dependant albedo distribution with three regions of albedo regions 
  |rarr| dynamic absorbed downward solar radiation flux  

- upward radiation flux given by the empirical law according to :ref:`Budyko <Budyko>`

- a symmetric diffusive transfer energy flux according to :ref:`Budyko <Budyko>`

The parameters of the tutorial-file are chosen to reproduce the EBM as it was introduced by :ref:`Budyko (1968) <Budyko>`.
The temperature dependence of the albedo is defined in :doc:`Functions <code/functions>`.


1D EBM Sellers-type (temperature-dependant albedo)
==================================================

A 1D EBM equipped with:

- dynamic albedo distribution with a continuous temperature dependant albedo function |rarr| dynamic absorbed downward solar radiation flux  

- upward radiation flux given by an edited Stefan-Boltzmann radiation law according to :ref:`Sellers (1969) <Sellers>`

- transfer energy flux according to :ref:`Sellers <Sellers>`

- temperature distributions corrected by the average latitudinal band elevation

The parameters of the tutorial-file are chosen to reproduce the EBM as it was introduced by :ref:`Sellers (1969) <Sellers>`.


