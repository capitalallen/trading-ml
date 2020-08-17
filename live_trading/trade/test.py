import trading 
from binance.client import Client
t = trading.Buy_sell() 
# t.order_limit_buy("BTCUSDT",0.01,10000)
# Enter your own API-key here
# binance_api_key = 'C48jZb7iNQwKZFEbCke3vClNqDEGpI68Le4G0og6hZauu3Kx7rFrCH31XbcaH7aC'
# # Enter your own API-secret here
# binance_api_secret = '8FIEyg5s9uKpAvTHBr6mH2zMEmPZD4VWgfbLF7AW3e0xMBcadmhL2Faqr5n8koDD'
# binance_client = Client(api_key=binance_api_key, api_secret=binance_api_secret)
# print(binance_client.futures_create_order(symbol="BTCUSDT",side="BUY",type="TRAILING_STOP_MARKET",quantity=0.01,activationPrice=10000,callbackRate=1))
# print(t.change_leverage("BTCUSDT",50))
print(t.change_margin_type_future("BTCUSDT","ISOLATED"))
#futures_change_margin_type