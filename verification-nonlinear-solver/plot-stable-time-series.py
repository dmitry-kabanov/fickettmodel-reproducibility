#!/usr/bin/env python
"""Plot time series of detonation velocity for stable case."""
import os
import sys

import matplotlib.pyplot as plt

from lib_helpers import (get_target_dirs_and_resolutions,
                         get_time_series)


def generate_plot(filename=None):
    """Plot time series of detonation velocity."""
    target_dirs, resolutions = get_target_dirs_and_resolutions('stable')
    t_list, d_list = get_time_series(target_dirs)

    styles = ['-', '--', '-.', ':', '.', ',']

    if len(d_list) > len(styles):
        print('WARNING: insufficient number of line styles specified')

    plt.figure()
    for i in range(len(target_dirs)):
        plt.plot(t_list[i], d_list[i], styles[i], label=resolutions[i])

    plt.xlabel(r'$t$')
    plt.ylabel(r'$D$')
    plt.legend()
    plt.tight_layout(pad=0.1)

    if filename:
        plt.savefig(filename)
    else:
        plt.show()


if __name__ == '__main__':
    filename = None
    if len(sys.argv) > 1:
        filename = os.path.join('_assets', 'verification-nonlinear.tex')
    generate_plot(filename)
