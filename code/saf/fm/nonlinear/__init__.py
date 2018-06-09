"""
Package `fm.nonlinear`.

`fm` stands for "Fickett's model".

Fickett's model is detonation-analogue model based on one-dimensional reactive
Burgers' equation with one-step chemistry.

"""

from .config import Config
from .reader import Reader

__all__ = [Config, Reader]
