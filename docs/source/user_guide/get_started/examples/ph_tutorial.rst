.. _my-ref-to-ph-tutorial:

Phonon
======

.. toctree::
   :maxdepth: 2
   
In this chapter will get you through the launching of a phonon calculation with 
Quantum Espresso, with ``ph.x``, a density functional perturbation theory code.
For this tutorial, it is required that you managed to launch a ``pw.x``
calculation, which is at the base of the phonon code; and of course it is
assumed that you already know how to use the QE code.

The input of a phonon calculation can be actually very simple: the only care that has to be taken
is to point to the same scratch of the previous pw calculation.
Here we will try to compute the dynamical matrix on a mesh of points (actually consisting
of a 1x1x1 mesh for brevity). 
The input file that we should create looks like the following: ::

  AiiDA calculation
  &INPUTPH
     epsil = .true.
     fildyn = 'DYN_MAT/dynamical-matrix-'
     iverbosity = 1
     ldisp = .true.
     nq1 = 1
     nq2 = 1
     nq3 = 1
     outdir = './out/'
     prefix = 'aiida'
     tr2_ph =   1.0000000000d-08
  /



Walkthrough
-----------

The only novel thing you will have to learn is how to set a parent calculation.
As for the PWscf calculation, we write a script step-by-step.

We first load a couple of useful modules that you already met in the previous tutorial,
and load the database settings::

    #!/usr/bin/env python
    from aiida import load_profile
    load_profile()

    from aiida.orm import Code
    from aiida.plugins import DataFactory


Code
----

To proceed, we assume you have compiled the code on the cluster and configured a new code ``ph.x``
in AiiDA in the very same way you installed ``pw.x`` the  (see :ref:`setup_code` section in the 
AiiDA manual for more information).
Then we load the ``Code`` class-instance from the database::

    codename = 'my-ph.x'
    code = Code.get_from_string(codename)

Parameter
---------

Just like the PWscf calculation, here we load the class :py:class:`Dict <aiida.orm.nodes.data.dict.Dict>` 
and we instanciate it in parameters.
Again, ``Dict`` will simply represent a nested dictionary in the database,
namelists at the first level, and then variables and values.
But this time of course, we need to use the variables of the *PHonon* code!

::

    Dict = DataFactory('dict')
    parameters = Dict(dict={
		'INPUTPH': {
		    'tr2_ph' : 1.0e-8,
		    'epsil' : True
		    }})

Several keywords, like the name of the outputs, number of q-points, *ldisp* and *qplot*,
that are present in the input at the top of this section, are left to be set by the plugin.

Calculation
-----------

Now we create the object PH-calculation.
Again, we can use the general ``get_builder`` method 
to assign all the inputs of the calculation, starting from the parameters::

    builder = code.get_builder()
    builder.parameters = parameters

To set the resource that you you want to allocate
to this calculation, you can assign values in the ``metadata.options`` input: ::

    builder.metadata.options.resources = {'num_machines': 1}
    builder.metadata.options.max_wallclock_seconds = 60*30 # half an hour
    
More options are available, and can be explored by expanding 
``builder.metadata.options.`` + ``TAB``.
    

Parent folder
------------------

The phonon calculation needs to know on which PWscf do the perturbation theory calculation.
From the database point of view, it means that the ``PHonon`` calculation
is always a child of a ``PWscf``.
In practice, this means that when you want to impose this relationship,
you decided to take the input parameters of the parent PWscf calculation,
take its charge density and use them in the phonon run.

This information is submitted by providing a :py:class:`~aiida.orm.nodes.data.remote.RemoteData`
object to the ``builder.parent_folder`` input.
The ``RemoteData`` is one of the results of a successful pw calculation. 

You first need to remember the ``pk`` (or ``uuid``) of the parent calculation that you launched
before (let's assume it is #6): so that you can load *a* QE-PWscf calculation,
and load the object that represent *the* QE-PWscf calculation with ``pk```` #6::

    from aiida.orm import load_node
    parent_pk = 6
    pw_calc = load_node(parent_pk)
    pw_folder = pw_calc.outputs.remote_folder
    builder.parent_folder = pw_folder

Q-points
---------

The phonon calculation requires a grid of q-point in the Brillouin zone on which
calculate the dynamical matrix: these are specified by the
nq1, nq2 and nq3 inputs in *ph* . 
In the AiiDA plugin, these points are provided through a
:py:class:`KpointsData <aiida.orm.nodes.data.array.kpoints.KpointsData>` 
object to the ``qpoints`` input of the builder: for one q-point, as in the example above::

    KpointsData = DataFactory('array.kpoints')
    qpoints = KpointsData()
    qpoints.set_kpoints_mesh([1,1,1])
    

Labels and comments
-------------------

These properties, useful to tag a calculation, can be set in the ``metadata`` input of the calculation,
with a *label* (meant to be a short description) and *description* (longer) ::

    builder.metadata.label = 'My generic title'
    builder.metadata.description 'A longer description: phonon calculation for BaTiO3'

.. note::
   The ``TAB`` expansion works also on nested properties: from ``builder.metadata.``
   you can explore the available options


Execution
---------

Now, everything is ready, and we can launch the phonon calculation using 
the ``run`` or ``submit`` methods (see the previous section, or the AiiDA documentation
for more information) ::

    from aiida.engine import submit
    calc = submit(builder)



Script: source code
-------------------

In this section you'll find a scripts that do what explained in the tutorial.

You can download it, modify the two strings ``codename``
and ``pw_calc_id`` with the correct values, and execute it with::

  python ph_short_example.py


Download: :download:`this example script <ph_short_example.py>`