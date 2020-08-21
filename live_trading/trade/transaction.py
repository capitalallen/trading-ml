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
    # positionSide LONG or SHORT 
    # side BUY or SELL
    def trailing_stop_mkt_future(self,pair,price=None,q=None,side=None,positionSide="BOTH",callbackRate=1,leverage=20):
        try:
            self.change_leverage_future(pair,leverage)
        except:
            print('No need to change leverage type.')
        try:
            self.change_margin_type_future(pair,"ISOLATED")
        except:
            print("not need to change margin type")
        if price:
            his = self.binance_client.futures_create_order(symbol=pair,side=side,type="TRAILING_STOP_MARKET",quantity=q,activationPrice=price,callbackRate=callbackRate,positionSide=positionSide)
        else: 
            his = self.binance_client.futures_create_order(symbol=pair,side=side,type="TRAILING_STOP_MARKET",quantity=q,callbackRate=callbackRate,positionSide=positionSide)
        return his 
    # LONG OR SHORT 
    def mkt_buy_sell_future(self,pair,quantity,positionSide="LONG",side='BUY',leverage=0):
        his = self.binance_client.futures_create_order(symbol=pair,side=side,type="MARKET",quantity=str(quantity),positionSide=positionSide)
        return his    

    def limit_buy_sell_future(self,pair,price,quantity,positionSide="LONG",side='BUY'):
        try:
            self.change_leverage_future(pair,leverage)
        except:
            print('No need to change leverage type.')
        try:
            self.change_margin_type_future(pair,"ISOLATED")
        except:
            print("not need to change margin type")
        his = self.binance_client.futures_create_order(symbol=pair,side=side,price=str(price),type="LIMIT",quantity=str(quantity),positionSide=positionSide)
        return his           
    
    def change_leverage_future(self,pair,leverage):
        self.change_margin_type_future(pair,"ISOLATED")
        his = self.binance_client.futures_change_leverage(symbol=pair,leverage=leverage)
        return his 
    def change_margin_type_future(self,pair,marginType="ISOLATED"):
        return self.binance_client.futures_change_margin_type(symbol=pair,marginType=marginType)
