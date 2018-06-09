"""
Linearized problem based on the Fickett's model.

Fickett's model is a detonation-analogue model based on the one-dimensional
reactive Burgers' equation with one-step chemistry.

Fickett's model is described in [1]_.

References
----------

.. [1] Fickett W. Detonation in Miniature.
       American Journal of Physics, vol. 47, issue 12, pages 1050--1059.
       doi:10.1119/1.11973

"""

from .config import Config
from .reader import Reader

__all__ = [Config, Reader]
