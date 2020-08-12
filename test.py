from data_downloader import data_getter

d = data_getter()
print(d.get_all_binance("BNBUSDT", "1d"))
