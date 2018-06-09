#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np

from lib_normalmodes import CarpetAnalyzer

from helpers import FIGSIZE_NORMAL as figsize
from helpers import savefig

carpet_file = '_output/carpet.npz'

with np.load(carpet_file, 'r') as data:
    alpha_re = data['ALPHA_RE']
    alpha_im = data['ALPHA_IM']
    H = data['H']

analyzer = CarpetAnalyzer(alpha_re, alpha_im, H)
analyzer.print_minima()

fig_1 = analyzer.get_carpet_contour_plot(figsize)
savefig('normal-modes-carpet.pdf')

# fig_2 = analyzer.get_carpet_3d_plot(figsize)
# savefig('normal-modes-carpet-3d.pdf')
