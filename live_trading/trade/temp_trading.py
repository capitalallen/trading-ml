import trailing 
from multiprocessing import Process

t1 = trailing.Trailing(31.63, 'long',2,1, 2, "ETHUSDT",385.76)
Process(target=t1.trailing_stop_short).start()
t2 = trailing.Trailing(15, 'short',1,1, 2, "ETHUSDT",384.33)
Process(target=t2.trailing_stop_long).start()
#t3 = trailing.Trailing(101, 'long',1,1, 2, "BNBUSDT",21.996)
#Process(target=t3.trailing_stop_long).start()
