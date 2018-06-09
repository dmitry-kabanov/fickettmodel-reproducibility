#!/usr/bin/env python
"""Generate LaTeX table with verification results."""
import os
import sys

from lib_helpers import (get_target_dirs_and_resolutions,
                         get_errors,
                         get_orders_of_accuracy,
                         render_table_as_latex)


def generate_table(filename=None):
    target_dirs, resolutions = get_target_dirs_and_resolutions()
    errors = get_errors(target_dirs)
    orders = get_orders_of_accuracy(errors, resolutions)

    error_format = r'\num{{{:.0e}}}'
    order_format = '{:.2f}'

    columns = [
        resolutions,
        errors['l1'], orders['l1'],
        errors['l2'], orders['l2'],
        errors['linf'], orders['linf']
    ]

    headers = [
        '$N_{1/2}$',
        '$E_1$', '$r_1$',
        '$E_2$', '$r_2$',
        '$E_\infty$', '$r_\infty$',
    ]

    formatters = [
        '{:d}',
        error_format, order_format,
        error_format, order_format,
        error_format, order_format,
    ]

    table = render_table_as_latex(columns, headers, formatters)

    if filename is None:
        print(table)
    else:
        with open(filename, 'w') as f:
            f.write(table)


if __name__ == '__main__':
    filename = None
    if len(sys.argv) > 1:
        filename = os.path.join('_assets', 'verification-linear-solver.tex')
    generate_table(filename)
