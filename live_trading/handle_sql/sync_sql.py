import pandas as pd 
import preprocess_sql as psql
import sys 
sys.path.append("../preprocessing")
sys.path.append("../data_getter")
import proprecess 
import get_data 
"""
get dol_bar
add feature to dol_bar 
store to sql 
"""
# df = pd.read_csv('dol_bar.csv',index_col=0)
# threshold = df.cum_dollar_value.sum()/df.shape[0]
# print(threshold)
# df.date_time = pd.to_datetime(df.date_time)
# df1 = df.iloc[-30:-20]
# df2 = df.iloc[-20:]

# p = proprecess.Proprecessing() 
# p.combine_df(df1,df2)
# p.add_features()
# df2 = p.get_df2()
# print(df2.head())
# pre_sql = psql.Preprocess_sql('features.sqlite',"x_features") 
# pre_sql.store_df(df2)

"""
sync dol bar 
"""
def sync_dol_bar(pair,db_name,record_name,threhold,interval='1m'):
    #get time of last row from db 
    # 'features.sqlite',"x_features"
    pre_sql = psql.Preprocess_sql(db_name,record_name) 
    time = str(pre_sql.get_last_n(1).date_time[0])
    if get_data.is_limit(klines,threhold):
        # get klines from last time to current time 
        klines = get_data.get_klines_df(time,symbol=pair,interval=interval)
        #convert klines to dol_bar
        dol_bar = get_data.form_dol_bar(klines,threhold)

        # get last 25 rows 
        # combine them to nwe dol bar 
        #calculate features 
        #get only df2 
        #store to db 
        last_twenty = pre_sql.get_last_n(25)
        p = proprecess.Proprecessing()
        p.combine_df(last_twenty,dol_bar)
        p.add_features()
        new_bars = p.get_df2() 
        pre_sql.store_df(new_bars)
        print("finished")
    else:
        print("up to date")
# sync_dol_bar("ETHUSDT",'features.sqlite',"x_features",8636198,interval="15m")
