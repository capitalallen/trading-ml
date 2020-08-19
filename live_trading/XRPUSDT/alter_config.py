import sys 
sys.path.append('../alter_config')
import change_config 

# "long_strategy" or short_strategy
def change_strategy(pred,side,pair='ETHUSDT',strategy="short_strategy"):
    cc = change_config.Change_config()
    cc.update_config(pair,strategy,{"side":side,"pred":pred})

# change discout rate 
def change_discount(pair="ETHUSDT",type="long_p",rate=0.005):
    cc = change_config.Change_config()
    cc.update_config(pair,type,rate)    
def get_strategy(pair="ETHUSDT"):
    cc = change_config.Change_config()
    print(cc.get_pair_config(pair))

pair = 'XRPUSDT'
change_strategy(pred=1,side=-1,pair=pair,strategy="long_strategy")
change_strategy(pred=0,side=-1,pair=pair,strategy="short_strategy")
change_discount(pair=pair,type="long_p",rate=0)
change_discount(pair=pair,type="short_p",rate=0)
off_long_short(pair,'short',False)
get_strategy()
