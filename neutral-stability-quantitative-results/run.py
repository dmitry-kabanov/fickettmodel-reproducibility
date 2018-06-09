#!/usr/bin/env python
import os
import shutil
import sys

import numpy as np

from mpi4py import MPI

from lib_neutral_stability import find_critical_e_act, FMT_SIGNED, FMT_UNSIGNED

OUTPUT_DIR = '_output'
GROWTH_RATE_TOL = 1e-3
MODE_NUMBER = 0
Q_LOWER = 0.81
Q_UPPER = 16.00
THETA_LOWER = 0.2
THETA_UPPER = 5.0
N12 = 40

# This is to prevent oversubscribing of cores during postprocessing.
os.environ['OMP_NUM_THREADS'] = '1'


def _worker(tasks, rank):
    for t in tasks:
        _worker_single_task(t, rank)


def _worker_single_task(t, rank):
    # task_list, = args
    theta_crit = 0.0

    q = t
    worker_name = rank

    try:
        outdir = 'q={:{fmt}}'.format(q, fmt=FMT_UNSIGNED)
        outdir = os.path.join(OUTPUT_DIR, outdir)

        if os.path.exists(outdir):
            shutil.rmtree(outdir)
        os.mkdir(outdir)
        outname = os.path.join(outdir, 'stdout.log')
        errname = os.path.join(outdir, 'stderr.log')
        sys.stdout = open(outname, 'w', buffering=1)
        sys.stderr = open(errname, 'w', buffering=1)
        print('Worker {} | q={:{fmt}}'.format(worker_name, q, fmt=FMT_UNSIGNED))
    except Exception as e:
        print('q={:{fmt}} | {}'.format(q, str(e), fmt=FMT_UNSIGNED))
        return

    theta_lower = THETA_LOWER
    theta_upper = THETA_UPPER

    params = {
        'n12': N12,
        'q': q,
        'theta_lower': theta_lower,
        'theta_upper': theta_upper,
    }

    try:
        theta_crit, rate, freq = find_critical_e_act(
            params, outdir, GROWTH_RATE_TOL, mode_number=MODE_NUMBER)

        result_file = os.path.join(outdir, 'result.txt')
        with open(result_file, 'w') as f:
            f.write('theta={:{fmt}}\n'.format(theta_crit, fmt=FMT_UNSIGNED))
            f.write('growth_rate={:{fmt}}\n'.format(rate, fmt=FMT_SIGNED))
            f.write('frequency={:{fmt}}\n'.format(freq, fmt=FMT_UNSIGNED))
    except Exception as e:
        print('q={:{fmt}} | {}'.format(q, str(e), fmt=FMT_UNSIGNED))
        # Write exception message to the master process stdout as well.
        sys.stdout = sys.__stdout__
        print('q={:{fmt}} | {}'.format(q, str(e), fmt=FMT_UNSIGNED))


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

counter = 0

all_tasks = []

# Build `all_tasks` in master process to distribute it to all processes.
if rank == 0:
    # Values of heat release :math:`q`.
    q_values = [0.81, 1, 2, 4, 9, 16]

    for i in range(size):
        all_tasks.append([])

    for i in range(len(q_values)):
        all_tasks[i % size].append(q_values[i])

# Now distribute the tasks to each process.
tasks = comm.scatter(all_tasks, root=0)
_worker(tasks, rank)
