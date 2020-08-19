# import json 

# class Change_config:
#     def __init__(self,file):
#         self.file = file
#         self.data =None 
#     def load_config(self):
import pymongo
class Change_config:
    def __init__(self):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["configs"]

    def init_pair_config(self,pair_name):
        # myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        # mydb = myclient["configs"]
        mycol = self.mydb[pair_name]
        mydict = {
            "long":True,
            "short":True,
            "time":None,
            "lev_long":50,
            "lev_short":50,
            "long_trades_avl":4,
            "short_trades_avl":4,
            "long_trades_limit":4,
            "short_trades_limit":4,
            "long_strategy":{
                "side":1,
                "pred":1
            },
            "short_strategy":{
                "side":-1, 
                "pred":0
            },
            "long_p":0,
            "short_p":0
        }
        x = mycol.insert_one(mydict)

    def get_pair_config(self,pair_name):
        # myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        # mydb = myclient["configs"]
        mycol = self.mydb[pair_name]

        return mycol.find_one()

    def query_config(self,pair_name,item):
        return self.get_pair_config(pair_name)[item]
    
    def update_config(self,pair_name,item,value):
        mycol = self.mydb[pair_name]
        myquery = {item:self.query_config(pair_name,item)}
        newvalues = {"$set":{item:value}}
        mycol.update_one(myquery,newvalues)
    
    def get_trading_num(self):
        mycol = self.mydb["total_trade_num"]
        return mycol.find_one() 
    
    def update_trading_num(self,trade_type,n):
        mycol = self.mydb["total_trade_num"]
        val = self.get_trading_num()[trade_type]
        myquery = {trade_type:val}
        newvalues = {"$set":{trade_type:val+n}}
        mycol.update_one(myquery,newvalues)

# m = Change_config() 
# print(m.get_pair_config("BTCUSDT"))
# m.update_config("BTCUSDT","long",False)
# tmp = m.query_config("BTCUSDT","long_strategy")
# print(type(tmp))