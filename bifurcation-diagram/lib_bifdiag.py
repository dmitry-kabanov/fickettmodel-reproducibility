"""
Library of functions for extracting bifurcation data from simulation data.

"""
import os

import numpy as np

from scipy import signal


def get_bifurcation_data(n12, start_time, comparator, order,
                         output_dir='_output', cache_dir='_output-cache'):
    params = {
        'n12': n12,
        'start_time': start_time,
        'comparator': comparator,
        'order': order,
        'output_dir': output_dir,
        'cache_dir': cache_dir,
        'outdir': os.path.join(output_dir, 'N12=%04d' % n12)
    }

    if not os.path.isdir(params['cache_dir']):
        msg = 'Directory `%s` does not exist' % params['cache_dir']
        raise FileNotFoundError(msg)

    cache_filename = get_bif_data_filename(params)

    if os.path.isfile(cache_filename):
        theta, bif_data = load_bifurcation_data(params)
    else:
        if not os.path.isdir(params['outdir']):
            msg = 'Directory `%s` does not exist' % params['outdir']
            raise FileNotFoundError(msg)

        theta, D = get_simulation_data(params)
        extrema = extract_bifurcation_data(D, params)
        save_bifurcation_data((theta, extrema), params)
        theta, bif_data = load_bifurcation_data(params)

    return theta, bif_data


def get_simulation_data(params):
    """Get simulation data."""
    outdir = params['outdir']
    n12 = params['n12']
    cache_dir = params['cache_dir']
    start_time = params['start_time']

    cache_file = 'simulation-data-N12={:04d}-start_time={:d}.npz'
    cache_file = cache_file.format(n12, start_time)
    cache_file = os.path.join(cache_dir, cache_file)

    # If there is cache file with simulation data, then use data from it.
    if os.path.isfile(cache_file):
        with np.load(cache_file) as data:
            theta = data['theta']
            D = data['D']

        return theta, D

    dir_list = os.listdir(outdir)
    dir_list.sort()

    theta_list = []
    dw_list = []

    for i, dirname in enumerate(dir_list[:]):
        if not dirname.startswith('theta'):
            continue

        fn = os.path.join(outdir, dirname, 'detonation-velocity.npz')

        if i % 10 == 0:
            print(dirname)

        with np.load(fn) as data:
            t, d = data['t'], data['d']

        tw = t[t >= start_time]
        dw = d[t >= start_time]

        dw_list.append(dw)

        chunks = dirname.split('=')
        theta = float(chunks[1])
        theta_list.append(theta)

        del t, d, tw, dw

    assert len(theta_list) > 1, ('No simulation data was found in the '
                                 'directory `%s`'.format(outdir))

    assert len(dw_list) == len(theta_list)

    theta_array = np.array(theta_list)
    dw_array = np.array(dw_list)

    np.savez(cache_file, theta=theta_array, D=dw_array)

    return theta_array, dw_array


def extract_bifurcation_data(sim_data, params):
    """Save bifurcation data to disk to use them later."""
    comparator = params['comparator']
    order = params['order']

    if comparator == 'maxima':
        comparator_func = signal.argrelmax
    elif comparator == 'minima':
        comparator_func = signal.argrelmin
    else:
        raise ValueError('Comparison is either maxima or minima')

    data = []

    for dw in sim_data:
        indices = comparator_func(dw, order=order)[0]

        # Remove first and last indices as they could give false extrema.
        indices = indices[1:-1]

        extrema = dw[indices]
        data.append(extrema)

    return data


def save_bifurcation_data(bif_data, params):
    cache_file = get_bif_data_filename(params)
    np.savez(cache_file, theta=bif_data[0], extrema=bif_data[1])


def load_bifurcation_data(params):
    cache_file = get_bif_data_filename(params)
    with np.load(cache_file) as data:
        theta = data['theta']
        extrema = data['extrema']

    return theta, extrema


def get_bif_data_filename(params):
    n12 = params['n12']
    comparator = params['comparator']
    order = params['order']
    start_time = params['start_time']
    cache_dir = params['cache_dir']

    filename = 'bif-data-N12=%04d-%s-order=%d-start_time=%d.npz'
    filename = filename % (n12, comparator, order, start_time)
    filename = os.path.join(cache_dir, filename)

    return filename
