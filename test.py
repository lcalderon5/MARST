# test how much numba speeds up a function

import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import numpy as np
from numba import njit, jit
from Config.bodies_data import earth

def test_func(n):
    """
    This function calculates the sum of the first n numbers.
    """
    sum = 0
    matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    for i in range(n):
        sum += i
        cross_product = np.cross(matrix, matrix)
    return sum

@njit()
def test_func_numba(n,):
    """
    This function calculates the sum of the first n numbers.
    """
    sum = 0
    matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    for i in range(n):
        sum += i
        cross_product = np.cross(matrix, matrix)

    return sum

# Test the function
n = 1000000

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
