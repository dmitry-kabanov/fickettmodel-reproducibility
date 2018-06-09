from saf.nonlinear.config import Config as BaseConfig


class Config(BaseConfig):
    """Configuration for nonlinear simulations with Fickett model."""

    def __init__(self):
        super(Config, self).__init__()

        opts = {
            'lambda_tol': None,
            'q': None,
            'theta': None,
            'reaction_rate_version': 'v1',
            'f': 1.0,
            'ic_amplitude': 0.0,
            'ic_type': None,
            'truncation_coef': None,
        }
        self._options['problem'] = opts

    @property
    def lambda_tol(self):
        return self._options['problem']['lambda_tol']

    @lambda_tol.setter
    def lambda_tol(self, value):
        r"""
        Lambda tolerance, that is, the value :math:`\tau` such that
        the domain defined in :math:`\bar \lambda` variable is
        :math:`[0; 1-\tau]`.

        """
        value_cast = float(value)
        min_val, max_val = 1e-14, 1e-4
        if min_val <= value_cast <= max_val:
            self._options['problem']['lambda_tol'] = value_cast
        else:
            raise Exception(
                'Parameter `lambda_tol` must be in the range '
                '[{}, {}]'.format(min_val, max_val))

    @property
    def lamda_tol(self):
        return self._options['problem']['lambda_tol']

    @property
    def q(self):
        """Chemical reaction heat release."""
        return self._options['problem']['q']

    @q.setter
    def q(self, value):
        value_cast = float(value)
        if value_cast >= 0.0:
            self._options['problem']['q'] = value_cast
        else:
            raise Exception('Parameter `q` must be nonnegative.')

    @property
    def theta(self):
        return self._options['problem']['theta']

    @theta.setter
    def theta(self, value):
        value_cast = float(value)
        if value_cast >= 0.0:
            self._options['problem']['theta'] = value_cast
        else:
            raise Exception('Parameter `theta` must be nonnegative.')

    @property
    def reaction_rate_version(self):
        return self._options['problem']['reaction_rate_version']

    @reaction_rate_version.setter
    def reaction_rate_version(self, value):
        choices = ['v1', '1', 'v2', '2']
        if value in choices:
            self._options['problem']['reaction_rate_version'] = value
        else:
            msg = ('Value of the parameter `reaction_rate_version` '
                   'must be one of the {}.')
            raise Exception(msg.format(choices))

    @property
    def f(self):
        r"""Overdrive ratio math:`f = \left( D / D_{CJ} \right)^2`."""
        return self._options['problem']['f']

    @f.setter
    def f(self, value):
        value_cast = float(value)
        if value_cast >= 1.0:
            self._options['problem']['f'] = value_cast
        else:
            raise Exception('Parameter `f` must be greater or equal to 1.')

    @property
    def ic_amplitude(self):
        """Initial value of the perturbation of detonation speed."""
        return self._options['problem']['ic_amplitude']

    @ic_amplitude.setter
    def ic_amplitude(self, value):
        value_cast = float(value)
        if value_cast >= 0.0:
            v = value_cast
            self._options['problem']['ic_amplitude'] = v
        else:
            raise Exception('Parameter `ic_amplitude` must be positive.')

    @property
    def ic_type(self):
        """Type of the initial perturbation.
        pulse type is when the perturbation is supplied only to the shock
        point.
        gaussian type is when the perturbation is supplied as the gaussian
        profiles for all state variables with the Gaussian centered at the
        shock with maximum amplitude defined by initial_perturbation_amplitude
        and the Rankine--Hugoniot conditions.
        gaussian-in-the-middle type is when the Gaussian is specified somewhere
        in the middle of the domain.
        znd type is when the initial condition is a multiple of ZND solution.

        """
        return self._options['problem']['ic_type']

    @ic_type.setter
    def ic_type(self, value):
        choices = ['pulse', 'gaussian', 'gaussian-in-the-middle', 'znd']

        if value in choices:
            self._options['problem']['ic_type'] = value
        else:
            msg = ('Value of the parameter `ic_type` must be one of the {}.')
            raise Exception(msg.format(choices))

    @property
    def truncation_coef(self):
        """Fraction of ZND D, at which simulation should terminate."""
        return self._options['problem']['truncation_coef']

    @truncation_coef.setter
    def truncation_coef(self, value):
        if value >= 0.0:
            self._options['problem']['truncation_coef'] = value
        else:
            raise Exception('Truncation coefficient must be nonnegative.')

    def _process_parser(self, cp):
        super(Config, self)._process_parser(cp)
        problem_params = cp['problem']

        self.lambda_tol = float(problem_params['lambda_tol'])
        self.q = float(problem_params['q'])
        self.theta = float(problem_params['theta'])
        self.f = float(problem_params['f'])
        self.ic_amplitude = float(problem_params['ic_amplitude'])
        self.ic_type = problem_params['ic_type']
        self.truncation_coef = float(problem_params['truncation_coef'])

    def __str__(self):
        base_content = super(Config, self).__str__()

        lines = [
            '',
            '[problem]',
            '; Lambda tolerance.',
            'lambda_tol = {}'.format(self.lambda_tol),
            '',
            '; Heat release.',
            'q = {}'.format(self.q),
            '',
            '; Activation energy.',
            'theta = {}'.format(self.theta),
            '',
            '; Overdrive ratio. Default value is 1.0.',
            'f = {}'.format(self.f),
            '',
            '; Initial condition: perturbation amplitude.',
            'ic_amplitude = {}'.format(self.ic_amplitude),
            '',
            '; Initial condition: type of perturbation.',
            'ic_type = {}'.format(self.ic_type),
            '',
            '; Truncation coef.',
            'truncation_coef = {}'.format(self.truncation_coef),
            '',
        ]

        content = '\n'.join(lines)

        return base_content + content
