import pandas as pd
import numpy as np
import execution.slippage as exc


def get_profit_and_loss(returns, signals, ex):
    """
    Loads Market data of different types (currently only returns) and combines it with trading signals df
    As a result we obtain dataset with profits and losses for each strategy in signals dataframe
    """

    # TODO: We need to check whether the market data we receive has 2 dimensions and if not to transform it
    # TODO: We need to check whether the market data we receive has datetime index and whether it coerces with signals

    # if data.shape[1] == 1:  # if 2nd dimention = 1 then we have dataframe with returns
    if isinstance(signals, pd.DataFrame):
        pnl_data = pd.concat([data, signals], axis=1).dropna()
        for signal in signals.columns:
            pnl_data[signal + '_pnl'] = uniframe[signal] * uniframe['Returns']
            if ex == 1:
                slip = exc.slippage_and_comission(returns)
                pnl_data[signal + '_pnl'] = uniframe[signal] * (returns + slip)
    else:
        if ex == 1:
            slip = exc.slippage_and_comission(returns)
            pnl_data = (returns + slip) * signals
        else:
            pnl_data = returns * signals

    return pnl_data


def get_confusion_matrix(data, signals):
    """
    Returns confsion matrix of trading strategy
    data input here is a series or a numpy array
    """
    actual_movements = np.where(data.diff() > 0, 1, -1)
    actual_movements = pd.Series(actual_movements, name='Actual', index=data.index)
    signals = pd.Series(signals, name='Predicted')
    return pd.crosstab(actual_movements, signals,  # .replace(0, 1)
                       rownames=['Actual'], colnames=['Predicted'], margins=True)


def get_hit_ratio(confusion_matrix):
    right_hit = confusion_matrix.loc[-1, -1] + confusion_matrix.loc[1, 1]
    wrong_hit = confusion_matrix.loc[1, -1] + confusion_matrix.loc[-1, 1]
    return right_hit/wrong_hit
