from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string
import jsonpickle as jp
import numpy as np

class Trader:
    
    position = {'AMETHYSTS': 0, 'STARFRUIT' : 0}
    market = {'AMETHYSTS': [], 'STARFRUIT' : []}
    star_mid_prices = []
    
    def star_update_mid_price(self, price):
        self.star_mid_prices.append(price)
        if len(self.star_mid_prices) > 20:
            self.star_mid_prices.pop(0)
    
    def star_lin_regress(self):
        times = np.linspace(0, 0.1*(len(self.star_mid_prices)), len(self.star_mid_prices)) # List of timestamps
        A = np.vstack([times, np.ones(len(times))]).T
        m, c = np.linalg.lstsq(A, self.star_mid_prices, rcond=None)[0]
        next_time = 1.01 # Assuming next point is one time step ahead
        next_stock_mid_price = m * next_time + c
        return next_stock_mid_price
    
    #SELL > BUY
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
        #Use pytorch to find linear regression next time
        star_orders = []
        star_s_min = min(orders.sell_orders.keys()) #maximum price it is sold at
        star_b_max = max(orders.buy_orders.keys()) #minimum price it can be bought at
        spread = star_s_min - star_b_max
        
        self.star_update_mid_price((star_s_min + star_b_max)//2)
        
        trend = self.star_lin_regress()
        
        values = [i + star_b_max for i in range(spread)]
        
        s_tradable = -1*(20 + position)
        b_tradable = (20 - position)
        mm_b = b_tradable
        mm_s = s_tradable
        
        if spread <= 8:
            if trend > ((star_s_min + star_b_max)//2):
                star_orders.append(Order('STARFRUIT', star_b_max, mm_b))
            else:
                star_orders.append(Order('STARFRUIT', star_s_min, mm_s))
            return star_orders
        
        mid_ind = ((star_s_min + star_b_max)//2) + 1 - values[0]
        
        b_val = values[0:mid_ind]
        s_val = values[mid_ind:]
        
        if len(self.star_mid_prices) == 50:
            mm_b_inc = mm_b / sum([i for i in range(1, len(b_val) + 2)])
            mm_s_inc = mm_s / sum([i for i in range(1, len(s_val) + 2)])
            
            star_orders += [Order('STARFRUIT', b_val[i - 1], int(mm_b_inc*i)) for i in range(1, len(b_val) + 1)]
            b_residue = mm_b - sum([int(mm_b_inc*i) for i in range(1, len(b_val) + 1)])
            star_orders.append(Order('STARFRUIT', star_b_max + 2, b_residue))
            
            star_orders += [Order('STARFRUIT', s_val[::-1][i - 1], int(mm_s_inc*i)) for i in range(1, len(s_val) + 1)]
            s_residue = mm_s - sum([int(mm_s_inc*i) for i in range(1, len(s_val) + 1)])
            star_orders.append(Order('STARFRUIT', star_s_min - 2, s_residue))
            
        return star_orders
        
    def run(self, state: TradingState):
        # Only method required. It takes all buy and sell orders for all symbols as an input, and outputs a list of orders to be sent
        """SETUP"""
        
        if state.traderData != "":
            self.star_mid_prices = jp.decode(state.traderData)
        
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
        result['STARFRUIT'] = self.star_ord_to_make(star_curr_pos, star_curr_ords)
        
        """END STARFRUIT"""
        
        
        
        #result['STARFRUIT'] = star_ord
        
        traderData = jp.encode(self.star_mid_prices)
        traderData = ""
        
        return result, 0, traderData