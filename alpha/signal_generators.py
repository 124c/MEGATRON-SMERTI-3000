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


def macd_signals(signal_line, upper_threshold=0.000, lower_threshold=-0.000):  # 15
    """
    Generates buy/sell signals with macd logic
    """
    sigline = signal_line
    macd_signs = np.where(sigline > upper_threshold, -1,
                          np.where(sigline < lower_threshold, 1, 0))
    macd_signs = pd.Series(macd_signs, index=signal_line.index)
    return macd_signs


def rsi_signals(signal_line, upper_threshold=70, lower_threshold=30):  # 15
    """
    Generates buy/sell signals with mean reversion logic
    """
    sigline = signal_line
    rsi_signs = np.where(sigline > upper_threshold, -1,
                         np.where(sigline < lower_threshold, 1, 0))
    rsi_signs = pd.Series(rsi_signs, index=signal_line.index)
    return rsi_signs


# TODO: Smb should take it as an assignment
def generate_signal_dataframe(indicators_df):
    """
    Accepts a dataframe with indicator values as input and orienting by colnames,
    generates a dataframe with signals
    """
    return 'not ready'


def hurst_filter(momentum_ind, meanreverse_ind, hurst, mom_barrier=0, meanrev_barrier=0):
    if mom_barrier < meanrev_barrier:
        raise ValueError('Your threshold values overlap!\n Please change your threshold values')

    mom_signals = np.where(hurst.values > mom_barrier, momentum_ind, 0)
    meanreversion_signals = np.where(hurst < meanrev_barrier, meanreverse_ind, 0)
    signals = meanreversion_signals + mom_signals
    signals = pd.DataFrame(signals, index=momentum_ind.index)
    return signals
