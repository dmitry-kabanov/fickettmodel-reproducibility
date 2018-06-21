#!/usr/bin/env python
"""Plot the bifurcation diagram.

Bifurcation data are obtained by extracting local extrema from the time series.
We also cache data to avoid rereading the time series multiple times.

"""
import argparse

import matplotlib.pyplot as plt
import numpy as np

from helpers import FIGSIZE_LARGER as FIGSIZE
from helpers import savefig

from lib_bifdiag import get_bifurcation_data


def parse_args():
    """Parse command-line arguments."""
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('N12', help='Resolution', type=int)
    p.add_argument('--comparator', '-c', help='Min or max comparator',
                   choices=['minima', 'maxima'], default='minima')
    p.add_argument('--order', '-o', type=int, default=100,
                   help='How many points on each side to '
                        'consider for determining local extrema')
    p.add_argument('--start-time', '-t', type=int, default=800,
                   help='From what time process the time series')
    p.add_argument('--save', '-s', help='Save or show on display',
                   action='store_true')

    return p.parse_args()


def plot_bifurcation_diagram(theta_array, bif_data, comparator):
    plt.figure(figsize=FIGSIZE)
    for i, theta in enumerate(theta_array):
        extrema = bif_data[i]
        thetas = theta * np.ones_like(extrema)
        plt.plot(thetas, extrema, 'k.', markersize=1, rasterized=True)
        plt.ylim((1.73, 2.07))

    plt.xlabel(r'$\theta$')
    plt.ylabel(r'Local %s of $D$' % comparator)
    plt.xlim((theta_array[0], theta_array[-1]))
    plt.tight_layout(pad=0.1)


if __name__ == '__main__':
    args = parse_args()
    N12 = args.N12
    comparator = args.comparator
    order = args.order
    start_time = args.start_time
    save = args.save

    theta, D = get_bifurcation_data(N12, start_time, comparator, order)
    plot_bifurcation_diagram(theta, D, comparator)

    fn = 'bif-diag-N12=%04d-comparator=%s-order=%d-start_time=%d.pdf'
    fn = fn % (N12, comparator, order, start_time)
    savefig(fn, dpi=300)
