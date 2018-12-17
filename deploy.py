import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.cluster import KMeans
from numpy.random import randn
import talib
import pickle


from datasets.clean_dataset import load_ohlc_dataset
import alpha.technical_indicators as tech
import alpha.signal_generators as sign
import alpha.alpha_engine as alpha
import backtesting.backtester as bt
import backtesting.backtester_engine as backtest
import optimization.optimization as optim
import optimization.optimization_engine as optimization
import visualization.visualize_optimization as viz

start_time = '2002-04-08'
end_time = '2003-04-07'

data = load_ohlc_dataset(start_time=start_time, end_time=end_time)
print('check for Na in datasets: \n', data.isnull().any())
# 04 09 12 00

# deploy alpha engine with random parameters
params_dict = {'hurst_period': 24,
               'macd_fastperiod': 5,
               'macd_slowperiod': 8,
               'macd_signalperiod': 4,
               'rsi_period': 5,
               'upper_threshold': 70,
               'lower_threshold': 30,
               'mom_barrier': 0,
               'meanrev_barrier': 0
               }
signals = alpha.deploy_alpha_engine(data, params_dict=params_dict)
indicator_signals = pd.read_csv('datasets/alpha/alpha_signals.csv', index_col=0)

# deploy backtesting engine
backtest.deploy_backtesting_engine(data=data, indicator_signals=indicator_signals, ex=0)
hit_ratio = float(pd.read_csv('datasets/backtesting/hit_ratio.csv').columns[0])
pnl_data = pd.read_csv('datasets/backtesting/pnl_data.csv', index_col=0)
conf_matrix = pd.read_csv('datasets/backtesting/conf_matrix.csv', index_col=0)
print(hit_ratio)
print(sum(pnl_data['filtered_signals_pnl'].dropna()))

# visualization of first results
viz.bokeh_cumulative_return(pnl_data=pnl_data)

optimization.deploy_optimization(data=data, params_dict=params_dict)

pkl_file = open('datasets/optimization/params_dict.pkl', 'rb')
params_dict = pickle.load(pkl_file)
pkl_file.close()

# deploy tuned alpha
signals = alpha.deploy_alpha_engine(data, params_dict=params_dict)
indicator_signals = pd.read_csv('datasets/alpha/alpha_signals.csv', index_col=0)
# deploy backtesting engine
backtest.deploy_backtesting_engine(data=data, indicator_signals=indicator_signals, ex=0)
print(hit_ratio)
print(sum(pnl_data['filtered_signals_pnl'].dropna()))

# visualization of first results
viz.bokeh_cumulative_return(pnl_data=pnl_data)

# now check for the next year
start_time = '2003-04-08'
end_time = '2004-04-08'
data = load_ohlc_dataset(start_time=start_time, end_time=end_time)
print('check for Na in datasets: \n', data.isnull().any())

indicator_data = pd.DataFrame()
hurst_data = tech.hurst_exponent(data['close'], 24)
# tech.hurst_core(data['close'][133:143])
macd, macdsignal, macdhist = talib.MACD(data['close'].shift(), fastperiod=5, slowperiod=8, signalperiod=4)
rsi_values = talib.RSI(data['close'].shift(), timeperiod=rsi_period)

indicator_signals = pd.DataFrame()
indicator_signals['macd_signal'] = sign.momentum_signals(macdsignal)
indicator_signals['rsi_signal'] = sign.rsi_signals(rsi_values, upper_threshold=rsi_upper, lower_threshold=rsi_lower)
indicator_signals['hurst'] = hurst_data
indicator_signals['filtered_signals'] = sign.hurst_filter(momentum_ind=indicator_signals['macd_signal'],
                                                          meanreverse_ind=indicator_signals['rsi_signal'],
                                                          hurst=indicator_signals['hurst'],
                                                          mom_barrier=0.1,
                                                          meanrev_barrier=-0.1)

pnl_data = bt.get_profit_and_loss(data=data['close'].pct_change(), signals=indicator_signals, ex=1)
conf_matrix = bt.get_confusion_matrix(data['close'], pnl_data['filtered_signals'])
hit_ratio = bt.get_hit_ratio(conf_matrix)
print(hit_ratio)
print(sum(pnl_data['filtered_signals_pnl'].dropna()))

plt.plot(pnl_data['filtered_signals_pnl'].cumsum())
plt.plot(pnl_data['rsi_signal_pnl'].cumsum())


