from binance_d import RequestClient
from binance_d.constant.test import *
from binance_d.base.printobject import *
from binance_d.model.constant import *

request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
result = request_client.get_open_orders(symbol="btcusd_200925")
PrintMix.print_data(result)
