import get_training_data as gtd

outfolder="./BNBUSDT/"
inputfile = outfolder+"dol_bar.csv"
from multiprocessing import Process
def preprocessing(outfolder):
    #get dollar bar 
    handle = gtd.get_dol_bar_30(outfolder)

    #get features from dollar bar 
    gtd = gtd.add_features(outfolder)

    #get label file 
    labels = gtd.get_labels(outfolder)

    # generate training data set
    gtd.get_training_dataset(outfolder)
def preprocessing_15(outfolder):
    #get dollar bar 
    handle = gtd.get_dol_bar_15(outfolder)

    #get features from dollar bar 
    gtd = gtd.add_features(outfolder)

    #get label file 
    labels = gtd.get_labels(outfolder)

    # generate training data set
    gtd.get_training_dataset(outfolder)
outfolder = ["EOSUSDT","ETHUSDT","IOTAUSDT","LTCUSDT","XRPUSDT"]

p1 = Process(target=preprocessing_15,args=(outfolder[0],))
p1.start() 
p1 = Process(target=preprocessing,args=(outfolder[1],))
p2.start()
p1 = Process(target=preprocessing,args=(outfolder[2],))
p3.start()
p1 = Process(target=preprocessing_15,args=(outfolder[3],))
p4.start()
p1 = Process(target=preprocessing_15,args=(outfolder[4],))
p4.start()

