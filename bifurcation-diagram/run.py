#!/usr/bin/env python
r""" Run many simulations with varying :math:`\theta`.

The simulations are run.
Separate script should plot bifurcation diagram.

"""
import argparse
import os
import sys
import shutil

import numpy as np

from mpi4py import MPI

from saf.fm.nonlinear import Config
from saf.action import solve
from saf.util import reset_logging

TOTAL_THETAS = 251
FINAL_TIME = 1000
Q = 4
IO_FORMAT = 'numpy'

# Format for floating-point numbers.
FMT = '.3f'


def _worker(tasks, rank):
    for t in tasks:
        _worker_single_task(t, rank)


def _worker_single_task(task, rank):
    theta = task
    worker_name = rank

    try:
        outdir = 'theta={:{fmt}}'.format(theta, fmt=FMT)
        outdir = os.path.join(OUTPUT_DIR, outdir)

        if os.path.exists(outdir):
            shutil.rmtree(outdir)
        os.mkdir(outdir)
        outname = os.path.join(outdir, 'stdout.log')
        errname = os.path.join(outdir, 'stderr.log')
        sys.stdout = open(outname, 'w')
        sys.stderr = open(errname, 'w')
        msg = 'Worker {} | theta={:{fmt}}'.format(worker_name, theta, fmt=FMT)
        print(msg)
    except Exception as e:
        print('theta={:{fmt}} | {}'.format(theta, str(e), fmt=FMT))
        return

    try:
        c = _get_config(theta)
        solve('nonlinear', c, outdir, log_to_file=False)
        reset_logging()
    except Exception as e:
        print('theta={:{fmt}} | {}'.format(theta, str(e), fmt=FMT))
        sys.stdout = sys.__stdout__
        print('theta={:{fmt}} | {}'.format(theta, str(e), fmt=FMT))


def _get_config(theta):
    c = Config()

    c.n12 = N12
    c.final_time = FINAL_TIME
    c.dt = 0.005
    c.approximator = 'godunov-minmod'
    c.time_integrator = 'dopri5'
    c.plot_time_step = 0
    c.io_format = IO_FORMAT
    c.play_animation = False

    c.lambda_tol = 1e-6
    c.q = Q
    c.theta = theta
    c.reaction_rate_version = 'v2'  # Expression exactly as in FariaEtAl2015.
    c.f = 1
    c.ic_amplitude = 0.0
    c.ic_type = 'gaussian'
    c.truncation_coef = 1e6

    return c


p = argparse.ArgumentParser()
p.add_argument('N12', help='Resolution', type=int)
args = p.parse_args()
N12 = args.N12
OUTPUT_DIR = os.path.join('_output', 'N12={:04d}'.format(N12))

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

all_tasks = []

# Build `all_tasks` in master process to distribute it to all processes.
if rank == 0:
    # Uniformly spaced values of :math:`\theta`.
    theta_values = np.linspace(0.90, 1.15, num=TOTAL_THETAS)

    for i in range(size):
        all_tasks.append([])

    for i in range(len(theta_values)):
        all_tasks[i % size].append(theta_values[i])

# Now distribute the tasks to each process.
tasks = comm.scatter(all_tasks, root=0)
_worker(tasks, rank)
