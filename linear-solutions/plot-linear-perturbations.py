#!/usr/bin/env python
import os
import sys

import matplotlib.pyplot as plt
import numpy as np

from helpers import FIGSIZE_LARGE as figsize
from helpers import savefig

time_step = 5000
profile_name = 'profile-{:d}.txt'.format(time_step)

dir_1 = os.path.join('_output', 'theta=0.920')
dir_2 = os.path.join('_output', 'theta=0.950')

data_1 = np.loadtxt(os.path.join(dir_1, 'profiles', profile_name))
x_1, u_1, lamda_1 = data_1[:, 0], data_1[:, 1], data_1[:, 2]

data_2 = np.loadtxt(os.path.join(dir_2, 'profiles', profile_name))
x_2, u_2, lamda_2 = data_2[:, 0], data_2[:, 1], data_2[:, 2]

fig, ax = plt.subplots(nrows=2, ncols=2, figsize=figsize)

ax[0, 0].plot(x_1, u_1, '-')
ax[0, 0].set_xlabel(r'$x$')
ax[0, 0].set_ylabel(r"$u '$")

ax[0, 1].plot(x_2, u_2, '-')
ax[0, 1].set_xlabel(r'$x$')
ax[0, 1].set_ylabel(r"$u '$")

ax[1, 0].plot(x_1, lamda_1, '-')
ax[1, 0].set_xlabel(r'$x$')
ax[1, 0].set_ylabel(r"$\lambda '$")

ax[1, 1].plot(x_2, lamda_2, '-')
ax[1, 1].set_xlabel(r'$x$')
ax[1, 1].set_ylabel(r"$\lambda '$")

fig.tight_layout(pad=0.1)

filename = 'linear-perturbations.pdf'
savefig(filename)
