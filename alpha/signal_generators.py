import numpy as np
import pandas as pd


def momentum_signals(momentum_values):
    """
    Generates buy/sell signals if current increment is bigger than the previous one
    The ideology is that an uptrend has a speed growth property
    """
    momentum_diff = momentum_values.diff()
    momentum_signs = np.where(momentum_diff > momentum_diff.shift(), 1,
                              np.where(momentum_diff < momentum_diff.shift(), -1, 0))
    momentum_signs = pd.Series(momentum_signs, index=momentum_values.index)  # a series must be returned
    # TODO: add filters on maximum consecutive number of signals. Find the optimal value for filter
    return momentum_signs


def macd_signals(macd_dataframe, upper_threshold=0.00015, lower_threshold=-0.00015):
    """
    Generates buy/sell signals with mean reversion logic
    """
    sigline = macd_dataframe['MACD_signal_line']
    macd_signs = np.where(sigline > upper_threshold, -1,
                          np.where(sigline < lower_threshold, 1, 0))
    macd_signs = pd.Series(macd_signs, index=macd_dataframe.index)
    return macd_signs


def hurst_filter(ind1signal, ind2signal, hurst,
                 hurst1threshold=0.5,
                 hurst2threshold=0.5):
    """
    Generates a rule that defines when to execute 1st indicator and when the 2nd one
    Remember that threshold should not intercept each other
    """
    # TODO: Create a warning message if threshold intercept each other
    ind1_signals = np.where(hurst > hurst1threshold, ind1signal, 0)  # for momentum signal
    ind2_signals = np.where(hurst < hurst2threshold, ind2signal, 0)  # for mean reversion signal
    final_signals = ind1_signals + ind2_signals
    return final_signals
