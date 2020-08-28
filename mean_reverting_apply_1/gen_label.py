import sys
sys.path.append("../mean_reverting")
import preprocess 
import get_training_data as gtd 
import pandas as pd 
from multiprocessing import Process
import get_training_data as gtd 
def get_labels(outfolder,inputfile="x_features.csv"):
    inputfile = outfolder+inputfile
    pre = preprocess.Preprocess(inputfile)
    df = pd.read_csv(inputfile,index_col=0)
    df['date_time'] = pd.to_datetime(df.date_time)
    df.index = df.date_time 
    df.drop(columns=['date_time'],inplace=True)
    # print(df.head())
    # return 
    df = pre.labeling(df)
    print(df.head())
    df.to_csv(outfolder+"labels.csv")
# get_labels("./BNBUSDT/")
# outfolder = ["./BNBUSDT/","./ETHUSDT/"]
# p1 = Process(target=get_labels,args=(outfolder[0],"x_features.csv"))
# p1.start() 
# p2 = Process(target=get_labels,args=(outfolder[1],))
# p2.start() 

# def clean_df(outfolder,inputfile="x_features.csv"):
#     inputfile = outfolder+inputfile
#     df = pd.read_csv(inputfile)
#     df.dropna(axis=0, how='any', inplace=True)
#     df.to_csv(outfolder+"x_features_clean.csv")

# outfolder = ["./BNBUSDT/","./ETHUSDT/"]
# p1 = Process(target=gtd.get_training_dataset,args=(outfolder[0],))
# p1.start() 
# p2 = Process(target=gtd.get_training_dataset,args=(outfolder[1],))
# p2.start() 