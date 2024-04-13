import numpy as np
import matplotlib.pyplot as plt

# Generate some example stock price data
# Replace this with your actual stock price data
stock_prices = np.array([100, 110, 120, 130, 140, 150, 160, 170, 180, 190])

# Define parameters for the moving averages
short_window = 3  # Short-term moving average window
long_window = 7   # Long-term moving average window

# Calculate the moving averages
short_moving_avg = np.convolve(stock_prices, np.ones(short_window) / short_window, mode='valid')
long_moving_avg = np.convolve(stock_prices, np.ones(long_window) / long_window, mode='valid')

# Predictions based on crossover
prediction = np.where(short_moving_avg > long_moving_avg, 1, 0)

# Calculate the indices for plotting
short_indices = np.arange(short_window - 1, len(stock_prices))
long_indices = np.arange(long_window - 1, len(stock_prices))

# Plot the stock prices and moving averages
plt.plot(np.arange(len(stock_prices)), stock_prices, label='Stock Prices', color='blue')
plt.plot(short_indices, short_moving_avg, label=f'Short-term SMA ({short_window})', color='orange')
plt.plot(long_indices, long_moving_avg, label=f'Long-term SMA ({long_window})', color='green')

# Plot buy/sell signals based on crossover
buy_signals = np.where(prediction[:-1] < prediction[1:], stock_prices[:-1], np.nan)
sell_signals = np.where(prediction[:-1] > prediction[1:], stock_prices[:-1], np.nan)
plt.scatter(np.arange(len(buy_signals)), buy_signals, color='green', marker='^', label='Buy Signal')
plt.scatter(np.arange(len(sell_signals)), sell_signals, color='red', marker='v', label='Sell Signal')

plt.xlabel('Time')
plt.ylabel('Price')
plt.title('Stock Prices and Moving Averages')
plt.legend()
plt.grid(True)
plt.show()
