import dataset_handle as dh  
from multiprocessing import Process
p1 = Process(target=dh.store_raw_data,args=("BTCUSDT",None,"./test_data1","daily.csv",))
# p2 = Process(target=dh.store_raw_data,args=("BTCUSDT",None,"./test","test_data2",))
p1.start() 
# p2.start()