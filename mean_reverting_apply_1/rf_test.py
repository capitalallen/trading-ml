from ml_random_forest import model
import pandas as pd 

# infile = './BTCUSDT/x_y_min_fix.csv'
infile = './BTCUSDT/x_y_min_fix.csv'
df = pd.read_csv(infile,index_col=0)
df.index =pd.to_datetime(df.index)
# cols = ['rsi','kdj_k','kdj_d','williams','cci']
#cols = ['fast_mavg','slow_mavg','rsi']
cols = ['fast_mavg','slow_mavg','srsi','kdj_k','kdj_d','williams','cci']
df.drop(columns=cols,inplace=True)
# print(df.columns)
# print(df[df['y']==1].shape)
m = model.Model(df) 
m.split_dataset()
m.train() 
folder = './BTCUSDT'
m.performance_matrics_accuracy_train(outfolder=folder)
m.performance_matrics_accuracy(outfolder=folder)
m.feature_importance(outfolder=folder)
m.store_prediction(outfolder=folder)
m.save_model(outfolder=folder)