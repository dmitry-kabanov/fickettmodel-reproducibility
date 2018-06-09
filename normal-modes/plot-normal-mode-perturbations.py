#!/usr/bin/env python
import matplotlib.pyplot as plt

from lib_normalmodes import LeeStewartSolver

from helpers import FIGSIZE_TWO_SUBPLOTS_TWO_ROWS as figsize
from helpers import savefig


q = 4
theta = 0.95
tol = 1e-4

s = LeeStewartSolver(q, theta, tol)

alpha = 0.0290 + 0.8700j

result = s.solve_eigenvalue_problem(alpha)

print(result['eigenvalue'])

solution = result['pert']

fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=figsize)
ax1.plot(solution.x, solution.u_real, '-')
ax1.plot(solution.x, solution.lamda_real, '--')
ax1.set_xlim((-14, 0))
ax1.set_xlabel(r'$x$')
ax1.set_ylabel(r'$u\prime_\mathrm{re}, \lambda\prime_\mathrm{re}$')
ax2.plot(solution.x, solution.u_imag, '-')
ax2.plot(solution.x, solution.lamda_imag, '--')
ax2.set_xlim((-14, 0))
ax2.set_xlabel(r'$x$')
ax2.set_ylabel(r'$u\prime_\mathrm{im}, \lambda\prime_\mathrm{im}$')

fig.tight_layout(pad=0.1)

savefig('normal-modes-perturbations.pdf')
