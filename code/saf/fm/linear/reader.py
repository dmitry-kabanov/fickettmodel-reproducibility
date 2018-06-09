import logging
import os

from .asciireader import ASCIIReader
from .numpyreader import NumpyReader

_hdf5_enabled = False

try:
    from .hdf5reader import HDF5Reader
    _hdf5_enabled = True
except ImportError:
    logger = logging.getLogger(__name__)
    logger.warning('Reading HDF5 format is not available as '
                   '`h5py` module is not installed')


class Reader(object):
    """Read the results of the simulation with the Fickett's model.

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
            raise ReaderError('Directory does not exist')

        self._results_dir = results_dir

        det_vel_file_ascii = os.path.join(self._results_dir,
                                          'detonation-velocity.txt')
        det_vel_file_numpy = os.path.join(self._results_dir,
                                          'detonation-velocity.npz')
        det_vel_file_hdf5 = os.path.join(self._results_dir,
                                         'detonation-velocity.h5')

        if os.path.exists(det_vel_file_ascii):
            self._reader = ASCIIReader(results_dir)
        elif os.path.exists(det_vel_file_numpy):
            self._reader = NumpyReader(results_dir)
        elif os.path.exists(det_vel_file_hdf5) and _hdf5_enabled:
            self._reader = HDF5Reader(results_dir)
        else:
            raise ReaderError('Unknown format')

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

    def get_stability_info(self):
        """Read file with stability info for time series of detonation speed.

        Returns
        -------
        eigvals : list
            List with eigenvalues. Each element is a dictionary
            with keys {'growth_rate', 'frequency'}.

        Raises
        ------
        Exception
            If the file with stability information cannot be read.

        """
        eigvals = []

        fit_file = os.path.join(self._results_dir, 'stability.txt')

        if not os.path.isfile(fit_file):
            raise ReaderError("Cannot find file 'stability.txt'.")

        with open(fit_file, 'r') as f:
            for line in f:
                # Skip file header.
                if line.startswith('#'):
                    continue
                # Stop when meeting the sentinel of the eigenvalues list.
                if line.startswith('---'):
                    break
                chunks = line.split()
                gr = float(chunks[0])
                fr = float(chunks[1])

                if len(eigvals):
                    prev_eig = eigvals[-1]

                    if type(prev_eig) is dict:
                        if fr == eigvals[-1]['frequency']:
                            eig_1 = eigvals.pop()
                            eig_2 = {'growth_rate': gr, 'frequency': fr}
                            eigs = [eig_1, eig_2]
                            eigvals.append(eigs)
                        else:
                            eig = {'growth_rate': gr, 'frequency': fr}
                            eigvals.append(eig)
                    elif type(prev_eig) is list:
                        if fr == prev_eig[-1]['frequency']:
                            eigs = eigvals.pop()
                            eig_2 = {'growth_rate': gr, 'frequency': fr}
                            eigs.append(eig_2)
                            eigvals.append(eigs)
                        else:
                            eig = {'growth_rate': gr, 'frequency': fr}
                            eigvals.append(eig)
                    else:
                        raise Exception('Cannot parse stability.txt')
                else:
                    # Should be used only for the first line.
                    eig = {'growth_rate': gr, 'frequency': fr}
                    eigvals.append(eig)

        return eigvals


class ReaderError(Exception):
    pass
