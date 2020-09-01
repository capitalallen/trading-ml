import pandas as pd
import time
import requests
import ast
import transaction
import trailing_mkt 
import sys 
sys.path.append("../message")
sys.path.append('../alter_config')
import send_sms
import change_config
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
        self.buy_price = p
        self.config_func = change_config.Change_config()
        if not p:
            p =  float(ast.literal_eval(requests.get(self.url, headers=self.headers).content.decode("UTF-8"))['price'])
            self.buy_price = p 
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

        self.threhold = [0.01,0.02,0.03,0.04,0.05]
        self.sell_per = [0.3,0.3,0.2,0.04,0.05,0.05]
        self.quantity_remain = self.quantity
        self.target = 0
        self.decimals = {"BTCUSDT":3,"ETHUSDT":2,"BNBUSDT":1,"XRPUSDT":0}
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
            self.config_func.update_long_trade_avl(self.pair,-1)
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
                    """
                    sell when threshold is reached 
                    """
                    if self.target<5 and self.curr_price>=self.buy_price*(1+self.threhold[self.target]):
                        q = round(self.quantity*self.sell_per[self.target],self.decimals[self.pair])
                        self.quantity_remain = self.quantity-q 
                        self.transaction_func.mkt_buy_sell_future(self.pair, q,positionSide="LONG",side='SELL')
                        self.target+=1 
                    if self.target>=2 and self.deviation!=0.02:
                        self.deviation = 0.02 
                    # update price 
                    self.get_price()
                    print("trigger:",self.trigger_p, "current_price: ",self.curr_price)
                    if max_p < self.curr_price:
                        max_p = self.curr_price
                        self.trailing_p = (1-self.deviation)*max_p
                    time.sleep(1)
                self.transaction_func.mkt_buy_sell_future(
                    self.pair, self.quantity_remain,positionSide="LONG",side='SELL')
                self.messaging.send_a_message("sold!")
            # update trade allowed number 
            self.config_func.update_long_trade_avl(self.pair,1)
            return True
        except Exception as e:
            print(e)
            self.messaging.send_a_message(str(e))

    def trailing_stop_short(self):
        try:
            self.config_func.update_short_trade_avl(self.pair,-1)
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
                    """
                    sell when threshold is reached 
                    """
                    if self.target<6 and self.curr_price<=self.buy_price*(1-self.threhold[self.target]):
                        q = round(self.quantity*self.sell_per[self.target],self.decimals[self.pair])
                        self.quantity_remain = self.quantity-q 
                        self.transaction_func.mkt_buy_sell_future(self.pair, q,positionSide="SHORT",side='BUY')
                        self.target+=1 
                    if self.target>=2 and self.deviation!=0.02:
                        self.deviation = 0.02 

                    self.get_price()
                    print("trigger:",self.trigger_p, "current_price: ",self.curr_price)
                    if min_p > self.curr_price:
                        min_p = self.curr_price
                        self.trailing_p = (1+self.deviation)*min_p
                    time.sleep(1)
                self.transaction_func.mkt_buy_sell_future(
                    self.pair, self.quantity_remain,positionSide="SHORT",side='BUY')
                self.messaging.send_a_message("sold start!")
            self.config_func.update_short_trade_avl(self.pair,1)
            return True
        except Exception as e:
            print(e)
            self.messaging.send_a_message(str(e))
