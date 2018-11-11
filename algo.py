import pandas as pd
import numpy as np
from numpy.random import randn

from datasets.clean_dataset import load_ohlc_dataset
import alpha.technical_indicators as tech

start_time = '2002-04-08'
end_time = '2003-04-07'

data = load_ohlc_dataset(start_time=start_time, end_time=end_time)
print('check for Na in datasets: \n', data.isnull().any())
# 04 09 12 00
hurstdata = tech.hurst_exponent(data['close'], 10)
# tech.hurst_core(data['close'][133:143])

hurstdata.plot()
