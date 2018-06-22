#!/usr/bin/env python
import os
import sys

import matplotlib.pyplot as plt

from saf.fm.linear import Reader

from helpers import FIGSIZE_TWO_SUBPLOTS_ONE_ROW as figsize
from helpers import savefig


theta = 0.95

dir_lin = os.path.join('_output', 'linear-theta=%.2f' % theta)
r_lin = Reader(dir_lin)
t_lin, d_lin = r_lin.get_time_and_detonation_velocity()

# Add steady detonation velocity to `d_lin` (which is a perturbation only).
comp_val = r_lin.get_computed_values()
d_lin += comp_val['d_znd']

dir_nonlin = os.path.join('_output', 'nonlinear-theta=%.2f' % theta)
r_nonlin = Reader(dir_nonlin)
t_nonlin, d_nonlin = r_nonlin.get_time_and_detonation_velocity()

# Plotting
coord_x = 0.05
coord_y = 0.85
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=figsize)
ax1.plot(t_lin, d_lin, '-')
ax1.plot(t_nonlin, d_nonlin, '--')
ax1.set_xlim(50, 150)
ax1.set_ylim(1.98, 2.02)
ax1.set_xlabel(r'$t$')
ax1.set_ylabel(r'$D$')
ax1.text(coord_x, coord_y, 'a', transform=ax1.transAxes)

ax2.plot(t_lin, d_lin, '-')
ax2.plot(t_nonlin, d_nonlin, '--')
ax2.set_xlim(150, 250)
ax2.set_ylim(1.8, 2.2)
ax2.set_xlabel(r'$t$')
ax2.set_ylabel(r'$D$')
ax2.text(coord_x, coord_y, 'b', transform=ax2.transAxes)

fig.tight_layout(pad=0.1)

filename = 'linear-vs-nonlinear.pdf'
savefig(filename)
