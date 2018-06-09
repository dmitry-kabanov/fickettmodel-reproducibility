#!/usr/bin/env python
import os
import shutil

from saf.action import solve
from saf.ffm.linear import Config

OUTPUT_DIR = '_output'


def _run_solver(args):
    theta, outdir = args

    c = Config()
    c.n12 = 40
    c.final_time = 300
    c.dt = 0.005
    c.approximator = 'henrick-upwind5-lf'
    c.time_integrator = 'dopri5'
    c.plot_time_step = 0
    c.play_animation = False

    c.lambda_tol = 1e-6
    c.q = 4
    c.theta = theta
    c.reaction_rate_version = 'v2'  # Expression exact as in FariaEtAl2015.
    c.f = 1
    c.ic_amplitude = 1e-4
    c.ic_type = 'znd'
    c.truncation_coef = 1e6

    outdir = os.path.join(OUTPUT_DIR, outdir)
    if os.path.isdir(outdir):
        shutil.rmtree(outdir)
    os.mkdir(outdir)

    solve('linear', c, outdir, log_to_file=False)

if __name__ == '__main__':
    theta = 0.95
    outdir = 'linear-theta=%.2f' % theta
    args = (theta, outdir)
    _run_solver(args)
