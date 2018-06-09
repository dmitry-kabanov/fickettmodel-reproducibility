#!/usr/bin/env python
"""Plot bifurcation diagram.

Bifurcation data are obtained by extracting local extrema from the time series.
We also cache data to avoid rereading time series multiple times.

"""
import argparse
import os

import matplotlib.pyplot as plt
import numpy as np

from lib_bifdiag import get_bifurcation_data

START_TIME = 800


def parse_args():
    """Parse command-line arguments."""
    p = argparse.ArgumentParser()
    p.add_argument('N12', help='Resolution', type=int)
    p.add_argument('--comparator', '-c', help='Min or max comparator',
                   choices=['minima', 'maxima'], default='minima')
    p.add_argument('--order', '-o', type=int, default=100,
                   help='How many points on each side to '
                        'consider for determining local extrema')
    p.add_argument('--save', '-s', help='Save or show on display',
                   action='store_true')

    return p.parse_args()


def plot_bifurcation_diagram(theta_array, bif_data, comparator):
    plt.figure()
    for i, theta in enumerate(theta_array):
        extrema = bif_data[i]
        thetas = theta * np.ones_like(extrema)
        plt.plot(thetas, extrema, 'k.', markersize=1, rasterized=True)

    plt.xlabel(r'$\theta$')
    plt.ylabel(r'Local %s of $D$' % comparator)
    plt.xlim((theta_array[0], theta_array[-1]))
    plt.tight_layout(pad=0.1)


if __name__ == '__main__':
    args = parse_args()
    N12 = args.N12
    comparator = args.comparator
    order = args.order
    save = args.save

    theta, D = get_bifurcation_data(N12, START_TIME, comparator, order)
    plot_bifurcation_diagram(theta, D, comparator)

    if save:
        filename = 'bif-diag-N12=%04d-comparator=%s-order=%03d.pdf'
        filename = filename % (N12, comparator, order)
        filename = os.path.join('_assets', filename)
        plt.savefig(filename, dpi=300)
    else:
        plt.show()
