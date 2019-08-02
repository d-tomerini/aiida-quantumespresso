.. _my-ref-to-projwfc-tutorial:

Projwfc
=======

.. toctree::
   :maxdepth: 2


This chapter will show how to launch a single Projwfc (``projwfc.x``) calculation.
It assumes you already familiar with the underlying code as well
as how to use basic features of AiiDA.
This tutorial assumes you are at least familiar
with the concepts introduced in the :ref:`my-ref-to-ph-tutorial` section,
specifically you should be familiar with using a parent calculation.

This section is intentially left short, as there is really nothing new
in using projwfc calculations relative to ph calculations.
Simply adapt the script below to suit your needs,
and refer to the Quantum ESPRESSO documentation.
for more information.

Script to execute
-----------------

This is the script described in the tutorial above. You can use it, just
remember to customize it using the right ``parent_id``,
the code, and the proper scheduler info.

Script: source code
----------------------------

You can download the script to run a projwfc calculation in AiiDA, 
modify the two strings ``codename`` and ``parent_id`` with the correct values,
and execute it with::

  python projwfc_short_example.py

Download: :download:`this example script <projwfc_short_example.py>`