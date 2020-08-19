import trailing 
import transaction 
import sys 
sys.path.append("../alter_config")
import change_config
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
    transaction_func = transaction.Buy_sell()
    trailing_func = trailing.Trailing(q=quantity,trade_type=trade_type,trigger_per=trigger_per, deviation=deviation, stop_loss_per=stop_loss_per, pair=pair)
    # buy 
    configs.update_trading_num("short",-1)
    buy = transaction_func.mkt_buy_sell_future(pair=pair,quantity=quantity,positionSide="SHORT",side='BUY')
    # trailing 
    configs.update_trading_num("long",-1)
    trailing_func.trailing_stop_short()
    print("successful")
