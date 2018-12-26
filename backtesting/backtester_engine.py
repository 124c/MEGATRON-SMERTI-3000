import pandas as pd
import numpy as np

import backtesting.backtester as bt


def deploy_backtesting_engine(data, indicator_signals, ex=0):
    """
    Performs automated testing of a strategy
    data parameter should be a Dataframe with close prices!
    """
    pnl_data = bt.get_profit_and_loss(returns=data['Returns'], signals=indicator_signals, ex=0)
    conf_matrix = bt.get_confusion_matrix(data['Close'], pnl_data['filtered_signals_pnl'])
    hit_ratio = bt.get_hit_ratio(conf_matrix)

    return pnl_data, conf_matrix, hit_ratio


