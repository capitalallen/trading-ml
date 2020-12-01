import pandas as pd 
import sqlite3 
def convert_to_sql(db='../pair_db/features.sqlite',record="x_features"):
    try:
        conn = sqlite3.connect(db)
        #if the count is 1, then table exists
        # if not convert csv_file to record and print 
        df = pd.read_csv('x_features.csv',index_col=0)
        df.date_time = pd.to_datetime(df.date_time)
        df = df.iloc[df.shape[0]-100:]
        # df.rename(columns={"Unnamed: 0":"i"},inplace=True)
        df.to_sql(record, con=conn)
        conn.close()
    except:
        print('record exists')
# convert_to_sql(record="XRPUSDT")