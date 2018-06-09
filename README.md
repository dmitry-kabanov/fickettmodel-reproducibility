# Reproducibility package for the paper on the Fickett model

This is a reproducibility repository for paper on the Fickett model submitted
to *???Journal name???* and authored by Dmitry Kabanov (me) and Aslan Kasimov.

# Installation
This package was developed under Ubuntu 16.04 and should work under other
flavors of Unix without any modification (macOS, Centos, Fedora, and so on).
Using this package under Windows operating system may or may not work as it
depends on `make` utility.

To be able to run the scripts in this repository, you need to clone it:

    git clone --depth=1 git@github.com:dmitry-kabanov/fickettmodel-reproducibility.git

and change current directory to the repository directory:

    cd fickettmodel-reproducibility

Besides, you need Python along with several scientific libraries, such as
NumPy, SciPy, and Matplotlib.
We recommend to use Anaconda Python distribution 5.0 to achieve this, as we
used it ourselves for development of this package.
It can be downloaded from `https://repo.continuum.io/archive/`.
Alternatively, you can get Python and the libraries from other places.
In this case, you need Python 3.6.3, NumPy 1.13.3, SciPy 0.19.1, and Matplotlib
2.1.0.

To generate assets (figures and LaTeX tables), use

    make BUILD_DIR=<path to directory for generated assets>

where `<path to directory for generated assets>` must exist before running the
command.
For example:

    make BUILD_DIR=_build

will create the `_build` directory inside the repository and generate the
assets inside the directory.

Generation of the assets for the `bifurcation-diagram` experiment requires
downloading ~500 MB of datasets from Zenodo.org.
These datasets contain raw time series of detonation velocity for various
values of activation energy.


# Description of the experiments
