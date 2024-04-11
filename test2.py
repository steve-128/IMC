import numpy as np
import matplotlib.pyplot as plt

# Parameters for the triangular distribution
left = 900
mode = 1000
right = 1000

# Generate samples from the triangular distribution
num_samples = 10000  # Number of goldfish samples
reserve_prices = np.random.triangular(left, mode, right, num_samples)


maximum = 0
maximum_prof = 0
for n1 in range(0, 100):
    for n2 in range(n1,100):
        low = 900 + n1
        high = 900 + n2
        money_used = 0
        count = 0
        for i in reserve_prices:
            if i < low:
                count += 1
                money_used += low
            elif i < high:
                count += 1
                money_used += high
        if maximum_prof < (1000*count - money_used):
            maximum_prof = 1000*count - money_used
            maximum = (n1, n2)
        
        
print(maximum)
print(maximum_prof)
