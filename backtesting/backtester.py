import pandas as pd
import numpy as np
import execution.slippage as exc


def get_profit_and_loss(returns, signals, ex):
    """
    Loads Market data of different types (currently only returns) and combines it with trading signals df
    As a result we obtain dataset with profits and losses for each strategy in signals dataframe
    """

    # TODO: We need to check whether the market data we receive has datetime index and whether it coerces with signals

    # if data.shape[1] == 1:  # if 2nd dimention = 1 then we have dataframe with returns
    # returns.drop_duplicates(inplace=True)
    # signals.drop_duplicates(inplace=True)
    uniframe = pd.DataFrame(signals).join(returns, how='outer').dropna()
    uniframe.drop_duplicates(inplace=True)
    pnl_data = pd.DataFrame(index=uniframe.index)

    if isinstance(signals, pd.DataFrame):
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


def get_confusion_matrix(data, filtered_signals):
    """
    Returns confsion matrix of trading strategy
    data input here is a series or a numpy array
    """
    actual_movements_flags = np.where(data > 0, 1, -1)
    actual_movements_flags = pd.DataFrame(actual_movements_flags, columns=['Actual'], index=data.index)
    # filtered_signals = filtered_signals.to_frame(name='Predicted')
    filtered_signals = pd.DataFrame(data=filtered_signals.values,
                                    index=filtered_signals.index,
                                    columns=['Predicted'])
    uniframe = filtered_signals.join(actual_movements_flags, how='outer').dropna()
    return pd.crosstab(uniframe['Actual'], uniframe['Predicted'],  # .replace(0, 1)
                       rownames=['Actual'], colnames=['Predicted'], margins=True)


def get_hit_ratio(confusion_matrix):
    right_hit = confusion_matrix.loc[-1, -1] + confusion_matrix.loc[1, 1]
    wrong_hit = confusion_matrix.loc[1, -1] + confusion_matrix.loc[-1, 1]
    return right_hit/wrong_hit
