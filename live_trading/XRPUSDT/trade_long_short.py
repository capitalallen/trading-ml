import sys 
sys.path.append("../price_getter")
sys.path.append("../alter_config")
sys.path.append("../trade")
sys.path.append("../message")
import price 
import change_config 
import transaction
import send_sms
"""
input: pair 
- get transaction_long or transaction_short 
- get levg_long or lev_short 
- get price 
- get discount rate 
"""
def get_configs(pair,type):
    config_func = change_config.Change_config()
    controls = config_func.get_pair_config(pair)
    configs = {}
    if type == "long":
        transactions = config_func.get_trading_num()
        
        lev_long = controls['lev_long']
        dicount_rate=controls['long_p']
        # precision 
        curr_price = round(price.get_price(pair),3)

        configs['discount_rate']=dicount_rate
        configs['price']=curr_price
        configs["transaction"]=transactions['transaction_long']
        configs['leverage_rate'] = controls['lev_long']
        if not configs['discount_rate']:
            configs['price'] = configs['price']*(1-configs['discount_rate'])
    elif type=="short":
        transactions = config_func.get_trading_num()

        lev_long = controls['lev_short']
        dicount_rate=controls['short_p']
        curr_price = round(price.get_price(pair),3)

        configs['discount_rate']=dicount_rate
        configs['price']=curr_price
        configs["transaction"]=transactions['transaction_short']
        configs['leverage_rate'] = controls['lev_short']
        if not configs['discount_rate']:
            configs['price'] = configs['price']*(1+configs['discount_rate'])
    else:
        print("type invalid")
    return configs

def compute_quantity(configs):
    q = configs['leverage_rate']*configs['transaction']/configs['price'] 
    print(configs['transaction'],configs['price'] )
    return round(q*0.9,2)

def get_quantity(pair,type):
    configs = get_configs(pair,type)
    price = configs['price']
    quantity = compute_quantity(configs)
    return {'price':price,'quantity':quantity}
    
def trade_long_ex(pair="ETHUSDT"):
    configs = get_configs(pair,"long")
    quantity = compute_quantity(configs)
    trade_ex = transaction.Buy_sell()
    his = trade_ex.trailing_stop_mkt_future(pair=pair,price=configs['price'],q=quantity,side="BUY",leverage=configs['leverage_rate'])
    #long with mkt price
    configs['price']=None
    message = pair +" long at " + str(configs['price']) + ". Quantity: "+str(quantity)
    mess = send_sms.Send_message()
    mess.send_a_message(message)
    return his 
def trade_short_ex(pair="ETHUSDT"):
    configs = get_configs(pair,"short")
    quantity = compute_quantity(configs)
    trade_ex = transaction.Buy_sell()
    #short with mkt price
    configs['price']=None
    his = trade_ex.trailing_stop_mkt_future(pair=pair,price=configs['price'],q=quantity,side="SELL",positionSide="SHORT",leverage=configs['leverage_rate'])
    
    message = pair +" short at " + str(configs['price']) + ". Quantity: "+str(quantity)
    mess = send_sms.Send_message()
    mess.send_a_message(message)
    return his 
# print(b)
# a = compute_quantity(b)

# print(a)
# print(get_configs("BTCUSDT","short"))