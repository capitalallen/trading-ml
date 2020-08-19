import pandas as pd 
import sqlite3 

class Preprocess_sql:
    def __init__(self,db_path,record_name):
        self.db_path = db_path 
        self.record_name = record_name 
    # retrive last n rows of data and convert to df 
    def get_last_n(self,n):
        print(self.db_path)
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor() 
        statement = 'SELECT * FROM ' + self.record_name + ' ORDER BY date_time DESC LIMIT '+str(n)
        rows = cur.execute(statement)
        df = pd.read_sql_query(statement,conn)
        df.date_time = pd.to_datetime(df.date_time)
        return df 
        conn.close()
    
    # store df to sql 
    # notice index 
    def store_df(self,df):
        try:
            conn = sqlite3.connect(self.db_path)
            df.to_sql(self.record_name,con=conn, if_exists='append') 
            conn.close()
        except:
            print("insert failed")