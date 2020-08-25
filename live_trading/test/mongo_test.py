import sys 
sys.path.append('../alter_config')
import change_config 
cc = change_config.Change_config()
pairs = ["XRPUSDT","BTCUSDT","ETHUSDT","BNBUSDT"]
for p in pairs:
    print(cc.get_pair_config(p))
    
