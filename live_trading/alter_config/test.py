import pymongo
import change_config
cc=change_config.Change_config() 
#cc.update_trading_num("long",5)
#cc.update_trading_num("short",3)
print(cc.get_trading_num())
#myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#mydb = myclient["configs"]
#mycol = mydb["total_trade_num"]
#mycol.update({"_id":mycol.find_one()['_id']},{"$set":{"transaction_long":100,"transaction_short":150}})
#print(mycol.find_one())
#mydict = {"long":10,"short":10,"time":None}
#mycol.insert_one(mydict)

#cc = change_config.Change_config()
# # print(type(cc.query_config("ETHUSDT","long")))
#cc.update_trading_num("long",5)
#cc.update_trading_num("long",1)
#cc.init_pair_config("XRPUSDT")
# cc.init_pair_config("BNBUSDT")
# cc.init_pair_config("IOTAUSDT")
# cc.init_pair_config("LTCUSDT")
# cc.init_pair_config("NEOUSDT")
# cc.init_pair_config("EOSUSDT")
# cc.init_pair_config("ETCUSDT")
# cc.init_pair_config("BTCUSDT")
