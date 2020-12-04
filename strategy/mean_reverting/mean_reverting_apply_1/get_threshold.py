import pandas as pd 
import numpy as np 
def threshold_getter_50(pair):
    path = "./"+pair+"/"+"daily_timebar.csv"
    df = pd.read_csv(path)
    return np.sum((df['open']+df['close'])/2*df['volume'])/df.shape[0]/50
def threshold_getter_100(pair):
    path = "./"+pair+"/"+"daily_timebar.csv"
    df = pd.read_csv(path)
    return np.sum((df['open']+df['close'])/2*df['volume'])/df.shape[0]/100
# pair = "BNBUSDT"
# print(threshold_getter_50(pair))
import sys
print("type: 50 or 100; pair name")
t = sys.argv[1]

if t =="50":
    print(threshold_getter_50(sys.argv[2]))
elif t=="100":
    print(threshold_getter_50(sys.argv[2]))

