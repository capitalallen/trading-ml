import data_getter

d = data_getter.data_getter()

data = d.get_all_binance("BTCUSDT", "30m")
