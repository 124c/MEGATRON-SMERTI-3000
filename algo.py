import pandas as pd
import numpy as np
from numpy.random import randn

from datasets.clean_dataset import load_ohlc_dataset
import alpha.technical_indicators as tech
import alpha.signal_generators as sign

start_time = '2002-04-08'
end_time = '2003-04-07'

data = load_ohlc_dataset(start_time=start_time, end_time=end_time)
print('check for Na in datasets: \n', data.isnull().any())
# 04 09 12 00

indicator_data = pd.DataFrame()
indicator_data['hurst_data'] = tech.hurst_exponent(data['close'], 12)
# tech.hurst_core(data['close'][133:143])
indicator_data['momentum_data'] = tech.momentum(data['close'], 3)
indicator_data = pd.concat([indicator_data, tech.macd(data['close'], 12, 8, 6)], axis=1)

indicator_signals = pd.DataFrame()
indicator_signals['momentum_signal'] = sign.momentum_signals(indicator_data['momentum_data'])
indicator_signals['macd_signal'] = sign.macd_signals(indicator_data)
indicator_signals['hurst'] = indicator_data['hurst_data']
indicator_signals