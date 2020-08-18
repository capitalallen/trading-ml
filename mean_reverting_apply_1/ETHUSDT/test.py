import get_predict 
import pandas as pd 
import json 
gp = get_predict.Get_predict()

gp.load_model(path="model.joblib")

df1 = pd.read_csv("x_features.csv",index_col=0)
df1.index = pd.to_datetime(df1.date_time)
df1.drop(columns=['date_time'],inplace=True)
df2 = pd.read_csv("test_predictions.csv",index_col=0)
df2.index = pd.to_datetime(df2.index)
df3 = df1.loc[df2.index]
# print(df1.head())
# print(df2.head())
# print(df3.head())
data = json.load(open('column_order.json'))['columns']
for i in range(1,100):
    features = df3.iloc[i][data].tolist()
    print(int(gp.predict([features])[0]))
    print(int(df2.iloc[i].values[0]))
    break
    if int(gp.predict([features])[0]) == df2.iloc[i].values[0]:
        print('match')
    else:
        print("data date: ",df3.index[i])   
        print("reuslt date:",df2.index[i])
        print(gp.predict([features]))
        print(df2.iloc[i].values)
        print("not match")
        break