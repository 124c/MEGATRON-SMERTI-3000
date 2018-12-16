import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

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
        pnl_data = bt.get_profit_and_loss(data=data['close'].pct_change(), signals=signs, ex=0)
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
            pnl_data = sum(bt.get_profit_and_loss(data=data['close'].pct_change(), signals=signs, ex=0).dropna())
            conf_matrix = bt.get_confusion_matrix(data['close'], signs)
            try:
                hit_ratio = bt.get_hit_ratio(conf_matrix)
            except KeyError:
                hit_ratio = np.nan
            del conf_matrix

            hit_heatmap.loc[j, k] = hit_ratio
            profit_heatmap.loc[j, k] = pnl_data
    return hit_heatmap, profit_heatmap


def find_robust_areas(heatmap, n_clusters=50):
    """
    Calculates centroids in heatmaps using k-means clustering
    """
    arr = heatmap.fillna(0).unstack()
    indvals = arr.index.values
    Y_data = np.round(arr.values, decimals=3)
    X_data = np.array([list(x) for x in indvals], dtype=float)
    X_data = np.insert(X_data, 2, Y_data, axis=1)

    # KMeans algorithm
    kmeans_model = KMeans(n_clusters=n_clusters).fit(X_data)
    centroids = pd.DataFrame(kmeans_model.cluster_centers_)
    mx = max(centroids[2])
    key_index = list(centroids[2]).index(mx)
    best_thresholds = np.round(centroids[centroids.index == key_index].values[0][:2])
    return best_thresholds
