from pubtk.runtk import NetpyneRunner

import json

hh = NetpyneRunner()

cfg = hh.get_cfg()
netParams = hh.get_netParams()

"""
cfg
"""
cfg.duration = 2000
cfg.dt = 0.025
cfg.hParams = {'celsius': 34, 'v_init': -70}
cfg.recordTraces = {'v': {'sec':'soma_0', 'loc':0.5, 'var':'v'}}
cfg.recordStep = 0.1

"""
batch
"""
cfg.amp = 0.5

"""
netParams
"""
fptr = open("na1612.json", "r")
hhcell = json.load(fptr)
fptr.close()

hhcell['conds'] = {'cellType': 'hh'}

netParams.cellParams['hh'] = hhcell

# add stim source
netParams.stimSourceParams['ic'] = {'type': 'IClamp', 'delay': 300, 'dur': 1000, 'amp': cfg.amp}
# connect stim source to target
netParams.stimTargetParams['ic->hh'] = {'source': 'ic', 'conds': {'pop': 'hh'}, 'sec': 'soma_0', 'loc': 0.5}
netParams.popParams['hh'] = {'cellType': 'hh', 'numCells': 1}

















"""
hhcell = netParams.importCellParams('PT', 'TTPC_M1_Na_HH.py', 'Na1612Model')
fptr = open("na1612.json", "w")
json.dump(hhcell, fptr)
fptr.close()
"""
