
*****
Input
*****

All the input required to run an EBM with this source code is provided by a **configuration.ini** file which you have to create.
And as already mentioned in the section :doc:`How to use <howtouse>`:

.. Important::

   The configuration.ini file will provide the physical sense of the EBM!

Here shown is, how this file is structured and which syntax has to be maintained to make it readable to the *importer* function.

There are four main components of the file, the modelequation parameters `eqparam`, the runge-kutta parameters `rk4input`, the initial condition parameters `initials` and a compilation of physical functions with their specific parameters `funccomp`.

If you want to put together a new model simply create a textfile with the suffix **.ini**. These four main components will be used as header, whereas the headers the `funccomp` has to be replaced by `func0`, `func1`,*...* depending on how many functions you want to include.



