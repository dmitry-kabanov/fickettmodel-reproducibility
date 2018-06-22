#!/usr/bin/env python
import os

import matplotlib.pyplot as plt
import numpy as np

from helpers import FIGSIZE_TWO_SUBPLOTS_TWO_ROWS as figsize
from helpers import savefig

from lib_stability import get_stability_info


FMT = '.3f'

MAX_NUMBER_OF_MODES = 6


OUTPUT_DIR = './_output'

theta_range = (0.90, 1.15)
theta_values = []

dirs = os.listdir(OUTPUT_DIR)
dirs.sort()

dirs_sorted = []

for d in dirs:
    q = float(d.split('=')[1])
    theta_values.append(q)

dirs_sorted = [d for (q, d) in sorted(zip(theta_values, dirs))]

theta_values = []
conjugate_rates = []
exponential_rates_upper = []
exponential_rates_bottom = []
freq_0 = []
other_rates = np.empty((MAX_NUMBER_OF_MODES, len(dirs_sorted)))
other_freqs = np.empty((MAX_NUMBER_OF_MODES, len(dirs_sorted)))
other_rates.fill(np.nan)
other_freqs.fill(np.nan)

for j, d in enumerate(dirs_sorted):
    d_path = os.path.join(OUTPUT_DIR, d)

    if not os.path.isfile(d_path + '/stability.txt'):
        print(d)
        continue

    q = float(d.split('=')[1])
    theta_values.append(q)

    modes = get_stability_info(d_path)
    assert len(modes) <= MAX_NUMBER_OF_MODES

    growth_rates = np.zeros_like(modes)
    for i, m in enumerate(modes):
        if isinstance(m, list):
            # Implicit assumption that there only two branches.
            growth_rates[i] = m[1]['growth_rate']
        else:
            growth_rates[i] = m['growth_rate']

    mode = modes[0]

    if isinstance(mode, list):
        assert len(mode) == 2
        conjugate_rates.append(None)

        exponential_rates_bottom.append(mode[0]['growth_rate'])
        exponential_rates_upper.append(mode[1]['growth_rate'])
        freq_0.append(mode[0]['frequency'])
    else:
        conjugate_rates.append(mode['growth_rate'])
        exponential_rates_upper.append(None)
        exponential_rates_bottom.append(None)
        freq_0.append(mode['frequency'])

    if len(modes) > 1:
        for i, m in enumerate(modes[1:]):
            assert isinstance(m, dict)

            other_freqs[i+1, j] = m['frequency']
            other_rates[i+1, j] = m['growth_rate']

# Analysis
for i, __ in enumerate(conjugate_rates):
    if conjugate_rates[i] is None or conjugate_rates[i+1] is None:
        continue

    if conjugate_rates[i] < 0.0 and conjugate_rates[i+1] >= 0.0:
        theta_crit = theta_values[i+1]
        msg = 'Switch from stable to unstable at theta={:{fmt}}'
        print(msg.format(theta_crit, fmt=FMT))
        break

i = np.argmax(freq_0)
theta_max_freq = theta_values[i]
msg = 'Maximum frequency {:{fmt}} at theta={:{fmt}}'
print(msg.format(freq_0[i], theta_max_freq, fmt=FMT))

msg = 'For theta_min={:{fmt}} rate={:{fmt}}, freq={:{fmt}}'
print(msg.format(theta_values[0], conjugate_rates[0], freq_0[0], fmt=FMT))

msg = 'For theta_max={:{fmt}} rate={:{fmt}}, freq={:{fmt}}'
print(msg.format(theta_values[-1], conjugate_rates[-1], freq_0[-1], fmt=FMT))

# Plotting.
coord_x = 0.05
coord_y = 0.70
fig, (ax_1, ax_2) = plt.subplots(2, 1, figsize=figsize)
ax_1.plot(theta_values, conjugate_rates, '-', label='Mode 0')
ax_1.set_xlim(theta_range)
ax_1.set_xlabel(r'Activation energy $\theta$')
ax_1.set_ylabel(r'Growth rate $\alpha_{\mathrm{re}}$')
ax_1.text(coord_x, coord_y, 'a', transform=ax_1.transAxes)

ax_2.plot(theta_values, freq_0, '-', label='Mode 0')
ax_2.set_xlim(theta_range)
ax_2.set_xlabel(r'Activation energy $\theta$')
ax_2.set_ylabel(r'Frequency $\alpha_{\mathrm{im}}$')
ax_2.text(coord_x, coord_y, 'b', transform=ax_2.transAxes)

fig.tight_layout(pad=0.1)

savefig('linear-spectrum.pdf')
