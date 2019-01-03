import pandas as pd
# import numpy as np
import talib

import alpha.technical_indicators as tech
import alpha.signal_generators as sign


def deploy_alpha_engine(data, params_dict):
    """
    Generate indicator values and signals
    """
    hurst_data = tech.hurst_exponent(data['Close'], params_dict['hurst_period'])
    macd, macdsignal, macdhist = talib.MACD(data['Close'].shift(),
                                            fastperiod=params_dict['macd_fastperiod'],
                                            slowperiod=params_dict['macd_slowperiod'],
                                            signalperiod=params_dict['macd_signalperiod'])
    rsi_values = talib.RSI(data['Close'].shift(), timeperiod=params_dict['rsi_period'])

    indicator_signals = pd.DataFrame()
    indicator_signals['macd_signal'] = sign.momentum_signals(macdsignal)
    indicator_signals['rsi_signal'] = sign.rsi_signals(rsi_values)
    indicator_signals['hurst'] = hurst_data
    indicator_signals['filtered_signals'] = sign.hurst_filter(momentum_ind=indicator_signals['macd_signal'],
                                                              meanreverse_ind=indicator_signals['rsi_signal'],
                                                              hurst=indicator_signals['hurst'],
                                                              mom_barrier=params_dict['mom_barrier'],
                                                              meanrev_barrier=params_dict['meanrev_barrier'])

    # indicator_signals.to_csv('datasets/alpha/alpha_signals.csv')
    # return True
    return indicator_signals
