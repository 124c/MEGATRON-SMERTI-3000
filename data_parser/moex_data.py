import pandas_datareader.data as web
import pandas as pd


def moex_data(tickers, start_date, end_date, form='OHLCV', boardID='TQBR'):
    """
    Returns a pandas Data Frame with tickers that you input
    :param tickers: list with selected tickers ['MGNT', 'SBER'] with a datetime index
    :param start_date: string or datetime object
    :param end_date: string or datetime object
    :param boardID: string denoting ASTS trading board
    :param form: form of dataset to be returned
    :return: pandas Data Frame
    """

    # TODO: add hashed data saving feature. i.e. if you have ever loaded data,
    #  then you won't have to use internet but just load previous data from pickle or else

    dirty_data = web.DataReader(tickers, 'moex', start_date, end_date)
    dirty_data = dirty_data[dirty_data['BOARDID'] == boardID]

    if data_form == 'OHLCV':
        returndata = dirty_data[['OPEN', 'HIGH', 'LOW', 'CLOSE', 'NUMTRADES', 'VOLUME', 'SECID']]
        returndata.columns = ['Open', 'High', 'Low', 'Close', 'Numtrades', 'Volume', 'SECID']
        return returndata
    elif data_form == 'Close':
        close_data = pd.DataFrame(index=dirty_data.drop_duplicates().index)
        for i in dirty_data['SECID'].unique():
            close_data[i] = dirty_data.groupby(['SECID']).get_group(i)[['CLOSE']].drop_duplicates()
        return close_data
    else:
        raise ValueError('Specified wrong dataset form!')
