from netpyne import specs

cfg = specs.simConfig()
"""
cfg
"""
cfg.duration = 2000
cfg.dt = 0.025
cfg.hParams = {'celsius': 34, 'v_init': -65}
cfg.recordTraces = {'v': {'sec':'soma_0', 'loc':0.5, 'var':'v'}}
cfg.recordStep = 0.1

# Analysis and plotting
cfg.analysis['plotTraces'] = {'include': [0], 'saveFig': True, 'showFig': False} # Plot cell traces

"""
batch parameter exploration
"""
cfg.amp = 0.6

