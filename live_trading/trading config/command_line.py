import change_config 

cc = change_config.Change_config()
while True: 
    option = input("1: update int, 2: get current, 3: quit, 4: update float, 5: update boolean")
    if int(option)==1:
        pair = input("pair name?")
        print("long,short,lev_long,lev_short,long_trades_avl,short_trade_avl,long_p,short_p,long_amount,short_amount")
        entry = input("which entry to change?")
        value = int(input("value?"))
        cc.update_config(pair,entry,value)
    elif int(option)==2:
        pair = input("pair name?")
        print(cc.get_pair_config(pair))
    elif int(option)==4:
        pair = input("pair name?")
        print("long,short,lev_long,lev_short,long_trades_avl,short_trade_avl,long_p,short_p,long_amount,short_amount")
        entry = input("which entry to change?")
        value = float(input("value?"))
        cc.update_config(pair,entry,value)
    elif int(option)==5:
        pair = input("pair name?")
        print("long,short,lev_long,lev_short,long_trades_avl,short_trade_avl,long_p,short_p,long_amount,short_amount")
        entry = input("which entry to change?")
        value = bool(input("value?"))
        cc.update_config(pair,entry,value)
    else:
        break
