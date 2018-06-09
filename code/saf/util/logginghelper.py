import logging
import sys


def init(filename=None, stdout=True):
    """Configure the root logger.

    Does the following:
    - set custom formatting for the message
    - set logging level to DEBUG
    - add either StreamHandler or FileHandler to the root logger depending on
    the parameter `filename`.

    This function adds only one handler: either StreamHandler or FileHandler
    but not both.

    Parameters
    ----------
    filename : str, optional (default is `None`)
        Name of the file to which the log should be redirected.
        If `None`, then the log will be written to the `stderr` or to `stdout`
        depending on the value of `stdout`.
    stdout : bool, optional (default is True)
        Whether to output to standard output (stdout) or to standard error
        output (stderr).

    """
    logger = logging.getLogger()

    # If one of the handlers in `logger` is a `StreamHandler` or `FileHandler`,
    # then it means that logging is configured already.
    for h in logger.handlers:
        if isinstance(h, logging.StreamHandler):
            return
        if isinstance(h, logging.FileHandler):
            return

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(name)-32.32s | %(levelname)1.1s | %(message)s')

    if filename is None:
        if stdout:
            # Stream is standard output (stdout).
            h = logging.StreamHandler(sys.stdout)
        else:
            # Stream is standard error output (stderr).
            h = logging.StreamHandler()
    else:
        h = logging.FileHandler(filename, mode='w')

    h.setLevel(logging.DEBUG)
    h.setFormatter(formatter)

    logger.addHandler(h)


def reset():
    """Reset the root logger by removing attached handlers."""
    logger = logging.getLogger()

    # Copying handlers list. The weird syntax `list(...)` is due to the
    # required compatibility with python 2.7.
    handlers = list(logger.handlers)

    for h in handlers:
        if isinstance(h, logging.StreamHandler):
            logger.removeHandler(h)
        if isinstance(h, logging.FileHandler):
            logger.removeHandler(h)
            h.close()
