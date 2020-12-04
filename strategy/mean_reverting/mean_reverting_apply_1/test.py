import sys
sys.path.append("../bar_generator")
sys.path.append("../data_downloader")
sys.path.append("../labeling")
sys.path.append("../mean_reverting")
import data_getter 
import filter_label
import bar_generate
import preprocess
import os 
import pandas as pd 
from finta import TA
import dataset_handle as dh  
from multiprocessing import Process

# inputfile_min = './BTCUSDT/minute_timebar.csv'
# inputfile_daily = './BTCUSDT/daily_timebar.csv'
# output_folder = './BTCUSDT'
# out_bar_filename = 'dol_bar.csv'
# daily = bar_generate.bar_generate(read_df=False,inputFile=inputfile_daily, outfolder=output_folder,outFile='daily_time.csv')
# daily.cal_threshold("daily_av_50")
# threshold = daily.get_threshold()

# generator = bar_generate.bar_generate(read_df=False,inputFile=inputfile_min,outFile=out_bar_filename,outfolder=output_folder)
# generator.set_threshold(threshold)
# generator.convert_dol_bar()
def store_features(name):

    pre = preprocess.Preprocess('./BTCUSDT/dol_bar.csv')
    df = pre.x_features1()
    df.to_csv("./BTCUSDT/features_close.csv")
    df = pre.clean_df() 
    df.to_csv("./BTCUSDT/features_close_clean.csv")
    print(name)

def store_features2(name):
    pre = preprocess.Preprocess('./BTCUSDT/dol_bar.csv')
    df = pre.x_feature2()
    df.to_csv("./BTCUSDT/features_min.csv")
    df = pre.clean_df() 
    df.to_csv("./BTCUSDT/features_min_clean.csv")
    print(name)


# combine features with labels 
label_file = ['./BTCUSDT/labels_vol_close.csv','./BTCUSDT/labels_fix_close.csv','./BTCUSDT/labels_vol_min.csv','./BTCUSDT/labels_fix_min.csv']
feature_file = ['./BTCUSDT/features_close_clean.csv','./BTCUSDT/features_min_clean.csv']
x = pd.read_csv(feature_file[0],index_col=0)
x.index = pd.to_datetime(x.date_time)
x.drop(columns=['date_time'],inplace=True)
y = pd.read_csv(label_file[1],index_col=0)
y.index = pd.to_datetime(y.index)
#useless_cols = {'tick_num', 'open', 'high', 'low', 'close', 'volume', 'cum_buy_volume','cum_ticks', 
#                'cum_dollar_value', 'avg', 'upper', 'lower', 'side','sma'}
useless_cols = {'tick_num', 'open', 'high', 'low', 'close', 'volume', 'cum_buy_volume','cum_ticks', 
                'cum_dollar_value', 'avg', 'upper', 'lower', 'side','sma'}
cols = [i for i in x.columns if i not in useless_cols]

x = x[cols]
x['y'] = y.bin
# print(x.isnull().sum(axis = 0))
# print(x.shape)
x.dropna(axis=0,inplace=True) # shouldn't be here
# print(x[x.y==0].shape)
# print(x[x.y==1].shape)
# print(x.shape)
# # print(y.head())
# # print(x.shape)
# # print(y.shape)
outfile = './BTCUSDT/x_y_close_fix.csv'
x.to_csv(outfile)