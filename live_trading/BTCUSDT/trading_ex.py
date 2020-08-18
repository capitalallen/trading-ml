import trading 

db_name= "../pair_db/features.sqlite"
record_name="BTCUSDT"
t = trading.Trading(pair="BTCUSDT",db_name=db_name,record_name=record_name,model_path="model.joblib",columns_path="column_order.json")
t.live_trading()