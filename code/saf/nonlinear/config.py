import os
import shutil

from configparser import ConfigParser


class Config(object):
    """Base configuration class for nonlinear simulations.

    This class specifies configuration options that are required to conduct a
    simulation in the shock-attached frame irrespective of the problem
    at hand: for example, grid resolution or final time of integration, etc.

    """
    def __init__(self):
        self._options = {
            'simulation': dict(),
            'problem': dict()
        }

        self._options['simulation'] = {
            'n12': None,
            'final_time': None,
            'dt': None,
            'approximator': None,
            'approximator_type': 'cy',
            'weno_eps': 1e-6,
            'time_integrator': None,
            'plot_time_step': None,
            'play_animation': False,
            'io_format': 'ascii'
        }
        self._config_filename = None
        self._config_string = None

    @property
    def n12(self):
        """
        Number of numerical zones per unit length:
        """
        return self._options['simulation']['n12']

    @n12.setter
    def n12(self, value):
        if not isinstance(value, int):
            raise Exception('Invalid argument value')

        if value <= 0:
            raise Exception('Invalid argument value')

        self._options['simulation']['n12'] = value

    @property
    def final_time(self):
        return self._options['simulation']['final_time']

    @final_time.setter
    def final_time(self, value):
        if not float(value) >= 0.0:
            raise Exception('Invalid argument value')

        self._options['simulation']['final_time'] = value

    @property
    def dt(self):
        return self._options['simulation']['dt']

    @dt.setter
    def dt(self, value):
        if not float(value) >= 0.0:
            raise Exception('Invalid argument value')

        self._options['simulation']['dt'] = float(value)

    @property
    def approximator(self):
        return self._options['simulation']['approximator']

    @approximator.setter
    def approximator(self, value):
        choices = [
            'henrick-weno5js-lf',
            'henrick-weno5js-llf',
            'henrick-weno5m-lf',
            'henrick-weno5m-llf',
            'godunov',
            'godunov-minmod',
        ]

        if value in choices:
            self._options['simulation']['approximator'] = value
        else:
            msg = ('Value of the `approximator` parameter is incorrect. '
                   'Correct choices are: {}'.format(choices))
            raise Exception(msg)

    @property
    def approximator_type(self):
        return self._options['simulation']['approximator_type']

    @approximator_type.setter
    def approximator_type(self, value):
        choices = ['cy', 'py']

        if value in choices:
            self._options['simulation']['approximator_type'] = value
        else:
            msg = ('Value of the `approximator_type` parameter is incorrect. '
                   'Correct choices are: {}'.format(choices))
            raise ValueError(msg)

    @property
    def weno_eps(self):
        """
        Parameter for WENO interpolation. It is used in computation of
        WENO weights to avoid division by zero.
        Default value is 1e-6.

        """
        return self._options['simulation']['weno_eps']

    @weno_eps.setter
    def weno_eps(self, value):
        self._options['simulation']['weno_eps'] = value

    @property
    def time_integrator(self):
        """
        What time integrator to use. Possible choices:
        * tvdrk3 - TVD Runge-Kutta of third order of accuracy
        * dopri5 - Dormand-Prince 5(4) Runge-Kutta of fourth order of accuracy
        * rk65   - Runge-Kutta of fifth order of accuracy

        """
        return self._options['simulation']['time_integrator']

    @time_integrator.setter
    def time_integrator(self, value):
        choices = ['tvdrk3', 'dopri5', 'rk65']

        if value in choices:
            self._options['simulation']['time_integrator'] = value
        else:
            raise Exception(
                'Value of the `time_integrator` parameter is incorrect. '
                'Correct choices are: {}.'.format(choices))

    @property
    def plot_time_step(self):
        """
        Time step divider for profiles output. That is at every nth time step
        the profile of detonation wave will be saved to disk.  The smaller
        time step will give you an ability to create smoother animation.
        However, the size of output folder will increase, too.

        """
        return self._options['simulation']['plot_time_step']

    @plot_time_step.setter
    def plot_time_step(self, value):
        if isinstance(value, int):
            self._options['simulation']['plot_time_step'] = value
        else:
            raise Exception('Invalid argument value.')

    @property
    def play_animation(self):
        """
        Specify whether animation should be played during simulation.
        Optional parameter.
        If not specified, then the animation will not be played.

        """
        return self._options['simulation']['play_animation']

    @play_animation.setter
    def play_animation(self, value):
        if value in ['true', 'True', 1]:
            self._options['simulation']['play_animation'] = True
        elif value in ['false', 'False', 0]:
            self._options['simulation']['play_animation'] = False
        else:
            raise Exception('Unknown value for `play_animation`')

    @property
    def io_format(self):
        return self._options['simulation']['io_format']

    @io_format.setter
    def io_format(self, value):
        choices = ['ascii', 'numpy', 'hdf5']

        if value in choices:
            self._options['simulation']['io_format'] = value
        else:
            raise ValueError('Parameter `io_format` has incorrect value. '
                             'Correct values: {}'.format(choices))

    @property
    def extend(self):
        """Specify if solution can be extended.
        Optional parameter.
        If True, then solution can be extended.
        The logic of extension is actually depends on the Problem class that
        implements the logic.
        The Problem class can even ignore this property if needed.

        """
        return self._options['simulation']['extend']

    @extend.setter
    def extend(self, value):
        if value in ['true', 'True', 1]:
            self._options['simulation']['extend'] = True
        elif value in ['false', 'False', 0]:
            self._options['simulation']['extend'] = False
        else:
            raise Exception('Unknown value for `extend`. Must be of bool type')


    def from_file(self, config_filename=None, config_string=None):
        """Read configuration from file `config_filename`."""
        cp = ConfigParser()
        self._config_filename = config_filename
        cp.read(config_filename)

        self._process_parser(cp)

    def from_string(self, config_string):
        """Read configuration from string `config_string`."""
        cp = ConfigParser()
        self._config_string = config_string
        cp.read_string(config_string)

        self._process_parser(cp)

    def _process_parser(self, cp):
        sim_params = cp['simulation']
        self.n12 = int(sim_params['n12'])
        self.dt = float(sim_params['dt'])
        self.final_time = float(sim_params['final_time'])
        self.approximator = sim_params['approximator']
        self.weno_eps = float(sim_params['weno_eps'])
        self.time_integrator = sim_params['time_integrator']
        self.plot_time_step = int(sim_params['plot_time_step'])
        if 'play_animation' in sim_params:
            self.play_animation = sim_params['play_animation']

    def copy_to_output(self, outdir):
        self._validate()
        if self._config_filename is not None:
            shutil.copy2(self._config_filename, outdir)
        elif self._config_string is not None:
            fn = os.path.join(outdir, 'config.ini')
            with open(fn, 'w') as f:
                f.write(self._config_string)
        else:
            content = self.__str__()
            fn = os.path.join(outdir, 'config.ini')
            with open(fn, 'w') as f:
                f.write(content)

    def _validate(self):
        for k in ['simulation', 'problem']:
            d = self._options[k]
            assert type(d) == dict

            for key, val in d.items():
                if val is None:
                    msg = 'Parameter `{}` is not specified.'
                    raise Exception(msg.format(key))

    def __str__(self):
        self._validate()

        lines = [
            '[simulation]',
            '; Number of numerical zones on the grid per unit length.',
            'n12 = {}'.format(self.n12),
            '',
            '; Time step.',
            'dt = {}'.format(self.dt),
            '',
            '; Final time of computations.',
            'final_time = {}'.format(self.final_time),
            '',
            '; Parameter defining how flux derivatives are approximated.',
            'approximator = {}'.format(self.approximator),
            '',
            '; Use Python or Cython implementation of the approximator.',
            'approximator_type = {}'.format(self.approximator_type),
            '',
            '; Parameter for WENO interpolation. Default value is 1e-6.',
            'weno_eps = {}'.format(self.weno_eps),
            '',
            '; What time integrator to use.',
            'time_integrator = {}'.format(self.time_integrator),
            '',
            '; Time step divider for profiles output.',
            'plot_time_step = {}'.format(self.plot_time_step),
            '',
            '; Whether animation should be played during simulation. Default value is False.',
            'play_animation = {}'.format(self.play_animation),
            '',
            '; Input-output format.',
            'io_format = {}'.format(self.io_format)
        ]

        return '\n'.join(lines)
