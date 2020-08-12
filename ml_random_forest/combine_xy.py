import pandas as pd 

# drop unnecessary columns and add one y column to the df 
# store to csv 

x = pd.read_csv("clean_x_features.csv",index_col=0)
x.index = pd.to_datetime(x.date_time)
x.drop(columns=['date_time'],inplace=True)
y = pd.read_csv('label_vol.csv',index_col=0)
y.index = pd.to_datetime(y.index)
x = x[['mom1', 'mom2', 'mom3', 'mom4', 'mom5',
       'autocorr_1', 'autocorr_2', 'autocorr_3', 'autocorr_4',
       'autocorr_5', 'log_t1', 'log_t2', 'log_t3', 'log_t4', 'log_t5', 'log_ret','volatility']]

x['y'] = y.bin
# y = y[x.index]
x.fillna(0,inplace=True) # shouldn't be here 
# print(y.head())
# print(x.shape)
# print(y.shape)
x.to_csv('training.csv')