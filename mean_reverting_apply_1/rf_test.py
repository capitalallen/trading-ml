from ml_random_forest import model
import pandas as pd 
import json
from multiprocessing import Process
# # infile = './BTCUSDT/x_y_min_fix.csv'
# infile = './BTCUSDT/x_y_min_fix.csv'
# df = pd.read_csv(infile,index_col=0)
# df.index =pd.to_datetime(df.index)
# # cols = ['rsi','kdj_k','kdj_d','williams','cci']
# #cols = ['fast_mavg','slow_mavg','rsi']
# cols = ['fast_mavg','slow_mavg','srsi','kdj_k','kdj_d','williams','cci']
# df.drop(columns=cols,inplace=True)
# # print(df.columns)
# # print(df[df['y']==1].shape)
# m = model.Model(df) 
# m.split_dataset()
# m.train() 
# folder = './BTCUSDT'
# m.performance_matrics_accuracy_train(outfolder=folder)
# m.performance_matrics_accuracy(outfolder=folder)
# m.feature_importance(outfolder=folder)
# m.store_prediction(outfolder=folder)
# m.save_model(outfolder=folder)

def training(outfolder,inputfile="x_y.csv"):
    inputfile = outfolder+inputfile
    df = pd.read_csv(inputfile,index_col=0)
    df.index =pd.to_datetime(df.index)
    m = model.Model(df) 
    m.split_dataset()
    with open(outfolder+'column_order.json','w') as f:
        json.dump({'columns':m.get_columns()},f)
    m.train() 
    m.performance_matrics_accuracy_train(outfolder=folder)
    m.performance_matrics_accuracy(outfolder=folder)
    m.feature_importance(outfolder=folder)
    m.store_prediction(outfolder=folder)
    m.save_model(outfolder=folder)

outfolder = ["./EOSUSDT/","./ETHUSDT/","./IOTAUSDT/","./NEOUSDT/","./XRPUSDT/"]

p1 = Process(target=training,args=(outfolder[0],))
p1.start() 
p2 = Process(target=training,args=(outfolder[1],))
p2.start()
# p3 = Process(target=training,args=(outfolder[2],))
# p3.start()
# p4 = Process(target=training,args=(outfolder[3],))
# p4.start()
# p5 = Process(target=training,args=(outfolder[4],))
# p5.start()
