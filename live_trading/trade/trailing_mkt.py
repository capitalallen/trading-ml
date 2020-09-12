import trailing 
import transaction 
import sys 
sys.path.append("../alter_config")
sys.path.append('../price_getter')
import change_config
import price 
import time 
"""
mkt long trailing 
buy with market price 
    - input: quantity 
    - side = LONG
call trailing with pric - buy-price 
"""
def mkt_long_trailing(pair,quantity,trade_type='long',trigger_per=1, deviation=0.5, stop_loss_per=2):
    configs = change_config.Change_config() 
    transaction_func = transaction.Buy_sell()
    trailing_func = trailing.Trailing(q=quantity,trade_type=trade_type,trigger_per=trigger_per, deviation=deviation, stop_loss_per=stop_loss_per, pair=pair)
    # buy 
    buy = transaction_func.mkt_buy_sell_future(pair=pair,quantity=quantity,positionSide="LONG",side='BUY')
    # trailing 
    configs.update_trading_num("long",-1)
    trailing_func.trailing_stop_long()
    configs.update_trading_num("long",1)
    print("successful")
def mkt_short_trailing(pair,quantity,trade_type='short',trigger_per=1, deviation=0.5, stop_loss_per=2):
    configs = change_config.Change_config()
    transaction_func = transaction.Buy_sell()
    trailing_func = trailing.Trailing(q=quantity,trade_type=trade_type,trigger_per=trigger_per, deviation=deviation, stop_loss_per=stop_loss_per, pair=pair)
    # buy 
    configs.update_trading_num("short",-1)
    buy = transaction_func.mkt_buy_sell_future(pair=pair,quantity=quantity,positionSide="SHORT",side='SELL')
    # trailing 
    configs.update_trading_num("long",-1)
    trailing_func.trailing_stop_short()
    print("successful")


def limit_long_trailing(pair,long_price,quantity,trade_type='long',trigger_per=1, deviation=0.5, stop_loss_per=2):
    configs = change_config.Change_config() 
    transaction_func = transaction.Buy_sell()
    # buy 
    """
    get order_time 
    while curr_price is higher than price
        sleep 1.5 second 
        get current price 
        if current time > order_time +2h:
            print time expired 
            return 
    else: 
        buy 
    """
    # trailing 
    configs.update_trading_num("long",-1)
    configs.update_long_trade_avl(pair,-1)
    start_time = int(time.time())
    curr_price = price.get_price(pair)
    while curr_price>long_price:
        print("current price: " + str(curr_price) + "| long price:" + str(long_price))
        time.sleep(1.5)
        if int(time.time())>start_time+7200:
            print("time expired")
            configs.update_trading_num("long",1)
            configs.update_long_trade_avl(pair,1)
            return 
        curr_price = price.get_price(pair)
    else:
        buy = transaction_func.mkt_buy_sell_future(pair=pair,quantity=quantity,positionSide="LONG",side='BUY')
        print("bought at "+ str(curr_price))
    trailing_func = trailing.Trailing(q=quantity,trade_type=trade_type,trigger_per=trigger_per, deviation=deviation, stop_loss_per=stop_loss_per, pair=pair,)
    trailing_func.trailing_stop_long()
    configs.update_trading_num("long",1)
    configs.update_long_trade_avl(pair,1)
    print("successful")
def limit_short_trailing(pair,short_price,quantity,trade_type='short',trigger_per=1, deviation=0.5, stop_loss_per=2):
    configs = change_config.Change_config()
    transaction_func = transaction.Buy_sell()
    # buy
    """
    get order_time 
    while curr_price is higher than price
        sleep 1.5 second 
        get current price 
        if current time > order_time +2h:
            print time expired 
            return 
    else: 
        buy 
    """
    # update trade number allowed
    configs.update_trading_num("short",-1)
    configs.update_short_trade_avl(pair,-1)
    start_time = int(time.time())
    curr_price = price.get_price(pair)
    print("current price:",curr_price)
    while curr_price < short_price:
        print("current price: " + str(curr_price) + "| long price:" + str(short_price))
        time.sleep(1.5)
        if int(time.time())>start_time+7200:
            print("time expired")
            configs.update_trading_num("short",1)
            configs.update_short_trade_avl(pair,1)
            return 
        curr_price = price.get_price(pair)  
    else:     
        buy = transaction_func.mkt_buy_sell_future(pair=pair,quantity=quantity,positionSide="SHORT",side='SELL')
    # trailing 
    trailing_func = trailing.Trailing(q=quantity,trade_type=trade_type,trigger_per=trigger_per, deviation=deviation, stop_loss_per=stop_loss_per, pair=pair)
    trailing_func.trailing_stop_short()
    
    configs.update_trading_num("short",1)
    configs.update_short_trade_avl(pair,1)
    
    print("successful")
