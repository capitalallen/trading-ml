from evaulate import evaulate
import pandas as pd 
from multiprocessing import Process
def evaulate_ex(folder):

    pre_file = folder+"test_predictions.csv"
    label_file = folder+"labels.csv"

    ev = evaulate(label_file,pre_file,folder)
    ev.long_stats()
    ev.short_stats()

outfolder = ["./EOSUSDT/","./ETHUSDT/","./IOTAUSDT/","./NEOUSDT/","./XRPUSDT/"]

p1 = Process(target=evaulate_ex,args=(outfolder[0],))
p1.start() 
# p2 = Process(target=evaulate_ex,args=(outfolder[1],))
# p2.start()
# p3 = Process(target=evaulate_ex,args=(outfolder[2],))
# p3.start()
# p4 = Process(target=evaulate_ex,args=(outfolder[3],))
# p4.start()
# p5 = Process(target=evaulate_ex,args=(outfolder[4],))
# p5.start()

