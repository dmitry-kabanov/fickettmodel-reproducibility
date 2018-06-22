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

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=figsize)
coord_x = 0.05
coord_y = 0.80
x_range = (int(x_1[0]), int(x_1[-1]))

ax = axes[0, 0]
ax.plot(x_1, u_1, '-')
ax.set_xlabel(r'$x$')
ax.set_ylabel(r"$u '$")
ax.set_xlim(x_range)
ax.text(coord_x, coord_y, 'a', transform=ax.transAxes)

ax = axes[0, 1]
ax.plot(x_2, u_2, '-')
ax.set_xlabel(r'$x$')
ax.set_ylabel(r"$u '$")
ax.set_xlim(x_range)
ax.text(coord_x, coord_y, 'b', transform=ax.transAxes)

ax = axes[1, 0]
ax.plot(x_1, lamda_1, '-')
ax.set_xlabel(r'$x$')
ax.set_ylabel(r"$\lambda '$")
ax.set_xlim(x_range)
ax.text(coord_x, coord_y, 'c', transform=ax.transAxes)

ax = axes[1, 1]
ax.plot(x_2, lamda_2, '-')
ax.set_xlabel(r'$x$')
ax.set_ylabel(r"$\lambda '$")
ax.set_xlim(x_range)
ax.text(coord_x, coord_y, 'd', transform=ax.transAxes)

fig.tight_layout(pad=0.1)

filename = 'linear-perturbations.pdf'
savefig(filename)
