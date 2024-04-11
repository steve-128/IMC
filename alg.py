from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string
import jsonpickle as jp
import numpy as np

class Trader:
    
    position = {'AMETHYSTS': 0, 'STARFRUIT' : 0}
    market = {'AMETHYSTS': [], 'STARFRUIT' : []}
    star_mid_prices = [5045.5]
    
    def ameth_ord_to_make(self, position):
        
        sells = [10003, 10002]
        buys = [9997, 9998]
        
        n = 3
        
        s_increment = -1*(20 + position) / 3
        b_increment = (20 - position) / 3
        
        sell_total = [Order('AMETHYSTS', sells[i - 1], int(s_increment*i)) for i in range(1, n)]
        buy_total = [Order('AMETHYSTS', buys[i - 1], int(b_increment*i)) for i in range(1, n)]
        
        s_residue = -20 - (sum([int(s_increment*i) for i in range(1, n)]) + position)
        sell_total.append(Order('AMETHYSTS', 10003, s_residue))
        b_residue = 20 - (sum([int(b_increment*i) for i in range(1, n)]) + position)
        buy_total.append(Order('AMETHYSTS', 9997, b_residue))
        
        return buy_total, sell_total
        
    """
    def updateStarPrice(self, val):
        if len(self.star_mid_prices) == 10:
            self.star_mid_prices.pop(0)
        self.star_mid_prices.append(val)
    
    def linear_regression(self, X, y):
        # Calculate the mean of X and y
        mean_X = np.mean(X)
        mean_y = np.mean(y)

        # Calculate the slope (m) and intercept (c) of the regression line
        numerator = np.sum((X - mean_X) * (y - mean_y))
        denominator = np.sum((X - mean_X) ** 2)
        m = numerator / denominator
        c = mean_y - m * mean_X

        return m, c

    def starfruit_ord_to_make(self, position):
        # Perform linear regression on historical stock mid prices
        n = len(self.star_mid_prices)
        times = np.linspace(0, 0.1 * n, n)
        m, c = self.linear_regression(times, self.star_mid_prices)

        # Predict the next stock mid price
        next_time = 1.1  # Assuming next point is one time step ahead
        next_stock_mid_price = np.round(m * next_time + c)

        # Calculate maximum buy and sell quantities based on position
        max_buy = 20 - position
        max_sell = -1 * (20 + position)
        
        # Determine the number of orders based on the slope of the regression line
        n = 3
        v = 2
        inc_b = max_buy / sum(range(1, n + 1))
        inc_s = max_sell / sum(range(1, n + 1))
        
        if m < 0:
            orders = [Order('STARFRUIT', int(next_stock_mid_price - i), int(inc_b * i)) for i in range(1, n + 1)]
            orders += [Order('STARFRUIT', int(next_stock_mid_price + i + v), int(inc_s * (n-i))) for i in range(1, n)]
            
            residue = max_buy - sum(int(inc_b * i) for i in range(1, n + 1))
            orders.append(Order('STARFRUIT', int(next_stock_mid_price), residue))
            residue = max_sell - sum(int(inc_s * (n-i)) for i in range(1, n))
            orders.append(Order('STARFRUIT', int(next_stock_mid_price+v), residue))
        else:
            orders = [Order('STARFRUIT', int(next_stock_mid_price + i), int(inc_s * i)) for i in range(1, n + 1)]
            orders += [Order('STARFRUIT', int(next_stock_mid_price - i - v), int(inc_b * (n-i))) for i in range(1, n)]
            
            residue = max_sell - sum(int(inc_s * i) for i in range(1, n + 1))
            orders.append(Order('STARFRUIT', int(next_stock_mid_price), residue))
            residue = max_buy - sum(int(inc_b * (n-i)) for i in range(1, n))
            orders.append(Order('STARFRUIT', int(next_stock_mid_price-v), residue))

        return orders
    """
        
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
        
        #ameth_curr_ords = state.order_depths['AMETHYSTS']
        """AMETHYST"""
        ameth_curr_pos = self.position['AMETHYSTS']
        
        buy_ameth, sell_ameth = self.ameth_ord_to_make(ameth_curr_pos)
        """END AMETHYST"""
        
        """STARFRUIT"""
        """
        starfruit_curr_ords = state.order_depths['STARFRUIT']
        
        star_mid = (max(starfruit_curr_ords.buy_orders.keys()) + min(starfruit_curr_ords.sell_orders.keys()))/2
        
        #self.updateStarPrice(star_mid)
        
        star_curr_pos = self.position['STARFRUIT']
        star_ord = self.starfruit_ord_to_make(star_curr_pos)
        """
        """END STARFRUIT"""
        
        
        result['AMETHYSTS'] = buy_ameth + sell_ameth
        #result['STARFRUIT'] = star_ord
        
        #traderData = jp.encode(self.star_mid_prices)
        traderData = ""
        
        return result, 0, traderData