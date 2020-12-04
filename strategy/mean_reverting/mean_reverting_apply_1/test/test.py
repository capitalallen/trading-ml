import pandas as pd 

df = pd.read_csv('./BTCUSDT/x_features.csv',index_col=0)
print(df.head())
print(df.columns)
df = df[['mom1', 'mom2', 'mom3', 'mom4', 'mom5', 'log_ret',
       'autocorr_1', 'autocorr_2', 'autocorr_3', 'autocorr_4',
       'autocorr_5', 'log_t1', 'log_t2', 'log_t3', 'log_t4', 'log_t5','volatility','rsi']]
print(df.head())
print(df.columns)