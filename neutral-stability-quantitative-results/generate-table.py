#!/usr/bin/env python
import os
import sys

import numpy as np

from lib_helpers import render_table_as_latex


OUTPUT_DIR = '_output'
RESULTS_FILE = os.path.join(OUTPUT_DIR, 'results.txt')


def _collect_data():
    q_list = []
    theta_list = []
    freq_list = []

    dirs = os.listdir(OUTPUT_DIR)
    for d in dirs:
        chunks = d.split('=')
        q = float(chunks[1])

        q_list.append(q)

        result_file = os.path.join(OUTPUT_DIR, d, 'result.txt')
        if os.path.isfile(result_file):
            with open(result_file, 'r') as f:
                theta_line = f.readline()
                chunks = theta_line.split('=')
                theta = float(chunks[1])
                theta_list.append(theta)

                f.readline()  # Skipping growth_rate line.

                freq_line = f.readline()
                chunks = freq_line.split('=')
                freq = float(chunks[1])
                freq_list.append(freq)
        else:
            theta_list.append(0.0)
            freq_list.append(0.0)

    tmp = sorted(zip(q_list, theta_list, freq_list))
    q_sorted = [a for (a, b, c) in tmp]
    theta_sorted = [b for (a, b, c) in tmp]
    f_sorted = [c for (a, b, c) in tmp]

    headers = [
        'Neutral stability data',
        'Columns: heat release, activation energy, frequency',
    ]
    header = '\n'.join(headers)
    data = list(zip(q_sorted, theta_sorted, f_sorted))
    np.savetxt(RESULTS_FILE, data, header=header)


def generate_table(filename=None):
    q_list, theta_list, freq_list = np.loadtxt(RESULTS_FILE, unpack=True)
    numbers = np.arange(1, len(q_list)+1)

    param_format = r'\num{{{:.2f}}}'
    value_format = '{:.3f}'

    columns = [numbers, q_list, theta_list, freq_list]

    headers = [r'$i$', r'$q$', r'$\theta_\text{crit}$', r'$\alpha_\text{im}$']
    formatters = ['{:d}', param_format, value_format, value_format]

    table = render_table_as_latex(columns, headers, formatters)

    if filename is None:
        print(table)
    else:
        with open(filename, 'w') as f:
            f.write(table)


if __name__ == '__main__':
    # Collect and read results.
    if not os.path.exists(RESULTS_FILE):
        _collect_data()

    filename = os.path.join('_assets', 'neutral-stability-table.tex')
    generate_table(filename)
