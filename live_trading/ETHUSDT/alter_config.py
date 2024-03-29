import sys 
sys.path.append('../alter_config')
import change_config 

# "long_strategy" or short_strategy
def change_strategy(pred,side,pair='ETHUSDT',strategy="short_strategy"):
    cc = change_config.Change_config()
    cc.update_config(pair,strategy,{"side":side,"pred":pred})


# "long_strategy" or short_strategy
def turn_off(pair='ETHUSDT',t="long",option=False):
    cc = change_config.Change_config()
    cc.update_config(pair,t,option)

# change discout rate 
def change_discount(pair="ETHUSDT",type="long_p",rate=0.005):
    cc = change_config.Change_config()
    cc.update_config(pair,type,rate)    
def get_strategy(pair="ETHUSDT"):
    cc = change_config.Change_config()
    print(cc.get_pair_config(pair))

# lev_long lev_short
def change_lev(pair,lev_type,rate):
    cc = change_config.Change_config()
    cc.update_config(pair,lev_type,rate)
pair = "ETHUSDT"
#change_strategy(pred=1,side=-1,pair='ETHUSDT',strategy="long_strategy")
#change_strategy(pred=0,side=-1,pair='ETHUSDT',strategy="short_strategy")
#change_discount(pair="ETHUSDT",type="long_p",rate=0.02)
#change_lev(pair,'lev_short',30)
change_discount(pair="ETHUSDT",type="short_p",rate=0.005)
turn_off()
get_strategy(pair)
