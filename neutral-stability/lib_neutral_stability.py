import os

import numpy as np

from saf.action import solve
from saf.action import postprocess
from saf.ffm.linear import Config
from saf.ffm.linear import Reader
from saf.ffm.linear import ZNDSolverError

from saf.linear.postprocessor import CannotConstructHankelMatrix


# Format for floating-point numbers.
FMT_UNSIGNED = '22.16e'
FMT_SIGNED = '+22.16e'

POSITIVE_INDEFINITE_RATE = +9.999999999999+00
NEGATIVE_INDEFINITE_RATE = -9.999999999999+00


def find_critical_e_act(params, outdir, tol, mode_number=0):
    assert 'n12' in params, 'Parameter `n12` is missing'
    assert 'q' in params, 'Parameter `q` is missing'
    assert 'theta_lower' in params, 'Parameter `theta_lower` is missing'
    assert 'theta_upper' in params, 'Parameter `theta_upper` is missing'

    e_act_a_new, e_act_b_new = params['theta_lower'], params['theta_upper']
    assert e_act_a_new < e_act_b_new, '`theta_lower` >= `theta_upper`'

    # Set dummy initial values for growth rates.
    gr_a, gr_b = -1.0, 1.0

    print('Find crit. e_act for q={:{fmt}}'.format(params['q'],
                                                   fmt=FMT_UNSIGNED))
    print('Mode number is {}'.format(mode_number))

    a_list, b_list = [], []

    i = 0
    while abs(gr_a) > tol and abs(gr_b) > tol:
        i += 1

        e_act_a = e_act_a_new
        e_act_b = e_act_b_new

        if np.allclose(e_act_a, e_act_b, rtol=1e-10):
            raise Exception('ERROR: '
                            'Boundaries of the range for activation energy '
                            'are the same for 10 digits. '
                            'Aborting.')

        print('Iteration {}'.format(i))
        print('    e_act_a = {:{fmt}}, e_act_b = {:{fmt}}'.format(
            e_act_a, e_act_b, fmt=FMT_UNSIGNED))

        current_params = {
            'n12': params['n12'],
            'q': params['q'],
            'e_act_a': e_act_a,
            'e_act_b': e_act_b,
        }
        eig_a, eig_b = _get_abs_growth_rates(current_params, outdir,
                                             mode_number=mode_number)
        gr_a, freq_a = eig_a
        gr_b, freq_b = eig_b

        if gr_a is None:
            gr_a = NEGATIVE_INDEFINITE_RATE
        if gr_b is None:
            gr_b = POSITIVE_INDEFINITE_RATE

        # Hack that fixes a weird situation when for the lower bound of
        # the activation energy an unstable mode is found sometimes.
        if e_act_a == params['theta_lower'] and gr_a > 0.0:
            gr_a = NEGATIVE_INDEFINITE_RATE

        gr_msg = '    growth_rate_a = {:{fmt}}, growth_rate_b = {:{fmt}}'
        print(gr_msg.format(gr_a, gr_b, fmt=FMT_SIGNED))

        a_list.append((e_act_a, gr_a))
        b_list.append((e_act_b, gr_b))

        if gr_a < 0.0 and gr_b > 0.0:
            e_act_c = 0.5 * (e_act_a + e_act_b)
            if abs(gr_a) > abs(gr_b):
                e_act_a_new = e_act_c
            else:
                e_act_b_new = e_act_c
        elif gr_a > 0.0 and gr_b > 0.0:
                while len(a_list):
                    e, r = a_list.pop()
                    if r < 0.0:
                        a_list.append((e, r))
                        break
                e_act_a_new = 0.5 * e + 0.5 * e_act_a
                e_act_b_new = e_act_a
        elif gr_a < 0.0 and gr_b < 0.0:
                while len(b_list):
                    e, r = b_list.pop()
                    if r > 0.0:
                        b_list.append((e, r))
                        break
                e_act_a_new = e_act_b
                e_act_b_new = 0.5 * e + 0.5 * e_act_b
        else:
            raise Exception('ERROR: Unhandled situation')

        assert e_act_a_new < e_act_b_new, \
            ('ERROR: e_act_a must be smaller than e_act_b, '
             'e_act_a={}, e_act_b={}'.format(e_act_a_new, e_act_b_new))

    if abs(gr_a) < abs(gr_b):
        (e_act_crit, gr_crit, freq_crit) = (e_act_a, gr_a, freq_a)
    else:
        (e_act_crit, gr_crit, freq_crit) = (e_act_b, gr_b, freq_b)

    final_msg = 'e_act = {:{fmt}}, rate = {:{fmt}}, freq = {:{fmt_unsigned}}'
    print(final_msg.format(e_act_crit, gr_crit, freq_crit,
                           fmt_unsigned=FMT_UNSIGNED, fmt=FMT_SIGNED))

    return (e_act_crit, gr_crit, freq_crit)


def _get_abs_growth_rates(params, outdir, mode_number=0):
    n12 = params['n12']
    q = params['q']
    a, b = params['e_act_a'], params['e_act_b']

    d_a = 'theta={:{fmt}}'.format(a, fmt=FMT_UNSIGNED)
    d_b = 'theta={:{fmt}}'.format(b, fmt=FMT_UNSIGNED)
    outdir_a = os.path.join(outdir, d_a)
    outdir_b = os.path.join(outdir, d_b)

    try:
        if not os.path.exists(outdir_a):
            c_a = _get_config(n12, q, a)
            os.mkdir(outdir_a)
            solve('linear', c_a, outdir_a, log_to_file=True)
            postprocess(outdir_a, savetofile=True)

        r_a = Reader(outdir_a)
        stab_info_a = r_a.get_stability_info()
        mode = stab_info_a[mode_number]
        if type(mode) is list:
            mode = mode[-1]
        rate_a = mode['growth_rate']
        freq_a = mode['frequency']
    except CannotConstructHankelMatrix:
        rate_a = POSITIVE_INDEFINITE_RATE
        freq_a = None
    except ZNDSolverError:
        rate_a = POSITIVE_INDEFINITE_RATE
        freq_a = None
    except Exception:
        rate_a = None
        freq_a = None

    try:
        if not os.path.exists(outdir_b):
            c_b = _get_config(n12, q, b)
            os.mkdir(outdir_b)
            solve('linear', c_b, outdir_b, log_to_file=True)
            postprocess(outdir_b, savetofile=True)

        r_b = Reader(outdir_b)
        stab_info_b = r_b.get_stability_info()
        mode = stab_info_b[mode_number]
        if type(mode) is list:
            mode = mode[-1]
        rate_b = mode['growth_rate']
        freq_b = mode['frequency']
    except CannotConstructHankelMatrix:
        rate_b = POSITIVE_INDEFINITE_RATE
        freq_b = None
    except ZNDSolverError:
        rate_b = POSITIVE_INDEFINITE_RATE
        freq_b = None
    except Exception as e:
        raise e
        rate_b = None
        freq_b = None

    return ((rate_a, freq_a), (rate_b, freq_b))


def _get_config(n12, q, theta):
    c = Config()
    c.n12 = n12
    c.dt = 0.005
    c.final_time = 10.0
    c.approximator = 'henrick-upwind5-lf'
    c.time_integrator = 'dopri5'
    c.io_format = 'numpy'
    c.plot_time_step = 0
    c.play_animation = False

    c.lambda_tol = 1e-6
    c.q = q
    c.theta = theta
    c.reaction_rate_version = 'v2'
    c.f = 1
    c.ic_amplitude = 1e-10
    c.ic_type = 'znd'
    c.truncation_coef = 1e6

    return c
