import dataset_handle as dh  
from multiprocessing import Process
dol_bar_file = "dol_bar.csv"
p1 = Process(target=dh.store_raw_data,args=("XRPUSDT",'06 May 2018',"./XRPUSDT",dol_bar_file,"1m",))
p1.start() 
p2 = Process(target=dh.store_raw_data,args=("NEOUSDT",'10 Nov 2017',"./NEOUSDT",dol_bar_file,"5min",))
p2.start()
p3 = Process(target=dh.store_raw_data,args=("LTCUSDT",'10 Dec 2017',"./LTCUSDT",dol_bar_file,"5min",))
p3.start()
p4 = Process(target=dh.store_raw_data,args=("BNBUSDT",'05 Nov 2017',"./BNBUSDT",dol_bar_file,"5min",))
p4.start()

