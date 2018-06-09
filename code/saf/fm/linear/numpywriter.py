import os

import numpy as np

from .asciiwriter import ASCIIWriter


class NumpyWriter(ASCIIWriter):
    """Writer of the simulation output for linear Fickett--Faria model.

    This writer writes simulation data in the Numpy format [1]_.

    References
    ----------
    [1] https://docs.scipy.org/doc/numpy/neps/npy-format.html

    """

    def close(self):
        super(NumpyWriter, self).close()

        npz_filename = os.path.join(self._output, 'detonation-velocity.npz')
        t, d = np.loadtxt(self._filename, unpack=True)

        np.savez(npz_filename, t=t, d=d)
        os.remove(self._filename)
