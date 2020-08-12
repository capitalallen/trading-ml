import dataset_handle as dh  
from multiprocessing import Process
dol_bar_file = "dol_bar.csv"
p1 = Process(target=dh.store_raw_data,args=("BTCUSDT",None,"./BTCUSDT",dol_bar_file,))
p1.start() 
# p2 = Process(target=dh.store_raw_data,args=("ETHUSDT",None,"./ETHUSDT",dol_bar_file,))
# p2.start()