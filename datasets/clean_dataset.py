import pandas as pd


def load_ohlc_dataset(filepath='datasets/eurusd_h1.csv', start_time='2010-1-1', end_time='2014-1-1'):
    """ Return an OHLC dataset.
    Filepath can be both. if relative, then the root folder is it4Fin
    Start and end can be defined as strings in Y-m-d H:T:S, where T defines minutes """
    data = pd.read_csv(filepath)
    data['date'] = pd.to_datetime(data['date'] + ' ' + data['time'])
    data.set_index('date', drop=True, inplace=True)
    del data['time']
    data = data[(data.index >= start_time) & (data.index <= end_time)]
    print('dataset shape: ', data.shape)
    return data

