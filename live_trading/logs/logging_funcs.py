# import json 

# class Change_config:
#     def __init__(self,file):
#         self.file = file
#         self.data =None 
#     def load_config(self):
import pymongo
from time import gmtime, strftime  
class Logging:
    def __init__(self):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["configs"]
        self.mycol = self.mydb["logs"]
    def insert_log(self,message):
        # myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        # mydb = myclient["configs"]
        time = str(strftime("%Y-%m-%d %H:%M:%S", gmtime())  )
        self.mycol.insert_one({time:message})
    
    def get_all_logs(self):
        cursor = self.mycol.find({})
        result = []
        for i in cursor:
            result.append(i)
        return result

def test_func():
    print("test")