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

    return pnl_data, conf_matrix, hit_ratio


