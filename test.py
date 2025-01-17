# test how much numba speeds up a function

import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import numpy as np
from numba import njit, jit
from Config.bodies_data import earth

def test_func(n, method="normal"):
    """
    This function calculates the sum of the first n numbers.
    """
    sum = 0

    for i in range(n):
        sum += i
        if method == "normal":
            a = earth.gravitational_parameter
    return sum

@njit()
def test_func_numba(n, method="numba"):
    """
    This function calculates the sum of the first n numbers.
    """
    sum = 0

    for i in range(n):
        sum += i
        if method == "numba":
            a = earth.gravitational_parameter
    return sum

# Test the function
n = 100000000

# Test the normal function
start = time.time()
print(test_func(n))
end = time.time()
print(f"Normal function: {end - start}")

# Test the numba function
start = time.time()
sum = test_func_numba(n)
print(sum)
end = time.time()
print(f"Numba function: {end - start}")
