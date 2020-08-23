import trailing 
from multiprocessing import Process

t1 = trailing.Trailing(18.53, 'short',1,1, 2, "ETHUSDT",390.92)
Process(target=t1.trailing_stop_short).start()
t2 = trailing.Trailing(18.53, 'long',1,1, 2, "BTCUSDT",390.92)
Process(target=t2.trailing_stop_long).start()
t2 = trailing.Trailing(101, 'long',1,1, 2, "BNBUSDT",21.996)
Process(target=t3.trailing_stop_long).start()