from netpyne import sim

cfg, netParams = sim.readCmdLineArgs(simConfigDefault='src/cfg.py', netParamsDefault='src/netParams.py')

sim.initialize( simConfig = cfg, netParams = netParams)