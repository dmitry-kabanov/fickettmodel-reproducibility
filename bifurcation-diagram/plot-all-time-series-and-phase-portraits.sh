#/usr/bin/env bash

# First argument is resolution N_1/2, second is activation energy theta.
./plot-time-series-and-phase-portrait.py 1280 0.950 --save
./plot-time-series-and-phase-portrait.py 1280 1.000 --save
./plot-time-series-and-phase-portrait.py 1280 1.004 --save
./plot-time-series-and-phase-portrait.py 1280 1.055 --with-inset --save
./plot-time-series-and-phase-portrait.py 1280 1.065 --with-inset --save
./plot-time-series-and-phase-portrait.py 1280 1.089 --with-inset --save
