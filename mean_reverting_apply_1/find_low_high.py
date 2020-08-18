import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import json 
def save_low_high(path):
    x_path = path + "x_features.csv"
    df = pd.read_csv(x_path,index_col=0)
    df.index = pd.to_datetime(df.date_time)
    df.drop(columns=["date_time"],inplace=True)
    col = ['tick_num','open','high','low','close']
    df = df[col]

    df['lowest'] = np.nan
    df['highest'] = np.nan 
    n = 0
    for i, row in df.iterrows():
        df.at[i,'lowest'] = (df.iloc[n+1:n+5].low.min()-row['close'])/row['close']
        df.at[i,'highest'] = (df.iloc[n+1:n+5].high.max()-row['close'])/row['close']
        n+=1 
    y_path = path+"test_predictions.csv"
    df2 = pd.read_csv(y_path,index_col=0)
    df2.index = pd.to_datetime(df2.index)
    pos = df2[df2['0']==1]
    neg = df2[df2['0']==0]
    df_pos = df.loc[pos.index]
    df_neg = df.loc[neg.index]
    plt.scatter(df_pos.index,df_pos.lowest)
    plt.savefig(path+"pos_lowest.png")
    plt.close()
    
    plt.scatter(df_neg.index,df_neg.highest)
    plt.savefig(path+"neg_highest.png")
    plt.close()
    df.to_csv(path+"low_high.csv")

def low_high_stats(path):
    df = pd.read_csv(path+"low_high.csv",index_col=0)

    # > 0 
    df0 = df[df.lowest>0].shape[0]
    df1 = df[df.lowest<-0.01].shape[0]
    df2 = df[df.lowest<-0.02].shape[0]
    df3 = df[df.lowest<0].shape[0]
    low = {">0":df0/df.shape[0],
           "-1%~0":(df3-df1)/df.shape[0],
           "-2%~1%":(df1-df2)/df.shape[0],
           "<-2%":df2/df.shape[0]}
    df0 = df[df.lowest<0].shape[0]
    df1 = df[df.lowest>=0.01].shape[0]
    df2 = df[df.lowest>0.02].shape[0]
    df3 = df[df.lowest>0].shape[0]
    high = {"0~0.01":(df3-df1)/df.shape[0],
           "0.01~0.02":(df1-df2)/df.shape[0],
           ">0.02":df2/df.shape[0],
           "<0":df0/df.shape[0]}
    with open(path+"long_short_range.json",'w') as f:
        json.dump({"long":low,"short":high},f)
path = "./BTCUSDT/"
low_high_stats(path)
# save_low_high(path)

# x_path = path + "x_features.csv"
# df = pd.read_csv(x_path,index_col=0)
# df.index = pd.to_datetime(df.date_time)
# df.drop(columns=["date_time"],inplace=True)

# y_path = path+"test_predictions.csv"
# df2 = pd.read_csv(y_path,index_col=0)
# df2.index = pd.to_datetime(df2.index)
# df3 = df.loc[df2.index]
# print(df3.head())