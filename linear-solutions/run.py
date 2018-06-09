#!/usr/bin/env python
""" Run simulations for different values of activation energy."""
import os
import multiprocessing as mp
import shutil

from saf.action import solve
from saf.fm.linear import Config

Q = 4


def _run_solver(args):
    theta, = args
    c = Config()

    c.n12 = 20
    c.final_time = 2
    c.dt = 0.01
    c.approximator = 'henrick-upwind5-lf'
    c.time_integrator = 'dopri5'
    c.io_format = 'ascii'
    c.plot_time_step = 1000
    c.play_animation = False

    c.lambda_tol = 1e-6
    c.q = Q
    c.theta = theta
    c.reaction_rate_version = 'v2'
    c.f = 1
    c.ic_amplitude = 1e-10
    c.ic_type = 'znd'
    c.truncation_coef = 0.01

    outdir = 'theta={:.3f}'.format(theta)
    outdir = os.path.join('_output', outdir)
    if os.path.exists(outdir):
        shutil.rmtree(outdir)
    os.mkdir(outdir)
    solve('linear', c, outdir, log_to_file=True)


if __name__ == '__main__':
    theta = [0.92, 0.95]
    tasks = [(x,) for x in theta]

    pool = mp.Pool(processes=2)
    pool.map(_run_solver, tasks)
