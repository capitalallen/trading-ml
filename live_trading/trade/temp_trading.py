import trailing 
from multiprocessing import Process

#t1 = trailing.Trailing(29.99, 'short',1,1, 2, "ETHUSDT",391.69)
#Process(target=t1.trailing_stop_short).start()
t2 = trailing.Trailing(0.965, 'long',1,1, 2, "BTCUSDT",11702.39)
Process(target=t2.trailing_stop_long).start()
#t3 = trailing.Trailing(101, 'long',1,1, 2, "BNBUSDT",21.996)
#Process(target=t3.trailing_stop_long).start()
