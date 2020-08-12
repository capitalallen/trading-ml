from mlfinlab.data_structures import standard_data_structures as ds
from mlfinlab.data_structures import get_ema_dollar_imbalance_bars, get_const_dollar_imbalance_bars
import pandas as pd
import numpy as np
import json
from os import path


class bar_generate:
    """
    init:
    - input: file name, outfile name, threshold_type 
    - ouput: void
    - read csv file to df 
    - calculate threshold
    """
    
    def __init__(self, inputFile=None,read_df=False,df=None, outFile=None,outfolder=None):
        self.inputFile = inputFile
        self.threshold = None
        if read_df:
            self.df = df 
        else: 
            self.df = pd.read_csv(inputFile)
        if outfolder:
            self.outFile = outfoldr + "/" + outFile    

        cols = ["timestamp", "close", "volume"]
        cols_threshold = ["timestamp", "close", "open", "volume"]
        self.raw_for_threshold = self.df.loc[:, cols_threshold]
        self.df = self.df.loc[:, cols]
        self.df.rename(columns={'timestamp': 'date_time'}, inplace=True)
        self.df.date_time = pd.to_datetime(self.df['date_time'])

    """
    change input_file
    """

    def set_inputFile(self, f):
        self.inputFile = f

    """
    store threshold to a given json file 
    """

    def store_threshold(self, fileName):
        data = {self.inputFile: self.threshold}
        if path.exists(fileName):
            with open(fileName, 'a') as f:
                json.dump(data, f)
                f.close()
        else:
            with open(fileName, 'w') as f:
                json.dump(data, f)
                f.close()
    """
    cal_threshold
    - input: type 
    - output: self.threhold
    - use switch to handle different cases 
    types: average, 2-year daily average/50, 1-year daily average/50, daily average/50
    """

    def cal_threshold(self, t, fileName="threshold.json"):
        if t == "daily_av_50":
            self.threshold = np.sum(
                (self.raw_for_threshold['open']+self.raw_for_threshold['close'])/2*self.raw_for_threshold['volume'])/self.raw_for_threshold.shape[0]/50
        elif t == "average":
            self.threshold = np.sum(
                (self.raw_for_threshold['open']+self.raw_for_threshold['close'])/2*self.raw_for_threshold['volume'])/self.raw_for_threshold.shape[0]
        self.store_threshold(fileName)
    
    def set_threshold(self,num):
        self.threshold = num
    
    def get_threshold(self):
        return self.threshold
    """
    convert_dol_bar
    if not threhold: raise threhold undefined 
    else: get dollar bar and store to csv 
    """

    def convert_dol_bar(self):
        if not self.threshold:
            print("threshold not defined")
            return
        dollar = ds.get_dollar_bars(
            self.df, threshold=self.threshold, batch_size=1000, verbose=False)
        dollar.to_csv(self.outFile)
    """
    convert_imb_bar_const
    if not threhold: raise threhold undefined 
    else: get dollar bar and store to csv 
    """

    def convert_imb_bar_const(self, exp_num_ticks_init=10, expected_imbalance_window=10):
        bars = get_const_dollar_imbalance_bars(
            self.df, exp_num_ticks_init=exp_num_ticks_init, expected_imbalance_window=expected_imbalance_window)
        # print(type(bars), type(bars[0]))
        bars[0].to_csv(self.outFile)

    """
    convert_imb_bar_ema
    if not threhold: raise threhold undefined 
    else: get dollar bar and store to csv 
    """

    def convert_imb_bar_ema(self,  num_prev_bars=3, exp_num_ticks_init=5,
                            exp_num_ticks_constraints=[5, 100], expected_imbalance_window=5):
        bars = get_ema_dollar_imbalance_bars(self.df, num_prev_bars=num_prev_bars, exp_num_ticks_init=exp_num_ticks_init,
                                             exp_num_ticks_constraints=exp_num_ticks_constraints, expected_imbalance_window=expected_imbalance_window)

        bars[0].to_csv(self.outFile)
