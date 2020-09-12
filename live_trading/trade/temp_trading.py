import trailing 
from multiprocessing import Process

#t1 = trailing.Trailing(2.17, 'short',1,6, 5, "ETHUSDT",437.73)
#Process(target=t1.trailing_stop_short).start()
t2 = trailing.Trailing(0.28, 'short',1,1.5, 5, "BTCUSDT",10207.78)
Process(target=t2.trailing_stop_short).start()
#t3 = trailing.Trailing(14241.6, 'long',1,2, 3, "XRPUSDT",0.2369)
#Process(target=t3.trailing_stop_long).start()
