import os

import matplotlib.pyplot as plt


# Figure size for a single-plot figure that takes 50 % of text width.
FIGSIZE_NORMAL = (3.0, 2.0)
# Figure size for a single-plot figure that takes about 75 % of text width.
FIGSIZE_LARGER = (4.5, 3.0)
# Figure size for a figure with two subplots in one row.
FIGSIZE_TWO_SUBPLOTS_ONE_ROW = (6.0, 2.0)
# Figure size for a figure with two subplots in two rows.
FIGSIZE_TWO_SUBPLOTS_TWO_ROWS = (4.5, 3.0)
# Figure size for a figure with six subplots.
FIGSIZE_SIX_SUBPLOTS = (6.0, 8.0)
# Figure size for a large figure that takes ~100 % of text width.
FIGSIZE_LARGE = (6.0, 4.0)
# Figure size for time series with phase portraits.
FIGSIZE_TIME_SERIES_WITH_PHASE_PORTRAIT = (1.9, 4.0)

TARGET_DIR = '_assets'


def savefig(filename, **kwargs):
    """Save figure if the environment variable SAVE_FIGURES is set."""
    cur_fig = plt.gcf()

    if 'SAVE_FIGURES' in os.environ:
        if os.path.isdir(TARGET_DIR):
            filename = os.path.join(TARGET_DIR, filename)
            cur_fig.savefig(filename, **kwargs)
        else:
            raise HelperError('Directory `%s` does not exist' % TARGET_DIR)
    else:
        plt.show()


class HelperError(Exception):
    pass
