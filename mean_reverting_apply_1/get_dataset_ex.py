import dataset_handle as dh  
from multiprocessing import Process
dol_bar_file = "dol_bar.csv"
p1 = Process(target=dh.store_raw_data,args=("IOTAUSDT",'01 JUN 2018',"./IOTAUSDT",dol_bar_file,"1m",))
p1.start() 
p2 = Process(target=dh.store_raw_data,args=("ETHUSDT",'01 AUG 2017',"./ETHUSDT",dol_bar_file,"5m",))
p2.start()
p3 = Process(target=dh.store_raw_data,args=("ETCUSDT",'01 JUN 2018',"./ETCUSDT",dol_bar_file,"1m",))
p3.start()
p4 = Process(target=dh.store_raw_data,args=("EOSUSDT",'01 MAY 2018',"./EOSUSDT",dol_bar_file,"1m",))
p4.start()

