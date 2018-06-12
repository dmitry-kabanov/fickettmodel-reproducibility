#!/usr/bin/env python
"""
Verify the nonlinear solver for a stable limit-cycle case.

Generate a LaTeX table with the order-of-accuracy results for the nonlinear
solver when the long-time behavior of the nonlinear solution is a stable
limit-cycle case.
The case we consider is weakly unstable, that is, the magnitude of oscillations
of the limit cycle is small.
Hence, the nonlinear solver uses only the second-order algorithms.

"""
import argparse
import os

import numpy as np

from scipy import signal

from saf.util import compute_observed_order_of_accuracy
from saf.fm.nonlinear import Reader

from lib_helpers import (get_target_dirs_and_resolutions,
                         render_table_as_latex)


START_TIME = 900


def generate_table(filename=None):
    target_dirs, resolutions = get_target_dirs_and_resolutions()
    errors = get_errors(target_dirs)
    orders = compute_observed_order_of_accuracy(errors, resolutions)

    error_format = r'\num{{{:.0e}}}'
    order_format = '{:.2f}'

    columns = [
        resolutions,
        errors, orders,
    ]

    headers = [
        '$N_{1/2}$',
        '$E$', '$r$',
    ]

    formatters = [
        '{:d}',
        error_format, order_format,
    ]

    table = render_table_as_latex(columns, headers, formatters)

    if filename is None:
        print(table)
    else:
        with open(filename, 'w') as f:
            f.write(table)


def get_errors(target_dirs):
    """Compute errors by comparing the mean of late-time minima of D(t)."""
    mean_min = []

    for outdir in target_dirs:
        r = Reader(outdir)
        t, d = r.get_time_and_detonation_velocity()

        dw = d[t >= START_TIME]
        indices = signal.argrelmin(dw)[0]
        minima = dw[indices]

        mean_min.append(minima.mean())

    errors = [float('nan')]
    for i, __ in enumerate(mean_min[:-1]):

        error = np.abs(mean_min[i] - mean_min[i+1])
        errors.append(error)

    errors = np.array(errors)

    return errors


if __name__ == '__main__':
    filename = 'verification-nonlinear-solver-limit-cycle.tex'
    filename = os.path.join('_assets', filename)

    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('-s', '--save', action='store_true',
                   help='save the results to `{:s}`'.format(filename))
    args = p.parse_args()

    if not args.save:
        filename = None

    generate_table(filename)
