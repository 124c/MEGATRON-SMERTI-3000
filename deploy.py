import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from numpy.random import randn
import talib

from datasets.clean_dataset import load_ohlc_dataset
import alpha.technical_indicators as tech
import alpha.signal_generators as sign
import backtesting.backtester as bt

start_time = '2002-04-08'
end_time = '2003-04-07'

data = load_ohlc_dataset(start_time=start_time, end_time=end_time)
print('check for Na in datasets: \n', data.isnull().any())
# 04 09 12 00

indicator_data = pd.DataFrame()
hurst_data = tech.hurst_exponent(data['close'], 24)
# tech.hurst_core(data['close'][133:143])
macd, macdsignal, macdhist = talib.MACD(data['close'].shift(), fastperiod=5, slowperiod=8, signalperiod=4)
rsi_values = talib.RSI(data['close'].shift(), timeperiod=5)

indicator_signals = pd.DataFrame()
indicator_signals['macd_signal'] = sign.momentum_signals(macdsignal)
indicator_signals['rsi_signal'] = sign.rsi_signals(rsi_values)
indicator_signals['hurst'] = hurst_data
indicator_signals['filtered_signals'] = sign.hurst_filter(momentum_ind=indicator_signals['macd_signal'],
                                                          meanreverse_ind=indicator_signals['rsi_signal'],
                                                          hurst=indicator_signals['hurst'],
                                                          mom_barrier=0,
                                                          meanrev_barrier=0)

pnl_data = bt.get_profit_and_loss(data=data['close'].pct_change(), signals=indicator_signals)
conf_matrix = bt.get_confusion_matrix(data['close'], pnl_data['filtered_signals'])
hit_ratio = bt.get_hit_ratio(conf_matrix)
plt.plot(pnl_data['filtered_signals_pnl'].cumsum())
plt.plot(pnl_data['momentum_signal_pnl'].cumsum())



