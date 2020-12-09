from random import randrange

"""
fix the market assumptions 
- validate trading strategies 

"""
class MarketSimulator:
    def __init__(self, om_2_gw=None,gw_2_om=None):
        self.orders = []
        self.om_2_gw = om_2_gw
        self.gw_2_om = gw_2_om
    
    """
    helper function to look up outstanding orders 
    """
    def lookup_orders(self,order):
        count=0
        for o in self.orders:
            if o['id'] ==  order['id']:
                return o, count
            count+=1
        return None, None



