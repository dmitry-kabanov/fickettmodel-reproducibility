"""Library for normal-mode computations for the Fickett's model."""
import warnings

import matplotlib.pyplot as plt
import numpy as np

from numpy import array, exp, log, sqrt
from mpl_toolkits.mplot3d import Axes3D

from scipy import integrate
from scipy import optimize
from scipy import signal


class ZNDSolution(object):
    """Structure that holds steady-state quantities."""
    def __init__(self, params=None):
        self.u = None
        self.lamda = None
        self.omega = None
        self.du_dx = None
        self.dlamda_dx = None
        self.domega_du = None
        self.domega_dlamda = None
        self.params = params

    @property
    def x(self):
        c = LamdaZNDToXConverter(self.params)
        return c.convert_to_x(self._lamda_znd)


class Eigenfunctions(object):
    """Solutions of the linearized problem."""
    def __init__(self, params):
        self.params = params
        self._lamda_znd = None
        self.u_real = None
        self.u_imag = None
        self.lamda_real = None
        self.lamda_imag = None

    @property
    def lamda_znd(self):
        return self._lamda_znd

    @lamda_znd.setter
    def lamda_znd(self, value):
        self._lamda_znd = np.array(value)

    @property
    def x(self):
        c = LamdaZNDToXConverter(self.params)
        return c.convert_to_x(self._lamda_znd)


class LamdaZNDToXConverter(object):
    def __init__(self, params):
        self.params = params

    def convert_to_x(self, lamda_znd):
        s = integrate.ode(self._rhs_dx_dlamda)
        s.set_integrator('dopri5')
        s.set_initial_value(lamda_znd[0], 0.0)

        soln = [lamda_znd[0]]

        for lam in lamda_znd[1:]:
            s.integrate(lam)
            soln.append(s.y[0])

        assert s.successful()

        return np.array(soln)

    def _rhs_dx_dlamda(self, s, x):
        """Compute RHS of :math:`dx/ds`, where `s` is ZND :math:`\lambda`."""
        d, k, = self.params.d, self.params.k
        q, theta = self.params.q, self.params.theta

        u = d + sqrt(d**2 - q*s)
        omega = k * (1 - s) * exp(theta*(sqrt(q)*u + q*s))
        result = -d / omega

        return result


class Parameters(object):
    def __init__(self, q, theta, tol):
        self.q = q
        self.theta = theta

        assert tol > 0

        self.tol = tol

        self.sigma = 0.5 * q
        self.d = np.sqrt(q)
        self.k, __ = integrate.quad(self._compute_k, 0, 0.5)

        assert self.k > 0

    def _compute_k(self, lamda):
        d, q, theta = self.d, self.q, self.theta
        u = d + np.sqrt(d**2 - q*lamda)
        denom = (1 - lamda) * np.exp(theta*(np.sqrt(q)*u + q*lamda))

        return d / denom


class LeeStewartSolver(object):
    def __init__(self, q, theta, tol):
        self.params = Parameters(q, theta, tol)
        self.q = q
        self.theta = theta
        self.tol = tol
        self.sigma = self.params.sigma
        self.d = self.params.d
        self.k = self.params.k

    def solve_eigenvalue_problem(self, guess):
        guess_check_1 = isinstance(guess, np.ndarray) and len(guess) == 2
        guess_check_2 = isinstance(guess, complex)
        if not guess_check_1 and not guess_check_2:
            msg = ('Guess for an eigenvalue must be given either '
                   'as a complex number or an array with two elements')
            raise ValueError(msg)

        if isinstance(guess, complex):
            guess = np.array([guess.real, guess.imag])

        cb = self.compute_boundedness_function
        root, infodict, ier, msg = optimize.fsolve(cb, guess, full_output=True)

        if ier != 1:
            warnings.warn('Finding an eigenvalue was unsuccessful: %s' % msg)

        pert = self.compute_linearized_problem(complex(root[0], root[1]))
        znd = self.compute_znd_solution(pert.lamda_znd)

        result = {
            'eigenvalue': root,
            'infodict': infodict,
            'pert': pert,
            'znd': znd
        }

        return result

    def compute_boundedness_function(self, alpha):
        alpha_complex = complex(alpha[0], alpha[1])
        sigma = self.sigma

        eigfuncs = self.compute_linearized_problem(alpha_complex)

        pert_u = eigfuncs.u_real[-1] + 1j*eigfuncs.u_imag[-1]
        pert_lamda = eigfuncs.lamda_real[-1] + 1j*eigfuncs.lamda_imag[-1]

        znd = self.compute_znd_solution(eigfuncs.lamda_znd[-1])

        term_1 = alpha_complex * (znd.u * pert_u + sigma * pert_lamda)
        term_2 = -sigma * znd.domega_dlamda * pert_lamda

        H = term_1 + term_2

        return [H.real, H.imag]

    def compute_linearized_problem(self, alpha):
        self._alpha = alpha
        end = 1.0 - self.tol
        y0 = [2*np.real(alpha), 2*np.imag(alpha), 0.0, 0.0]

        s = integrate.ode(self._rhs)
        s.set_integrator('dopri5', nsteps=5000)
        s.set_solout(self._solout)
        s.set_initial_value(y0, 0)

        self._x = []
        self._sol = []

        s.integrate(end)

        sol = np.array(self._sol)

        soln = Eigenfunctions(self.params)
        soln.lamda_znd = self._x
        soln.u_real = sol[:, 0]
        soln.u_imag = sol[:, 1]
        soln.lamda_real = sol[:, 2]
        soln.lamda_imag = sol[:, 3]

        return soln

    def _rhs(self, lamda_znd, y):
        assert len(y) == 4
        pert = [y[0] + y[1]*1j, y[2] + y[3]*1j]
        alpha = self._alpha

        znd = self.compute_znd_solution(lamda_znd)

        # Just a sanity check.
        assert znd.lamda == lamda_znd

        d, sigma = self.d, self.sigma

        det = d**2 - znd.u * d
        A_inv = (1/det) * np.array([[-d, -sigma],
                                    [0, znd.u - d]])
        I_mat = np.eye(2)
        C = np.array([[znd.du_dx, 0],
                      [-znd.domega_du, -znd.domega_dlamda]])
        b = np.array([znd.du_dx, znd.dlamda_dx])
        coeff = -d / znd.omega
        tmp = coeff * A_inv.dot(-(alpha * I_mat + C).dot(pert) + alpha * b)

        rhs = [np.real(tmp[0]), np.imag(tmp[0]),
               np.real(tmp[1]), np.imag(tmp[1])]

        return rhs

    def _solout(self, x, y):
        self._x.append(x)
        self._sol.append(y.copy())

    def compute_znd_solution(self, lamda):
        k, d, q, theta = self.k, self.d, self.q, self.theta

        u = d + np.sqrt(d**2 - q*lamda)

        exponent = np.exp(theta*(np.sqrt(q)*u + q*lamda))
        omega = k * (1 - lamda) * exponent

        dlamda_dx = -omega / d

        du_dx = (q*k)/(2*d**2) * np.sqrt(1 - lamda) * exponent

        domega_du = theta * np.sqrt(q) * omega
        domega_dlamda = k * exponent * (theta * q * (1 - lamda) - 1)

        znd = ZNDSolution(params=self.params)
        znd.u = u
        znd.lamda = lamda
        znd.omega = omega
        znd.exponent = exponent
        znd.du_dx = du_dx
        znd.dlamda_dx = dlamda_dx
        znd.domega_du = domega_du
        znd.domega_dlamda = domega_dlamda

        return znd


class CarpetAnalyzer(object):
    """Analyze carpet of boundedness function `H` by considering its minima."""
    def __init__(self, alpha_re, alpha_im, H):
        assert len(H[:, 0]) == len(alpha_re)
        assert len(H[0, :]) == len(alpha_im)

        self._alpha_re = alpha_re
        self._alpha_im = alpha_im
        self._H = H

        idx = signal.argrelmin(H)
        ax_0 = []
        ax_1 = []

        # Check that idx contains minima along columns as well.
        for i in range(len(idx[0])):
            j = idx[0][i]
            k = idx[1][i]
            res = signal.argrelmin(H[j, :])

            if k == res:
                ax_0.append(j)
                ax_1.append(k)

        self._idx = (array(ax_0), array(ax_1))

    def print_minima(self):
        alpha_re = self._alpha_re
        alpha_im = self._alpha_im
        H = self._H
        idx = self._idx

        for i in range(len(idx[0])):
            x = alpha_re[idx[0][i]]
            y = alpha_im[idx[1][i]]
            h = log(1 + H[idx[0][i], idx[1][i]])

            msg = 'alpha_re = %.4f, alpha_im = %.4f, log(1 + |H|) = %.2f'
            print(msg % (x, y, h))

    def get_carpet_contour_plot(self, figsize):
        alpha_re = self._alpha_re
        alpha_im = self._alpha_im
        H = self._H
        idx = self._idx

        fig, ax = plt.subplots(1, 1, figsize=figsize)
        mappable = ax.contourf(alpha_re, alpha_im, log(1 + H.T), 20)

        for i in range(len(idx[0])):
            x = alpha_re[idx[0][i]]
            y = alpha_im[idx[1][i]]
            ax.plot(x, y, 'ro')

        ax.set_xlabel(r'$\alpha_\mathrm{re}$')
        ax.set_ylabel(r'$\alpha_\mathrm{im}$')

        plt.colorbar(mappable)
        plt.tight_layout(pad=0.1)

        return fig

    def get_carpet_3d_plot(self, figsize):
        alpha_re = self._alpha_re
        alpha_im = self._alpha_im
        H = self._H

        ALPHA_RE, ALPHA_IM = np.meshgrid(alpha_re, alpha_im)

        fig = plt.figure(figsize=figsize)
        ax = fig.gca(projection=Axes3D.name)
        ax.plot_surface(ALPHA_RE, ALPHA_IM, log(1 + H.T))

        return fig
