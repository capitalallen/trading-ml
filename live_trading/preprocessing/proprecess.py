import pandas as pd 
import sys
sys.path.append("../features")
sys.path.append("../handle_sql")
import Features 
import preprocess_sql
class Proprecessing:
    def __init__(self):
        pass 

    def combine_df(self,df1,df2):
        self.df2_start_index = df1.shape[0]
        df1 = df1[list(df2.columns)]
        self.df = df1.append(df2)
        self.df2 = df2 
    
    # add features to dol_bar 
    def add_features(self):
        f = Features.Features(self.df)
        f.add_bbands()
        f.compute_side_min()
        f.add_momantum()
        f.add_volatility()
        f.add_serial_correlation()
        f.add_log_returns()
        f.mov_average()
        f.add_rsi()
        f.add_srsi()
        f.add_trending_signal()
    
    def get_df2(self):
        return self.df.iloc[self.df2_start_index:]
    
    def get_df2_test(self):
        return self.df2

    #@staticmethod
    def get_last_row(self,db_name,record_name,n=1):
        p = preprocess_sql.Preprocess_sql(db_name,record_name)
        return p.get_last_n(n)