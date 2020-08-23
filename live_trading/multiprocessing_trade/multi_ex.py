from multiprocessing import Process
import sys 
sys.path.append("../XRPUSDT")
sys.path.append("../BNBUSDT")
import bnb_ex 
import xrp_ex

t = int(sys.argv[1])
if t == 1:
    p1 = Process(target=bnb_ex.trade_ex,args=[1])
    p1.daemon = False
    p1.start()

    p2 = Process(target=xrp_ex.trade_ex,args=[1])
    p2.daemon = False
    p2.start()
elif t==2:
    #p1 = Process(target=bnb_ex.trade_ex,args=[2])
    #p1.daemon = False
    #p1.start()

    p2 = Process(target=xrp_ex.trade_ex,args=[2])
    p2.daemon = False
    p2.start()    

