#!/usr/bin/env python
r"""
Plot the carpet of the boundedness function :math:`$H(\alpha)$`.

"""
import numpy as np

from lib_normalmodes import CarpetAnalyzer

from helpers import FIGSIZE_NORMAL as FIGSIZE
from helpers import savefig

carpet_file = '_output/carpet.npz'

with np.load(carpet_file, 'r') as data:
    alpha_re = data['ALPHA_RE']
    alpha_im = data['ALPHA_IM']
    H = data['H']

analyzer = CarpetAnalyzer(alpha_re, alpha_im, H)
analyzer.print_minima()

fig = analyzer.get_carpet_contour_plot(FIGSIZE)
savefig('normal-modes-carpet.pdf')
