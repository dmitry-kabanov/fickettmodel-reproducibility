#!/usr/bin/env python
r"""Plot phase portrait for given :math:`\theta`."""
import argparse
import os
import shutil
import sys

import matplotlib.pyplot as plt
import numpy as np

from matplotlib import ticker

from lib_timeseries import movingaverage, compute_fft

CUTOFF_TIME = 800


p = argparse.ArgumentParser()
p.add_argument('theta', help='Value of theta', type=float)
p.add_argument('--with-fft', help='Whether to plot FFT spectrum',
               action='store_true')
p.add_argument('--with-inset', help='Use inset or not', action='store_true')
p.add_argument('--save', '-s', help='Save or show on display',
               action='store_true')
args = p.parse_args()
theta = args.theta
with_inset = args.with_inset
with_fft = args.with_fft

if with_inset and with_fft:
    print('ERROR: cannot use both `with-inset` and `with-fft` flags')
    sys.exit(2)

N12 = 1280

dirname = 'N12=%04d/theta=%.3f' % (N12, theta)
dirname = os.path.join('_output', dirname)
filename = os.path.join(dirname, 'detonation-velocity.npz')

dirname_cache = os.path.join('N12=%04d/theta=%.3f' % (N12, theta))
dirname_cache = os.path.join('_output-cache', dirname_cache)
filename_cache = os.path.join(dirname_cache, 'detonation-velocity.npz')
if not os.path.exists(dirname_cache):
    os.makedirs(dirname_cache)

if not os.path.exists(filename_cache):
    shutil.copyfile(filename, filename_cache)

try:
    with np.load(filename_cache) as data:
        t, d = data['t'], data['d']
except IOError as exc:
    print('ERROR: %s' % exc)
    sys.exit(2)

cond = t >= CUTOFF_TIME

t_window = t[cond]
D_window = d[cond]

tw = t
dw = d

dw = movingaverage(dw, 11)

assert len(dw) == len(d)

dD_dt = np.empty_like(dw)
dD_dt[1:] = (dw[1:] - dw[:-1]) / (tw[1:] - tw[:-1])
dD_dt[0] = 0.0

dD_dt = movingaverage(dD_dt, 5)


# -----------------------------------------------------------------------------
# Plotting

# Line width for the phase portrait.
# It should be thinner than usual line width that we use, to make plot
# looking correct (?, or maybe, better to say, looking good).
lw = 1

nrows = 2
if with_fft:
    nrows = 3

if theta == 0.950:
    label_x_coord = 0.0

fig, ax = plt.subplots(nrows=nrows, ncols=1, figsize=(6, 8))
ax[0].plot(t_window, D_window, '-')
ax[0].set_xlabel(r'$t$')
ax[0].set_ylabel(r'$D$')
ax[0].set_xlim((t_window[0], t_window[-1]))
ax[0].get_yaxis().set_label_coords(0.03, 0.8, transform=fig.transFigure)

# Omit first `i` time steps as they look ugly.
i = 20
ax[1].plot(dw[i:-i], dD_dt[i:-i], '-', lw=lw, rasterized=True)
ax[1].plot(dw[0], dD_dt[0], 'ro')
ax[1].set_xlabel(r'$D$')
ax[1].set_ylabel(r'$\mathrm{d}D/\mathrm{d}t$')
ax[1].yaxis.set_label_coords(0.03, 0.3, transform=fig.transFigure)

if dD_dt.max() > 100:
    formatter = ticker.ScalarFormatter(useOffset=True, useMathText=True)
    formatter.set_powerlimits((-2, 2))
    ax[1].yaxis.set_major_formatter(formatter)

if with_fft:
    freq, power, peaks = compute_fft(t_window, D_window)
    ax[2].plot(freq, power)
    ax[2].plot(freq[peaks], power[peaks], 'ro')
    ax[2].set_xlim(0, 1)
    ax[2].set_xlabel('Frequency')
    ax[2].set_ylabel('Power spectrum')

fig.tight_layout(pad=0.2)

if with_inset:
    plt.axes([0.25, 0.25, 0.2, 0.2])
    plt.plot(dw[i:], dD_dt[i:], '-', lw=lw, rasterized=True)
    plt.plot(dw[0], dD_dt[0], 'ro')
    plt.xlim((1.8, 2.5))
    plt.ylim((-1, 1))

if args.save:
    filename = 'analysis-theta=%.3f.pdf' % theta
    filename = os.path.join('_assets', filename)
    plt.savefig(filename, dpi=300)
else:
    plt.show()
