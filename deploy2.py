import pandas as pd
import pickle

from data_parser.moex_data import moex_data
import alpha.alpha_engine as alpha
import backtesting.backtester_engine as backtest
import optimization.optimization_engine as optimization
import visualization.visualize_optimization as viz


if __name__ == "__main__":
    start_time = '2015-04-08'
    end_time = '2016-12-31'

    data = moex_data(tickers=['SBER'], start_date=start_time, end_date=end_time, data_form='OHLCV')
    data['Returns'] = data['Close'].ffill().pct_change()
    data = data.dropna()
    data.drop_duplicates(inplace=True)

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
    indicator_signals = alpha.deploy_alpha_engine(data, params_dict=params_dict)
    indicator_signals = indicator_signals.dropna()
    indicator_signals.drop_duplicates(inplace=True)

    # deploy backtesting engine
    # TODO: I see infs with  2015-04-08 - 2016-12-31 in pnl data. backtesting module should be cleared and reworked
    pnl_data, conf_matrix, hit_ratio = backtest.deploy_backtesting_engine(data=data,
                                                                          indicator_signals=indicator_signals, ex=0)

    print(hit_ratio)
    print(sum(pnl_data['filtered_signals_pnl'].dropna()))
    # visualization of first results
    viz.bokeh_cumulative_return(pnl_data=pnl_data)
