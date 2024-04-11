import numpy as np

file = open("./round-1-island-data-bottle/prices_round_1_day_0.csv", "r")
n = 7
stock_mid_prices = []
for line in file:
    if "STARFRUIT" in line:
        stock_mid_prices.append(float(line.split(";")[15]))
    if len(stock_mid_prices) == n:
        print(stock_mid_prices.pop())
        break

# Sample data: list of times and stock_mid_prices
times = np.linspace(0, 0.1*(n-1), n-1) # List of timestamps


# Calculate the coefficients of the best fit line
# y = mx + c
# where m is the slope and c is the y-intercept
A = np.vstack([times, np.ones(len(times))]).T
m, c = np.linalg.lstsq(A, stock_mid_prices, rcond=None)[0]

# Predict the next stock mid price
next_time = 1.01 # Assuming next point is one time step ahead
print(m)
print(c)
next_stock_mid_price = m * next_time + c

print("Next stock mid price:", next_stock_mid_price)