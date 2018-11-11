import pandas as pd
import numpy as np
# from numpy.random import randn


def hurst_core(array):
    """Returns the value of Hurst Exponent for time series ts"""
    # Make sure ve pass numpy arrays not pandas series
    if type(array) == pd.Series:
        array = array.values

    # Create the range of lag values
    lags = range(1, array.size-1)
    # default variant was lags = range(2, 100) and
    # [sqrt(std(subtract(ts[lag:], ts[:-lag]))) for lag in lags]

    # Calculate the array of the variances of the lagged differences
    tau = []
    for lag in lags:
        tau.append(np.sqrt(np.std(array[lag:] - array[:-lag])))

    # Use a linear fit to estimate the Hurst Exponent
    poly = np.polyfit(np.log(lags), np.log(tau), 1)

    # Return the Hurst exponent from the polyfit output
    return poly[0]*2.0


def hurst_exponent(time_series, window):
    """Returns a vector of rolling hurst exponent values"""
    return time_series.rolling(window).apply(hurst_core)


# gbm = np.log(np.cumsum(randn(100000))+1000)
# mr = np.log(randn(100000)+1000)
# tr = np.log(np.cumsum(randn(100000)+1)+1000)
#
# print("Hurst(GBM):   %s" % hurst(gbm))
# print("Hurst(MR):    %s" % hurst(mr))
# print("Hurst(TR):    %s" % hurst(tr))
