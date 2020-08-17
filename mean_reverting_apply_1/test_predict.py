import pandas as pd 
import json 
import get_predict 

x_y = pd.read_csv("./BTCUSDT/x_y_close_fix.csv")
predictions = pd.read_csv("./BTCUSDT/test_predictions.csv",index_col=0)
x_y.index = pd.to_datetime(x_y.date_time)
predictions.index = pd.to_datetime(predictions.index)
x_y = x_y.loc[predictions.index]
# print(x_y.head())
# print(predictions.head())
data = json.load(open('./BTCUSDT/column_order.json'))['columns']
pre = get_predict.Get_predict()
pre.load_model('./BTCUSDT/close-fix2/model.joblib')
print(data)
print(x_y.iloc[0][data].tolist())
# for i in range(10):
#     df = x_y.iloc[i][data].tolist()
#     p = pre.predict([df])
#     if p[0] != predictions.iloc[i].values[0]:
#         print("not matched ")
#     else:
#         print("matched")