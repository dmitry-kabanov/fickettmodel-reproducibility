#!/usr/bin/env python
import os
import multiprocessing as mp
import shutil

import numpy as np

from scipy import linalg

from saf.action import solve
from saf.fm.nonlinear import Config
from saf.fm.nonlinear import Reader


Q = 4
THETA = 0.95
T_FINAL = 1000


def _run_solver(args):
    n12, = args
    c = Config()

    c.n12 = n12
    c.final_time = T_FINAL
    c.dt = 0.005
    c.approximator = 'godunov-minmod'
    c.time_integrator = 'dopri5'
    c.io_format = 'numpy'
    c.plot_time_step = 0
    c.play_animation = False

    c.lambda_tol = 1e-6
    c.q = Q
    c.theta = THETA
    c.reaction_rate_version = 'v2'
    c.f = 1
    c.ic_amplitude = 0
    c.ic_type = 'znd'
    c.truncation_coef = 1e6

    outdir = 'N12={:04d}'.format(n12)
    outdir = os.path.join('_output', outdir)

    if os.path.exists(outdir):
        shutil.rmtree(outdir)
    os.mkdir(outdir)
    solve('nonlinear', c, outdir, log_to_file=True)

    return outdir


if __name__ == '__main__':
    n12_list = [20, 40, 80, 160, 320, 640, 1280]
    tasks = [(n12, ) for n12 in n12_list]

    with mp.Pool(processes=4) as pool:
        results = pool.map(_run_solver, tasks)
