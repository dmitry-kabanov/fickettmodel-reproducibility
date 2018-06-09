#!/usr/bin/env python
"""Plot two bifurcation diagrams on one figure to estimate convergence."""
import argparse
import os

import matplotlib.pyplot as plt
import numpy as np

from lib_bifdiag import get_bifurcation_data


START_TIME = 800


def parse_args():
    """Parse command-line arguments."""
    p = argparse.ArgumentParser()
    p.add_argument('N12_1', help='First resolution N_{1/2}', type=int)
    p.add_argument('N12_2', help='First resolution N_{1/2}', type=int)
    p.add_argument('--comparator', '-c', help='Min or max comparator',
                   choices=['minima', 'maxima'], default='minima')
    p.add_argument('--order', '-o', type=int, default=100,
                   help='How many points on each side to '
                        'consider for determining local extrema')
    p.add_argument('--save', '-s', help='Save or show on display',
                   action='store_true')

    return p.parse_args()


def plot_bifurcation_diagrams_together(data_1, data_2, comparator):
    x_1, y_1 = data_1
    x_2, y_2 = data_2
    x_min, x_max = x_1[0], x_1[-1]

    # Marker size.
    ms = 1

    plt.figure()
    for i, theta in enumerate(x_1):
        extrema = y_1[i]
        thetas = theta * np.ones_like(extrema)
        plt.plot(thetas, extrema, 'ko', markersize=ms, rasterized=True)

    for i, theta in enumerate(x_2):
        extrema = y_2[i]
        thetas = theta * np.ones_like(extrema)
        plt.plot(thetas, extrema, 'C0s', markersize=ms, rasterized=True)

    plt.xlabel(r'$\theta$')
    plt.ylabel(r'Local %s of $D$' % comparator)
    plt.xlim((x_min, x_max))
    plt.tight_layout(pad=0.1)


if __name__ == '__main__':
    args = parse_args()
    N12_1 = args.N12_1
    N12_2 = args.N12_2
    comparator = args.comparator
    order = args.order

    bif_data_1 = get_bifurcation_data(N12_1, START_TIME, comparator, order)
    bif_data_2 = get_bifurcation_data(N12_2, START_TIME, comparator, order)

    # Check that the values of :math:`$\theta$` are the same.
    assert np.all(bif_data_1[0] == bif_data_2[0])

    plot_bifurcation_diagrams_together(bif_data_1, bif_data_2, comparator)

if args.save:
    filename = 'bif-diag-N12_1=%d-N12_2=%d-comparator=%s-order=%d.pdf'
    filename = filename % (N12_1, N12_2, comparator, order)
    filename = os.path.join('_assets', filename)
    plt.savefig(filename, dpi=300)
else:
    plt.show()
