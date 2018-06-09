#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np

from mpi4py import MPI
from numpy import linspace, log, empty

from lib_normalmodes import LeeStewartSolver

q = 4
theta = 0.95
tol = 1e-4

alpha_re_list = linspace(0, 0.05, num=51)
alpha_im_list = linspace(0, 1, num=101)

H = empty((len(alpha_re_list), len(alpha_im_list)))


def _worker(rank):
    solver = LeeStewartSolver(q, theta, tol)

    size = int(len(alpha_re_list) / comm_size + 1)

    i_1 = rank*size
    i_2 = (rank+1)*size

    if i_2 > len(alpha_re_list):
        i_2 = len(alpha_re_list)

    for i, alpha_re in enumerate(alpha_re_list[i_1:i_2]):
        for j, alpha_im in enumerate(alpha_im_list):
            #print('%d: %d %d' % (rank, i_1+i, j))
            h = solver.compute_boundedness_function([alpha_re, alpha_im])
            H[i_1+i, j] = abs(complex(h[0], h[1]))

    # Transfer computed data to the master process.
    if rank > 0:
        data = H[i_1:i_2, :]
        comm.Send((data, MPI.DOUBLE), dest=0)


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
comm_size = comm.Get_size()

_worker(rank)

comm.Barrier()

if rank == 0:
    # Collect data from all other processes.

    for r in range(1, comm_size):
        size = int(len(alpha_re_list) / comm_size + 1)
        data = H[r*size:(r+1)*size, :]
        comm.Recv([data, MPI.DOUBLE], source=r)

    np.savez_compressed('_assets/carpet_new.npz',
                        ALPHA_RE=alpha_re_list,
                        ALPHA_IM=alpha_im_list,
                        H=H)

    # plt.contourf(alpha_re_list, alpha_im_list, log(1 + H.T))
    # plt.show()
