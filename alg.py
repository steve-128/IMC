from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string

class Trader:
    
    position = {'AMETHYSTS': 0, 'STARFRUIT' : 0}
    market = {'AMETHYSTS': [], 'STARFRUIT' : []}
    
    def ameth_ord_to_make(self, position):
        
        sells = [10000, 10001, 10002, 10003, 10004]
        buys = [10000, 9999, 9998, 9997, 9996]
        
        s_increment = -1*(20 + position) / 15
        b_increment = (20 - position) / 15
        
        sell_total = [Order('AMETHYSTS', sells[i - 1], int(s_increment*(i))) for i in range(1, 6)]
        buy_total = [Order('AMETHYSTS', buys[i - 1], int(b_increment*(i))) for i in range(1, 6)]
        
        s_residue = -20 - (sum([int(s_increment*(i)) for i in range(1, 6)]) + position)
        sell_total.append(Order('AMETHYSTS', 10000, s_residue))
        b_residue = 20 - (sum([int(b_increment*(i)) for i in range(1, 6)]) + position)
        buy_total.append(Order('AMETHYSTS', 10000, b_residue))
        
        return buy_total, sell_total
        
    
    def starfruit_ord_to_make(self, position):
        
        return    
    
        
    def run(self, state: TradingState):
        # Only method required. It takes all buy and sell orders for all symbols as an input, and outputs a list of orders to be sent
        result = {'AMETHYSTS' : [], 'STARFRUIT' : []}
        ameth_curr_ords = state.order_depths['AMETHYSTS']
        
        for key in self.position.keys():
            self.position[key] = state.position.get(key, 0)
        
        ameth_curr_pos = self.position['AMETHYSTS']
        
        buy_ameth, sell_ameth = self.ameth_ord_to_make(ameth_curr_pos)
        
        result['AMETHYSTS'] = buy_ameth + sell_ameth
        
        traderData = "Test"
        
        return result, 0, traderData