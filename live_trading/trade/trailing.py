import pandas as pd
import time
import requests
import ast
import transaction
import trailing_mkt 
import sys 
sys.path.append("../message")
import send_sms
class Trailing:
    """
    constructor 
        input: p and q,trigger_per, deviation, id 
        compute trigger_p, trailing_p, stop_loss_p 
        connect to Binance.Client
        get current p 
    """

    def __init__(self, q, trade_type='long',trigger_per=1, deviation=0.5, stop_loss_per=2, pair="BTCUSDT",p=None):
        # trigger percentage 
        self.trigger_per = trigger_per/100
        # trailing percentage 
        self.trailing_per = (trigger_per-deviation)/100
        # deviation percetage 
        self.deviation = deviation/100
        
        self.headers = {"Content-Type": "application/json"}
        self.url = "https://api.binance.com/api/v3/ticker/price?symbol="+pair
        self.pair = pair
        if not p:
            p =  float(ast.literal_eval(requests.get(self.url, headers=self.headers).content.decode("UTF-8"))['price'])
        if trade_type == 'long':
            # trigger price 
            self.trigger_p = p*(1+self.trigger_per)
            # trailing price 
            self.trailing_p = p*(1+self.trailing_per)
            # stop loss price 
            self.stop_loss = p*(1-(stop_loss_per/100))
        elif trade_type == 'short':
            self.trigger_p = p*(1-self.trigger_per)
            # trailing price 
            self.trailing_p = p*(1-self.trailing_per)
            # stop loss price 
            self.stop_loss = p*(1+(stop_loss_per/100))    
        else:
            return          
        self.quantity = q
        self.transaction_func = transaction.Buy_sell()
        self.messaging = send_sms.Send_message()

    def get_price(self):
        self.curr_price = float(ast.literal_eval(requests.get(
            self.url, headers=self.headers).content.decode("UTF-8"))['price'])

    """
    trailing_stop:
        float(ast.literal_eval(requests.get(url, headers=headers).content.decode("UTF-8"))['price'])
        - output return True or False 
        try
            when current price <= trigger price and >=stop_loss price:
                wait one second 
                update current price  

            if current price <=stop_loss price, call sell method at current price  
            max_p = current price 
            when current price >= trail price 
                wait one second 
                update current price
                if curr_price >tmp:
                    update trail_price: max_p*(1-deviation) 
            call sell method at current price 
            return True 
            update profolio 
        except:
            return False 
    """

    def trailing_stop_long(self):
        error = ""
        try:
            # send message start trailing
            self.messaging.send_a_message("trailing start!")
            self.get_price()
            error="updating current price"
            # when current price less than trigger price and larger than stop loss
            while self.curr_price <= self.trigger_p and self.curr_price >= self.stop_loss:
                time.sleep(1.5)
                self.get_price()
                print("trigger:",self.trigger_p,"stop loss:",self.stop_loss, "current_price: ",self.curr_price)
            error="prepare to sell"
            # when current price less or equal to stop loss price, sell 
            if self.curr_price <= self.stop_loss:
                self.transaction_func.mkt_buy_sell_future(
                    self.pair, self.quantity,positionSide="LONG",side='SELL')
            else:
                error = "trailing"
                max_p = self.curr_price
                while self.curr_price >= self.trailing_p:
                    self.get_price()
                    print("trigger:",self.trigger_p, "current_price: ",self.curr_price)
                    if max_p < self.curr_price:
                        max_p = self.curr_price
                        self.trailing_p = (1-self.deviation)*max_p
                    time.sleep(1)
                self.transaction_func.mkt_buy_sell_future(
                    self.pair, self.quantity,positionSide="LONG",side='SELL')
                self.messaging.send_a_message("sold!")
            return True
        except:
             self.messaging.send_a_message(error)

    def trailing_stop_short(self):
        try:
            # send message start trailing
            self.messaging.send_a_message("trailing start!")
            self.get_price()

            # when current price less than trigger price and larger than stop loss
            while self.curr_price >= self.trigger_p and self.curr_price <= self.stop_loss:
                time.sleep(1.5)
                self.get_price()
                print("trigger:",self.trigger_p,"stop loss:",self.stop_loss, "current_price: ",self.curr_price)
            
            # when current price less or equal to stop loss price, sell 
            if self.curr_price <= self.stop_loss:
                self.transaction_func.mkt_buy_sell_future(
                    self.pair, self.quantity,positionSide="SHORT",side='BUY')
            else:
                min_p = self.curr_price
                while self.curr_price <= self.trailing_p:
                    self.get_price()
                    print("trigger:",self.trigger_p, "current_price: ",self.curr_price)
                    if min_p > self.curr_price:
                        min_p = self.curr_price
                        self.trailing_p = (1+self.deviation)*min_p
                    time.sleep(1)
                self.transaction_func.mkt_buy_sell_future(
                    self.pair, self.quantity,positionSide="SHORT",side='BUY')
                self.messaging.send_a_message("sold start!")
        except:
             self.messaging.send_a_message("short trailing failed!")
