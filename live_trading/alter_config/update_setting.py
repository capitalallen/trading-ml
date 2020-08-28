import change_config 

def update_settings(cols):
    cc = change_config.Change_config()
    for i in cols: 
        cc.add_amount_entry(i)

cols = ["BNBUSDT","BTCUSDT","ETHUSDT","XRPUSDT"]
update_settings(cols)
# cc = change_config.Change_config()
# # cc.update_long_trade_avl("BTCUSDT",1)
# cc.update_short_trade_avl("BTCUSDT",-1)
# # cc.get_trade_avl('BTCUSDT','long')
# cc.get_trade_avl('BTCUSDT','short')