import sys 
sys.path.append("../logs_use")
sys.path.append("../model_use")
sys.path.append('../handle_db')
import logging 
import get_predict
import configparser
# import sync_sql
# g = get_predict.Get_predict()
# l = logging.test_func()
config_func = configparser.ConfigParser() 

config_func.read("config.init")
pair = config_func.get("control","db_name")
# print(pair)
import sqlite3 
conn = sqlite3.connect(pair)