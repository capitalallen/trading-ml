import pandas as pd 
import sys
import json 
sys.path.append("../model_use")
sys.path.append("../alter_config")
sys.path.append("../data_getter")
sys.path.append("../handle_sql")
sys.path.append("../preprocessing")
# sys.path.append("../mean_reverting")
import get_predict
import change_config
import preprocess_sql as psql
import get_data
import proprecess 

"""

if side is not none 
    get only feature column from df columns 
    pred = get prediction
    if pred = config.long.pred and side = config.long.side:
        trade_long(pair, leverage)
        total trade # allowed - 1 
    elif pred = config.short.pred and side = config.short.side:
        trade_short(pair,leverage)
        total trade # allowed - 1 
"""
class Trading: 
    def __init__(self,pair,db_name,record_name,threshold,interval='1m',model_path=None,columns_path=None):
        self.predict = get_predict.Get_predict()
        self.predict.load_model(model_path)
        self.columns = json.load(open(columns_path))['columns']
        self.configs = change_config.Change_config() 
        self.pair = pair 
        self.interval = interval
        self.db_name = db_name 
        self.record_name = record_name 
        self.threshold = threshold    
        self.load_long_strategy()
        self.load_short_strategy()

        #connect to sql database 
        self.pre_sql = psql.Preprocess_sql(self.db_name,self.record_name)
    def load_long_strategy(self):
        self.long_strategy = self.configs.query_config(self.pair,"long_strategy")
    
    def load_short_strategy(self):
        self.short_strategy = self.configs.query_config(self.pair,"short_strategy")

    def live_trading(self):
        time = str(self.pre_sql.get_last_n(1).date_time[0])
        # get klines from last time to current time 
        klines = get_data.get_klines_df(time,symbol=self.pair,interval=self.interval)
        if get_data.is_limit(klines,self.threshold):
            #convert klines to dol_bar
            dol_bar = get_data.form_dol_bar(klines,self.threshold)

            # get last 25 rows 
            # combine them to nwe dol bar 
            #calculate features 
            #get only df2 
            #store to db 
            last_twenty = self.pre_sql.get_last_n(25)
            p = proprecess.Proprecessing()
            p.combine_df(last_twenty,dol_bar)
            p.add_features()
            new_bars = p.get_df2() 
            self.pre_sql.store_df(new_bars)
            df = new_bars.iloc[-1]
            
            if new_bars['side']:
                features = df[self.columns].tolist()
                pred = int(self.predict.predict([features])[0])
                num_allowed = self.configs.get_trading_num()
                if num_allowed['long']>0 and pred == self.long_strategy["pred"] and side == self.long_strategy["side"]:
                    print("trade long")
                    self.configs.update_trading_num("long",-1)
                elif num_allowed['short']>0 and pred == self.short_strategy["pred"] and side == self.short_strategy["side"]:
                    print("trade short")
                    self.configs.update_trading_num("short",-1)