import trailing 
from multiprocessing import Process

t1 = trailing.Trailing(0.5, 'long',1,1, 2, "BTCUSDT",11289.99)
Process(target=t1.trailing_stop_long).start()
#t2 = trailing.Trailing(15, 'short',1,1, 2, "ETHUSDT",384.33)
#Process(target=t2.trailing_stop_short).start()
#t3 = trailing.Trailing(101, 'long',1,1, 2, "BNBUSDT",21.996)
#Process(target=t3.trailing_stop_long).start()
