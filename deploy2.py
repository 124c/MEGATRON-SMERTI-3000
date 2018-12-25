import pandas as pd
import pickle

from datasets.clean_dataset import load_ohlc_dataset
import alpha.alpha_engine as alpha
import backtesting.backtester_engine as backtest
import optimization.optimization_engine as optimization
import visualization.visualize_optimization as viz

start_time = '2015-04-08'
end_time = '2016-04-07'

data = pd.read_csv('datasets/market_data/stocks.csv', index_col=0, parse_dates=True)
close_data = pd.DataFrame(index=data.index)
for i in data['SECID'].unique():
    close_data[i] = data.groupby(['SECID']).get_group(i)[['CLOSE']].drop_duplicates()


