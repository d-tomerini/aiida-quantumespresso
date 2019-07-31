#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################################
# Copyright (c), The AiiDA team. All rights reserved.                     #
# This file is part of the AiiDA code.                                    #
#                                                                         #
# The code is hosted on GitHub at https://github.com/aiidateam/aiida_core #
# For further information on the license, see the LICENSE.txt file        #
# For further information please visit http://www.aiida.net               #
###########################################################################
from __future__ import absolute_import
from __future__ import print_function
from aiida import load_profile

from aiida.orm import Code, load_node
from aiida.plugins import DataFactory
from aiida.engine import submit

load_profile()

###############################
# Set your values here
codename = 'ph-6.3@TheHive'
pw_calc_id = 6
###############################

code = Code.get_from_string(codename)
builder = code.get_builder()

Dict = DataFactory('dict')
parameters = {
    'INPUTPH': {
	'tr2_ph' : 1.0e-8,
	'epsil' : True
    }
}

builder.parameters = Dict(dict=parameters)

KpointsData = DataFactory('array.kpoints')
qpoints = KpointsData()
qpoints.set_kpoints_mesh([1,1,1])

builder.qpoints = qpoints

builder.metadata.options.resources = {'num_machines': 1}
builder.metadata.options.max_wallclock_seconds = 1800

pw = load_node(pw_calc_id) # parent calculation
pw_folder = pw.outputs.remote_folder
builder.parent_folder = pw_folder

builder.metadata.label = 'My generic title'
builder.metadata.description ='My generic description'

calc = submit(builder)

print("created calculation with PK={}".format(calc.pk))