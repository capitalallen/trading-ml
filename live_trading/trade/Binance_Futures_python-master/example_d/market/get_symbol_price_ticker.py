from binance_d import RequestClient
from binance_d.constant.test import *
from binance_d.base.printobject import *

request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)

result = request_client.get_symbol_price_ticker()
# result = request_client.get_symbol_price_ticker(symbol="btcusd_200925")

print("======= Symbol Price Ticker =======")
PrintMix.print_data(result)
print("===================================")
