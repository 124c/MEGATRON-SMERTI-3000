import pandas as pd
import pickle

from datasets.clean_dataset import load_ohlc_dataset
import alpha.alpha_engine as alpha
import backtesting.backtester_engine as backtest
import optimization.optimization_engine as optimization
import visualization.visualize_optimization as viz

start_time = '2013-04-08'
end_time = '2014-04-07'

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

# deploy optimization
optimization.deploy_optimization(data=data, params_dict=params_dict)

# load tuned parameters
pkl_file = open('datasets/optimization/params_dict.pkl', 'rb')
params_dict = pickle.load(pkl_file)
pkl_file.close()

# deploy tuned alpha
signals = alpha.deploy_alpha_engine(data, params_dict=params_dict)
indicator_signals = pd.read_csv('datasets/alpha/alpha_signals.csv', index_col=0)

# deploy backtesting engine
backtest.deploy_backtesting_engine(data=data, indicator_signals=indicator_signals, ex=1)
print(hit_ratio)
print(sum(pnl_data['filtered_signals_pnl'].dropna()))
hit_ratio = float(pd.read_csv('datasets/backtesting/hit_ratio.csv').columns[0])
pnl_data = pd.read_csv('datasets/backtesting/pnl_data.csv', index_col=0)
conf_matrix = pd.read_csv('datasets/backtesting/conf_matrix.csv', index_col=0)

# visualization of tuned results
viz.bokeh_cumulative_return(pnl_data=pnl_data)

# now check for the next year
start_time = '2014-04-08'
end_time = '2015-04-08'
data = load_ohlc_dataset(start_time=start_time, end_time=end_time)
print('check for Na in datasets: \n', data.isnull().any())

# deploy tuned alpha
signals = alpha.deploy_alpha_engine(data, params_dict=params_dict)
indicator_signals = pd.read_csv('datasets/alpha/alpha_signals.csv', index_col=0)

# deploy backtesting engine
backtest.deploy_backtesting_engine(data=data, indicator_signals=indicator_signals, ex=1)
hit_ratio = float(pd.read_csv('datasets/backtesting/hit_ratio.csv').columns[0])
pnl_data = pd.read_csv('datasets/backtesting/pnl_data.csv', index_col=0)
conf_matrix = pd.read_csv('datasets/backtesting/conf_matrix.csv', index_col=0)
print(hit_ratio)
print(sum(pnl_data['filtered_signals_pnl'].dropna()))
# visualization of tuned results
viz.bokeh_cumulative_return(pnl_data=pnl_data)
