import pymongo
import change_config
# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["configs"]
# mycol = mydb["total_trade_num"]
# mydict = {"long":5,"short":5,"time":None}
# mycol.insert_one(mydict)

cc = change_config.Change_config()
# print(type(cc.query_config("ETHUSDT","long")))
cc.update_trading_num("long",1)
# cc.update_trading_num("long",1)
# cc.init_pair_config("ETHUSDT")
# cc.init_pair_config("BNBUSDT")
# cc.init_pair_config("IOTAUSDT")
# cc.init_pair_config("LTCUSDT")
# cc.init_pair_config("NEOUSDT")
# cc.init_pair_config("EOSUSDT")
# cc.init_pair_config("ETCUSDT")
# cc.init_pair_config("BTCUSDT")