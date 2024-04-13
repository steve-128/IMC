from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string
import jsonpickle as jp
import numpy as np

class Trader:
    
    position = {'AMETHYSTS': 0, 'STARFRUIT' : 0}
    market = {'AMETHYSTS': [], 'STARFRUIT' : []}
    
    def ameth_ord_to_make(self, position, orders):
        
        ameth_s_max = min(orders.sell_orders.keys()) #maximum price it is sold at
        ameth_b_min = max(orders.buy_orders.keys()) #minimum price it can be bought at
        print(f"Amethyst: {ameth_s_max - ameth_b_min}")
        print(ameth_s_max, ameth_b_min)
        sells = [10002, 10003]#[ameth_s_max, 10003] 
        buys = [9998, 9997]#[ameth_b_min, 9997] 
        
        n = 3
        
        s_increment = -1*(20 + position) / 3
        b_increment = (20 - position) / 3
        
        sell_total = [Order('AMETHYSTS', sells[i - 1], int(s_increment*(n-i))) for i in range(1, n)]
        buy_total = [Order('AMETHYSTS', buys[i - 1], int(b_increment*(n-i))) for i in range(1, n)]
        
        s_residue = -20 - (sum([int(s_increment*i) for i in range(1, n)]) + position)
        sell_total.append(Order('AMETHYSTS', 10002, s_residue))
        b_residue = 20 - (sum([int(b_increment*i) for i in range(1, n)]) + position)
        buy_total.append(Order('AMETHYSTS', 9998, b_residue))
        
        return buy_total + sell_total
    
        
    def star_ord_to_make(self, position, orders):
        print(f"Starfruit: {max(orders.buy_orders.keys()) - min(orders.sell_orders.keys())}")
        return 
        
    def run(self, state: TradingState):
        # Only method required. It takes all buy and sell orders for all symbols as an input, and outputs a list of orders to be sent
        """SETUP"""
        """
        if state.traderData != "":
            self.star_mid_prices = jp.decode(state.traderData)
        """
        result = {'AMETHYSTS' : [], 'STARFRUIT' : []}

        for key in self.position.keys():
            self.position[key] = state.position.get(key, 0)
        """END SETUP"""
        
        
        """AMETHYST"""
        ameth_curr_ords = state.order_depths['AMETHYSTS']
        ameth_curr_pos = self.position['AMETHYSTS']
        result['AMETHYSTS'] = self.ameth_ord_to_make(ameth_curr_pos, ameth_curr_ords)
        """END AMETHYST"""
        
        
        """STARFRUIT"""
        star_curr_ords = state.order_depths['STARFRUIT']
        star_curr_pos = self.position['STARFRUIT']
        self.star_ord_to_make(star_curr_pos, star_curr_ords)
        
        """END STARFRUIT"""
        
        
        
        #result['STARFRUIT'] = star_ord
        
        #traderData = jp.encode(self.star_mid_prices)
        traderData = ""
        
        return result, 0, traderData