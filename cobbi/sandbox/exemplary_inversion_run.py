import torch
import matplotlib.pyplot as plt
import numpy as np
import os
import shutil

from cobbi.core import gis, test_cases
from cobbi.core.utils import NonRGIGlacierDirectory
from cobbi.core.first_guess import compile_first_guess
from cobbi.core.inversion import InversionDirectory
from cobbi.core.dynamics import create_glacier
from cobbi.core.cost_function import create_cost_func
from cobbi.core.inversion import InversionDirectory
from cobbi.core import data_logging
from oggm import cfg

np.seed = 0  # needs to be fixed for reproducible results with noise

cfg.initialize()

basedir = '/path/to/example'
basedir = '/data/philipp/thesis_test/Giluwe/perfect_reference'

# TODO: think about IceThicknesses for case Giluwe
# Choose a case
case = test_cases.Giluwe
gdir = NonRGIGlacierDirectory(case, basedir)
# only needed once:
gis.define_nonrgi_glacier_region(gdir)

# create settings for inversion
lambdas = np.zeros(4)
lambdas[0] = 0.2  # TODO: better
lambdas[1] = 1.5  # TODO: really useful? (Better if smaller than 1 to focus
# on inner domain)
lambdas[2] = 2
lambdas[3] = 1e5

minimize_options = {
    'maxiter': 300,
    'ftol': 0.5e-3,
    #'xtol': 1e-30,
    'gtol': 1e-4,
    #'maxcor': 5,
    #'maxls': 10,
    'disp': True
}

gdir.write_inversion_settings(mb_spinup=None,
                              yrs_spinup=2000,
                              yrs_forward_run=200,
                              reg_parameters=lambdas,
                              solver='L-BFGS-B',
                              minimize_options=minimize_options,
                              inversion_counter=0,
                              fg_shape_factor=1.,
                              bounds_min_max=(2, 600)
                              )

# Optional, if not reset=True and already ran once
# only needed once:
create_glacier(gdir)
compile_first_guess(gdir)
idir = InversionDirectory(gdir)
res = idir.run_minimize()
#dl = data_logging.load_pickle(idir.get_current_basedir() + '/data_logger.pkl')


# copy this script to inversion directory for reproducibility
path_to_file = '/home/philipp/COBBI/cobbi/sandbox/exemplary_inversion_run.py'
fname = os.path.split(path_to_file)[-1]
shutil.copy(path_to_file, os.path.join(idir.get_current_basedir(), fname))

print('end')