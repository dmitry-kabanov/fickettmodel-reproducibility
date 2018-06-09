import logging
import os

import numpy as np

try:
    import h5py
except ImportError:
    raise Exception('Cannot import h5py module')

from .solution import Solution


class HDF5Writer(object):
    """Writer of the simulation output in the HDF5 format.

    Parameters
    ----------
    config : Config
        Configuration object.
    grid : array_like
        Grid.
    znd : ZNDSolver
        ZND solution.
    outdir : str
        Path to the directory to which simulation results should be written.

    """

    def __init__(self, config, grid, dx, znd, outdir):
        self._logger = logging.getLogger(__name__)
        self._config = config
        self._grid = grid
        self._dx = dx
        self._znd = znd

        self._output = outdir
        self._profiles_path = self._output + '/profiles'

        if not os.path.isdir(self._output):
            os.mkdir(self._output)

        if not os.path.isdir(self._profiles_path):
            os.mkdir(self._profiles_path)

        filename_det_vel = os.path.join(self._output, 'detonation-velocity.h5')
        self._file_det_vel = h5py.File(filename_det_vel, 'w')

        self._det_vel_dataset = self._file_det_vel.create_dataset(
            'detonation-velocity', dtype=np.float64,
            shape=(1000, 2), maxshape=(None, 2),
            chunks=(1000, 2), compression='gzip')

        self._counter = 0
        self._buffer_size = 1000
        self._buffer = np.empty((self._buffer_size, 2))

    def save_configuration(self):
        self._config.copy_to_output(self._output)

        znd = self._znd
        filename = os.path.join(self._output, 'computed-values.txt')
        with open(filename, 'w') as f:
            f.write('dx = {:24.16e}\n'.format(self._dx))
            f.write('reaction_length = {rl:24.16e}\n'.format(
                rl=self._znd.reaction_length))
            f.write('k = {k:24.16e}\n'.format(k=znd.k))
            f.write('d_cj = {d:24.16e}\n'.format(d=znd.dcj))
            f.write('d_znd = {d:24.16e}\n'.format(d=znd.d))

    def save_znd_solution(self):
        filename = os.path.join(self._output, 'znd-solution.txt')

        header_lines = []
        header_lines.append('ZND solution.')
        header_lines.append('Columns are: spatial coordinate; '
                            'specific volume; density;')
        header_lines.append('flow velocity in lab frame; pressure; '
                            'reaction progress variable.')
        header = '\n'.join(header_lines)

        data = np.empty((len(self._grid), 3), order='F')
        data[:, 0] = self._grid
        data[:, 1] = self._znd.u
        data[:, 2] = self._znd.lamda

        np.savetxt(filename, data, fmt='%24.16e', header=header)

    def save(self, time_step, time, soln_data):
        self.save_detonation_speed(time_step, time, soln_data)

        if self._config.plot_time_step == 0:
            return

        if time_step % self._config.plot_time_step == 0:
            self.save_profile(time_step, time, soln_data)

        # Output profiles if we reached the end of simulation.
        if time == self._config.final_time:
            self.save_profile(time_step, time, soln_data, force=True)

    def save_detonation_speed(self, time_step, time, soln_data):
        det_speed = soln_data[-1]
        buffer_size = self._buffer_size
        _buffer = self._buffer
        dset = self._det_vel_dataset

        _buffer[self._counter % buffer_size, :] = (time, det_speed)

        if self._counter % buffer_size == buffer_size - 1:
            idx_1 = self._counter - buffer_size + 1
            idx_2 = self._counter + 1
            dset[idx_1: idx_2, :] = _buffer
            dset.resize(dset.shape[0] + buffer_size, axis=0)

        self._counter += 1

    def save_profile(self, time_step, time, soln_data, force=False):
        if force:
            profile_filename = '/profile-' + str(time_step) + '.txt'
            profile_filename = self._profiles_path + profile_filename
            h1 = 'Columns: x, rho, u, p, lamda'
            h2 = 'time_step {}\n'.format(time_step)
            h3 = 'time {0:24.16e}'.format(time)
            header = h1 + h2 + h3
            data = np.empty((len(self._grid), 3))
            solution = Solution(soln_data)
            data[:, 0] = self._grid
            data[:, 1] = solution.u
            data[:, 2] = solution.lamda
            np.savetxt(profile_filename, data, fmt='%24.16e', header=header)

    def close(self):
        buffer_size = self._buffer_size
        _buffer = self._buffer
        dset = self._det_vel_dataset

        if self._counter <= dset.shape[0] - 1:
            idx_1 = self._counter - self._counter % buffer_size
            idx_2 = self._counter + 1
            idx_3 = 0
            idx_4 = self._counter % buffer_size + 1
            dset[idx_1:idx_2, :] = _buffer[idx_3:idx_4, :]
            dset.resize(self._counter, axis=0)

        self._file_det_vel.close()
