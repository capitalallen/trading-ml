from random import randrange
from random import sample,seed

class LiquidityProvider:
    def __init__(self, lp_2_gateway=None):
        self.orders = []
        self.order_id = 0
        seed(0)
        self.lp_2_gateway = lp_2_gateway
