def ameth_ord_to_make(position):
        
    sells = [9999, 10000, 10001, 10002]
    buys = [9999, 9998, 9997, 9996]
        
    s_increment = -1*(20 + position) / 10
    b_increment = (20 - position) / 10
        
    sell_total = [int(s_increment*(5-i)) for i in range(1, 5)]
    buy_total = [int(b_increment*(5-i)) for i in range(1, 5)]
        
    return buy_total, sell_total

for i in range(-20, 21, 1):
    buy, sell = ameth_ord_to_make(i)
    print(f"{i} : {sum(buy) + i}, {sum(sell) + i}")