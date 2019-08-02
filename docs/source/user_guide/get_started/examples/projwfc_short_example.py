from aiida.orm import Code, load_node
from aiida.plugins import DataFactory
from aiida.engine import submit

from aiida import load_profile
load_profile()

#####################
# ADAPT TO YOUR NEEDS
codename = 'my-projwfc.x'
parent_id = 6
#####################

code = Code.get_from_string(codename)

Dict = DataFactory('dict')
parameters = Dict(dict={
    'PROJWFC': {
        'DeltaE' : 0.2,
        'ngauss' : 1,
        'degauss' : 0.02
        }
    }
)

builder = code.get_builder()

builder.metadata.options.resources = {'num_machines': 1}
builder.metadata.options.max_wallclock_seconds = 60*30 # half an hour

builder.parameters = parameters

ph_calc = load_node(parent_id)
ph_folder = ph_calc.outputs.remote_folder
builder.parent_folder = ph_folder

calc = submit(builder)

print("created calculation with PK={}".format(calc.pk))