import logging
import os

from .asciireader import ASCIIReader
from .numpyreader import NumpyReader

_hdf5_enabled = False

try:
    import h5py
    _hdf5_enabled = True
    from .hdf5reader import HDF5Reader
except ImportError:
    logger = logging.getLogger(__name__)
    logger.warning('Reading HDF5 format is not available as '
                   '`h5py` module is not installed')


class Reader(object):
    """Read the results of the nonlinear simulation with the Fickett's model.

    This class acts as a facade for the readers of different formats such that
    the user could be abstracted from dealing with the concrete format.

    Currently, the check of the simulation format is done by checking the
    extension of the `detonation-velocity` file.

    Parameters
    ----------
    results_dir : str
        Path to the directory with simulation results.

    """

    def __init__(self, results_dir):
        if not os.path.exists(results_dir):
            raise ValueError('Directory does not exist')

        self._results_dir = results_dir

        det_vel_file_ascii = os.path.join(self._results_dir,
                                          'detonation-velocity.txt')
        det_vel_file_numpy = os.path.join(self._results_dir,
                                          'detonation-velocity.npz')
        det_vel_file_hdf5 = os.path.join(self._results_dir,
                                         'detonation-velocity.h5')

        if os.path.exists(det_vel_file_ascii):
            self._reader = ASCIIReader(results_dir)
        if os.path.exists(det_vel_file_numpy):
            self._reader = NumpyReader(results_dir)
        elif os.path.exists(det_vel_file_hdf5):
            self._reader = HDF5Reader(results_dir)
        else:
            raise Exception('Unknown format')

    def get_computed_values(self):
        return self._reader.get_computed_values()

    def get_time_and_detonation_velocity(self):
        """Read detonation velocity vs time from simulation results.

        Returns
        -------
        t: ndarray
            Array with time data
        d: ndarray
            Array with detonation velocity data

        """
        return self._reader.get_time_and_detonation_velocity()

    def get_time_and_normalized_detonation_velocity(self):
        """Read detonation velocity vs time from simulation results.

        Returns
        -------
        t: ndarray
            Array with time data.
        d_normalized: ndarray
            Array with normalized detonation velocity data.

        """
        return self._reader.get_time_and_normalized_detonation_velocity()

    def get_znd_data(self):
        return self._reader.get_znd_data()
