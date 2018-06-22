#!/usr/bin/env python
r"""Plot phase portrait for given :math:`\theta`."""
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from helpers import FIGSIZE_SIX_SUBPLOTS as FIGSIZE
from helpers import savefig

from lib_timeseries import get_data

CUTOFF_TIME = 900


N12 = 1280

inputs = [
    {'theta': 0.950, 'with_inset': False},
    {'theta': 1.000, 'with_inset': False},
    {'theta': 1.004, 'with_inset': False},
    {'theta': 1.055, 'with_inset': True},
    {'theta': 1.065, 'with_inset': True},
    {'theta': 1.089, 'with_inset': True},
]

# Data is a list of dictionaries:
# Elements: time window, window of detonation velocity,
# detonation velocity smoothed, acceleration of detonation velocity.
data = []


for inp in inputs:
    theta = inp['theta']
    tw, Dw, D_smooth, dD_dt = get_data(N12, theta, CUTOFF_TIME)
    datum = {'tw': tw, 'Dw': Dw, 'D_smooth': D_smooth, 'dD_dt': dD_dt}
    data.append(datum)


assert len(inputs) == len(data)

# -----------------------------------------------------------------------------
# Plotting

# Line width for the phase portrait.
# It should be thinner than usual line width that we use, to make plot
# looking correct (?, or maybe, better to say, looking good).
lw = 1

fig, axes = plt.subplots(nrows=4, ncols=3, figsize=FIGSIZE)

coord_x = -0.20
coord_y = -0.20
labels = ['a', 'b', 'c', 'd', 'e', 'f']

for i in [0,  1]:
    for j in [0, 1, 2]:
        k = 3*i + j
        theta = inputs[k]['theta']
        with_inset = inputs[k]['with_inset']

        datum = data[k]
        tw, Dw = datum['tw'], datum['Dw']
        D_smooth, dD_dt = datum['D_smooth'], datum['dD_dt']

        if theta == 0.950:
            label_x_coord = 0.0

        ax = axes[2*i, j]
        ax.plot(tw, Dw, '-')
        # ax.set_xlabel(r'$t$')
        # ax.set_ylabel(r'$D$')
        ax.set_xlim((tw[0], tw[-1]))
        ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('% .2f'))
        ax.text(coord_x, coord_y, labels[k], transform=ax.transAxes)
        # ax.get_yaxis().set_label_coords(0.03, 0.8, transform=fig.transFigure)

        # Omit first `i` time steps as they look ugly.
        idx = 20
        ax = axes[2*i+1, j]
        ax.plot(D_smooth[idx:], dD_dt[idx:], '-', lw=lw, rasterized=True)
        ax.plot(D_smooth[0], dD_dt[0], 'ro')
        # ax.set_xlabel(r'$D$')
        # ax.set_ylabel(r'$\mathrm{d}D/\mathrm{d}t$')
        # ax.yaxis.set_label_coords(0.03, 0.3, transform=fig.transFigure)

        if dD_dt.max() > 100:
            fmt = ticker.ScalarFormatter(useOffset=True, useMathText=True)
            fmt.set_powerlimits((-2, 2))
            ax.yaxis.set_major_formatter(fmt)

        if with_inset:
            ax_inset = inset_axes(ax, width='35%', height='35%', loc=2)
            ax_inset.plot(D_smooth[i:], dD_dt[i:], '-', lw=lw, rasterized=True)
            ax_inset.plot(D_smooth[0], dD_dt[0], 'ro')
            ax_inset.set_xlim((1.8, 2.5))
            ax_inset.set_ylim((-1, 1))

            # Remove ticks and labels from the inset.
            ax_inset.tick_params(left=False, bottom=False,
                                 labelleft=False, labelbottom=False)

fig.tight_layout(pad=0.1)

filename = 'time-series-and-phase-portraits-together.pdf'
savefig(filename, dpi=300)
