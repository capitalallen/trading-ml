# IMPORTS
import pandas as pd
import math
import os.path
import time
from binance.client import Client
from datetime import timedelta, datetime
from dateutil import parser
from tqdm import tqdm_notebook  # (Optional, used for progress-bars)
from configparser import ConfigParser


class data_getter:
    def __init__(self):
        config = ConfigParser()
        config.read('config.ini')

        # Enter your own API-key here
        self.binance_api_key = config.get('main', 'binance_api_key')
        # Enter your own API-secret here
        self.binance_api_secret = config.get('main', 'binance_api_secret')

        self.binsizes = {"1m": 1, "5m": 5, "30m": 30,
                         "1h": 60, "6h": 360, "1d": 1440}
        self.batch_size = config.get('main', 'batch_size')
    """
    minutes_of_new_data: get old data 
    """

    def minutes_of_new_data(self, symbol, kline_size, data, source, startDate="01 Nov 2017"):
        if len(data) > 0:
            old = parser.parse(data["timestamp"].iloc[-1])
        elif source == "binance":
            old = datetime.strptime(startDate, '%d %b %Y')

        if source == "binance":
            binance_client = Client(
                api_key=self.binance_api_key, api_secret=self.binance_api_secret)
            new = pd.to_datetime(binance_client.get_klines(
                symbol=symbol, interval=kline_size)[-1][0], unit='ms')
        return old, new

    """
    get_all_binance: download data 
    """

    def get_all_binance(self, symbol, kline_size, save=True, folder=None, source="binance", start_time='01 Nov 2017'):
        binance_client = Client(
            api_key=self.binance_api_key, api_secret=self.binance_api_secret)
        self.filename = '%s-%s-data.csv' % (symbol, kline_size)
        if folder:
            self.filename = folder+"/"+self.filename

        # check if the file already exists
        if os.path.isfile(self.filename):
            data_df = pd.read_csv(self.filename)
        else:
            data_df = pd.DataFrame()

        oldest_point, newest_point = self.minutes_of_new_data(
            symbol, kline_size, data_df, source=source)

        delta_min = (newest_point - oldest_point).total_seconds()/60
        available_data = math.ceil(delta_min/self.binsizes[kline_size])

        if oldest_point == datetime.strptime(start_time, '%d %b %Y'):
            print('Downloading all available %s data for %s. Be patient..!' %
                  (kline_size, symbol))
        else:
            print('Downloading %d minutes of new data available for %s, i.e. %d instances of %s data.' % (
                delta_min, symbol, available_data, kline_size))

        klines = binance_client.get_historical_klines(symbol, kline_size, oldest_point.strftime(
            "%d %b %Y %H:%M:%S"), newest_point.strftime("%d %b %Y %H:%M:%S"))

        data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close',
                                             'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore'])

        data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')

        # form pd dataframe
        if len(data_df) > 0:
            temp_df = pd.DataFrame(data)
            data_df = data_df.append(temp_df)
        else:
            data_df = data
        data_df.set_index('timestamp', inplace=True)
        if save:
            data_df.to_csv(self.filename)
            return self.filename
        else:
            return data_df
        print('Finished')
