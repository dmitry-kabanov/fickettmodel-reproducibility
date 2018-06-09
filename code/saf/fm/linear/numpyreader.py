"""Description of the class fickettmodel.euler1d.linear.asciireader."""
import numpy as np
import os

from .asciireader import ASCIIReader


class NumpyReader(ASCIIReader):
    """Read the results of the simulation.

    Works with the results written in Numpy format.

    """
    def get_time_and_detonation_velocity(self):
        """Read detonation velocity vs time from simulation results.

        Returns
        -------
        t: ndarray
            Array with time data.
        d: ndarray
            Array with detonation velocity data.

        """
        fn = os.path.join(self._results_dir, 'detonation-velocity.npz')
        data = np.load(fn)
        t = data['t']
        d = data['d']

        return t, d
