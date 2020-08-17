import pandas as pd
from binance.client import Client
from datetime import timedelta, datetime
import mlfinlab as ml
import time
import numpy as np


def get_klines_df(start_time, curr=None, symbol="BTCUSDT", interval="1m"):
    binance_api_key = '7kMDnOgQD8cTq6rHTLxPwcjT8iPnfnw0B4k52yycHUGZf8SzwJKqIjxavzVVdh9i'
    # Enter your own API-secret here
    binance_api_secret = 'tDGmclXOVOD8KTOIqsaswwraU9WxBtZuF8H4KDsNaDrEdQHv0MuCxdQxsnxxfrhR'
    binance_client = Client(api_key=binance_api_key,
                            api_secret=binance_api_secret)
    start = str(int(datetime.strptime(
        start_time, '%Y-%m-%d %H:%M:%S').timestamp()*1000+1))
    # get the data from start_time to curr time and convert to dataframe
    klines = pd.DataFrame(
        binance_client.get_historical_klines(symbol, interval, start, curr))
    # leave only time price volume
    klines = klines.drop([6, 7, 8, 9, 10, 11], axis=1)
    klines = klines.rename({0: "date_time", 1:"open",2:"high",3:"low",4: "close", 5: "volume"}, axis=1)
    klines['date_time'] = pd.to_datetime(klines['date_time'].div(1000), unit='s')
    for col in ['open','high','low','close','volume']:
        klines[col] = klines[col].astype('float32')
    return klines

"""
is_limit(df,limit)
check if (open+close)/2*volume >=limit
"""
def is_limit(df,threshold):
    return ((df['open']+df['close'])/2*df['volume']).sum() >= threshold

"""
form_dol
"""
def form_dol_bar(df, threshold):
    # print(df.head())
    d = ml.data_structures.standard_data_structures.get_dollar_bars(
        df.loc[:,['date_time','close','volume']], threshold=threshold, batch_size=100, verbose=False)
    return d