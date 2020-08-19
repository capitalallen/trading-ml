import get_training_data as gtd

outfolder="./BNBUSDT/"
inputfile = outfolder+"dol_bar.csv"
from multiprocessing import Process
from multiprocessing import Pool
def preprocessing(outfolder):
    #get dollar bar 
    gtd.get_dol_bar_30(outfolder)

    #get features from dollar bar 
    gtd.add_features(outfolder)

    #get label file 
    gtd.get_labels(outfolder)

    # generate training data set
    gtd.get_training_dataset(outfolder)
def preprocessing_15(outfolder):
    #get dollar bar 
    gtd.get_dol_bar_15(outfolder)

    #get features from dollar bar 
    gtd.add_features(outfolder)

    #get label file 
    gtd.get_labels(outfolder)

    # generate training data set
    gtd.get_training_dataset(outfolder)
# outfolder = ["./EOSUSDT/","./ETHUSDT/","./IOTAUSDT/","./NEOUSDT/","./XRPUSDT/"] 
outfolder = ["./ETCUSDT/","./EOSUSDT/","./XRPUSDT/","./NEOUSDT/","./LTCUSDT/"]
# outfolder = ["./BTCUSDT/"]
#p = Pool(len(outfolder))
# p.map(preprocessing_15,outfolder)
p1 = Process(target=preprocessing_15,args=(outfolder[0],))
p1.start() 
p2 = Process(target=preprocessing_15,args=(outfolder[1],))
p2.start()
p3 = Process(target=preprocessing,args=(outfolder[2],))
p3.start()
p4 = Process(target=preprocessing,args=(outfolder[3],))
p4.start()
p5 = Process(target=preprocessing_15,args=(outfolder[4],))
p5.start()
#p.map(preprocessing_15,outfolder)
