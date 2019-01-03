import pandas as pd
import numpy as np
import talib
import pickle

import optimization.optimization as optim
import visualization.visualize_optimization as viz


def deploy_optimization(data, params_dict):
    """
    Optimizes all parameters
    """
    params_dict['rsi_period'] = optim.optimize_rsi_period(data)
    rsi_values = talib.RSI(data['Close'].shift(), timeperiod=params_dict['rsi_period'])

    rsi_hit_ratio_map, rsi_profit_map = optim.optimize_rsi_thresholds(data, rsi_values)
    # visualize and give it best thresholds based on that
    # viz.visualize_heatmap_hit_ratio(profit_heatmap=rsi_profit_map, hit_heatmap=rsi_hit_ratio_map)

    params_dict['upper_threshold'], params_dict['lower_threshold'] = optim.find_robust_areas(heatmap=rsi_profit_map,
                                                                                             n_clusters=120)
    # print(optim.find_robust_areas(heatmap=rsi_hit_ratio_map, n_clusters=30))
    # f = open("datasets/optimization/params_dict.pkl", "wb")
    # pickle.dump(params_dict, f)
    # f.close()

    return params_dict
