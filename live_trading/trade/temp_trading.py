import trailing 
from multiprocessing import Process

#t1 = trailing.Trailing(2.17, 'short',1,6, 5, "ETHUSDT",437.73)
#Process(target=t1.trailing_stop_short).start()
#t2 = trailing.Trailing(2.17, 'short',1,6, 5, "ETHUSDT",437.73)
#Process(target=t2.trailing_stop_short).start()
t3 = trailing.Trailing(1.4, 'long',1,2, 2, "ETHUSDT",342.17)
Process(target=t3.trailing_stop_long).start()
