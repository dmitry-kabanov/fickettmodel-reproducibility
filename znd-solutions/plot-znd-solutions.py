#!/usr/bin/env python
"""Plot ZND solutions for different values of activation energy."""
import os

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from saf.fm.linear import Reader

from helpers import FIGSIZE_TWO_SUBPLOTS_TWO_ROWS as figsize
from helpers import savefig


OUTPUT_DIR = '_output'

dirs = os.listdir(OUTPUT_DIR)
dirs.sort()

data = []

for d in dirs:
    dirname = os.path.join(OUTPUT_DIR, d)
    theta = dirname.split('=')[1]

    r = Reader(dirname)
    znd_data = r.get_znd_data()
    x = znd_data['x']
    u = znd_data['u']
    lamda = znd_data['lamda']

    data.append({'theta': theta, 'x': x, 'u': u, 'lamda': lamda})

x_range = (-15, 0)

fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=figsize)
ax1.set_xlim(x_range)
ax1.set_xlabel(r'$x$')
ax1.set_ylabel(r'$\bar u$')
ax1.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x}'))

ax2.set_xlim(x_range)
ax2.set_xlabel(r'$x$')
ax2.set_ylabel(r'$\bar \lambda$')

styles = ['-', '--', '-.', ':']

for i, datum in enumerate(data):
    label = r'$\theta=%s$' % datum['theta']
    ax1.plot(datum['x'], datum['u'], styles[i], label=label)
    ax2.plot(datum['x'], datum['lamda'], styles[i])

fig.tight_layout(pad=0.1)

filename = 'znd-solutions.pdf'
savefig(filename)
