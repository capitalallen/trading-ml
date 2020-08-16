import get_data as gd 
import pandas as pd 

import time
start_time = time.time()

df = pd.read_csv('x_features.csv',index_col=0)
df.index = pd.to_datetime(df.index)
d = str(df.iloc[-1:].index[0])
df = gd.get_klines_df(d,interval="12h")
# df = gd.convert_raw_data(d,interval="12h")
dol = gd.form_dol_bar(df,1851265300)
print(dol)
# print(gd.is_limit(k,3099318401.0))

print("--- %s seconds ---" % (time.time() - start_time))