from features import Features
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
f = Features()
df = pd.read_csv('test.csv', index_col=0)
df.date_time = pd.to_datetime(df['date_time'])
# df = f.add_bbands(df)
# df = f.compute_side(df)
k = f.add_kdj(df)

# print(df.columns)
# print(type(k.indx))

# df = f.add_momantum(df)
# df = f.add_volatility(df)
# df = f.add_serial_correlation(df)
# df = f.add_log_returns(df)
# df = f.mov_average(df)
# df = f.add_trending_signal(df)
df.to_csv('demo.csv')
