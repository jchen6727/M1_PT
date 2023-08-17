import utils
import ray
import pandas
import shutil
import os

import numpy
from ray import tune
from ray import air
from ray.air import session
#from ray.tune.search.optuna import OptunaSearch
from ray.tune.search.basic_variant import BasicVariantGenerator

cwd = os.getcwd()
kwargs = {
    'mpiexec': shutil.which('mpiexec'), 'cores': 4, 'nrniv': shutil.which('nrniv'),
    'python': shutil.which('python'), 'script': cwd + '/sim.py'
}

param_space = {
    'cfg.amp': tune.grid_search([0.3, 0.4, 0.5, 0.6])
}

# multicore command strings (mpiexec and shell)
MPI_CMDSTR = "{mpiexec} -n {cores} {nrniv} -python -mpi -nobanner -nogui {script}".format(**kwargs)
#SH_CMDSTR = "{mpiexec} -n $NSLOTS {nrniv} -python -mpi -nobanner -nogui {script}".format(**kwargs)
SH_CMDSTR = "python sim.py"

CONCURRENCY = 4
SAVESTR = "ap.csv"

ray.init(
    runtime_env={"working_dir": ".", # needed for import statements
                 "excludes": ["*.csv",
                              "*.run",
                              "*." 
                              "ray/",
                              "output/"]},
)

def sge_objective(config):
    data = utils.sge_run(config=config, cwd=cwd, cmdstr=SH_CMDSTR, cores=2)
    sdata = pandas.read_json(data, typ='series', dtype=float)
    freq = sdata['hh']
    session.report(dict(freq=freq, data=sdata))

algo = BasicVariantGenerator(max_concurrent=CONCURRENCY)

print("=====grid search=====")
print(param_space)

tuner = tune.Tuner(
    #objective,
    sge_objective,
    tune_config=tune.TuneConfig(
        search_alg=algo,
        num_samples=1, # grid search samples 1 for each param
        metric="freq"
    ),
    run_config=air.RunConfig(
        local_dir="./ray_ses",
        name="grid",
    ),
    param_space=param_space,
)

results = tuner.fit()

resultsdf = results.get_dataframe()

utils.write_csv(resultsdf, SAVESTR)
