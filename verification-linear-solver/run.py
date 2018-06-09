#!/usr/bin/env python
import os
import multiprocessing as mp
import shutil

import numpy as np

from scipy import linalg

from saf.action import solve
from saf.fm.linear import Config
from saf.fm.linear import Reader


Q = 4
THETA = 1.0
T_FINAL = 10


def _run_solver(args):
    n12, = args
    c = Config()

    c.n12 = n12
    c.final_time = T_FINAL
    c.dt = 0.005
    c.approximator = 'henrick-upwind5-lf'
    c.time_integrator = 'dopri5'
    c.io_format = 'ascii'
    c.plot_time_step = 0
    c.play_animation = False

    c.lambda_tol = 1e-6
    c.q = Q
    c.theta = THETA
    c.reaction_rate_version = 'v2'
    c.f = 1
    c.ic_amplitude = 1e-10
    c.ic_type = 'znd'
    c.truncation_coef = 1e6

    outdir = 'n12={:04d}'.format(n12)
    outdir = os.path.join('_output', outdir)

    if os.path.exists(outdir):
        shutil.rmtree(outdir)
    os.mkdir(outdir)
    solve('linear', c, outdir, log_to_file=True)

    return outdir


if __name__ == '__main__':
    n12_list = [20, 40, 80, 160, 320, 640, 1280]
    tasks = [(n12, ) for n12 in n12_list]

    with mp.Pool(processes=4) as pool:
        results = pool.map(_run_solver, tasks)

    assert results == sorted(results)

    sim_results = []
    for r in results:
        reader = Reader(r)
        __, d = reader.get_time_and_detonation_velocity()

        sim_results.append(d)

    for i, n12 in enumerate(n12_list[:-1]):
        print('*** Difference between N12={} and N12={}'.format(
            n12_list[i], n12_list[i+1]))

        d_1 = sim_results[i]
        d_2 = sim_results[i+1]

        norm_2 = linalg.norm(d_1 - d_2, 2)
        norm_inf = linalg.norm(d_1 - d_2, np.Inf)
        print('    L2-norm of difference: {}'.format(norm_2))
        print('    LInf-norm of difference: {}'.format(norm_inf))
