import pandas as pd
import numpy as np

import alpha.signal_generators as sign
import backtesting.backtester as bt
import talib


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


def optimize_rsi_period(data, optimization='profit+std'):
    hit_ratios = []
    profits = []
    av_profits = []
    for i in range(2, 72 + 1):
        rsi_values = talib.RSI(data['close'].shift(), timeperiod=i)
        signs = sign.rsi_signals(rsi_values)
        pnl_data = bt.get_profit_and_loss(data=data['close'].pct_change(), signals=signs)
        conf_matrix = bt.get_confusion_matrix(data['close'], signs)
        try:
            hit_ratio = bt.get_hit_ratio(conf_matrix)
        except KeyError:
            hit_ratio = np.nan

        hit_ratios.append(hit_ratio)
        profits.append(sum(pnl_data.dropna()))
        av_profits.append(np.median(pnl_data.dropna()))

    if optimization == 'profit':
        approx_profit = np.mean(profits)
        key_profit = find_nearest(profits, approx_profit)
        key_index = profits.index(key_profit)
    elif optimization == 'profit+std':
        approx_profit = np.mean(profits) + np.std(profits)
        key_profit = find_nearest(profits, approx_profit)
        key_index = profits.index(key_profit)

    return key_index


def optimize_rsi_thresholds(data, rsi_values):
    """
    Optimize rsi profit or hit ratio by iterating thresholds
    """

    hit_heatmap = pd.DataFrame(np.nan, index=list(range(40)), columns=list(range(100 - 50, 100 + 1)))
    profit_heatmap = pd.DataFrame(np.nan, index=list(range(40)), columns=list(range(100 - 50, 100 + 1)))

    for j in range(1, 40 + 1):
        for k in range(50, 100 + 1):
            signs = sign.rsi_signals(rsi_values, upper_threshold=k, lower_threshold=j)
            pnl_data = sum(bt.get_profit_and_loss(data=data['close'].pct_change(), signals=signs).dropna())
            conf_matrix = bt.get_confusion_matrix(data['close'], signs)
            try:
                hit_ratio = bt.get_hit_ratio(conf_matrix)
            except KeyError:
                hit_ratio = np.nan
            del conf_matrix

            hit_heatmap.loc[j, k] = hit_ratio
            profit_heatmap.loc[j, k] = pnl_data
    return hit_heatmap, profit_heatmap
