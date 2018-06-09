import logging
import os

import numpy as np

_hdf5_enabled = False

try:
    import h5py
    _hdf5_enabled = True
except ImportError:
    logger = logging.getLogger(__name__)
    logger.warning('Reading HDF5 format is not available as '
                   '`h5py` module is not installed')


class Reader(object):
    """Generic reader that reads time series of detonation velocity.

    Parameters
    ----------
    results_dir : str
        Path to the directory with simulation results.

    """

    def __init__(self, results_dir):
        if not os.path.exists(results_dir):
            raise ValueError('Directory does not exist')

        self._results_dir = results_dir

    def get_time_and_detonation_velocity(self):
        det_vel_file_ascii = os.path.join(self._results_dir,
                                          'detonation-velocity.txt')
        det_vel_file_numpy = os.path.join(self._results_dir,
                                          'detonation-velocity.npz')
        det_vel_file_hdf5 = os.path.join(self._results_dir,
                                         'detonation-velocity.h5')

        if os.path.exists(det_vel_file_ascii):
            data = np.genfromtxt(det_vel_file_ascii)
            assert(data.shape[1] == 2), \
                'Detonation velocity file must have two columns'
            t = data[:, 0]
            d = data[:, 1]
        elif os.path.exists(det_vel_file_numpy):
            data = np.load(det_vel_file_numpy)
            t = data['t']
            d = data['d']
        elif os.path.exists(det_vel_file_hdf5):
            fh = h5py.File(det_vel_file_hdf5, 'r')

            t = fh['detonation-velocity'][:, 0]
            d = fh['detonation-velocity'][:, 1]
        else:
            raise Exception('Unknown format')

        return t, d

    @property
    def outdir(self):
        return self._results_dir
