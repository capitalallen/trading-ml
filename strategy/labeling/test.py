
import filter_label as fl
import matplotlib.pyplot as plt 
import pandas as pd 
f = fl.Filter_label("x_features.csv")
l_vol = pd.read_csv("label_vol.csv",index_col=0)
l_vol.index = pd.to_datetime(l_vol.index)
l_fix = pd.read_csv('label_fix.csv',index_col=0)
l_fix.index = pd.to_datetime(l_fix.index)
# f.cusum_filter()
# df = f.triple_barrier()
# df.to_csv('label_fix.csv')



"""
dollar bar vs daily volitaty
"""
# df1 = f.get_df()
# df2 = f.get_daily_vol()
# df2['close']=2
# print(df2)
# print(df2.columns)
# fig,axs = plt.subplots(2,1)
# axs[0].plot(df1.index,df1['close'])
# axs[1].plot(df2.index,df2['close'])
# plt.show()


"""
compare two types of labels 
"""
l_vol.fillna(0,inplace=True)
l_fix.fillna(0,inplace=True)
fig,axs = plt.subplots(2,1)
axs[0].plot(l_vol.index,l_vol['ret'])
axs[1].plot(l_fix.index,l_fix['ret'])
plt.show()