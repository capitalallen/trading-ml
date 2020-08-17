from binance.client import Client
import ast
from datetime import datetime
import time
# from binance_d import RequestClient
# from binance_d.constant.test import *
# from binance_d.base.printobject import *
# from binance_d.model.constant import *

class Buy_sell:
    def __init__(self):
        # Enter your own API-key here
        binance_api_key = 'C48jZb7iNQwKZFEbCke3vClNqDEGpI68Le4G0og6hZauu3Kx7rFrCH31XbcaH7aC'
        # Enter your own API-secret here
        binance_api_secret = '8FIEyg5s9uKpAvTHBr6mH2zMEmPZD4VWgfbLF7AW3e0xMBcadmhL2Faqr5n8koDD'
        self.binance_client = Client(
            api_key=binance_api_key, api_secret=binance_api_secret)

    def order_limit_buy(self, symbol, q, p):
        try:
            # ast.literal_eval(
            result = self.binance_client.order_limit_buy(
                symbol=symbol, quantity=q, price=p)
            return result
        except:
            print("order buy error")
            return None

    def order_mkt_buy(self, symbol, q):
        try:
            result = self.binance_client.order_market_buy(
                symbol=symbol, quantity=q)
            return result
        except:
            print("order buy error")
            return None

    def order_limit_sell(self, symbol, q, p):
        try:
            result = self.binance_client.order_limit_sell(
                symbol=symbol, quantity=q, price=p)
            return result
        except:
            print("order buy error")
            return None

    def order_mkt_sell(self, symbol, q):
        try:
            result = self.binance_client.order_market_sell(
                symbol=symbol, quantity=q)
            return result
        except:
            print("order buy error")
            return None

    def get_future_account(self):
        return self.binance_client.futures_account()

    def trailing_stop_mkt_future(self,pair,price,q,side,callbackRate=1):
        his = self.binance_client.futures_create_order(symbol=pair,side=side,type="TRAILING_STOP_MARKET",quantity=q,activationPrice=price,callbackRate=callbackRate)
        return his 
    
    def change_leverage_future(self,pair,leverage):
        self.change_margin_type_future(pair,"ISOLATED")
        his = self.binance_client.futures_change_leverage(symbol=pair,leverage=leverage)
        return his 
    def change_margin_type_future(self,pair,marginType="ISOLATED"):
        return self.binance_client.futures_change_margin_type(symbol=pair,marginType=marginType)
# class Buy_sell_future:
#     def __init__(self):
#         self.binance_api_key = 'C48jZb7iNQwKZFEbCke3vClNqDEGpI68Le4G0og6hZauu3Kx7rFrCH31XbcaH7aC'
#         # Enter your own API-secret here
#         self.binance_api_secret = '8FIEyg5s9uKpAvTHBr6mH2zMEmPZD4VWgfbLF7AW3e0xMBcadmhL2Faqr5n8koDD'
#     def get_info(self):
#         request_client = RequestClient(api_key=self.binance_api_key, secret_key=self.binance_api_secret)
#         # print(f'api_key: {g_api_key}\nsecret_key: {g_secret_key}')
#         result = request_client.get_account_information()
#         print("canDeposit: ", result.canDeposit)
#         print("canWithdraw: ", result.canWithdraw)
#         print("feeTier: ", result.feeTier)
#         # print("maxWithdrawAmount: ", result.maxWithdrawAmount)
#         # print("totalInitialMargin: ", result.totalInitialMargin)
#         # print("totalMaintMargin: ", result.totalMaintMargin)
#         # print("totalMarginBalance: ", result.totalMarginBalance)
#         # print("totalOpenOrderInitialMargin: ", result.totalOpenOrderInitialMargin)
#         # print("totalPositionInitialMargin: ", result.totalPositionInitialMargin)
#         # print("totalUnrealizedProfit: ", result.totalUnrealizedProfit)
#         # print("totalWalletBalance: ", result.totalWalletBalance)
#         print("updateTime: ", result.updateTime)
#         print("=== Assets ===")
#         PrintMix.print_data(result.assets)
#         print("==============")
#         print("=== Positions ===")
#         PrintMix.print_data(result.positions)
#         print("==============")