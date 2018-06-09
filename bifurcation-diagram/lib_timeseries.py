"""Collection of functions used to postprocess time series."""
import matplotlib.pyplot as plt
import numpy as np

from scipy import interpolate
from scipy import signal


def movingaverage(x, N):
    """Smooth `x` by simple moving average algorithm with windows size `N`."""
    cumsum = np.cumsum(np.insert(x, 0, 0))
    result = np.empty_like(x)
    result[N-1:] = (cumsum[N:] - cumsum[:-N]) / N
    result[:N-1] = x[:N-1]

    return result


def compute_fft(t, D, freq_ub=1):
    """Compute FFT for D(t) and return power spectrum with peaks."""

    # First, we interpolate because FFT expects time series
    # with a uniform time step.
    tck = interpolate.splrep(t, D)
    num_samples = 1024*(t[-1]-t[0])
    t_new, dt = np.linspace(t[0], t[-1], num=num_samples, retstep=True)
    print('dt = %f' % dt)
    d_new = interpolate.splev(t_new, tck)

    # First subtract the mean value to remove large harmonics with frequency 0.
    N = len(d_new)
    yhat = np.fft.rfft(d_new - d_new.mean())
    freq = np.fft.rfftfreq(N, dt)
    power = 2*np.abs(yhat) / N

    # Finding peaks in the FFT spectrum
    # and consider only peaks for frequencies less than Frequency Upper Bound.
    peaks = signal.argrelmax(power, order=10)[0]
    peaks = peaks[freq[peaks] <= freq_ub]
    msg = 'Frequency peaks:\n {}'
    print(msg.format(freq[peaks]))

    return freq, power, peaks


def find_average_det_vel(t, D):
    """Evaluate average detonation velocity."""
    all_minima_idx = signal.argrelmin(D, order=100)[0]
    low_minima_idx = signal.argrelmin(D[all_minima_idx])[0]

    if len(low_minima_idx) == 0 or len(low_minima_idx) == 1:
        low_minima_idx = all_minima_idx
        i_1 = all_minima_idx[0]
        i_2 = all_minima_idx[-1]
    else:
        i_1 = all_minima_idx[low_minima_idx[0]]
        i_2 = all_minima_idx[low_minima_idx[-1]]

    T = t[i_2] - t[i_1]

    plt.plot(t, D, '-')
    plt.plot([t[i_1], t[i_2]], [D[i_1], D[i_2]], 'ro')
    plt.show()

    # Using trapezoidal rule to evaluate :math:`\int D(\tau) d\tau`.
    integrand = 0.5 * (D[i_1:i_2-1] + D[i_1+1:i_2])
    integral = np.sum(integrand * np.diff(t[i_1:i_2]))

    D_avg = integral / T

    return D_avg
