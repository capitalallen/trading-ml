import trading 
import sys 
sys.path.append("../handle_sql")
import sync_sql
import time
def trade_ex():
    db_name= "../pair_db/features.sqlite"
    record_name="ETHUSDT"
    threshold = 7127690
    column_path = "column_order.json"
    pair = "ETHUSDT"
    while True:
        val = input("1 for sync; 2 for start trading; 3 for quite: ")
        if val == "1":
            ss = sync_sql.sync_dol_bar(pair,db_name,record_name,threshold)
        elif val == "2":
            t = trading.Trading(pair=pair,db_name=db_name,record_name=record_name,threshold=threshold,model_path="model.joblib",columns_path=column_path)
            while True:
                t.live_trading()
                time.sleep(200)
        elif val=="3":
            break

trade_ex()
