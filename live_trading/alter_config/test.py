import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["configs"]
mycol = mydb["total_trade_num"]
mydict = {"long":5,"short":5,"time":None}
mycol.insert_one(mydict)