import os

import numpy as np

from scipy import linalg

from saf.fm.linear import Reader
from saf.util import compute_observed_order_of_accuracy

# Human-friendly representation of a missing datum.
NAN_REPR = '{N/A}'


def get_target_dirs_and_resolutions():
    """Get lists of simulation results and corresponding grid resolutions."""
    rootdir = '_output'
    dirs = os.listdir(rootdir)
    dirs.sort()

    target_dirs = []
    for d in dirs:
        if d.startswith('n12'):
            target_dirs.append(os.path.join(rootdir, d))

    target_dirs.sort()

    resolutions = []
    for d in target_dirs:
        chunks = d.split('=')
        resolutions.append(int(chunks[-1]))

    return target_dirs, resolutions


def get_errors(target_dirs):
    """Compute relative errors in $L_1$, $L_2$, and $L_\infty$ norms."""
    d_list = []

    for outdir in target_dirs:
        r = Reader(outdir)
        __, d = r.get_time_and_detonation_velocity()

        d_list.append(d)

    errors_l1 = [float('NaN')]
    errors_l2 = [float('NaN')]
    errors_linf = [float('NaN')]
    for i, d in enumerate(d_list):
        if i == 0:
            continue

        d_1 = d_list[i-1]
        d_2 = d_list[i]

        error = linalg.norm(d_1 - d_2, 1) / linalg.norm(d_2, 1)
        errors_l1.append(error)

        error = linalg.norm(d_1 - d_2, 2) / linalg.norm(d_2, 2)
        errors_l2.append(error)

        error = linalg.norm(d_1 - d_2, np.Inf) / linalg.norm(d_2, np.Inf)
        errors_linf.append(error)

    assert len(target_dirs) == len(errors_linf)

    errors_l1 = np.array(errors_l1)
    errors_l2 = np.array(errors_l2)
    errors_linf = np.array(errors_linf)

    errors = {
        'l1': errors_l1,
        'l2': errors_l2,
        'linf': errors_linf,
    }

    return errors


def get_orders_of_accuracy(errors, resolutions):
    r_l1 = compute_observed_order_of_accuracy(errors['l1'], resolutions)
    r_l2 = compute_observed_order_of_accuracy(errors['l2'], resolutions)
    r_linf = compute_observed_order_of_accuracy(errors['linf'], resolutions)
    r = {'l1': r_l1, 'l2': r_l2, 'linf': r_linf}

    return r


def render_table_as_latex(columns, headers, formatters):
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
