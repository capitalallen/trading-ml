import change_config 

cc = change_config.Change_config()
while True: 
    option = input("1: update, 2: get current, 3:quit")
    if int(option)==1:
        pair = input("pair name?")
        print("long,short,lev_long,lev_short,long_trades_avl,short_trade_avl,long_p,short_p,long_amount,short_amount")
        entry = input("which entry to change?")
        value = input("value?")
        cc.update_config(pair,entry,value)
    elif int(option)==2:
        pair = input("pair name?")
        print(cc.get_pair_config(pair))
    else:
        break