from binance_d import RequestClient
from binance_d.constant.test import *
from binance_d.base.printobject import *
from binance_d.model.constant import *

request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
result = request_client.cancel_list_orders(symbol="btcusd_200925", orderIdList = [1140, 1142, 1143])
# result = request_client.cancel_list_orders(symbol="btcusd_200925", origClientOrderIdList = ["web_BL7xhx6cz2lDbVlbLCbQ", "web_tW94LJCxDRUSrXN19myG", "abc"])
PrintList.print_object_list(result)
