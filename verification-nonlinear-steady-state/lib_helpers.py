"""Library of functions for convergence study.

Contains functions that compute errors and generate data table with the results
of the convergence study.

"""
import os

import numpy as np

from scipy import linalg

from saf.fm.linear import Reader
from saf.util import compute_observed_order_of_accuracy

# Human-friendly representation of a missing datum.
NAN_REPR = '{N/A}'


def get_target_dirs_and_resolutions(prefix=None):
    """Get lists of simulation results and corresponding grid resolutions."""
    rootdir = '_output'
    dirs = os.listdir(rootdir)
    dirs.sort()

    target_dirs = []
    for d in dirs:
        if prefix is not None:
            if d.startswith(prefix):
                target_dirs.append(os.path.join(rootdir, d))
        else:
            target_dirs.append(os.path.join(rootdir, d))

    target_dirs.sort()

    resolutions = []
    for d in target_dirs:
        chunks = d.split('=')
        resolutions.append(int(chunks[-1]))

    return target_dirs, resolutions


def get_time_series(target_dirs):
    """Read simulation data from `target_dirs`"""
    t_list = []
    d_list = []

    for outdir in target_dirs:
        r = Reader(outdir)
        t, d = r.get_time_and_detonation_velocity()

        t_list.append(t)
        d_list.append(d)

    return t_list, d_list


def get_errors(target_dirs):
    """Read simulation data from `target_dirs` and compute errors."""
    t_list, d_list = get_time_series(target_dirs)

    errors = []
    for i, d in enumerate(d_list):
        t = t_list[i]
        #d = d[(t > 145) & (t < 150)]
        #d_ = d.mean()

        #error = np.abs(d_ - 2.0)
        error = linalg.norm(d - 2.0, 2) / np.sqrt(len(d))
        errors.append(error)

    assert len(target_dirs) == len(errors)

    errors = np.array(errors)

    return errors


def get_orders_of_accuracy(errors, resolutions):
    r = compute_observed_order_of_accuracy(errors, resolutions)

    return r


def render_table_as_latex(columns, headers, formatters):
    """Render data as LaTeX table."""
    if len(columns) != len(headers):
        raise ValueError('Mismatch between number of columns and headers')

    if len(columns) != len(formatters):
        raise ValueError('Mismatch between number of columns and formatters')

    headers = ' & '.join(headers) + r' \\'

    lines = []

    alignment = len(columns)*'c'
    whitespace = r'@{\extracolsep{\fill}}'
    tabular_line = r'\begin{tabular*}'
    tabular_line += r'{\textwidth}{' + whitespace + alignment + r'} \\'
    lines.append(tabular_line)
    lines.append(r'\toprule')
    lines.append(headers)
    lines.append(r'\midrule')

    height = len(columns[0])

    for i in range(height):
        cells = []

        for j in range(len(columns)):
            if formatters[j] is None:
                v = str(columns[j][i])
            else:
                v = _format(columns[j][i], formatters[j])

            cells.append(v)

        line = ' & '.join(cells) + r' \\'
        lines.append(line)

    lines.append(r'\bottomrule')
    lines.append(r'\end{tabular*}')
    lines.append('')  # To have a newline symbol at the end.

    table = '\n'.join(lines)

    return table


def _format(v, format_str):
    if np.isnan(v):
        return NAN_REPR
    else:
        return format_str.format(v)
