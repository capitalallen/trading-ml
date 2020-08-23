import pandas as pd 
import trading 
import trailing_mkt as tm 
import transaction 
import trailing_mkt 
# t = trading.Trading(pair="BTCUSDT",db_name="../pair_db/features.sqlite",record_name="x_features",threshold=7097226,model_path="model.joblib",columns_path="column_order.json")

# df1 = pd.read_csv("x_features.csv",index_col=0)
# df1.index = pd.to_datetime(df1.date_time)
# df1.drop(columns=['date_time'],inplace=True)
# df2 = pd.read_csv("test_predictions.csv",index_col=0)
# df2.index = pd.to_datetime(df2.index)
# df3 = df1.loc[df2.index]
# # for i in range(1,500):
# #     if "nan" not in df3.iloc[i].tolist():
# t.live_trading()
# tm.limit_short_trailing("ETHUSDT",389.5,str(1),trade_type='short',trigger_per=1, deviation=0.5, stop_loss_per=2)
# t = transaction.Buy_sell()
# t.mkt_buy_sell_future("ETHUSDT",1,positionSide="SHORT",side='BUY',leverage=0)

# trailing_mkt.limit_long_trailing("BNBUSDT",22.01,1,trade_type='long',trigger_per=1, deviation=0.5, stop_loss_per=2)