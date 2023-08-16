from netpyne import sim

from netpyne_model import hh

sim.create( hh.netParams, hh.cfg )
sim.simulate()
sim.analyze()
if sim.rank == 0:
    print(sim.analysis.prepareSpikeData()['legendLabels'])




"""
    sim.create(ca3.netParams, ca3.cfg)
    sim.simulate()
    sim.pc.barrier()
    if sim.rank == 0: # data out (print, and then file I/O if writefile specified)
        inputs = ca3.get_mappings()
        spikes = get_freq(sim.analysis.prepareSpikeData()['legendLabels'])
        out_json = json.dumps({**inputs, **spikes})
        print("===FREQUENCIES===\n")
        print(out_json)
        if ca3.writefile:
            print("writing to {}".format(ca3.writefile))
            ca3.write(out_json)
            ca3.signal()
"""