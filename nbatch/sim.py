from netpyne import sim
from utils import get_freq
from netpyne_model import hh
import json

sim.create( hh.netParams, hh.cfg )
sim.simulate()
sim.analyze()
if sim.rank == 0:
    spikes = get_freq(sim.analysis.prepareSpikeData()['legendLabels'])
    out_json = json.dumps({'amp': hh.cfg.amp, **spikes})
    print(out_json)
    hh.write(out_json)
    hh.signal()
