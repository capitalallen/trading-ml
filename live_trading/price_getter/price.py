import requests
import ast

"""
input pair 
output price
"""

def get_price(pair):
    url = "https://api.binance.com/api/v3/ticker/price?symbol="+pair 
    headers = {"Content-Type": "application/json"}
    return  round(float(ast.literal_eval(requests.get(url, headers=headers).content.decode("UTF-8"))['price']),2)

