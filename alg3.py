from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string
import jsonpickle as jp
import numpy as np

class Trader:
    
    position = {'AMETHYSTS': 0, 'STARFRUIT' : 0}
    market = {'AMETHYSTS': [], 'STARFRUIT' : []}
    
    #SELL > BUY
    def ameth_ord_to_make(self, position, orders):
        ameth_orders = []

        # Extract sell and buy orders for amethysts
        sell_prices = sorted(orders.sell_orders.keys())
        buy_prices = sorted(orders.buy_orders.keys(), reverse=True)

        # Determine the minimum sell price and maximum buy price
        ameth_s_min = sell_prices[0] if sell_prices else None
        ameth_b_max = buy_prices[0] if buy_prices else None

        # Calculate spread
        spread = 0
        if ameth_s_min is not None and ameth_b_max is not None:
            spread = ameth_s_min - ameth_b_max

        # Generate a range of values based on spread
        values = range(ameth_b_max + 1, ameth_s_min, max(spread - 1, 1))

        # Calculate buying and selling increments
        mm_b = (20 - position)
        mm_s = -1 * (20 + position)
        total_levels = len(values)
        mm_b_inc = mm_b / ((total_levels * (total_levels + 1)) / 2)
        mm_s_inc = mm_s / ((total_levels * (total_levels + 1)) / 2)

        # Generate buy and sell orders
        for i, price in enumerate(values):
            # Calculate buying and selling quantities
            sell_quantity = min(orders.sell_orders.get(price, 0), int(mm_s_inc * (i + 1)))
            buy_quantity = min(orders.buy_orders.get(price, 0), int(mm_b_inc * (i + 1)))
            
            # Ensure buy and sell quantities are positive
            if sell_quantity > 0:
                ameth_orders.append(Order('AMETHYSTS', price, sell_quantity))
            if buy_quantity > 0:
                ameth_orders.append(Order('AMETHYSTS', price, buy_quantity))

        return ameth_orders


        
    def star_ord_to_make(self, position, orders):
        """
        star_orders = []
        star_s_min = min(orders.sell_orders.keys()) #maximum price it is sold at
        star_b_max = max(orders.buy_orders.keys()) #minimum price it can be bought at
        spread = star_s_min - star_b_max
        values = [i + star_b_max for i in range(1, spread)]
        
        s_tradable = -1*(20 + position)
        b_tradable = (20 - position)
        mm_b = b_tradable
        mm_s = s_tradable
        mt_s = 0
        mt_b = 0
        
        if spread <= 4:
            
            mm_b = int(b_tradable*0.2)
            mt_b = b_tradable - mm_b
            ameth_orders.append(Order('AMETHYSTS', 9997, mt_b))
            
            mm_s = int(s_tradable*0.2)
            mt_s = s_tradable - mm_s
            ameth_orders.append(Order('AMETHYSTS', 10003, mt_s))

        mid_ind = 10001 - values[0]
        b_val = values[0:mid_ind]
        s_val = values[mid_ind:]
        mm_b_inc = mm_b / sum([i for i in range(1, len(b_val) + 2)])
        mm_s_inc = mm_s / sum([i for i in range(1, len(s_val) + 2)])
        
        ameth_orders += [Order('AMETHYSTS', s_val[::-1][i - 1], int(mm_s_inc*i)) for i in range(1, len(s_val) + 1)]
        ameth_orders += [Order('AMETHYSTS', b_val[::-1][i - 1], int(mm_b_inc*i)) for i in range(1, len(b_val) + 1)]
        
        s_residue = mm_s - sum([int(mm_s_inc*i) for i in range(1, len(s_val) + 1)])
        ameth_orders.append(Order('AMETHYSTS', 10002, s_residue))
        b_residue = mm_b - sum([int(mm_b_inc*i) for i in range(1, len(b_val) + 1)])
        ameth_orders.append(Order('AMETHYSTS', 9998, b_residue))
"""
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