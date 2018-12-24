import pandas_datareader.data as web
import pandas as pd


def moex_data(tickers, start_date, end_date, form='OHLCV', boardID='TQBR'):
    """
    Returns a pandas Data Frame with tickers that you input
    :param tickers: list with selected tickers ['MGNT', 'SBER']
    :param start_date: string or datetime object
    :param end_date: string or datetime object
    :param boardID: string denoting ASTS trading board
    :param form: form of dataset to be returned
    :return: pandas Data Frame
    """

    dirty_data = web.DataReader(tickers, 'moex', start_date, end_date)
    dirty_data = dirty_data[dirty_data['BOARDID'] == boardID]

    if form == 'OHLCV':
        return dirty_data[['OPEN', 'HIGH', 'LOW', 'CLOSE', 'NUMTRADES', 'VOLUME', 'SECID']]
    elif form == 'Close':
        close_data = pd.DataFrame()
        for i in dirty_data['SECID'].unique():
            close_data[i] = dirty_data.groupby(['SECID']).get_group(i)['CLOSE']
        return close_data
    else:
        raise ValueError('Specified wrong dataset form!')
