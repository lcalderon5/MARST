from Modules.dynamics import acceleration
from numba import njit
import numpy as np
import timeit

# Test the acceleration function with and without numba

# Define the initial conditions
position = np.array([10000, 0, 0])
velocity = np.array([0, 0, 0])

# Test the function without numba
print("Without numba:")
start = timeit.default_timer()
for i in range(100000):
    acceleration(position, velocity)

print("Time taken:", timeit.default_timer() - start)

