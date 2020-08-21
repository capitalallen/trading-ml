import trading 
import sys 
from multiprocessing import Process
sys.path.append("../handle_sql")
sys.path.append('../trade')
sys.path.append('../message')
import sync_sql
import trailing_mkt
import trade_long_short 
import send_sms
import time
def trade_ex(val):
    db_name= "../pair_db/features.sqlite"
    record_name="XRPUSDT"
    threshold = 701268.8
    column_path = "../XRPUSDT/column_order.json"
    pair ="XRPUSDT"
    trigger_per=1 
    deviation=0.5
    stop_loss_per= 2
    message_func = send_sms.Send_message()
    #configs = change_config.Change_config() 
    if val == 1:
        ss = sync_sql.sync_dol_bar(pair,db_name,record_name,threshold)
    elif val == 2:
        t = trading.Trading(pair=pair,db_name=db_name,record_name=record_name,threshold=threshold,model_path="../XRPUSDT/model.joblib",columns_path=column_path)
        while True:
            result = t.live_trading()
            print("-----XRP---------")
            if result == "long":
                print("-----XRP long------")
                try:
                    quantity = trade_long_short.get_quantity(pair,"long")
                    # pair,quantity,trade_type='long',trigger_per=1, deviation=0.5, stop_loss_per=2
                    Process(target=trailing_mkt.mkt_long_trailing, args=(pair,quantity,'long',trigger_per,deviation,stop_loss_per,)).start()
                except:
                    message_func.send_a_message("long buy failed")
            elif result == 'short':
                print("-----XRP short------")
                try:
                    quantity = trade_long_short.get_quantity(pair,"short")
                    # pair,quantity,trade_type='long',trigger_per=1, deviation=0.5, stop_loss_per=2
                    Process(target=trailing_mkt.mkt_short_trailing, args=(pair,quantity,'short',trigger_per,deviation,stop_loss_per,)).start()
                except:
                    message_func.send_a_message("short buy failed")
            time.sleep(150)
