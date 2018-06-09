"""
Compute observed order of accuracy."""
import numpy as np


def compute_observed_order_of_accuracy(errors, resolutions, exclude=False):
    """ Compute observed order of accuracy.

    Compute observed order of accuracy given `errors` and `resolutions`.
    First element in the result is necessarily 'nan' because order of accuracy
    is computed by comparing error in two different grids.

    Parameters
    ----------
    errors: array_like
        array_like of errors (or error norms)
    resolutions: array_like
        array_like of grid resolutions
    exclude : bool
        If True, then the first (NaN) value will be excluded from the returned
        value, otherwise the first value will stay there (for example, you need
        the first value when you format a convergence table). Default is False.

    Returns
    -------
    orders: array_like
        array_like of orders, with first element being 'nan'
    """

    if len(errors) != len(resolutions):
        raise Exception('To compute observed order of accuracy, '
                        'it is needed that number of errors and '
                        'number of grid resolutions match.')

    if len(resolutions) < 2:
        raise Exception('To compute observed order of accuracy, '
                        'it is required at least two different grid '
                        'resolutions.')

    errors = np.asarray(errors)
    resolutions = np.asarray(resolutions, dtype=float)

    orders = np.empty_like(errors)
    orders[:] = float('nan')

    # These strange +1s in denom due to the way we compute grid step size.
    # It will be better to delegate these operation to a special object
    # that builds grid and returns step size.
    numer = np.log(errors[:-1] / errors[1:])
    denom = np.log((resolutions[1:]+1) / (resolutions[:-1]+1))

    orders[1:] = numer / denom

    if exclude:
        orders = orders[1:]

    return orders
