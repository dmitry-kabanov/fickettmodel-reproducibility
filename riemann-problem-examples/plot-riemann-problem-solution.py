#!/usr/bin/env python
import argparse

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from helpers import FIGSIZE_LARGE as FIGSIZE
from helpers import savefig


def riemannsolver(state_l, state_r, params, x=0.0, t=1):
    """Compute solution of the Riemann problem at :math:`\sigma=x/t`."""

    u_l, lamda_l = state_l
    u_r, lamda_r = state_r

    q, D = params['q'], params['D']

    u_m = np.sqrt(u_l**2 + q * (lamda_l - lamda_r))
    lamda_m = lamda_r

    # If `u_l` < `u_r`, then wave configuration is a contact and
    # a rarefaction wave, otherwise the contact and a shock wave.
    if u_l < u_r:
        # `s_head` and `s_tail` are speeds
        # of the rarefaction's head and tail, respectively.
        s_head = u_r - D
        s_tail = u_m - D
        if x >= s_head * t:
            # To the right of rarefaction wave.
            return (u_r, lamda_r, -D, s_head)
        elif x >= s_tail * t:
            # Inside rarefaction wave.
            u_c, lamda_c = x/t + D, lamda_r
            return (u_c, lamda_c, -D, s_head)
        elif x >= -D * t:
            # Between contact and rarefaction.
            return (u_m, lamda_m, -D, s_head)
        else:
            # To the left of the contact.
            return (u_l, lamda_l, -D, s_head)
    else:
        # `s` is a shock speed.
        s = 0.5 * (u_l + u_r) - D
        if x >= s * t:
            return (u_r, lamda_r, -D, s)
        elif x >= -D * t:
            return (u_m, lamda_m, -D, s)
        else:
            return (u_l, lamda_l, -D, s)


def plot_riemann_problem(type, ax_1, ax_2, ax_chars):
    assert type in [1, 2]

    q = 9
    D = np.sqrt(q)

    if type == 1:
        state_l = (4, 1)
        state_r = (3, 0.0)

        x_l, x_r = -4, 1
        x = np.linspace(x_l, x_r, num=1001)
        assert 0.0 in x
    else:
        state_l = (4, 1.0)
        state_r = (6, 0.0)

        x_l, x_r = -4, 4
        x = np.linspace(x_l, x_r, num=1001)
    t = 1

    params = {'q': q, 'D': D}

    soln_u = np.empty_like(x)
    soln_lamda = np.empty_like(x)

    for i, x_i in enumerate(x):
        result = riemannsolver(state_l, state_r, params, x=x_i, t=t)
        soln_u[i] = result[0]
        soln_lamda[i] = result[1]
        # speed_l = result[2]
        speed_r = result[3]

    lw = mpl.rcParams['axes.linewidth']
    ax_1.plot(x, soln_u, '-')
    ax_1.set_xlabel(r'$x$')
    ax_1.set_ylabel(r'$u$')
    ax_1.set_xlim((x_l, x_r))
    ax_2.plot(x, soln_lamda, '-')
    ax_2.set_xlabel(r'$x$')
    ax_2.set_ylabel(r'$\lambda$')
    ax_2.set_xlim((x_l, x_r))

    # ---------------------
    # Plot characteristics
    # ---------------------
    # Solution in the "M" region to plot characteristics.
    result = riemannsolver(state_l, state_r, params, x=0, t=t)
    u_m = result[0]
    # lamda_m = result[1]

    u_l = state_l[0]
    u_r = state_r[0]

    if u_l >= u_r:
        # Left wave is contact with speed -D, right wave is shock.
        x_0_list = np.arange(x_l-5, x_r+5, step=0.25)
        if 0.0 not in x_0_list:
            x_0_list = list(x_0_list) + [0.0]
        # `char_x` and `char_t` contain characteristics information.
        chars_x = [[x] for x in x_0_list]
        chars_t = [[0] for x in x_0_list]

        s = speed_r
        for i, x_0 in enumerate(x_0_list):
            if x_0 < 0.0:
                # Collision time with the contact.
                t_1 = -x_0 / (u_l)
                x_1 = -D * t_1

                # Collision time with the shock.
                t_2 = (-x_1 + (u_m - D) * t_1) / (u_m - D - s)
                x_2 = s * t_2
                chars_x[i].append(x_1)
                chars_x[i].append(x_2)
                chars_t[i].append(t_1)
                chars_t[i].append(t_2)

            elif x_0 == 0.0:
                shock_index = i
                chars_x[i].append(s * t)
                chars_t[i].append(t)
            else:
                # Collision time with the shock.
                t_1 = -x_0 / (u_r - D - s)
                x_1 = s * t_1
                chars_x[i].append(x_1)
                chars_t[i].append(t_1)

        for i in range(len(chars_x)):
            line, = ax_chars.plot(chars_x[i], chars_t[i], 'k-', lw=lw)

        ax_chars.plot(chars_x[shock_index], chars_t[shock_index],
                      'k-', linewidth=2*lw)

        chars_2_t = [0.0, t]
        for i in range(len(chars_x)):
            chars_2_x = [chars_x[i][0], chars_x[i][0] - D*t]

        contact_x = [0.0, -D * t]
        contact_t = [0.0, t]
        ax_chars.plot(contact_x, contact_t, 'k-', lw=2*lw)

        ax_chars.set_xlim((x_l, x_r))
        ax_chars.set_ylim((0, t))
        ax_chars.set_xlabel(r'$x$')
        ax_chars.set_ylabel(r'$t$')

        fig.tight_layout(pad=0.1)
    else:
        # Left wave is contact with speed -D, right wave is rarefaction.
        x_0_list = np.arange(x_l-5, x_r+5, step=0.5)
        if 0.0 not in x_0_list:
            x_0_list = list(x_0_list) + [0.0]
        # `char_x` and `char_t` contain characteristics information.
        chars_x = [[x] for x in x_0_list]
        chars_t = [[0] for x in x_0_list]
        # s_head = speed_r
        # s_tail = u_m - D
        for i, x_0 in enumerate(x_0_list):
            if x_0 < 0.0:
                # Collision time with the contact.
                t_1 = -x_0 / u_l
                x_1 = -D * t_1

                x_2 = x_1 + (u_m - D) * (t - t_1)
                chars_x[i].append(x_1)
                chars_x[i].append(x_2)
                chars_t[i].append(t_1)
                chars_t[i].append(t)
            elif x_0 == 0.0:
                rarefaction_index = i
            else:
                x_1 = x_0 + (u_r - D) * t
                chars_x[i].append(x_1)
                chars_t[i].append(t)

        i_tail = len(x_0_list)
        chars_x.append([0.0, (u_m - D) * t])
        chars_t.append([0.0, t])
        i_head = i_tail + 1
        chars_x.append([0.0, (u_r - D) * t])
        chars_t.append([0.0, t])

        for i in range(3):
            u = u_m + (i+1) * (u_r - u_m) / 4.0
            chars_x.append([0.0, (u - D) * t])
            chars_t.append([0.0, t])

        for i in range(len(chars_x)):
            line, = ax_chars.plot(chars_x[i], chars_t[i], 'k-', linewidth=lw)

        ax_chars.plot(chars_x[i_tail], chars_t[i_tail], 'k-', linewidth=2*lw)
        ax_chars.plot(chars_x[i_head], chars_t[i_head], 'k-', linewidth=2*lw)

        chars_2_t = [0.0, t]
        for i in range(len(chars_x)):
            chars_2_x = [chars_x[i][0], chars_x[i][0] - D*t]

        contact_x = [0.0, -D * t]
        contact_t = [0.0, t]
        ax_chars.plot(contact_x, contact_t, 'k-', linewidth=2*lw)

        ax_chars.set_xlim((x_l, x_r))
        ax_chars.set_ylim((0, t))
        ax_chars.set_xlabel(r'$x$')
        ax_chars.set_ylabel(r'$t$')


if __name__ == '__main__':
    fig, axes = plt.subplots(nrows=3, ncols=2, figsize=FIGSIZE)

    plot_riemann_problem(1, axes[0, 0], axes[1, 0], axes[2, 0])
    plot_riemann_problem(2, axes[0, 1], axes[1, 1], axes[2, 1])

    fig.tight_layout(pad=0.1)

    savefig('riemann-problem.pdf')
