#!/usr/bin/env python
import os

import matplotlib.pyplot as plt
import numpy as np

from helpers import FIGSIZE_TWO_SUBPLOTS_ONE_ROW as figsize
from helpers import savefig


OUTPUT_DIR = '_output'
RESULTS_FILE = os.path.join(OUTPUT_DIR, 'results.txt')


def _collect_data():
    q_list = []
    theta_list = []
    freq_list = []

    dirs = os.listdir(OUTPUT_DIR)
    for d in dirs:
        if not os.path.isdir(d):
            continue

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


def onclick_1(event):
    """On double-click inside the ax_1 frame, show the closest data point."""
    if event.inaxes != ax_1:
        return

    if not event.dblclick:
        return

    x = event.xdata
    y = event.ydata

    if x is None or y is None:
        return

    x_clicked, y_clicked = _get_clicked_point(x, y, theta_list, q_list)
    line_1_onclicks.set_xdata(x_clicked)
    line_1_onclicks.set_ydata(y_clicked)
    plt.draw()
    msg = 'Found data point: q={:22.16e}, e={:22.16e}'
    print(msg.format(y_clicked, x_clicked))


def onclick_2(event):
    """On double-click inside the ax_2 frame, show the closest data point."""
    if event.inaxes != ax_2:
        return

    if not event.dblclick:
        return

    x = event.xdata
    y = event.ydata

    if x is None or y is None:
        return

    x_clicked, y_clicked = _get_clicked_point(x, y, freq_list, q_list)
    line_2_onclicks.set_xdata(x_clicked)
    line_2_onclicks.set_ydata(y_clicked)
    plt.draw()
    msg = 'Found data point: q={:22.16e}, freq={:22.16e}'
    print(msg.format(y_clicked, x_clicked))


def _get_clicked_point(x, y, x_data, y_data):
    distances = np.sqrt(((x - x_data)/x)**2 + ((y - y_data)/y)**2)
    i = distances.argmin()

    return x_data[i], y_data[i]


# Collect and read results.
if not os.path.exists(RESULTS_FILE):
    _collect_data()

q_list, theta_list, freq_list = np.loadtxt(RESULTS_FILE, unpack=True)

# Check for fails.
idx = np.where(theta_list == 0.0)[0]

if len(theta_list[idx]) > 0:
    print('Number of fails: {}'.format(len(theta_list[idx])))
    print('Corresponding Q:')
    for i in idx:
        print('{:22.16e}'.format(q_list[i]))

# Obtain clean data by removing outliers.
idx = np.where(theta_list != 0.0)[0]
q_clean = np.array(q_list[idx])
theta_clean = np.array(theta_list[idx])
freq_clean = np.array(freq_list[idx])

# Plot figure.
fig, (ax_1, ax_2) = plt.subplots(nrows=1, ncols=2, figsize=figsize)
fig.canvas.mpl_connect('button_press_event', onclick_1)
fig.canvas.mpl_connect('button_press_event', onclick_2)
ax_1.plot(theta_clean, q_clean, '-')
line_1_onclicks, = ax_1.plot([], 'ro')
ax_1.set_xlabel(r'Activation energy $\theta$')
ax_1.set_ylabel(r'Heat release $q$')
ax_1.grid()

ax_2.plot(freq_clean, q_clean, '-')
line_2_onclicks, = ax_2.plot([], 'ro')
ax_2.set_xlabel(r'Frequency $\alpha_{\mathrm{im}}$')
ax_2.grid()

fig.tight_layout(pad=0.1)

fn = 'neutral-stability.pdf'
savefig(fn)
