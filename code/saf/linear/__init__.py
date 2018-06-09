"""
saf.linear package
------------------

This package implements a framework for solving unsteady linear problems
in detonation theory in a shock-attached frame.
Problems are of the form:

:math::
    dz'_t   = -A(z) z'_x - B(z) z'

    dD'
    --- = f(z, z'),
    dt

where z and z' are vectors of base state and perturbed variables, respectively,
and D' is the perturbation of the detonation velocity.

Main class in this package is Solver. It instantiates all other class
(time integrator, approximator of spatial derivatives, user-provided class
of problem to solve) and run the simulations.

USAGE. It is the easiest to use this package through the helper function
`saf.action.solve.solve()`::

    >> from saf.action import solve
    >> solve('linear', c, outdir)

where the first argument 'linear' defines that we conduct linear
computations, `c` is a configuration object that is a derived from
`saf.linear.config.Config` class, `outdir` specifies the directory to which
simulation results are written.

"""
