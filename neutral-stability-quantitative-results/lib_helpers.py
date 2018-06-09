import os

import numpy as np

from scipy import linalg

from saf.fm.linear import Reader
from saf.util import compute_observed_order_of_accuracy

# Human-friendly representation of a missing datum.
NAN_REPR = '{N/A}'


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
