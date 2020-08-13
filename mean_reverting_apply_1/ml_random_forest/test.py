from model import Model
import pandas as pd 


df = pd.read_csv('training.csv',index_col=0)
df.index =pd.to_datetime(df.index)
df = df.iloc[:500]
print(df.head())
m = Model(df) 
m.split_dataset()
m.train() 
m.performance_matrics_accuracy_train()
m.performance_matrics_accuracy()
m.feature_importance()
m.save_model()