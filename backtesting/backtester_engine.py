import pandas as pd
import numpy as np

import backtesting.backtester as bt


def deploy_backtesting_engine(data, indicator_signals, ex=0):
    """
    Performs automated testing of a strategy
    """
    pnl_data = bt.get_profit_and_loss(data=data['close'].pct_change(), signals=indicator_signals, ex=0)
    conf_matrix = bt.get_confusion_matrix(data['close'], pnl_data['filtered_signals'])
    hit_ratio = bt.get_hit_ratio(conf_matrix)

    pnl_data.to_csv('datasets/backtesting/pnl_data.csv')
    conf_matrix.to_csv('datasets/backtesting/conf_matrix.csv')
    np.savetxt('datasets/backtesting/hit_ratio.csv', np.array(hit_ratio).reshape(-1, 1), delimiter=",")
    # return pnl_data, conf_matrix, hit_ratio
    return True


