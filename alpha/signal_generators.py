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
    """Generates buy/sell signals with mean reversion logic"""
    sigline = macd_dataframe['MACD_signal_line']
    macd_signs = np.where(sigline > upper_threshold, -1,
                          np.where(sigline < lower_threshold, 1, 0))
    macd_signs = pd.Series(macd_signs, index=macd_dataframe.index)
    return macd_signs
