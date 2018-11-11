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
    poly = np.polyfit(np.log10(lags), np.log10(tau), 1)

    # Return the Hurst exponent from the polyfit output
    return poly[0]*2.0


def hurst_exponent(time_series, window):
    """Returns a series of rolling hurst exponent values"""
    return time_series.rolling(window).apply(hurst_core)


def momentum(time_series, window):
    """Returns a series of momentum indicator values"""
    # formula: (Pt/Pt-window) * 100
    return 100 * (time_series.pct_change(window)+1)


def macd(time_series, slow, fast, internal):
    """Returns MACD indicator and it's moving averages"""
    macd = pd.DataFrame()
    macd['EMA_slow'] = time_series.ewm(alpha=2/slow, min_periods=1).mean()
    macd['EMA_fast'] = time_series.ewm(alpha=2/fast, min_periods=1).mean()
    macd['EMA_slow-fast'] = macd['EMA_slow'] - macd['EMA_fast']
    macd['MACD_ema'] = macd['EMA_slow-fast'].ewm(alpha=2/internal, min_periods=1).mean()
    macd['MACD_signal_line'] = macd['EMA_slow-fast'] - macd['MACD_ema']
    return macd

# gbm = np.log(np.cumsum(randn(100000))+1000)
# mr = np.log(randn(100000)+1000)
# tr = np.log(np.cumsum(randn(100000)+1)+1000)
#
# print("Hurst(GBM):   %s" % hurst(gbm))
# print("Hurst(MR):    %s" % hurst(mr))
# print("Hurst(TR):    %s" % hurst(tr))
