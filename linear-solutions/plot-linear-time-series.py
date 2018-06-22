#!/usr/bin/env python
import os

import matplotlib.pyplot as plt

from saf.fm.linear import Reader

from helpers import FIGSIZE_TWO_SUBPLOTS_ONE_ROW as figsize
from helpers import savefig

dir_1 = os.path.join('_output', 'theta=0.920')
dir_2 = os.path.join('_output', 'theta=0.950')

r_1 = Reader(dir_1)
r_2 = Reader(dir_2)

t_1, d_1 = r_1.get_time_and_detonation_velocity()
t_2, d_2 = r_2.get_time_and_detonation_velocity()

fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=figsize)
coord_x = 0.10
coord_y = 0.85

ax1.plot(t_1, d_1)
ax1.set_xlabel(r'$t$')
ax1.set_ylabel(r"$\psi '$")
ax1.set_xlim((0, 100))
ax1.text(coord_x, coord_y, 'a', transform=ax1.transAxes)

ax2.plot(t_2, d_2)
ax2.set_xlabel(r'$t$')
ax2.set_ylabel(r"$\psi '$")
ax2.set_xlim((0, 100))
ax2.text(coord_x, coord_y, 'b', transform=ax2.transAxes)

fig.tight_layout(pad=0.1)

filename = 'linear-time-series.pdf'
savefig(filename)
