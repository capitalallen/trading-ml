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
def trade_ex():
    db_name= "../pair_db/features.sqlite"
    record_name="BTCUSDT"
    threshold = 7127690.2
    column_path = "column_order.json"
    pair ="BTCUSDT"
    trigger_per=1 
    deviation=1
    stop_loss_per= 2
    message_func = send_sms.Send_message()
    #configs = change_config.Change_config() 
    while True:
        val = input("1 for sync; 2 for start trading; 3 for quite: ")
        if val == "1":
            ss = sync_sql.sync_dol_bar(pair,db_name,record_name,threshold)
        elif val == "2":
            t = trading.Trading(pair=pair,db_name=db_name,record_name=record_name,threshold=threshold,model_path="model.joblib",columns_path=column_path)
            while True:
                result = t.live_trading()
                if result == "long":
                    try:
                        p_q = trade_long_short.get_quantity(pair,"long")
                        #pair,long_price,quantity,trade_type='long',trigger_per=1, deviation=0.5, stop_loss_per=2
                        message_func.send_a_message("BTC long price: "+ str(p_q['price']) + " quantity: "+ str(p_q['quantity']))
                        Process(target=trailing_mkt.limit_long_trailing, args=(pair,p_q['price'],p_q['quantity'],'long',trigger_per,deviation,stop_loss_per,)).start()
                    except Exception as e:
                        message_func.send_a_message("BTC long buy failed "+str(e))
                elif result == 'short':
                    result_error = ""
                    try:
                        p_q = trade_long_short.get_quantity(pair,"short")
                        #pair,quantity,trade_type='long',trigger_per=1, deviation=0.5, stop_loss_per=2
                        message_func.send_a_message("BTC long price: "+ str(p_q['price']) + " quantity: "+ str(p_q['quantity']))
                        result_error = str(p_q['price']) + " " +str(p_q['quantity'])+" "
                        Process(target=trailing_mkt.limit_short_trailing, args=(pair,p_q['price'],p_q['quantity'],'short',trigger_per,deviation,stop_loss_per,)).start()
                    except Exception as e:
                        message_func.send_a_message("BTC short buy failed "+result_error+str(e))
                time.sleep(150)
        elif val=="3":
            break

trade_ex()
