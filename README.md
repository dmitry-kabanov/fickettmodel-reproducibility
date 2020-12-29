![Link to the latest release on Zenodo.org](https://zenodo.org/badge/DOI/10.5281/zenodo.1297175.svg)

# Reproducibility package for the paper on the Fickett model

This is a reproducibility repository for the paper
[*A minimal hyperbolic system for unstable shock waves*][1]
on the Fickett model published in *Communications in Nonlinear Science and Numerical Simulation*
and authored by Dmitry Kabanov (me) and Aslan Kasimov.

[1]: https://doi.org/10.1016/j.cnsns.2018.10.022

# Installation
This package was developed under Ubuntu 16.04 and should work under other
flavors of Unix without any modification (macOS, Centos, Fedora, and so on).
Using this package under Windows operating system may or may not work as it
depends on `make` utility.

**Important**. Make sure that you have Git LFS installed and initialized with
`git lfs install`.

To be able to run the scripts in this repository, you need to clone it:

    git clone --depth=1 git@github.com:dmitry-kabanov/fickettmodel-reproducibility.git

and change current directory to the repository directory:

    cd fickettmodel-reproducibility

## Dependencies

Besides, you need Python along with several scientific libraries, such as
NumPy, SciPy, and Matplotlib.
We recommend to use Anaconda Python distribution 5.0 to achieve this, as we
used it ourselves for development of this package.
It can be downloaded from `https://repo.continuum.io/archive/`.
Alternatively, you can get Python and the libraries from other places.
In this case, you need Python 3.6.3, NumPy 1.13.3, SciPy 0.19.1, and Matplotlib
2.1.0, which can be installed in a `conda` environment with the command

    conda create -n ficketmodel-reproducibility \
        "python==3.6.3" \
        "numpy==1.13.3" \
        "scipy==0.19.1" \
        "matplotlib==2.1.0" \
        pyqt

and then activated with the command

    conda activate fickettmodel-reproducibility

# Usage

To generate assets (figures and LaTeX tables), use

    make BUILD_DIR=<path to directory for generated assets>

where `<path to directory for generated assets>` does not have to exist
before running the command.
For example:

    make BUILD_DIR=_build

will create the `_build` directory inside the repository (if required) and
generate the assets (tables and figures) inside the directory.

Generation of the assets for the `bifurcation-diagram` experiment requires
downloading ~500 MB of datasets from Zenodo.org.
These datasets contain raw time series of detonation velocity for various
values of activation energy.


# Description of the experiments
