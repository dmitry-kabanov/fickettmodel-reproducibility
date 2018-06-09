"""Description of the class HDF5Reader."""
import os

import numpy as np
import h5py


class HDF5Reader(object):
    """Read the results of the simulation.

    Works with the results written as text files.

    Parameters
    ----------
    results_dir: str
        Path to the directory with simulation results.

    """
    def __init__(self, results_dir):
        if not os.path.exists(results_dir):
            raise Exception('Not a directory')

        self._results_dir = results_dir
        self._znd_data = None

    def get_computed_values(self):
        results_dir = self._results_dir
        with open(os.path.join(results_dir, 'computed-values.txt')) as f:
            for line in f:
                chunks = line.split('=')
                par = chunks[0].strip()
                val = chunks[1].strip()
                if par == 'reaction_length':
                    reaction_length = float(val)
                elif par == 'k':
                    k = float(val)
                elif par == 'd_cj':
                    dcj = float(val)
                elif par == 'd_znd':
                    d_znd = float(val)
                else:
                    raise Exception('Unknown parameter name')

        result = {
            'reaction_length': reaction_length,
            'k': k,
            'd_cj': dcj,
            'd_znd': d_znd
        }

        return result

    def get_time_and_detonation_velocity(self):
        """Read detonation velocity vs time from simulation results.

        Returns
        -------
        t: ndarray
            Array with time data
        d: ndarray
            Array with detonation velocity data

        """
        fn = os.path.join(self._results_dir, 'detonation-velocity.h5')
        fh = h5py.File(fn, 'r')

        t = fh['detonation-velocity'][:, 0]
        d = fh['detonation-velocity'][:, 1]

        return t, d

    def get_time_and_normalized_detonation_velocity(self):
        """Read detonation velocity vs time from simulation results.

        Returns
        -------
        t: ndarray
            Array with time data.
        d_normalized: ndarray
            Array with normalized detonation velocity data.

        """
        comp_vals = self.get_computed_values()
        t, d = self.get_time_and_detonation_velocity()
        d_normalized = (comp_vals['d_znd'] + d) / comp_vals['d_znd']

        return t, d_normalized

    # def get_profile(self, time_step):
    #     """Read profile data from simulation results.

    #     Parameters
    #     ----------
    #     time_step : int
    #         Time step number.

    #     Returns
    #     -------
    #     t, x, u, lamda, omega: array_like
    #         Time, grid, velocity, reaction progress variable, reaction rate,
    #         respectively.

    #     """
    #     fn = 'profile-' + str(time_step) + '.txt'
    #     full_fn = os.path.join(results_dir, 'profiles', fn)

    #     with open(full_fn, 'r') as f:
    #         for line in f:
    #             if line.startswith('# time '):
    #                 chunks = line.split()
    #                 t = float(chunks[2].strip())

    #     data = np.genfromtxt(full_fn)
    #     x = data[3:, 0]
    #     u = data[3:, 1]
    #     lamda = data[3:, 2]
    #     omega = np.zeros_like(lamda)
    #     print('Hardcoded stripping off of ghost points on the left boundary')

    #     # config_filename = os.path.join(results_dir, 'config.ini')
    #     # c = Config(config_filename)
    #     # q = c.q
    #     # k = computed_values['k']
    #     # theta = k * np.exp * (theta * (u + q * lamda))
    #     # omega =

    #     return t, x, u, lamda, omega


    # def get_final_profile(self):
    #     """Read final profile data from simulation results.

    #     Returns
    #     -------
    #     t : float
    #         Simulation time for the final profile.
    #     x, u, lamda, omega : array_like
    #         Grid, velocity, reaction progress variable, reaction rate.

    #     """
    #     last_time_step = get_final_profile_time_step(results_dir)

    #     return get_profile(results_dir, last_time_step)

    # def get_profiles_time_steps(self):
    #     """Return a sorted array of time steps for which profiles were written.

    #     Precisely, profiles subdirectory of the `results_dir` is read and time
    #     steps of the profiles that were written during simulation are returned.

    #     Parameters
    #     ----------
    #     results_dir : str
    #         Path to the directory with simulation results.

    #     Returns
    #     -------
    #     time_steps : ndarray of int
    #         Sorted array of the time steps for which profiles were saved during
    #         simulation.

    #     """
    #     profiles_dir = os.path.join(results_dir, 'profiles')

    #     files_list = os.listdir(profiles_dir)

    #     time_steps = []

    #     for i, d in enumerate(files_list):
    #         ts = int(d.lstrip('profile-').rstrip('.txt'))
    #         time_steps.append(ts)

    #     time_steps.sort()

    #     return np.array(time_steps, dtype=np.int)


    def get_final_profile_time_step(results_dir):
        """Return time step of the final profile generated during simulation.

        This profile always exists, because it is written in the end of the
        simulation unconditionally.

        Parameters
        ----------
        results_dir : str
            Path to the directory with simulation results.

        Returns
        -------
        int
            Last time step.

        """

        time_steps = self.get_profiles_time_steps()

        return time_steps[-1]

    def get_znd_data(self):
        if self._znd_data is None:
            filename = os.path.join(self._results_dir, 'znd-solution.txt')
            self._znd_data = np.loadtxt(filename)

        result = {
            'x': self._znd_data[:, 0],
            'v': self._znd_data[:, 1],
            'rho': self._znd_data[:, 2],
            'u_lab': self._znd_data[:, 3],
            'p': self._znd_data[:, 4],
            'lamda': self._znd_data[:, 5],
        }

        return result

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
            raise ASCIIReaderError("Cannot find file 'stability.txt'.")

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


class ASCIIReaderError(Exception):
    pass

