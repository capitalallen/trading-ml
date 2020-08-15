import pandas as pd 
import matplotlib.pyplot as plt 

f = ['./BTCUSDT/labels_vol_close.csv','./BTCUSDT/labels_fix_close.csv','./BTCUSDT/labels_vol_min.csv','./BTCUSDT/labels_fix_min.csv']

df_vol = pd.read_csv(f[2],index_col=0)
df_vol.index = pd.to_datetime(df_vol.index)
print(df_vol.bin.count())
s_vol = df_vol[df_vol.side==1]
z_vol = df_vol[df_vol.side==-1]

df_fix = pd.read_csv(f[3],index_col=0)
df_fix.index = pd.to_datetime(df_fix.index)
print(df_fix.bin.count())
s_fix = df_fix[df_fix.side==1]
z_fix = df_fix[df_fix.side==-1]

pos_vol = s_vol[s_vol.ret>0]
pos_fix = z_fix[z_fix.ret>0]
# tmp = pos_vol.index.intersection(pos_fix.index)
print(pos_vol.shape)
# pos_vol = pos_vol.drop(index=tmp.index)
# print(tmp.shape)
# plt.plot(s_vol.index,s_vol.ret,label="vol")
plt.plot(pos_fix.index,pos_fix.ret,label="fix")
plt.legend()
plt.show()


# df = pd.read_csv(f[2],index_col=0)
# df.index = pd.to_datetime(df.index)
# s = df[df.side==1]
# z = df[df.side==-1]

# print('side 1 vs 0 proportion')
# print('totoal 1 and -1:%d' % (s.shape[0]+z.shape[0]))
# print("side=1:",s.shape[0])
# print("side=0:",z.shape[0])
# print("side=1 %:",s.shape[0]/(s.shape[0]+z.shape[0]))

# # when side ==1 and ret>0
# pos = s[s.ret>0].shape[0]
# # print('side = 1, total return: ',s.ret.sum())
# print('side = 1, ret >0: ',pos)
# print("side = 1, ret >0:, %: ",pos/s.shape[0]*100)
# print("sum of rets: ",s.ret.sum())
# plt.plot(s.index,s.ret)
# plt.plot(s.index,s.trgt)
# plt.show()
# print("")
# # when side ==-1 and ret<0
# neg = z[z.ret>0].shape[0]
# # print("side = -1, total return: ",z.ret.sum())
# print('side = -1, ret <0: ',neg)
# print("side = -1, ret <0:, %: ",neg/z.shape[0]*100)
# print("sum of rets: ",z.ret.sum())
# plt.plot(z.index,z.ret)
# plt.plot(z.index,z.trgt)
# plt.show()