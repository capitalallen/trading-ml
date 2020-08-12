import matplotlib.pyplot as plt 
import pandas as pd 
import seaborn as sns
import numpy as np 
from preprocess import Preprocess
from features import Features
f = Features()

df1 = pd.read_csv("x_features.csv",index_col=0)
# df1['date_time'] = pd.to_datetime(df1.date_time)
df1.index = pd.to_datetime(df1.date_time)
df1.drop(columns=['date_time'],inplace=True)
print(df1.columns)
clean_df1 = pd.read_csv("clean_x_features.csv",index_col=0)
# clean_df1['date_time'] = pd.to_datetime(clean_df1.date_time)
clean_df1.index = pd.to_datetime(clean_df1.date_time)
clean_df1.drop(columns=['date_time'],inplace=True)
# pre = Preprocess("dol_bar.csv")
# pre.x_features1() 
# df1 = pre.clean_df()
# df1.info(memory_usage="deep")
# df1.to_csv('clean_x_features.csv')
# df1.isnull().sum()
# sns.heatmap(df1.isnull(),cmap="viridis")
# plt.show()
# df2 = pd.read_csv('BTCUSDT-30m-data.csv')
# df2['timestamp'] = pd.to_datetime(df2.timestamp)
# print(df1.shape)
# print(df2.shape)
# # fig,axs = plt.subplots(2,1,sharey=False)
# # axs[0].plot(df1['date_time'],df1['close'])
# # axs[1].plot(df2['timestamp'],df2['close'])
# # plt.show()

# sns.set(context="notebook", style="darkgrid", palette="deep", font="sans-serif", font_scale=1, color_codes=True)
# df1 = f.add_rsi(df1)
# df1 = f.add_srsi(df1)
# df1.drop(columns=['tick_num','date_time', 'open', 'high', 'low', 'close', 'volume', 'cum_buy_volume','cum_ticks', 'cum_dollar_value', 'avg', 'upper', 'lower', 'side',],inplace=True)
# print(df1.columns)
#correlation 
# sns.heatmap(df1.corr(),cmap="YlGnBu",square=True,linewidths=.5,center=0,linecolor="red")
# plt.show()

# corr_matrix = df1.corr().abs()
# high_corr_var=np.where(corr_matrix>0.6)
# high_corr_var=[(corr_matrix.columns[x],corr_matrix.columns[y]) for x,y in zip(*high_corr_var) if x!=y and x<y]
# print(high_corr_var)


# group by month and plot the count
# plt.plot(clean_df1.index,clean_df1['close'])
# plt.show()

# labeling 
# pre = Preprocess("dol_bar.csv")
# l = pre.labeling(df1)
# l.to_csv('labels.csv')
l = pd.read_csv('labels.csv',index_col=0)
l.index = pd.to_datetime(l.index)
one = l[l['bin']==1]
one_data = clean_df1[one.index]
print(one_data.head())
# plt.plot(clean_df1.index,clean_df1['close'])
# plt.scatter(one_data.index,one_data['close'])
# plt.show()